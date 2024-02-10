from django.contrib import admin
from core.models import Review, Blog, BlogImages, Event, EventImages


admin.site.site_header = 'Openminds Administration'

class BlogImagesAdmin(admin.TabularInline):
    model = BlogImages

class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogImagesAdmin]
    list_display = ['user','image','blog_title', 'featured', 'date','bid']

class EventImagesAdmin(admin.TabularInline):
    model = EventImages

class EventAdmin(admin.ModelAdmin):
    inlines = [EventImagesAdmin]
    list_display = ['user','image','event_title', 'featured', 'date','eid']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','title','review']


admin.site.register(Blog, BlogAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Review, ReviewAdmin)

