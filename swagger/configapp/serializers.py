from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Category, Transaction, RecurringPayment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_display', 'icon', 'color']
        read_only_fields = ['id']


class AccountSerializer(serializers.ModelSerializer):
    """Сериализатор для счетов"""
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'currency', 'currency_display', 'icon', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Сериализатор для транзакций"""
    account_name = serializers.CharField(source='account.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'account', 'account_name', 'category', 'category_name',
            'type', 'type_display', 'amount', 'description', 'date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        account = transaction.account

        # Обновляем баланс счета
        if transaction.type == 'income':
            account.balance += transaction.amount
        elif transaction.type == 'expense':
            account.balance -= transaction.amount
        account.save()

        return transaction


class RecurringPaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для регулярных платежей"""
    account_name = serializers.CharField(source='account.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    frequency_display = serializers.CharField(source='get_frequency_display', read_only=True)

    class Meta:
        model = RecurringPayment
        fields = [
            'id', 'account', 'account_name', 'category', 'category_name',
            'amount', 'description', 'frequency', 'frequency_display',
            'start_date', 'end_date', 'is_active', 'last_executed'
        ]
        read_only_fields = ['id', 'last_executed']


class AccountDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для счета с транзакциями"""
    transactions = TransactionSerializer(many=True, read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'currency', 'currency_display', 'icon', 'created_at', 'transactions']
        read_only_fields = ['id', 'created_at', 'transactions']
