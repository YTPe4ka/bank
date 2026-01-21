from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from .models import Account, Transaction, Category, RecurringPayment
from .serializers import (
    AccountSerializer, TransactionSerializer, 
    CategorySerializer, RecurringPaymentSerializer
)


class AccountViewSet(viewsets.ModelViewSet):
    """
    API для работы со счетами.
    
    - list: Получить список всех счетов
    - create: Создать новый счет
    - retrieve: Получить детали счета
    - update: Обновить счет
    - destroy: Удалить счет
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Получить общую статистику по счетам"""
        accounts = Account.objects.all()
        total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
        
        return Response({
            'total_accounts': accounts.count(),
            'total_balance': total_balance,
            'accounts': AccountSerializer(accounts, many=True).data
        })


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API для работы с транзакциями.
    
    - list: Получить список транзакций
    - create: Создать новую транзакцию
    - retrieve: Получить детали транзакции
    - update: Обновить транзакцию
    - destroy: Удалить транзакцию
    """
    queryset = Transaction.objects.select_related('account', 'category').all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        """При создании транзакции обновляем баланс счета"""
        transaction = serializer.save()
        account = transaction.account
        
        if transaction.type == 'income':
            account.balance += transaction.amount
        elif transaction.type == 'expense':
            account.balance -= transaction.amount
        account.save()

    def perform_destroy(self, instance):
        """При удалении транзакции восстанавливаем баланс счета"""
        account = instance.account
        
        if instance.type == 'income':
            account.balance -= instance.amount
        elif instance.type == 'expense':
            account.balance += instance.amount
        account.save()
        
        instance.delete()

    @action(detail=False, methods=['get'])
    def by_account(self, request):
        """Получить транзакции конкретного счета"""
        account_id = request.query_params.get('account_id')
        if not account_id:
            return Response({'error': 'account_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        transactions = Transaction.objects.filter(account_id=account_id).select_related('account', 'category')
        
        # Фильтрация по типу
        transaction_type = request.query_params.get('type')
        if transaction_type:
            transactions = transactions.filter(type=transaction_type)
        
        # Фильтрация по периоду
        period = request.query_params.get('period', 'all')
        today = timezone.now().date()
        
        if period == 'today':
            transactions = transactions.filter(date__date=today)
        elif period == 'week':
            week_ago = today - timedelta(days=7)
            transactions = transactions.filter(date__date__gte=week_ago)
        elif period == 'month':
            month_start = today.replace(day=1)
            transactions = transactions.filter(date__date__gte=month_start)
        
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Получить статистику по транзакциям"""
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        # Расходы за месяц
        month_expenses = Transaction.objects.filter(
            type='expense',
            date__date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Доходы за месяц
        month_income = Transaction.objects.filter(
            type='income',
            date__date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Расходы сегодня
        today_expenses = Transaction.objects.filter(
            type='expense',
            date__date=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Доходы сегодня
        today_income = Transaction.objects.filter(
            type='income',
            date__date=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Расходы по категориям за месяц
        expenses_by_category = Transaction.objects.filter(
            type='expense',
            date__date__gte=month_start
        ).values('category__name').annotate(sum=Sum('amount')).order_by('-sum')
        
        return Response({
            'month_expenses': month_expenses,
            'month_income': month_income,
            'today_expenses': today_expenses,
            'today_income': today_income,
            'expenses_by_category': list(expenses_by_category)
        })


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для работы с категориями.
    
    - list: Получить список категорий
    - create: Создать новую категорию
    - retrieve: Получить детали категории
    - update: Обновить категорию
    - destroy: Удалить категорию
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RecurringPaymentViewSet(viewsets.ModelViewSet):
    """
    API для работы с регулярными платежами.
    
    - list: Получить список платежей
    - create: Создать новый платеж
    - retrieve: Получить детали платежа
    - update: Обновить платеж
    - destroy: Удалить платеж
    - activate: Активировать платеж
    - deactivate: Деактивировать платеж
    """
    queryset = RecurringPayment.objects.all()
    serializer_class = RecurringPaymentSerializer

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Активировать регулярный платеж"""
        recurring = self.get_object()
        recurring.is_active = True
        recurring.save()
        return Response({'status': 'Платеж активирован'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Деактивировать регулярный платеж"""
        recurring = self.get_object()
        recurring.is_active = False
        recurring.save()
        return Response({'status': 'Платеж деактивирован'})
