from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, InstructorView, ProductDetailView, ContactView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name='home'),
    path("contact/", ContactView.as_view(), name='contact'),
    path("instructor/", InstructorView.as_view(), name='instructor'),
    path("product_detail/<int:pk>/", ProductDetailView.as_view(), name='product_detail'),
]
