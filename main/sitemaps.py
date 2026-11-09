from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return News.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.published_at
