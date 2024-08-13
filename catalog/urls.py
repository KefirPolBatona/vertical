from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, InstructorView, ProductDetailView, ContactView, ProductCreateView, \
    ProductDeleteView, ProductUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name='home'),
    path("contact/", ContactView.as_view(), name='contact'),
    path("instructor/", InstructorView.as_view(), name='instructor'),
    path("product_detail/<int:pk>/", ProductDetailView.as_view(), name='product_detail'),
    path("create/", ProductCreateView.as_view(), name='create'),
    path("edit/<int:pk>/", ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
]
