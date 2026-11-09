# Этап 1: нейтральное имя премиум-тарифа + пункт меню «Контакты» для уже заполненных БД.
from django.db import migrations


def forwards(apps, schema_editor):
    Plan = apps.get_model('main', 'Plan')
    NavLink = apps.get_model('main', 'NavLink')

    # Переименовать «VIP / Сопровождение» -> «Премиум», если название не меняли вручную
    Plan.objects.filter(plan_key='vip', name='VIP / Сопровождение').update(name='Премиум')

    # Добавить пункт меню «Контакты», если его ещё нет
    if not NavLink.objects.filter(anchor='#contact').exists():
        last = NavLink.objects.order_by('-order').first()
        order = (last.order + 1) if last else 1
        NavLink.objects.create(label='Контакты', anchor='#contact', order=order)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_sitesettings_show_about_sitesettings_show_cases_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, noop),
    ]
