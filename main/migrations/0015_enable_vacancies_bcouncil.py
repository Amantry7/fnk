# Включить раздел «Вакансии» и задать ссылку на компанию в каталоге B-Council.
from django.db import migrations

BCOUNCIL_URL = 'https://b-council.kg/company/45/'


def forwards(apps, schema_editor):
    SiteSettings = apps.get_model('main', 'SiteSettings')
    NavLink = apps.get_model('main', 'NavLink')

    s = SiteSettings.objects.first()
    if s:
        s.show_vacancies = True
        if not s.company_url:
            s.company_url = BCOUNCIL_URL
        s.save()

    NavLink.objects.filter(anchor='#vacancies').update(is_active=True)


def backwards(apps, schema_editor):
    SiteSettings = apps.get_model('main', 'SiteSettings')
    NavLink = apps.get_model('main', 'NavLink')
    s = SiteSettings.objects.first()
    if s:
        s.show_vacancies = False
        if s.company_url == BCOUNCIL_URL:
            s.company_url = ''
        s.save()
    NavLink.objects.filter(anchor='#vacancies').update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_more_reviews_news'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
