import json

from django import forms
from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_cached_categories():
    """
    Проверяет кэш.
    Кеширует список категорий, если он в кеше отсутствует.
    Возвращает список категорий из кеша (при наличии) или из БД.
    """
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list


def open_json_file():
    """
    Возвращает список недопустимых слов для последующей проверки в ProductForm (clean_product_name, clean_description)
    """
    with open('catalog/clean_words.json', 'r', encoding='utf-8') as clean_words:
        str_data = json.load(clean_words)
        list_data = str_data.split(", ")
        return list_data


def valid_words(cleaned):
    """
    Применяется для class ProductForm(forms.ModelForm).
    Сверяет введенные пользователем слова в полях формы ('product_name', 'description')
    со списком запрещенных слов из json-файла.
    """
    list_data = open_json_file()
    if any(item in cleaned for item in list_data):
        raise forms.ValidationError('Недопустимая лексика')
    return cleaned
