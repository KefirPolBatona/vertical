from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView

from catalog.models import Product


class ProductListView(ListView):
    model = Product


class InstructorView(TemplateView):
    template_name = 'catalog/instructor.html'


class ProductDetailView(DetailView):
    model = Product


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message")
            print(f"You have new message from {name} ({phone}): {message}")
        return render(request, "catalog/contact.html")
