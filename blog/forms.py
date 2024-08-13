from django import forms
from django.forms import BooleanField

from blog.models import Article


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


class ArticleForm(StyleFormMixin, forms.ModelForm):
    """
    Класс для создания формы статьи.
    """
    class Meta:
        model = Article
        fields = ('article_name', 'article_content', 'article_image')
