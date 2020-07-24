from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField

class User(AbstractUser):
    pass


class category(models.Model):
    category = models.CharField(max_length=60)

    def __str__(self):
        return self.category

class Listing(models.Model):
    title= models.CharField(max_length=60)
    description = models.TextField(max_length=256)
    price = MoneyField(max_digits=7, decimal_places=2, default_currency='USD')
    image= models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Upload image")
    category = models.ForeignKey(category, null=True, blank=True, on_delete=models.CASCADE, related_name='+')
    active = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


