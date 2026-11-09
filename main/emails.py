"""Письма-уведомления о заявках с сайта."""
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from .models import SiteSettings

logger = logging.getLogger(__name__)


def notify_recipients():
    """Адреса, на которые уходят заявки: .env → иначе e-mail из настроек сайта."""
    if settings.REQUEST_NOTIFY_EMAILS:
        return settings.REQUEST_NOTIFY_EMAILS
    site_email = (SiteSettings.load().email or '').strip()
    return [site_email] if site_email else []


def send_request_notification(req):
    """Отправляет заявку на почту компании. Возвращает True при успехе.

    Ошибки SMTP не ломают отправку формы: заявка уже сохранена в БД,
    а проблема пишется в лог.
    """
    recipients = notify_recipients()
    if not recipients:
        logger.warning('Заявка #%s сохранена, но адрес для уведомлений не задан', req.pk)
        return False

    site = SiteSettings.load()
    created = timezone.localtime(req.created_at).strftime('%d.%m.%Y %H:%M')
    subject = f'[{site.brand_name}] Новая заявка с сайта — {req.name}, {req.phone}'

    lines = [
        f'Новая заявка с сайта ({created})',
        '',
        f'Имя:       {req.name}',
        f'Телефон:   {req.phone}',
        f'E-mail:    {req.email or "—"}',
        f'Компания:  {req.company or "—"}',
        f'Формат:    {req.get_plan_display()}',
        '',
        'Сообщение:',
        req.message or '—',
        '',
        f'Заявка #{req.pk}. Отметить обработанной можно в админке сайта.',
    ]

    msg = EmailMessage(
        subject=subject,
        body='\n'.join(lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipients,
        reply_to=[req.email] if req.email else None,
    )
    try:
        msg.send(fail_silently=False)
    except Exception:
        logger.exception('Не удалось отправить письмо о заявке #%s', req.pk)
        return False
    logger.info('Письмо о заявке #%s отправлено на %s', req.pk, ', '.join(recipients))
    return True
