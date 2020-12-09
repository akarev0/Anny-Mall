from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


def image_directory_path(instance, filename) -> str:
    return f'ad_images/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Имя категории")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    size = models.IntegerField(null=False, verbose_name="Размер")
    description = models.TextField(null=False, verbose_name="Описание")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField(upload_to=image_directory_path, blank=True, verbose_name="Фото")
    material = models.CharField(max_length=255, null=True, blank=True, verbose_name="Материал")
    season = models.CharField(max_length=255, null=True, blank=True, verbose_name="Сезон")

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'slug': self.slug})


class BasketProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name="Покупатель", on_delete=models.CASCADE, null=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    basket = models.ForeignKey("Basket", verbose_name="Корзина", on_delete=models.CASCADE,
                               related_name='related_products', blank=True)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name="Общая стоимость заказа")

    def __str__(self):
        return f"Продукт: {self.product.title} для корзины"

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Basket(models.Model):
    owner = models.ForeignKey("Customer", verbose_name="Владелец", on_delete=models.CASCADE, null=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    products = models.ManyToManyField(BasketProduct, blank=True, related_name='related_basket')
    total_products_in_basket = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name="Общая стоимость заказа")
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    orders = models.ManyToManyField('Order', verbose_name='Заказы', related_name='customer_orders')

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    basket = models.ForeignKey(Basket, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return f'{self.first_name}_{self.phone}_{self.order_date}'
