from django.db import models


# ============================================================
#  Заявки с лендинга
# ============================================================
class ConsultRequest(models.Model):
    """Заявка на консультацию, отправленная с лендинга."""

    FORMAT_CHOICES = [
        ('base', 'Базовый'),
        ('extended', 'Расширенный'),
        ('vip', 'VIP / Сопровождение'),
        ('other', 'Другое / не выбрано'),
    ]

    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=40)
    email = models.EmailField('E-mail', blank=True)
    company = models.CharField('Компания', max_length=160, blank=True)
    plan = models.CharField(
        'Формат', max_length=20, choices=FORMAT_CHOICES, default='other'
    )
    message = models.TextField('Сообщение', blank=True)

    is_processed = models.BooleanField('Обработана', default=False)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone} ({self.created_at:%d.%m.%Y %H:%M})'


# ============================================================
#  Глобальные настройки и тексты сайта (singleton)
# ============================================================
class SiteSettings(models.Model):
    """Все одиночные тексты сайта. Существует ровно одна запись."""

    # --- Бренд / шапка ---
    brand_name = models.CharField('Название бренда', max_length=60, default='ФНК')
    brand_sub = models.CharField('Подпись под брендом', max_length=120, default='Финансовый консалтинг')
    nav_cta_text = models.CharField('Кнопка в меню', max_length=60, default='Оставить заявку')

    # --- Hero ---
    hero_eyebrow = models.CharField('Hero · надпись сверху', max_length=160, default='Финансово-консалтинговая компания')
    hero_title = models.CharField('Hero · заголовок (белый)', max_length=160, default='Финансовый консалтинг')
    hero_title_gold = models.CharField('Hero · заголовок (золотой)', max_length=160, default='для роста вашего бизнеса')
    hero_lead = models.TextField('Hero · описание', default='ФНК помогает собственникам и руководителям видеть бизнес в цифрах, наводить порядок в финансах и принимать решения, которые увеличивают прибыль.')
    hero_btn_primary = models.CharField('Hero · кнопка 1', max_length=60, default='Получить консультацию')
    hero_btn_secondary = models.CharField('Hero · кнопка 2', max_length=60, default='Наши услуги')

    # --- О компании ---
    about_kicker = models.CharField('О компании · надкаголовок', max_length=80, default='О компании')
    about_title = models.CharField('О компании · заголовок', max_length=200, default='ФНК — ваш внешний финансовый департамент')
    about_text1 = models.TextField('О компании · абзац 1', default='Мы выстраиваем управленческий учёт, финансовую модель и систему контроля так, чтобы собственник в любой момент понимал: сколько компания реально зарабатывает, где теряет деньги и за счёт чего может вырасти.')
    about_text2 = models.TextField('О компании · абзац 2', default='Работаем с малым и средним бизнесом, холдингами и стартапами. Не просто считаем — внедряем процессы и сопровождаем команду до результата.')
    about_btn = models.CharField('О компании · кнопка', max_length=60, default='Обсудить задачу')

    # --- Факты ---
    facts_kicker = models.CharField('Факты · надзаголовок', max_length=80, default='Опыт и факты')
    facts_title = models.CharField('Факты · заголовок', max_length=200, default='Цифры, которым доверяют')

    # --- Боли ---
    pains_kicker = models.CharField('Боли · надзаголовок', max_length=80, default='Знакомо?')
    pains_title = models.CharField('Боли · заголовок', max_length=200, default='Типовые ситуации собственников')

    # --- Услуги ---
    services_kicker = models.CharField('Услуги · надзаголовок', max_length=80, default='Направления работы')
    services_title = models.CharField('Услуги · заголовок', max_length=200, default='Что мы делаем')
    services_sub = models.CharField('Услуги · подзаголовок', max_length=255, blank=True, default='Комплекс услуг — от наведения порядка в учёте до привлечения инвестиций.')

    # --- Процесс ---
    process_kicker = models.CharField('Процесс · надзаголовок', max_length=80, default='Как мы работаем')
    process_title = models.CharField('Процесс · заголовок', max_length=200, default='4 шага к финансовому порядку')

    # --- Кейсы ---
    cases_kicker = models.CharField('Кейсы · надзаголовок', max_length=80, default='Из практики')
    cases_title = models.CharField('Кейсы · заголовок', max_length=200, default='Кейсы клиентов')
    cases_sub = models.CharField('Кейсы · подзаголовок', max_length=255, blank=True, default='Имена компаний скрыты по соглашению о конфиденциальности.')

    # --- Тарифы ---
    pricing_kicker = models.CharField('Тарифы · надзаголовок', max_length=80, default='Форматы сотрудничества')
    pricing_title = models.CharField('Тарифы · заголовок', max_length=200, default='Выберите подходящий формат')
    pricing_sub = models.CharField('Тарифы · подзаголовок', max_length=255, blank=True, default='Точную стоимость рассчитываем после диагностики под ваши задачи.')

    # --- Отзывы ---
    reviews_kicker = models.CharField('Отзывы · надзаголовок', max_length=80, default='Отзывы')
    reviews_title = models.CharField('Отзывы · заголовок', max_length=200, default='Что говорят клиенты')

    # --- FAQ ---
    faq_kicker = models.CharField('FAQ · надзаголовок', max_length=80, default='FAQ')
    faq_title = models.CharField('FAQ · заголовок', max_length=200, default='Частые вопросы')

    # --- Контакты (секция формы) ---
    contact_kicker = models.CharField('Контакты · надзаголовок', max_length=80, default='Напишите напрямую')
    contact_title = models.CharField('Контакты · заголовок', max_length=200, default='Оставьте заявку — начнём с бесплатной диагностики')
    contact_lead = models.TextField('Контакты · описание', default='Заполните форму, и финансовый консультант ФНК свяжется с вами, чтобы разобрать вашу ситуацию и предложить решение.')

    # --- Контактные данные (используются в контактах и подвале) ---
    phone = models.CharField('Телефон', max_length=60, default='+996 (700) 00-00-00')
    email = models.EmailField('E-mail', default='info@fnk.kg')
    address = models.CharField('Адрес', max_length=200, default='г. Бишкек, ул. Примерная, 1')
    work_hours = models.CharField('График работы', max_length=120, default='Пн–Пт, 09:00–18:00')

    # --- Подвал ---
    footer_desc = models.TextField('Подвал · описание', default='Финансово-консалтинговая компания. Превращаем цифры в управленческие решения и устойчивый рост бизнеса.')
    footer_nav_title = models.CharField('Подвал · заголовок «Навигация»', max_length=60, default='Навигация')
    footer_contacts_title = models.CharField('Подвал · заголовок «Контакты»', max_length=60, default='Контакты')
    footer_social_title = models.CharField('Подвал · заголовок «Соцсети»', max_length=60, default='Мы в сети')
    footer_copyright = models.CharField('Подвал · копирайт (без года)', max_length=160, default='ФНК. Все права защищены.')
    footer_disclaimer = models.CharField('Подвал · дисклеймер', max_length=255, blank=True, default='Сайт носит информационный характер и не является публичной офертой.')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1  # всегда одна запись
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ============================================================
#  Базовый класс для упорядоченных списков
# ============================================================
class OrderedItem(models.Model):
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показывать', default=True)

    class Meta:
        abstract = True
        ordering = ['order', 'id']


