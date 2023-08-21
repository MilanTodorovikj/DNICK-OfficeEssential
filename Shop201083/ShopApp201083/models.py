from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ShopUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Product(models.Model):
    CATEGORIES = [
        ('Производи од Хартија', 'Производи од Хартија'),
        ('Канцелариски Мебел', 'Канцелариски Мебел'),
        ('Школски Производи', 'Школски Производи'),
        ('Тонери Медиуми и ИТ Производи', 'Тонери Медиуми и ИТ Производи'),
        ('Канцелариски Производи', 'Канцелариски Производи'),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    category = models.CharField(max_length=255, null=False, blank=False, choices=CATEGORIES)
    model = models.CharField(max_length=255, null=False, blank=False)
    manufacturer = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="ShopApp201083/static/images")
    description = models.TextField(max_length=600)

    def __str__(self):
        return f"{self.name} - {self.manufacturer} - {self.model} - {self.category}"


class Order(models.Model):
    buyer = models.ForeignKey(ShopUser, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)

    @property
    def get_order_total_price(self):
        order_items = self.orderitem_set.all()
        total_price = 0
        for item in order_items:
            total_price += int(item.product.price) * int(item.quantity)

        return total_price

    def __str__(self):
        return f'{self.buyer} - {self.is_ordered} - {self.orderitem_set.all()}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False, blank=False)

    def get_shopping_cart_item_price(self):
        total_price = self.product.price * self.quantity
        return total_price

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Delivery(models.Model):
    buyer = models.ForeignKey(ShopUser, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=False)

    name = models.CharField(max_length=255, null=False, blank=False)
    surname = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField()
    phone_number = models.IntegerField(null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)

    card_payment = models.BooleanField(default=False)
    card_name = models.CharField(max_length=255)
    card_number = models.IntegerField()
    card_valid_until = models.CharField(max_length=5)
    card_ccv = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.surname} - {self.order}"
