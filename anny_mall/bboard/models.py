from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=80, verbose_name="Вещь")
    length = models.IntegerField(null=False, verbose_name="Длина")
    description = models.TextField(null=False, blank=True, verbose_name="Описание")
    price = models.FloatField(null=True, blank=True, verbose_name="Цена")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, verbose_name="Рубрика")
    image = models.ImageField(default="default.jpg", upload_to="ad_images", blank=True, verbose_name="Фото")

    class Meta:
        verbose_name_plural = "Вещи"
        verbose_name = "Вещь"
        ordering = ["-published"]


class Rubric(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Рубрики"
        verbose_name = "Рубрика"
        ordering = ["name"]


# class Image(models.Model):
#     ad = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
#     title = models.ImageField(default="default.jpg", upload_to="media")

#     def __str__(self):
#         return f" {self.ad.name} image"

#     class Meta:
#         verbose_name_plural = "Фото"
#         verbose_name = "Фото"
#         ordering = ["title"]