# --- Меню (шапка + подвал) ---
class NavLink(OrderedItem):
    label = models.CharField('Пункт меню', max_length=60)
    anchor = models.CharField('Якорь (например #about)', max_length=60)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Меню (навигация)'

    def __str__(self):
        return self.label


# --- Соцсети ---
class SocialLink(OrderedItem):
    label = models.CharField('Название', max_length=60)
    url = models.CharField('Ссылка', max_length=255, default='#')

    class Meta(OrderedItem.Meta):
        verbose_name = 'Соцсеть'
        verbose_name_plural = 'Соцсети'

    def __str__(self):
        return self.label


# --- Hero: мини-статистика ---
class TrustStat(OrderedItem):
    value = models.CharField('Значение', max_length=40, help_text='Например: 120+, 8 лет')
    label = models.CharField('Подпись', max_length=80)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Hero · статистика'
        verbose_name_plural = 'Hero · статистика'

    def __str__(self):
        return f'{self.value} — {self.label}'


# --- О компании: преимущества ---
class AboutPoint(OrderedItem):
    number = models.CharField('Номер', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=80)
    text = models.CharField('Текст', max_length=200)

    class Meta(OrderedItem.Meta):
        verbose_name = 'О компании · преимущество'
        verbose_name_plural = 'О компании · преимущества'

    def __str__(self):
        return self.title


