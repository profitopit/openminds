from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
import cloudinary
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver 

cloudinary.config( 
  cloud_name = getattr(settings, 'CLOUD_NAME', None), 
  api_key = getattr(settings, 'API_KEY', None), 
  api_secret = getattr(settings, 'API_SECRET', None)
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notification_title = models.CharField(max_length=100, default="openminds")
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.notification_title

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bid = ShortUUIDField(unique=True, length=10, max_length=45, prefix="", alphabet="abcdefgh12345") 
    blog_title = models.CharField(max_length=100, default="blog")
    image =  CloudinaryField(folder="blog-images")
    blog_page_image = CloudinaryField(folder="blog-images")
    cover_image =  CloudinaryField(folder="blog-images")
    description = RichTextUploadingField(null=True, blank=True, default="Case study ")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    featured = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    def blog_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def save(self, *args, **kwargs):
        # Check if the instance is being updated and has an existing image
        shortened_title = self.blog_title[:40]  # You can adjust the length as needed
        # Convert the shortened title to a slug
        slug = slugify(shortened_title)
        # Set the bid to the slug
        self.bid = f"{slug}"
        if self.pk and self.blog_page_image:
            # Get the original instance from the database
            original_instance = Blog.objects.get(pk=self.pk)
            # Check if the image has changed
            if original_instance.blog_page_image != self.blog_page_image:
                # Delete the old image from Cloudinary
                public_id = original_instance.blog_page_image.public_id
                cloudinary.uploader.destroy(public_id)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the image from Cloudinary before deleting the Blog object
        if self.blog_page_image:
            # Get the public ID of the image from Cloudinary
            public_id = self.blog_page_image.public_id
            # Delete the image from Cloudinary
            cloudinary.uploader.destroy(public_id)
        # Call the parent class delete method to delete the Blog object
        super().delete(*args, **kwargs)
    def __str__(self):
        return self.blog_title
    def get_absolute_url(self):
        return f'/blog/{self.bid}/'
    

@receiver(post_delete, sender=Blog)
def delete_blog_image(sender, instance, **kwargs):
    # Delete the image from Cloudinary when a Blog instance is deleted
    if instance.blog_page_image:
        public_id = instance.blog_page_image.public_id
        cloudinary.uploader.destroy(public_id)
    
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