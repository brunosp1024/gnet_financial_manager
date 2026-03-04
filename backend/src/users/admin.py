from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'email')
    list_per_page = 20

admin.site.register(User, UserAdmin)
