from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import ArticleForm
from blog.models import Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания статьи.
    """
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.article_name)
            new_mat.save()
        return super().form_valid(form)


class ArticleListView(ListView):
    """
    Класс для вывода списка всех статей.
    """
    model = Article

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class ListFilterPub(ArticleListView):
    """
    Класс для вывода списка опубликованных статей.
    """
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ListFilterNoPub(ArticleListView):
    """
    Класс для вывода списка неопубликованных статей.
    """
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=False)
        return queryset


class ArticleDetailView(DetailView):
    """
    Класс для вывода статьи с информацией.
    """
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для внесения изменений в статью.
    """
    model = Article
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.article_name)
            new_mat.save()
        return super().form_valid(form)

    def get_form_class(self):
        """
        Проверяет права доступа пользователя на внесение изменений.
        """
        user = self.request.user

        if user.has_perm("blog.can_add_article"):
            return ArticleForm
        raise PermissionDenied


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс для удаления статьи.
    """
    model = Article
    success_url = reverse_lazy('blog:list')


def toggle_activity(request, pk):
    article_item = get_object_or_404(Article, pk=pk)
    if article_item.is_published:
        article_item.is_published = False
    else:
        article_item.is_published = True

    article_item.save()

    return redirect(reverse('blog:list'))
