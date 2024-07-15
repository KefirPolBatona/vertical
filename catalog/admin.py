from django.contrib import admin

from catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_category',)


@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price_product', 'category',)
    list_filter = ('category',)
    search_fields = ('product_name', 'description',)
