from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField( max_length=100)
    full_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default="Nigeria")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Users that contacted"
    def __str__(self):
        return self.email