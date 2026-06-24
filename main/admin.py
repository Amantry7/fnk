from django.contrib import admin

from .models import (
    AboutPoint, Case, ConsultRequest, FAQ, Fact, NavLink, Pain, Plan,
    Review, Service, SiteSettings, SocialLink, Step, TrustStat,
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


admin.site.site_header = 'ФНК — администрирование'
admin.site.site_title = 'ФНК'
admin.site.index_title = 'Управление сайтом'
