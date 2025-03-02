from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from pages.models import Developer

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    Developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user) 

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.id)])
# Create your models here.
