from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.db.models import Sum, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

from products.models import Product


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return 'Order status: %s' % self.name
        
    class Meta:
        verbose_name = 'Order status'
        verbose_name_plural = 'Order status'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    user_first_name = models.CharField(max_length=150, blank=True, default=None)
    user_last_name = models.CharField(max_length=150, blank=True, default=None)
    user_phone = PhoneNumberField(default=None)
    user_address = models.CharField(max_length=150, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return 'Order %s %s' % (self.id, self.status.name)
        
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s' % self.product.name
        
    class Meta:
        verbose_name = 'Product in order'
        verbose_name_plural = 'Products in order'
        
    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        if self.product.discount:
            price_per_item -= price_per_item * Decimal(self.product.discount / 100)
            self.price_per_item = price_per_item
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item
        
        super().save(*args, **kwargs)


@receiver(post_save, sender=ProductInOrder)
def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


class ProductInCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s' % self.product.name
        
    class Meta:
        verbose_name = 'Product in cart'
        verbose_name_plural = 'Products in cart'
        
    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        if self.product.discount:
            price_per_item -= price_per_item * Decimal(self.product.discount / 100)
            self.price_per_item = price_per_item
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item
        
        super().save(*args, **kwargs)


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='User')
    obj = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, verbose_name='Product', related_name='favorites')
    
    def __str__(self):
        return '{}{}'.format(self.user.username, self.obj.name)
