from django.core.management import BaseCommand

import json

from catalog.models import Product, Category


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        # Здесь мы получаем данные из фикстуры с категориями
        with open('catalog/fixtures/categories.json', encoding='utf-8') as f:
            data = f.read()
        return json.loads(data)

    @staticmethod
    def json_read_products():
        # Здесь мы получаем данные из фикстуры с продуктами
        with open('catalog/fixtures/products.json', encoding='utf-8') as f:
            data = f.read()
        return json.loads(data)

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    name_category=category['fields']['name_category'],
                    description=category['fields']['description'],
                    pk=category['pk']
                )
            )

        # Создаем объекты в БД с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    product_name=product["fields"]["product_name"],
                    description=product["fields"]["description"],
                    avatar=product["fields"]["avatar"],
                    category=Category.objects.get(pk=product["fields"]['category']),
                    price_product=product["fields"]["price_product"],
                    created_at=product["fields"]["created_at"],
                    updated_at=product["fields"]["updated_at"],
               )
            )

        # Создаем объекты в БД с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
