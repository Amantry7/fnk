# Этап 3: быстрые ссылки (нижняя панель), примеры вакансий, пункт меню «Вакансии» (скрыт).
from django.db import migrations


def seed(apps, schema_editor):
    QuickLink = apps.get_model('main', 'QuickLink')
    Vacancy = apps.get_model('main', 'Vacancy')
    NavLink = apps.get_model('main', 'NavLink')

    # --- Быстрые ссылки (значения-заглушки, заполнить в админке) ---
    if not QuickLink.objects.exists():
        links = [
            ('instagram', '#'),
            ('facebook', '#'),
            ('telegram', '#'),
            ('whatsapp', '996700000000'),
            ('phone', '+996 (700) 00-00-00'),
            ('email', 'info@fnk.kg'),
            ('address', 'г. Бишкек, ул. Примерная, 1'),
        ]
        for i, (kind, value) in enumerate(links, start=1):
            QuickLink.objects.create(kind=kind, value=value, order=i, is_active=True)

    # --- Вакансии (существуют, но раздел скрыт по умолчанию) ---
    if not Vacancy.objects.exists():
        vacancies = [
            ('Финансовый аналитик', 'Бишкек / удалённо', 'полная занятость', '',
             'Построение и поддержка финансовых моделей, управленческая отчётность, аналитика по клиентским проектам.'),
            ('Младший консультант по управленческому учёту', 'Бишкек', 'полная занятость', '',
             'Помощь во внедрении управленческого учёта, подготовка отчётов, работа с данными клиентов под руководством наставника.'),
        ]
        for i, (title, loc, emp, salary, desc) in enumerate(vacancies, start=1):
            Vacancy.objects.create(title=title, location=loc, employment=emp,
                                   salary=salary, description=desc, order=i, is_active=True)

    # --- Пункт меню «Вакансии» (по умолчанию скрыт: is_active=False) ---
    if not NavLink.objects.filter(anchor='#vacancies').exists():
        last = NavLink.objects.order_by('-order').first()
        order = (last.order + 1) if last else 1
        NavLink.objects.create(label='Вакансии', anchor='#vacancies', order=order, is_active=False)


def unseed(apps, schema_editor):
    apps.get_model('main', 'QuickLink').objects.all().delete()
    apps.get_model('main', 'Vacancy').objects.all().delete()
    apps.get_model('main', 'NavLink').objects.filter(anchor='#vacancies').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_quicklink_vacancy_sitesettings_company_url_and_more'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
