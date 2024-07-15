from django.db import models


NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    name_category = models.CharField(max_length=100, verbose_name="категория")
    description = models.TextField(verbose_name="описание", **NULLABLE)

    def __str__(self):
        return f"{self.name_category}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
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

    def __str__(self):
        return f"{self.product_name} {self.price_product}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("price_product",)
