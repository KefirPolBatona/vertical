from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, InstructorView, ProductDetailView, ContactView, ProductCreateView, \
    ProductDeleteView, ProductUpdateView, ProductModeratorListView, toggle_activity, CategoryListView, \
    CategoryDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path("", cache_page(10)(ProductListView.as_view()), name='home'),
    path("category/", cache_page(10)(CategoryListView.as_view()), name='category'),
    path("category_detail/<int:pk>/", cache_page(10)(CategoryDetailView.as_view()), name='category_detail'),
    path("moderator/", ProductModeratorListView.as_view(), name='product_list_moderator'),
    path("contact/", cache_page(10)(ContactView.as_view()), name='contact'),
    path("instructor/", cache_page(10)(InstructorView.as_view()), name='instructor'),
    path("product_detail/<int:pk>/", cache_page(10)(ProductDetailView.as_view()), name='product_detail'),
    path("create/", ProductCreateView.as_view(), name='create'),
    path("edit/<int:pk>/", ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]
