from django.contrib import admin
from userauths.models import User, Contact, Service, Booking

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(User, UserAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'message']

admin.site.register(Contact, ContactAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

admin.site.register(Service, ServiceAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ['business_name','email',  'company_type']
admin.site.register(Booking,BookingAdmin)