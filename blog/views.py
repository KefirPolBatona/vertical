from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('article_name', 'article_content', 'article_image')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.article_name)
            new_mat.save()

        return super().form_valid(form)


class ArticleListView(ListView):
    model = Article

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('article_name', 'article_content', 'article_image')

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.article_name)
            new_mat.save()

        return super().form_valid(form)


class ArticleDeleteView(DeleteView):
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
