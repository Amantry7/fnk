"""
Загрузка новостей из источников (RSS/Atom) — архитектура автозагрузки.

Использование:
    python manage.py fetch_news

Добавьте источники в админке (раздел «Источники новостей»), укажите URL RSS/Atom
ленты официального сайта. Команду можно повесить на cron/расписание.
Парсер работает на стандартной библиотеке (без внешних зависимостей).
"""
import urllib.request
from datetime import datetime
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import News, NewsSource

USER_AGENT = 'Mozilla/5.0 (compatible; FNK-NewsBot/1.0)'


def _text(el):
    return (el.text or '').strip() if el is not None else ''


def _strip_ns(tag):
    return tag.split('}', 1)[-1] if '}' in tag else tag


def _parse_date(raw):
    raw = (raw or '').strip()
    if not raw:
        return timezone.now()
    dt = None
    try:
        dt = parsedate_to_datetime(raw)          # RSS (RFC 822)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(raw.replace('Z', '+00:00'))  # Atom (ISO)
        except ValueError:
            dt = None
    if dt is None:
        return timezone.now()
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def _parse_feed(xml_bytes):
    """Возвращает список dict(title, link, summary, published)."""
    root = ET.fromstring(xml_bytes)
    items = []

    # RSS: <rss><channel><item>...  |  Atom: <feed><entry>...
    entries = root.findall('.//{*}item') or root.findall('.//{*}entry')
    for e in entries:
        data = {'title': '', 'link': '', 'summary': '', 'published': ''}
        for child in e:
            tag = _strip_ns(child.tag)
            if tag == 'title':
                data['title'] = _text(child)
            elif tag == 'link':
                # RSS: текст ссылки; Atom: атрибут href
                data['link'] = _text(child) or child.attrib.get('href', '')
            elif tag in ('description', 'summary'):
                data['summary'] = _text(child)
            elif tag in ('pubDate', 'published', 'updated'):
                if not data['published']:
                    data['published'] = _text(child)
        if data['title']:
            items.append(data)
    return items


class Command(BaseCommand):
    help = 'Загружает новости из активных источников (RSS/Atom)'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10,
                            help='Максимум новостей на источник за один запуск')

    def handle(self, *args, **opts):
        limit = opts['limit']
        sources = NewsSource.objects.filter(is_active=True)
        if not sources:
            self.stdout.write('Нет активных источников. Добавьте их в админке.')
            return

        total = 0
        for src in sources:
            try:
                req = urllib.request.Request(src.feed_url, headers={'User-Agent': USER_AGENT})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    raw = resp.read()
                entries = _parse_feed(raw)[:limit]
            except Exception as exc:  # noqa: BLE001 — источник может быть недоступен
                self.stderr.write(f'[{src.name}] ошибка загрузки: {exc}')
                continue

            created = 0
            for item in entries:
                link = item['link'].strip()
                # Дедуп по ссылке первоисточника
                if link and News.objects.filter(source_url=link).exists():
                    continue
                News.objects.create(
                    title=item['title'][:200],
                    excerpt=item['summary'][:300],
                    body=item['summary'],
                    source=src,
                    source_url=link,
                    published_at=_parse_date(item['published']),
                    is_active=True,
                )
                created += 1

            src.last_fetched = timezone.now()
            src.save(update_fields=['last_fetched'])
            total += created
            self.stdout.write(f'[{src.name}] добавлено: {created}')

        self.stdout.write(self.style.SUCCESS(f'Готово. Всего добавлено новостей: {total}'))
