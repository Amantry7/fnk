"""Проверка связки с почтой: отправляет тестовое письмо-заявку.

    python manage.py test_request_email
    python manage.py test_request_email --to someone@example.com
"""
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from main.emails import notify_recipients, send_request_notification
from main.models import ConsultRequest


class Command(BaseCommand):
    help = 'Отправить тестовое письмо о заявке на почту компании'

    def add_arguments(self, parser):
        parser.add_argument('--to', help='Адрес получателя (по умолчанию — из .env / настроек сайта)')

    def handle(self, *args, **options):
        if options['to']:
            settings.REQUEST_NOTIFY_EMAILS = [options['to']]

        self.stdout.write(f'Бэкенд:      {settings.EMAIL_BACKEND}')
        self.stdout.write(f'SMTP:        {settings.EMAIL_HOST or "(не задан — вывод в консоль)"}:{settings.EMAIL_PORT}')
        self.stdout.write(f'От кого:     {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'Получатели:  {", ".join(notify_recipients()) or "(нет)"}')
        self.stdout.write('')

        req = ConsultRequest(
            name='Тестовая заявка', phone='+996 (700) 00-00-00',
            email='test@example.com', company='ООО «Проверка»',
            plan='base', message='Это тестовое письмо: проверка связки сайта с почтой.',
        )
        req.pk = 0
        from django.utils import timezone
        req.created_at = timezone.now()

        if send_request_notification(req):
            self.stdout.write(self.style.SUCCESS('Письмо отправлено — проверьте почту (и папку «Спам»).'))
        else:
            raise CommandError('Письмо не отправлено — смотрите ошибку выше и настройки EMAIL_* в .env.')
