from django.urls import path

from catalog.views import home, contact, instructor

urlpatterns = [
    path("", home),
    path("contact/", contact),
    path("instructor/", instructor),
]
