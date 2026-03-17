from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'phone', 'start_date', 'is_active')
    list_display_links = ('name', 'cpf')
    search_fields = ('name', 'cpf')
    list_per_page = 20

admin.site.register(Customer, CustomerAdmin)
