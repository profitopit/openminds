from django.urls import path
from .views import index, contact, blog_detail_view, blog_view, event_detail_view, event_view, ajax_add_review, search_view

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('blogs/', blog_view, name='blogs'),
    path('blog/<bid>/', blog_detail_view, name='blog-detail'),
    path('events/', event_view, name='events'),
    path('event/<eid>/', event_detail_view, name='event-detail'),
    path("ajax-add-review/", ajax_add_review, name="ajax-add-review"),
    path("search/", search_view, name="search"),

]
