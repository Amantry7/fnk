from django.utils.text import slugify

# Транслитерация кириллицы для человекопонятных URL (ЧПУ)
_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def ru_slugify(text):
    """Слаг из кириллицы/латиницы: 'Новость №1' -> 'novost-1'."""
    text = (text or '').lower()
    out = ''.join(_TRANSLIT.get(ch, ch) for ch in text)
    slug = slugify(out)
    return slug or 'item'
