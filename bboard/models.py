from django.db import models
from django.urls import reverse


def image_directory_path(instance, filename) -> str:
    return f'ad_images/{filename}'


class Item(models.Model):
    name = models.CharField(max_length=80, verbose_name="Вещь")
    length = models.IntegerField(null=False, verbose_name="Длина")
    description = models.TextField(null=False, blank=True, verbose_name="Описание")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, verbose_name="Рубрика")
    image = models.ImageField(upload_to=image_directory_path, blank=True, verbose_name="Фото")

    class Meta:
        verbose_name_plural = "Вещи"
        verbose_name = "Вещь"
        ordering = ["-published"]

    def get_absolute_url(self):
        return reverse('ad-detail', kwargs={'pk': self.pk})


class Rubric(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Рубрики"
        verbose_name = "Рубрика"
        ordering = ["name"]
