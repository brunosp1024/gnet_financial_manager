from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'value', 'due_date', 'status', 'paid_at']
    list_filter = ['status']
    search_fields = ['customer__name']
