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