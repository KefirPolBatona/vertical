from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    toggle_activity, ListFilterPub, ListFilterNoPub

app_name = BlogConfig.name

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('', cache_page(10)(ArticleListView.as_view()), name='list'),
    path('filterpub/', cache_page(10)(ListFilterPub.as_view()), name='list_filter_published'),
    path('filternopub/', cache_page(10)(ListFilterNoPub.as_view()), name='list_filter_nopublished'),
    path('view/<int:pk>/', cache_page(10)(ArticleDetailView.as_view()), name='view'),
    path('edit/<int:pk>/', ArticleUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]
