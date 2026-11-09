from django.contrib import admin

from .models import (
    AboutPoint, Case, ConsultRequest, FAQ, Fact, ImportantItem, NavLink, News,
    NewsSource, Pain, Plan, QuickLink, Review, Service, SiteSettings, SocialLink,
    Step, TickerItem, TrustStat, Vacancy,
)


# ============================================================
#  Заявки
# ============================================================
@admin.register(ConsultRequest)
class ConsultRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'plan', 'company', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'plan', 'created_at')
    search_fields = ('name', 'phone', 'email', 'company', 'message')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Контакт', {'fields': ('name', 'phone', 'email', 'company')}),
        ('Заявка', {'fields': ('plan', 'message')}),
        ('Статус', {'fields': ('is_processed', 'created_at')}),
    )


# ============================================================
#  Настройки сайта (singleton)
# ============================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Бренд и меню', {'fields': ('brand_name', 'brand_sub', 'nav_cta_text')}),
        ('Главный экран (Hero)', {'fields': (
            'hero_eyebrow', 'hero_title', 'hero_title_gold', 'hero_lead',
            'hero_btn_primary', 'hero_btn_secondary')}),
        ('О компании', {'fields': (
            'about_kicker', 'about_title', 'about_text1', 'about_text2', 'about_btn')}),
        ('Факты', {'fields': ('facts_kicker', 'facts_title')}),
        ('Боли клиентов', {'fields': ('pains_kicker', 'pains_title')}),
        ('Услуги', {'fields': ('services_kicker', 'services_title', 'services_sub')}),
        ('Как мы работаем', {'fields': ('process_kicker', 'process_title')}),
        ('Кейсы', {'fields': ('cases_kicker', 'cases_title', 'cases_sub')}),
        ('Тарифы', {'fields': ('pricing_kicker', 'pricing_title', 'pricing_sub')}),
        ('Отзывы', {'fields': ('reviews_kicker', 'reviews_title')}),
        ('FAQ', {'fields': ('faq_kicker', 'faq_title')}),
        ('Секция «Контакты»', {'fields': ('contact_kicker', 'contact_title', 'contact_lead')}),
        ('Контактные данные', {'fields': ('phone', 'email', 'address', 'work_hours')}),
        ('Подвал', {'fields': (
            'footer_desc', 'footer_nav_title', 'footer_contacts_title',
            'footer_social_title', 'footer_copyright', 'footer_disclaimer')}),
        ('Новости и «Важное»', {'fields': (
            'news_kicker', 'news_title', 'news_sub',
            'important_kicker', 'important_title')}),
        ('Движущаяся лента', {'fields': (
            'ticker_enabled', 'ticker_speed', 'ticker_label')}),
        ('Анимация карточек (карусели)', {'fields': (
            'services_animated', 'services_speed',
            'reviews_animated', 'reviews_speed',
            'news_animated', 'news_speed')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'seo_keywords', 'og_image')}),
        ('Компания и быстрые ссылки', {'fields': ('company_url', 'quicklinks_enabled')}),
        ('Вакансии', {'fields': ('vacancies_kicker', 'vacancies_title')}),
        ('Видимость разделов (скрыть/показать)', {
            'classes': ('collapse',),
            'fields': (
                'show_about', 'show_facts', 'show_pains', 'show_services',
                'show_process', 'show_cases', 'show_pricing', 'show_reviews',
                'show_faq', 'show_news', 'show_important', 'show_vacancies',
                'show_contact')}),
    )

    def has_add_permission(self, request):
        # Разрешаем создать запись только если её ещё нет
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ============================================================
#  Списки контента
# ============================================================
class OrderedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(NavLink)
class NavLinkAdmin(OrderedAdmin):
    list_display = ('label', 'anchor', 'order', 'is_active')
    list_editable = ('anchor', 'order', 'is_active')


@admin.register(SocialLink)
class SocialLinkAdmin(OrderedAdmin):
    list_display = ('label', 'url', 'order', 'is_active')
    list_editable = ('url', 'order', 'is_active')


@admin.register(TrustStat)
class TrustStatAdmin(OrderedAdmin):
    list_display = ('value', 'label', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(AboutPoint)
class AboutPointAdmin(OrderedAdmin):
    list_display = ('number', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Fact)
class FactAdmin(OrderedAdmin):
    list_display = ('label', 'value', 'prefix', 'suffix', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Pain)
class PainAdmin(OrderedAdmin):
    list_display = ('text', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    list_display = ('icon', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Step)
class StepAdmin(OrderedAdmin):
    list_display = ('number', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Case)
class CaseAdmin(OrderedAdmin):
    list_display = ('tag', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Plan)
class PlanAdmin(OrderedAdmin):
    list_display = ('name', 'price', 'plan_key', 'is_featured', 'order', 'is_active')
    list_editable = ('is_featured', 'order', 'is_active')


@admin.register(Review)
class ReviewAdmin(OrderedAdmin):
    list_display = ('author_name', 'author_role', 'stars', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(FAQ)
class FAQAdmin(OrderedAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_pinned', 'is_active', 'source')
    list_filter = ('is_active', 'is_pinned', 'source', 'published_at')
    list_editable = ('is_pinned', 'is_active')
    search_fields = ('title', 'excerpt', 'body')
    date_hierarchy = 'published_at'
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'excerpt', 'body', 'image')}),
        ('Публикация', {'fields': ('published_at', 'is_pinned', 'is_active')}),
        ('Источник (для автозагрузки)', {'fields': ('source', 'source_url')}),
    )


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'feed_url', 'is_active', 'last_fetched')
    list_editable = ('is_active',)
    readonly_fields = ('last_fetched',)


@admin.register(ImportantItem)
class ImportantItemAdmin(OrderedAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(TickerItem)
class TickerItemAdmin(OrderedAdmin):
    list_display = ('text', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('category', 'order', 'is_active')


@admin.register(QuickLink)
class QuickLinkAdmin(OrderedAdmin):
    list_display = ('kind', 'value', 'order', 'is_active')
    list_filter = ('kind', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Vacancy)
class VacancyAdmin(OrderedAdmin):
    list_display = ('title', 'location', 'employment', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')


admin.site.site_header = 'ФНК — администрирование'
admin.site.site_title = 'ФНК'
admin.site.index_title = 'Управление сайтом'