# --- Факты (счётчики) ---
class Fact(OrderedItem):
    value = models.CharField('Число', max_length=20, help_text='Только число, например 120')
    prefix = models.CharField('Префикс', max_length=10, blank=True, help_text='Например $')
    suffix = models.CharField('Суффикс', max_length=20, blank=True, help_text='Например +, %, " млрд"')
    label = models.CharField('Подпись', max_length=120)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Факт'
        verbose_name_plural = 'Факты (счётчики)'

    def __str__(self):
        return f'{self.prefix}{self.value}{self.suffix} — {self.label}'


# --- Боли клиентов ---
class Pain(OrderedItem):
    text = models.CharField('Текст', max_length=200)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Боль клиента'
        verbose_name_plural = 'Боли клиентов'

    def __str__(self):
        return self.text


# --- Услуги ---
class Service(OrderedItem):
    icon = models.CharField('Иконка (эмодзи)', max_length=10, default='📊')
    title = models.CharField('Заголовок', max_length=80)
    text = models.CharField('Описание', max_length=255)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


# --- Шаги работы ---
class Step(OrderedItem):
    number = models.CharField('Номер', max_length=4, default='1')
    title = models.CharField('Заголовок', max_length=80)
    text = models.CharField('Описание', max_length=200)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Шаг работы'
        verbose_name_plural = 'Шаги работы'

    def __str__(self):
        return f'{self.number}. {self.title}'


# --- Кейсы ---
class Case(OrderedItem):
    tag = models.CharField('Тег (отрасль)', max_length=60)
    title = models.CharField('Заголовок', max_length=120)
    text = models.CharField('Описание', max_length=255)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'

    def __str__(self):
        return self.title


# --- Тарифы ---
class Plan(OrderedItem):
    PLAN_KEYS = [
        ('base', 'Базовый'),
        ('extended', 'Расширенный'),
        ('vip', 'VIP / Сопровождение'),
    ]
    name = models.CharField('Название', max_length=80)
    price = models.CharField('Цена', max_length=40, help_text='Например: от $500')
    period = models.CharField('Период', max_length=30, blank=True, default='/ мес')
    description = models.CharField('Краткое описание', max_length=200)
    features = models.TextField('Состав (каждый пункт с новой строки)')
    plan_key = models.CharField('Ключ формата', max_length=20, choices=PLAN_KEYS, default='base',
                                help_text='Подставляется в форму заявки')
    badge = models.CharField('Бейдж', max_length=40, blank=True, help_text='Например: Популярный')
    is_featured = models.BooleanField('Выделенный', default=False)
    button_text = models.CharField('Текст кнопки', max_length=40, default='Оставить заявку')

    class Meta(OrderedItem.Meta):
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name


# --- Отзывы ---
class Review(OrderedItem):
    stars = models.PositiveSmallIntegerField('Звёзды (1–5)', default=5)
    text = models.TextField('Текст отзыва')
    author_name = models.CharField('Имя автора', max_length=80)
    author_role = models.CharField('Должность / роль', max_length=120, blank=True)

    class Meta(OrderedItem.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.author_name

    @property
    def stars_display(self):
        return '★' * int(self.stars)


# --- FAQ ---
class FAQ(OrderedItem):
    question = models.CharField('Вопрос', max_length=200)
    answer = models.TextField('Ответ')

    class Meta(OrderedItem.Meta):
        verbose_name = 'Вопрос FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question
