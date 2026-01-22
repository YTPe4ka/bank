# Bank Management API - Полное руководство

## 🚀 Быстрый старт

### Доступ к Swagger
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Запуск сервера
```bash
python manage.py runserver
```

---

## 🔐 Аутентификация

### 1. Регистрация нового пользователя
**POST** `/api/register/`

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123",
  "password2": "secure_password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Ответ (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbea6f3ee4"
}
```

### 2. Использование токена в запросах
Добавьте заголовок к каждому авторизованному запросу:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbea6f3ee4
```

**Или в Swagger UI:**
1. Нажмите на кнопку "Authorize" в верхнем правом углу
2. Введите: `Token 9944b09199c62bcf9418ad846dd0e4bbea6f3ee4`
3. Нажмите "Authorize"

### 3. Получить информацию о текущем пользователе
**GET** `/api/users/me/`

**Ответ:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 4. Выход пользователя
**POST** `/api/users/logout/`

---

## 💳 Работа со счетами (Accounts)

### Создать новый счет
**POST** `/api/accounts/`

```json
{
  "name": "Основной счет",
  "balance": "5000.00",
  "currency": "UZS",
  "icon": "💳"
}
```

### Получить все счета
**GET** `/api/accounts/`

### Получить детали счета с историей транзакций
**GET** `/api/accounts/{id}/`

### Получить сводку по всем счетам
**GET** `/api/accounts/summary/`

**Ответ:**
```json
{
  "total_balance": "15000.00",
  "accounts_count": 3,
  "month_expenses": "2500.00",
  "month_income": "8000.00",
  "accounts": [...]
}
```

### Получить транзакции конкретного счета
**GET** `/api/accounts/{id}/transactions/`

**Параметры фильтрации:**
- `type`: expense или income
- `period`: all, today, week, month

**Примеры:**
```
GET /api/accounts/1/transactions/?type=expense&period=month
GET /api/accounts/1/transactions/?period=week
```

---

## 📁 Работа с категориями (Categories)

### Создать новую категорию
**POST** `/api/categories/`

```json
{
  "name": "Еда",
  "type": "expense",
  "icon": "🍔",
  "color": "#FF6B6B"
}
```

### Получить все категории
**GET** `/api/categories/`

### Получить категории по типу
**GET** `/api/categories/by_type/?type=expense`

**Параметры:**
- `type`: expense или income

---

## 💰 Работа с транзакциями (Transactions)

### Создать новую транзакцию
**POST** `/api/transactions/`

```json
{
  "account": 1,
  "category": 2,
  "type": "expense",
  "amount": "150.50",
  "description": "Обед в кафе",
  "date": "2026-01-22T12:30:00Z"
}
```

### Получить все транзакции
**GET** `/api/transactions/`

### Фильтрация транзакций
**GET** `/api/transactions/?account_id=1&type=expense&period=month`

**Параметры:**
- `account_id`: ID счета
- `type`: expense или income
- `category_id`: ID категории
- `period`: all, today, week, month

### Получить статистику по транзакциям
**GET** `/api/transactions/statistics/`

**Ответ:**
```json
{
  "month_expenses": "5000.00",
  "month_income": "12000.00",
  "balance": "7000.00",
  "expenses_by_category": [
    {
      "category__name": "Еда",
      "category__icon": "🍔",
      "total": "1500.00"
    },
    ...
  ]
}
```

---

## 🔄 Регулярные платежи (Recurring Payments)

### Создать регулярный платеж
**POST** `/api/recurring-payments/`

```json
{
  "account": 1,
  "category": 3,
  "amount": "500.00",
  "description": "Интернет",
  "frequency": "monthly",
  "start_date": "2026-01-22",
  "end_date": "2027-12-31",
  "is_active": true
}
```

### Получить все регулярные платежи
**GET** `/api/recurring-payments/`

### Фильтр по статусу
**GET** `/api/recurring-payments/?is_active=true`

