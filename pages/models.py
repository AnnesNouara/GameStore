from django.db import models
import uuid
from django.urls import reverse

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
    picture = models.ImageField(upload_to='covers/', blank=True, null=True)
    stock_quantity = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    updated = models.DateTimeField(auto_now=True, blank = True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null = True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def get_absolute_url(self):
        return reverse('pages:product_detail', args=[self.category.id, self.id])

    def __str__(self):
        return self.name