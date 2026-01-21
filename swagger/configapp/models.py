from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Account(models.Model):
    CURRENCY_CHOICES = [
        ('UZS', _('UZS')),
        ('USD', _('USD')),
        ('EUR', _('EUR')),
    ]

    name = models.CharField(max_length=100, verbose_name=_('Account name'))
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Balance'))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS', verbose_name=_('Currency'))
    icon = models.CharField(max_length=50, default='💳', verbose_name=_('Icon'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.currency})"


class Category(models.Model):
    TYPE_CHOICES = [
        ('expense', _('Expense')),
        ('income', _('Income')),
    ]

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=50, default='📊')
    color = models.CharField(max_length=7, default='#FF6B6B')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('transfer', _('Transfer')),
        ('expense', _('Expense')),
        ('income', _('Income')),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_type_display()} — {self.amount}"


class RecurringPayment(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=200)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_executed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description
