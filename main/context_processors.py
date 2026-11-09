from .models import (
    AboutPoint, Case, FAQ, Fact, ImportantItem, NavLink, News, Pain, Plan,
    QuickLink, Review, Service, SiteSettings, SocialLink, Step, TickerItem,
    TrustStat, Vacancy,
)


def site_content(request):
    """Контент сайта из БД — доступен во всех шаблонах."""
    return {
        'site': SiteSettings.load(),
        'nav_links': NavLink.objects.filter(is_active=True),
        'social_links': SocialLink.objects.filter(is_active=True),
        'trust_stats': TrustStat.objects.filter(is_active=True),
        'about_points': AboutPoint.objects.filter(is_active=True),
        'facts': Fact.objects.filter(is_active=True),
        'pains': Pain.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True),
        'steps': Step.objects.filter(is_active=True),
        'cases': Case.objects.filter(is_active=True),
        'plans': Plan.objects.filter(is_active=True),
        'reviews': Review.objects.filter(is_active=True),
        'faqs': FAQ.objects.filter(is_active=True),
        'news_items': News.objects.filter(is_active=True)[:12],
        'important_items': ImportantItem.objects.filter(is_active=True),
        'ticker_items': TickerItem.objects.filter(is_active=True),
        'quick_links': QuickLink.objects.filter(is_active=True),
        'vacancies': Vacancy.objects.filter(is_active=True),
    }
