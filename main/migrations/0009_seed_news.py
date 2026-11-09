# Этап 2: пункты меню «Новости»/«Важное» + примеры новостей, важного и ленты.
from django.db import migrations

from main.utils import ru_slugify


def seed(apps, schema_editor):
    NavLink = apps.get_model('main', 'NavLink')
    News = apps.get_model('main', 'News')
    ImportantItem = apps.get_model('main', 'ImportantItem')
    TickerItem = apps.get_model('main', 'TickerItem')

    # --- Пункты меню ---
    def add_nav(label, anchor):
        if not NavLink.objects.filter(anchor=anchor).exists():
            last = NavLink.objects.order_by('-order').first()
            order = (last.order + 1) if last else 1
            NavLink.objects.create(label=label, anchor=anchor, order=order)

    add_nav('Новости', '#news')
    add_nav('Важное', '#important')

    # --- Примеры новостей ---
    if not News.objects.exists():
        samples = [
            ('ФНК запускает направление налогового планирования для малого бизнеса',
             'Новая услуга помогает собственникам законно снизить налоговую нагрузку и выстроить безопасную структуру.',
             'ФНК расширяет спектр услуг: теперь мы системно занимаемся налоговым планированием для малого и среднего бизнеса.\n\nМы анализируем текущую структуру, находим точки легальной оптимизации и сопровождаем внедрение изменений. Первичная диагностика — бесплатно.',
             True),
            ('Обновили методику юнит-экономики для розницы',
             'Теперь клиенты видят прибыльность по каждому товару и точке продаж в едином отчёте.',
             'Мы доработали методику расчёта юнит-экономики для розничных сетей. Отчёт показывает вклад каждого SKU и магазина в прибыль, что позволяет быстрее принимать решения по ассортименту.',
             False),
            ('Кейс: закрыли кассовые разрывы производственной компании за квартал',
             'Платёжный календарь и модель оборотного капитала убрали регулярные кассовые разрывы.',
             'К нам обратилась производственная компания с постоянными кассовыми разрывами. Мы построили платёжный календарь и модель оборотного капитала — за один квартал разрывы исчезли, а планирование стало прозрачным.',
             False),
        ]
        for i, (title, excerpt, body, pinned) in enumerate(samples):
            base = ru_slugify(title)
            slug = base
            n = 2
            while News.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            News.objects.create(title=title, slug=slug, excerpt=excerpt, body=body,
                                is_pinned=pinned, is_active=True)

    # --- Важное ---
    if not ImportantItem.objects.exists():
        important = [
            ('Бесплатная финансовая диагностика', 'До конца месяца — бесплатный разбор финансов вашего бизнеса.', ''),
            ('Сроки сдачи отчётности', 'Напоминаем о приближении сроков сдачи квартальной отчётности.', ''),
            ('Новые требования к управленческой отчётности', 'Рекомендуем обновить формы управленческого учёта.', ''),
        ]
        for i, (title, text, link) in enumerate(important, start=1):
            ImportantItem.objects.create(title=title, text=text, link=link, order=i)

    # --- Лента ---
    if not TickerItem.objects.exists():
        ticker = [
            ('news', 'ФНК открыла направление налогового планирования', ''),
            ('important', 'Бесплатная финансовая диагностика до конца месяца', ''),
            ('announcement', 'Вебинар по управленческому учёту — регистрация открыта', ''),
            ('promo', 'Скидка 15% на первый месяц сопровождения', ''),
            ('news', 'Обновили методику юнит-экономики для розницы', ''),
        ]
        for i, (cat, text, link) in enumerate(ticker, start=1):
            TickerItem.objects.create(category=cat, text=text, link=link, order=i)


def unseed(apps, schema_editor):
    apps.get_model('main', 'News').objects.all().delete()
    apps.get_model('main', 'ImportantItem').objects.all().delete()
    apps.get_model('main', 'TickerItem').objects.all().delete()
    apps.get_model('main', 'NavLink').objects.filter(anchor__in=['#news', '#important']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_importantitem_newssource_tickeritem_and_more'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
