"""
Management command для инициализации примерных данных.
Запустите: python manage.py init_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from configapp.models import Account, Category


class Command(BaseCommand):
    help = 'Инициализирует примерные данные для тестирования API'

    def handle(self, *args, **options):
        # Создание пользователя
        username = "testuser"
        email = "test@example.com"
        password = "testpass123"

        # Проверка существования пользователя
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"✓ Пользователь '{username}' уже существует")
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name="Test",
                last_name="User"
            )
            self.stdout.write(self.style.SUCCESS(f"✓ Создан пользователь '{username}'"))

        # Создание или получение токена
        token, created = Token.objects.get_or_create(user=user)
        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Создан токен: {token.key}"))
        else:
            self.stdout.write(f"✓ Токен уже существует: {token.key}")

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
                self.stdout.write(self.style.SUCCESS(f"✓ Создана категория расходов: {cat_data['name']}"))
            else:
                self.stdout.write(f"✓ Категория расходов существует: {cat_data['name']}")

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
                self.stdout.write(self.style.SUCCESS(f"✓ Создана категория доходов: {cat_data['name']}"))
            else:
                self.stdout.write(f"✓ Категория доходов существует: {cat_data['name']}")

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
                self.stdout.write(self.style.SUCCESS(f"✓ Создан счет: {acc_data['name']}"))
            else:
                self.stdout.write(f"✓ Счет существует: {acc_data['name']}")

        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("✅ Инициализация завершена!"))
        self.stdout.write("="*60)
        self.stdout.write(f"\nДанные для входа:")
        self.stdout.write(f"  Пользователь: {username}")
        self.stdout.write(f"  Пароль: {password}")
        self.stdout.write(f"  Токен: {token.key}")
        self.stdout.write(f"\nИспользуйте этот токен для авторизации в Swagger:")
        self.stdout.write(f"  Authorization: Token {token.key}")
        self.stdout.write(f"\n📚 API документация доступна по адресам:")
        self.stdout.write(f"  - Swagger UI: http://localhost:8000/api/docs/")
        self.stdout.write(f"  - ReDoc: http://localhost:8000/api/redoc/")
        self.stdout.write(f"  - OpenAPI Schema: http://localhost:8000/api/schema/")
        self.stdout.write("="*60)
