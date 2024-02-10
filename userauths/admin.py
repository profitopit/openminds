from django.contrib import admin
from userauths.models import User, Contact

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(User, UserAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'message']

admin.site.register(Contact, ContactAdmin)