from django import forms
from django.forms import BaseInlineFormSet, BooleanField

from catalog.models import Product, Version
from catalog.open_json_file import open_json_file


class StyleFormMixin:
    """
    Класс для стилизации форм.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для создания формы абонемента.
    """
    class Meta:
        model = Product
        fields = '__all__'

    def clean_product_name(self):
        """
        Сверяет через функцию valid_words() название абонемента со списком запрещенных слов.
        """
        cleaned_name = self.cleaned_data['product_name']
        process_valid = valid_words(cleaned_name)
        return process_valid

    def clean_description(self):
        """
        Сверяет через функцию valid_words() описание абонемента со списком запрещенных слов.
        """
        cleaned_description = self.cleaned_data['description']
        process_valid = valid_words(cleaned_description)
        return process_valid


class VersionForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для создания формы версии абонемента.
    """
    class Meta:
        model = Version
        fields = '__all__'


class VersionFormset(BaseInlineFormSet):
    """
    Валидация формы по количеству активных версий.
    """
    def clean(self):
        count = 0
        for form in self.forms:
            if form.instance.version_active:
                count += 1
                if count > 1:
                    raise forms.ValidationError("Недопустимое количество активных версий")


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
