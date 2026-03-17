from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'phone', 'position', 'modality', 'is_active')
    list_display_links = ('name', 'cpf')
    search_fields = ('name', 'cpf')
    list_per_page = 20

admin.site.register(Employee, EmployeeAdmin)
