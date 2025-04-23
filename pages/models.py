from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

# Create your models here.


class Developer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'developer'
        verbose_name_plural = 'developers'

    def get_absolute_url(self):
        return reverse("developer", args=[str(self.id)])

    def __str__(self):
        return self.name
    
class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='covers/', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse('pages:products_by_category', args=[self.id])

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    age_rating = models.IntegerField(blank = True, null=True)
    picture = models.ImageField(upload_to='covers/', blank=True, null=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    updated = models.DateTimeField(auto_now=True, blank = True, null = True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null = True)
    preorder = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def get_absolute_url(self):
        return reverse('pages:product_detail', args=[self.category.id, self.id])

    def __str__(self):
        return self.name


class Rental(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    duration = models.IntegerField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user} rented {self.product.name}"

