# Конвертация старых эмодзи-иконок услуг в ключи SVG (для уже заполненных БД).
from django.db import migrations

EMOJI_TO_SLUG = {
    '📊': 'chart',
    '📈': 'growth',
    '🧾': 'tax',
    '🔍': 'audit',
    '💼': 'briefcase',
    '🤝': 'users',
}


def convert(apps, schema_editor):
    Service = apps.get_model('main', 'Service')
    for service in Service.objects.all():
        slug = EMOJI_TO_SLUG.get(service.icon)
        if slug:
            service.icon = slug
            service.save(update_fields=['icon'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_service_icon'),
    ]

    operations = [
        migrations.RunPython(convert, noop),
    ]
