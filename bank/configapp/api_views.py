from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta

from .models import Account, Category, Transaction, RecurringPayment
from .serializers import (
    UserSerializer, UserRegisterSerializer, CategorySerializer,
    AccountSerializer, TransactionSerializer, RecurringPaymentSerializer,
    AccountDetailSerializer
)


class UserRegisterViewSet(viewsets.ModelViewSet):
    """API для регистрации пользователей"""
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Создаём токен для нового пользователя
        token, created = Token.objects.get_or_create(user=user)
        
        return Response(
            {
                'user': UserSerializer(user).data,
                'token': token.key
            },
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Получить данные текущего пользователя"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Выход пользователя (удаление токена)"""
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """API для работы с категориями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем категории по типу если передан параметр"""
        queryset = Category.objects.all()
        category_type = self.request.query_params.get('type', None)
        
        if category_type:
            queryset = queryset.filter(type=category_type)
        
        return queryset

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Получить категории по типу"""
        category_type = request.query_params.get('type', None)
        
        if not category_type:
            return Response(
                {'error': 'type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        categories = self.get_queryset().filter(type=category_type)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
    """API для работы со счетами"""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Используем детальный сериализатор для retrieve"""
        if self.action == 'retrieve':
            return AccountDetailSerializer
        return AccountSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Получить сводку по всем счетам"""
        accounts = self.get_queryset()
        total_balance = accounts.aggregate(total=Sum('balance'))['total'] or 0
        
        # Расходы и доходы за текущий месяц
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        month_expenses = Transaction.objects.filter(
            type='expense',
            date__date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        month_income = Transaction.objects.filter(
            type='income',
            date__date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            'total_balance': total_balance,
            'accounts_count': accounts.count(),
            'month_expenses': month_expenses,
            'month_income': month_income,
            'accounts': AccountSerializer(accounts, many=True).data
        })

    @action(detail=True, methods=['get'])
    def transactions(self, request, pk=None):
        """Получить транзакции счета"""
        account = self.get_object()
        transactions = account.transactions.all()
        
        # Фильтрация по типу
        transaction_type = request.query_params.get('type', None)
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


class TransactionViewSet(viewsets.ModelViewSet):
    """API для работы с транзакциями"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем транзакции по параметрам"""
        queryset = Transaction.objects.all()
        
        # Фильтрация по счету
        account_id = self.request.query_params.get('account_id', None)
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        
        # Фильтрация по типу
        transaction_type = self.request.query_params.get('type', None)
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        
        # Фильтрация по категории
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Фильтрация по периоду
        period = self.request.query_params.get('period', None)
        if period:
            today = timezone.now().date()
            if period == 'today':
                queryset = queryset.filter(date__date=today)
            elif period == 'week':
                week_ago = today - timedelta(days=7)
                queryset = queryset.filter(date__date__gte=week_ago)
            elif period == 'month':
                month_start = today.replace(day=1)
                queryset = queryset.filter(date__date__gte=month_start)
        
        return queryset.order_by('-date')

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Получить статистику по транзакциям"""
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        # Расходы по категориям за месяц
        expenses_by_category = Transaction.objects.filter(
            type='expense',
            date__date__gte=month_start
        ).values('category__name', 'category__icon').annotate(
            total=Sum('amount')
        ).order_by('-total')[:10]
        
        # Общие статистики
        month_expenses = Transaction.objects.filter(
            type='expense',
            date__date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        month_income = Transaction.objects.filter(
            type='income',
            date__date__gte=month_start
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            'month_expenses': month_expenses,
            'month_income': month_income,
            'expenses_by_category': expenses_by_category,
            'balance': month_income - month_expenses
        })


class RecurringPaymentViewSet(viewsets.ModelViewSet):
    """API для работы с регулярными платежами"""
    queryset = RecurringPayment.objects.all()
    serializer_class = RecurringPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем активные платежи"""
        is_active = self.request.query_params.get('is_active', None)
        queryset = RecurringPayment.objects.all()
        
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Деактивировать регулярный платеж"""
        recurring = self.get_object()
        recurring.is_active = False
        recurring.save()
        return Response({'status': 'Payment deactivated'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Активировать регулярный платеж"""
        recurring = self.get_object()
        recurring.is_active = True
        recurring.save()
        return Response({'status': 'Payment activated'})
