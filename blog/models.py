from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Article(models.Model):
    article_name = models.CharField(max_length=100, verbose_name="статья")
    article_content = models.TextField(verbose_name="содержание", **NULLABLE)
    article_image = models.ImageField(upload_to="image_article/", verbose_name="превью", **NULLABLE)

    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания")
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)

    def __str__(self):
        return f"{self.article_name} (от {self.created_at})"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
