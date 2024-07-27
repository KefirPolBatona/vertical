from django.shortcuts import render

from catalog.models import Product


def home(request):
    product_list = Product.objects.all()
    context = {
        'objects_list': product_list
    }
    return render(request, "catalog/home.html", context)


def product_detail(request, pk):
    product_service = Product.objects.get(pk=pk)
    context = {
        'product_service': product_service
    }
    return render(request, "catalog/product_detail.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"You have new message from {name} ({phone}): {message}")
    return render(request, "catalog/contact.html")


def instructor(request):
    return render(request, "catalog/instructor.html")
