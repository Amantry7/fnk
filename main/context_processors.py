from .models import (
    AboutPoint, Case, FAQ, Fact, NavLink, Pain, Plan, Review, Service,
    SiteSettings, SocialLink, Step, TrustStat,
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
    }