### Деактивировать платеж
**POST** `/api/recurring-payments/{id}/deactivate/`

### Активировать платеж
**POST** `/api/recurring-payments/{id}/activate/`

---

## 🧪 Тестирование в Swagger UI

### Как использовать "Try It Out"

1. **Откройте Swagger** → http://localhost:8000/api/docs/
2. **Авторизуйтесь** → Нажмите "Authorize" и введите токен
3. **Выберите эндпоинт** → Раскройте нужный запрос
4. **Нажмите "Try It Out"** → Кнопка появится справа
5. **Заполните параметры** → Введите необходимые данные
6. **Нажмите "Execute"** → Выполнится запрос
7. **Смотрите результат** → Ответ будет отображен ниже

### Пример: Создание категории

1. Откройте `/api/categories/` → **POST**
2. Нажмите "Try It Out"
3. Заполните Request Body:
```json
{
  "name": "Развлечения",
  "type": "expense",
  "icon": "🎮",
  "color": "#4ECDC4"
}
```
4. Нажмите "Execute"
5. Вы получите ответ с ID новой категории

---

## 🛠️ Структура проекта

```
.
├── config/                    # Конфигурация Django
│   ├── settings.py           # Основные настройки
│   ├── urls.py               # URL маршруты
│   └── wsgi.py               # WSGI приложение
├── configapp/                # Основное приложение
│   ├── models.py             # Модели базы данных
│   ├── serializers.py        # DRF сериализаторы
│   ├── api_views.py          # API представления
│   ├── forms.py              # Django формы
│   └── migrations/           # Миграции БД
├── manage.py                 # Django управление
└── db.sqlite3                # База данных (разработка)
```

---

## 📊 Модели данных

### User
- `username`: строка
- `email`: email
- `first_name`: строка
- `last_name`: строка
- `password`: строка (хеш)

### Account
- `user`: ForeignKey(User)
- `name`: строка
- `balance`: decimal
- `currency`: выбор (UZS, USD, EUR)
- `icon`: строка
- `created_at`: datetime

### Category
- `user`: ForeignKey(User)
- `name`: строка
- `type`: выбор (expense, income)
- `icon`: строка
- `color`: hex цвет

### Transaction
- `account`: ForeignKey(Account)
- `category`: ForeignKey(Category)
- `type`: выбор (expense, income)
- `amount`: decimal
- `description`: строка
- `date`: datetime
- `created_at`: datetime

### RecurringPayment
- `account`: ForeignKey(Account)
- `category`: ForeignKey(Category)
- `amount`: decimal
- `description`: строка
- `frequency`: выбор (daily, weekly, monthly, yearly)
- `start_date`: date
- `end_date`: date
- `is_active`: boolean
- `last_executed`: datetime

---

## 🔗 Полезные ссылки

- **Django REST Framework**: https://www.django-rest-framework.org/
- **drf-spectacular**: https://drf-spectacular.readthedocs.io/
- **Django**: https://docs.djangoproject.com/

---

## ⚠️ Важно

- Все авторизованные эндпоинты требуют токена в заголовке `Authorization: Token <token>`
- API использует Token Authentication
- Для разработки используется SQLite база данных
- DEBUG режим включен (для разработки)

---

## 📝 Примеры скриптов

### Создание пользователя и получение токена (Python)
```python
import requests

url = "http://localhost:8000/api/register/"
data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
}

response = requests.post(url, json=data)
user_data = response.json()
token = user_data['token']
print(f"Токен: {token}")
```

### Создание счета с авторизацией (Python)
```python
import requests

token = "YOUR_TOKEN_HERE"
headers = {"Authorization": f"Token {token}"}

url = "http://localhost:8000/api/accounts/"
data = {
    "name": "Мой счет",
    "balance": "1000.00",
    "currency": "UZS",
    "icon": "💳"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

---

Всё готово! Вы можете начинать использовать API через Swagger! 🎉
