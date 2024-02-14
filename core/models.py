from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="", alphabet="abcdefgh12345") 
    blog_title = models.CharField(max_length=100, default="blog")
    image = models.ImageField(upload_to=user_directory_path, default="blog-img.jpg")
    blog_page_image = models.ImageField(upload_to=user_directory_path, default="blog-img.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="blog-cover.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="Case study ")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    featured = models.BooleanField(default=False)
    def blog_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def save(self, *args, **kwargs):
        # Generate a shorter version of the blog title
        shortened_title = self.blog_title[:20]  # You can adjust the length as needed
        # Convert the shortened title to a slug
        slug = slugify(shortened_title)
        # Set the bid to the slug
        self.bid = f"blog-{slug}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.blog_title
    def get_absolute_url(self):
        return f'/blog/{self.bid}/'
    
    
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    eid = ShortUUIDField(unique=True, length=10, max_length=40, prefix="", alphabet="abcdefgh12345") 
    event_title = models.CharField(max_length=100, default="event")
    event_discussion = models.CharField(max_length=150, default="")
    main_page_title = models.CharField(max_length=150, default="")
    image = models.ImageField(upload_to=user_directory_path, default="event-img.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="event-cover.jpg")
    description = models.TextField(null=True, blank=True, default="Case study ")
    host = models.CharField(max_length=30, default="event venue")
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    event_link = models.URLField()
    venue_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=100,default="event venue")
    featured = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def event_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def save(self, *args, **kwargs):
        # Generate a shorter version of the blog title
        shortened_title = self.event_title[:30]  # You can adjust the length as needed
        # Convert the shortened title to a slug
        slug = slugify(shortened_title)
        # Set the bid to the slug
        self.eid = f"event-{slug}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.event_title
    def get_absolute_url(self):
        return f'/event/{self.eid}/'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    occupation = models.CharField(max_length=40)
    title = models.CharField(max_length=50)
    review = models.CharField(max_length=130)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.title
    


class BlogImages(models.Model):
    images = models.ImageField(upload_to="blog-images", default="blog-img.jpg")
    blog = models.ForeignKey(Blog, related_name="blog_images", on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Blogs images"

class EventImages(models.Model):
    images = models.ImageField(upload_to="event-images", default="event-img.jpg")
    event = models.ForeignKey(Event, related_name="event_images", on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Events images"