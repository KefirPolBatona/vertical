from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contact, instructor, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name='home'),
    path("contact/", contact, name='contact'),
    path("instructor/", instructor, name='instructor'),
    path("product_detail/<int:pk>/", product_detail, name='product_detail'),
]
