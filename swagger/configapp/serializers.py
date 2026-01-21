from rest_framework import serializers
from .models import Account, Transaction, Category, RecurringPayment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'type']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'currency', 'icon', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    account_detail = AccountSerializer(source='account', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'account',
            'account_detail',
            'category',
            'category_detail',
            'amount',
            'type',
            'description',
            'date',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class RecurringPaymentSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    account_detail = AccountSerializer(source='account', read_only=True)

    class Meta:
        model = RecurringPayment
        fields = [
            'id',
            'account',
            'account_detail',
            'category',
            'category_detail',
            'amount',
            'description',
            'start_date',
            'end_date',
            'frequency',
            'is_active',
        ]
        read_only_fields = ['id']
