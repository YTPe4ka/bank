from django.contrib import admin
from .models import Account, Category, Transaction, RecurringPayment


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'currency', 'created_at')
    list_filter = ('currency', 'created_at')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'icon')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'type', 'amount', 'category', 'date')
    list_filter = ('type', 'account', 'category', 'date')
    search_fields = ('description', 'account__name')
    readonly_fields = ('created_at',)


@admin.register(RecurringPayment)
class RecurringPaymentAdmin(admin.ModelAdmin):
    list_display = ('description', 'account', 'amount', 'frequency', 'is_active')
    list_filter = ('frequency', 'is_active', 'account')
    search_fields = ('description',)
    readonly_fields = ('last_executed',)
