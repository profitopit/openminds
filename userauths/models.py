from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
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

class Service(models.Model):
    sid = models.CharField(unique=True, max_length=20) 
    title = models.CharField(max_length=100, default="Project management")

    description = models.TextField(null=True, blank=True, default="This is the service")
    
    
    date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        shortened_title = self.title[:20] 
        slug = slugify(shortened_title)
        # Set the bid to the slug
        self.sid = f"{slug}"
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Services"
    def __str__(self):
        return self.title

class Booking(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    business_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    company_type = models.CharField(max_length=20)
    company_needs = models.ManyToManyField(Service)
    message = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.business_name
    class Meta:
        verbose_name_plural = "Clients Booking"