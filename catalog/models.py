from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    """
    Категории товаров (услуг) - виды спорта, танцевальные направления.
    """

    name_category = models.CharField(max_length=100, verbose_name="категория")
    description = models.TextField(verbose_name="описание", **NULLABLE)

    def __str__(self):
        return f"{self.name_category}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """
    Товары (услуги) - абонементы на посещение занятий.
    """

    product_name = models.CharField(max_length=100, verbose_name="продукт")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    avatar = models.ImageField(
        upload_to="avatar/", verbose_name="изображение", **NULLABLE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="categories",
        verbose_name="категория",
        **NULLABLE,
    )
    price_product = models.IntegerField(verbose_name="цена")
    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="дата последнего изменения"
    )

    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        **NULLABLE,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.product_name} {self.price_product} {self.category}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("price_product",)


class Version(models.Model):
    """
    Версия продукта (товара/услуги) - модернизация абонемента по содержанию занятия.
    """

    version_name = models.CharField(max_length=150, verbose_name="версия продукта", **NULLABLE,)
    version_number = models.FloatField(verbose_name='номер версии')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт",
        **NULLABLE,
    )
    version_active = models.BooleanField(default=False, verbose_name='версия активна')

    def __str__(self):
        return f'Версия продукта: {self.version_number} {self.version_name}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
