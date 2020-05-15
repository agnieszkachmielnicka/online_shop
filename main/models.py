from django.db import models, __all__
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=20)
    product_description = models.CharField(max_length=100)
    product_price = models.FloatField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Basket(models.Model):
    products = models.ManyToManyField(Product, through='ProductsInBasket', blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ProductsInBasket(models.Model):
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, default=None, null=True)
    product_quantity = models.IntegerField(blank=True, default=0, null=True)


class ProductsList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()


class Order(models.Model):

    PAYMENT_CHOICES = (
        ('visa', 'Visa',),
        ('mastercard', 'MasterCard',),
        ('paypal', 'PayPal',),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_order = models.DateTimeField(editable=False)
    products = models.ManyToManyField(Product, blank=True, default=None)
    total_price = models.FloatField()
    address = models.CharField(max_length=500)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=200)
    country = CountryField()
    payment_method = models.CharField(
       max_length=40,
       choices=PAYMENT_CHOICES,
   )

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_of_order = timezone.now()
        return super().save(*args, **kwargs)


class Country(models.Model):
    country_name = models.CharField(max_length=250)
