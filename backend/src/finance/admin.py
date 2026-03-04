from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'category', 'payment_method', 'value', 'customer', 'created_at')
    list_display_links = ('type', 'category')
    search_fields = ('customer__name', 'created_at')
    list_per_page = 20

admin.site.register(Transaction, TransactionAdmin)
