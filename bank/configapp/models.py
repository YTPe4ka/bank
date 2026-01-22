from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class Account(models.Model):
    """Счет/Кошелек пользователя"""
    CURRENCY_CHOICES = [
        ('UZS', _('UZS')),
        ('USD', _('USD')),
        ('EUR', _('EUR')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100, verbose_name=_('Account name'))
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Balance'))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UZS', verbose_name=_('Currency'))
    icon = models.CharField(max_length=50, default='💳', verbose_name=_('Icon'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
    
    def __str__(self):
        return f"{self.name} ({self.currency})"


class Category(models.Model):
    """Категория расходов/доходов"""
    TYPE_CHOICES = [
        ('expense', _('Expense')),
        ('income', _('Income')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name=_('Type'))
    icon = models.CharField(max_length=50, default='📊', verbose_name=_('Icon'))
    color = models.CharField(max_length=7, default='#FF6B6B', verbose_name=_('Color'))
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        unique_together = ('name', 'type')
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    """Транзакция (операция)"""
    TRANSACTION_TYPES = [
        ('transfer', _('Transfer')),
        ('expense', _('Expense')),
        ('income', _('Income')),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', verbose_name=_('Account'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name=_('Type'))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Amount'))
    description = models.CharField(max_length=200, blank=True, verbose_name=_('Description'))
    date = models.DateTimeField(default=timezone.now, verbose_name=_('Date'))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.amount} {self.account.currency}"


class RecurringPayment(models.Model):
    """Регулярный платеж"""
    FREQUENCY_CHOICES = [
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recurring_payments', verbose_name=_('Account'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Amount'))
    description = models.CharField(max_length=200, verbose_name=_('Description'))
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name=_('Frequency'))
    start_date = models.DateField(verbose_name=_('Start date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End date'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    last_executed = models.DateTimeField(null=True, blank=True, verbose_name=_('Last executed'))
    
    class Meta:
        verbose_name = _('Recurring payment')
        verbose_name_plural = _('Recurring payments')
    
    def __str__(self):
        return f"{self.description} - {self.amount} ({self.get_frequency_display()})"


# Signal для создания токена при создании пользователя
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Автоматически создаём токен для нового пользователя"""
    if created:
        Token.objects.get_or_create(user=instance)
