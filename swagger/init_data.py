#!/usr/bin/env python
"""
Скрипт инициализации примерных данных для API.
Запустите через: python manage.py shell < init_data.py
"""

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from configapp.models import Account, Category

# Создание пользователя
username = "testuser"
email = "test@example.com"
password = "testpass123"

# Проверка существования пользователя
if User.objects.filter(username=username).exists():
    print(f"✓ Пользователь '{username}' уже существует")
    user = User.objects.get(username=username)
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name="Test",
        last_name="User"
    )
    print(f"✓ Создан пользователь '{username}'")

# Создание или получение токена
token, created = Token.objects.get_or_create(user=user)
if created:
    print(f"✓ Создан токен: {token.key}")
else:
    print(f"✓ Токен уже существует: {token.key}")

# Категории расходов
expense_categories = [
    {"name": "Еда", "icon": "🍔", "color": "#FF6B6B"},
    {"name": "Транспорт", "icon": "🚗", "color": "#4ECDC4"},
    {"name": "Развлечения", "icon": "🎮", "color": "#45B7D1"},
    {"name": "Коммунальные услуги", "icon": "💡", "color": "#FFA07A"},
    {"name": "Здоровье", "icon": "⚕️", "color": "#98D8C8"},
    {"name": "Одежда", "icon": "👔", "color": "#F7DC6F"},
]

# Категории доходов
income_categories = [
    {"name": "Зарплата", "icon": "💼", "color": "#52C41A"},
    {"name": "Фриланс", "icon": "💻", "color": "#1890FF"},
    {"name": "Инвестиции", "icon": "📈", "color": "#722ED1"},
    {"name": "Подарки", "icon": "🎁", "color": "#EB2F96"},
]

# Создание категорий расходов
for cat_data in expense_categories:
    category, created = Category.objects.get_or_create(
        user=user,
        name=cat_data["name"],
        type="expense",
        defaults={
            "icon": cat_data["icon"],
            "color": cat_data["color"]
        }
    )
    if created:
        print(f"✓ Создана категория расходов: {cat_data['name']}")
    else:
        print(f"✓ Категория расходов существует: {cat_data['name']}")

# Создание категорий доходов
for cat_data in income_categories:
    category, created = Category.objects.get_or_create(
        user=user,
        name=cat_data["name"],
        type="income",
        defaults={
            "icon": cat_data["icon"],
            "color": cat_data["color"]
        }
    )
    if created:
        print(f"✓ Создана категория доходов: {cat_data['name']}")
    else:
        print(f"✓ Категория доходов существует: {cat_data['name']}")

# Счета
accounts = [
    {"name": "Основной счет", "currency": "UZS", "balance": "5000.00", "icon": "💳"},
    {"name": "USD счет", "currency": "USD", "balance": "1000.00", "icon": "💵"},
    {"name": "EUR счет", "currency": "EUR", "balance": "500.00", "icon": "💶"},
]

# Создание счетов
for acc_data in accounts:
    account, created = Account.objects.get_or_create(
        user=user,
        name=acc_data["name"],
        defaults={
            "currency": acc_data["currency"],
            "balance": acc_data["balance"],
            "icon": acc_data["icon"]
        }
    )
    if created:
        print(f"✓ Создан счет: {acc_data['name']}")
    else:
        print(f"✓ Счет существует: {acc_data['name']}")

print("\n" + "="*60)
print("✅ Инициализация завершена!")
print("="*60)
print(f"\nДанные для входа:")
print(f"  Пользователь: {username}")
print(f"  Пароль: {password}")
print(f"  Токен: {token.key}")
print(f"\nИспользуйте этот токен для авторизации в Swagger:")
print(f"  Authorization: Token {token.key}")
print("\n📚 API документация доступна по адресам:")
print("  - Swagger UI: http://localhost:8000/api/docs/")
print("  - ReDoc: http://localhost:8000/api/redoc/")
print("  - OpenAPI Schema: http://localhost:8000/api/schema/")
print("="*60)

exit()
