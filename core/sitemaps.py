from django.contrib.sitemaps import Sitemap
from django.db.models.base import Model
from django.urls import reverse
from .models import Blog, Event

class StaticSitemap(Sitemap):
    def items(self):
        return ['core:index','core:about','core:contact','core:blogs','core:events','userauths:sign-in','userauths:sign-up']
    def location(self, item):
        return reverse(item)
    
class EventSitemap(Sitemap):
    def items(self):
        return Event.objects.all().order_by('-date')  
    
class BlogSitemap(Sitemap):
    def items(self):
        return Blog.objects.all().order_by('-date')  