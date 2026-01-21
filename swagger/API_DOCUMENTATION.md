# Bank Management API Documentation

## 📋 Обзор

Это REST API для управления банковскими счетами, транзакциями, категориями и регулярными платежами.

## 🚀 Запуск сервера

```bash
python manage.py runserver 8000
```

## 📚 Документация API

### Swagger UI
- **URL**: `http://localhost:8000/swagger/`
- Интерактивная документация для тестирования API

### ReDoc
- **URL**: `http://localhost:8000/redoc/`
- Красивая документация API

### JSON Schema
- **URL**: `http://localhost:8000/swagger.json`

### YAML Schema
- **URL**: `http://localhost:8000/swagger.yaml`

## 🔌 API Endpoints

### Счета (Accounts)
```
GET    /api/v1/accounts/              - Список всех счетов
POST   /api/v1/accounts/              - Создать новый счет
GET    /api/v1/accounts/{id}/         - Детали счета
PUT    /api/v1/accounts/{id}/         - Обновить счет
DELETE /api/v1/accounts/{id}/         - Удалить счет
GET    /api/v1/accounts/summary/      - Общая статистика по счетам
```

### Транзакции (Transactions)
```
GET    /api/v1/transactions/                    - Список всех транзакций
POST   /api/v1/transactions/                    - Создать новую транзакцию
GET    /api/v1/transactions/{id}/               - Детали транзакции
PUT    /api/v1/transactions/{id}/               - Обновить транзакцию
DELETE /api/v1/transactions/{id}/               - Удалить транзакцию
GET    /api/v1/transactions/by_account/         - Транзакции конкретного счета
GET    /api/v1/transactions/statistics/         - Статистика по транзакциям
```

**Параметры для фильтрации:**
- `account_id` - ID счета (обязательный для by_account)
- `type` - Тип транзакции: `income` или `expense`
- `period` - Период: `all`, `today`, `week`, `month`

### Категории (Categories)
```
GET    /api/v1/categories/            - Список всех категорий
POST   /api/v1/categories/            - Создать новую категорию
GET    /api/v1/categories/{id}/       - Детали категории
PUT    /api/v1/categories/{id}/       - Обновить категорию
DELETE /api/v1/categories/{id}/       - Удалить категорию
```

### Регулярные платежи (Recurring Payments)
```
GET    /api/v1/recurring-payments/                - Список всех платежей
POST   /api/v1/recurring-payments/                - Создать новый платеж
GET    /api/v1/recurring-payments/{id}/           - Детали платежа
PUT    /api/v1/recurring-payments/{id}/           - Обновить платеж
DELETE /api/v1/recurring-payments/{id}/           - Удалить платеж
POST   /api/v1/recurring-payments/{id}/activate/  - Активировать платеж
POST   /api/v1/recurring-payments/{id}/deactivate/ - Деактивировать платеж
```

## 📝 Примеры запросов

### 1. Создать счет
```bash
curl -X POST http://localhost:8000/api/v1/accounts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Мой счет",
    "account_number": "1234567890",
    "bank": "ОТП Банк",
    "balance": 1000.00,
    "currency": "UZS"
  }'
```

### 2. Получить все счета
```bash
curl http://localhost:8000/api/v1/accounts/
```

### 3. Создать транзакцию
```bash
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{
    "account": 1,
    "category": 1,
    "amount": 50000.00,
    "type": "expense",
    "description": "Обед",
    "date": "2026-01-21T12:30:00Z"
  }'
```

### 4. Получить статистику
```bash
curl http://localhost:8000/api/v1/transactions/statistics/
```

### 5. Получить транзакции конкретного счета
```bash
curl "http://localhost:8000/api/v1/transactions/by_account/?account_id=1&period=month&type=expense"
```

## ⚙️ Конфигурация

### REST Framework Settings (в settings.py)

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## 🔐 Безопасность

В текущей версии API открыт для всех. Для production рекомендуется добавить:
- Аутентификацию (JWT, OAuth2)
- Разрешения (Permissions)
- Rate limiting
- CORS конфигурацию

## 📦 Структура файлов

```
configapp/
├── models.py           - Модели данных
├── serializers.py      - DRF сериализаторы (новый файл)
├── api_views.py        - API viewsets (новый файл)
├── views.py            - Старые views (для совместимости)
├── urls.py             - URL patterns
├── admin.py            - Django admin
└── forms.py            - Django forms

config/
├── settings.py         - Конфигурация (обновлено)
├── urls.py             - URL routing (обновлено)
└── wsgi.py             - WSGI конфигурация
```

## ✅ Что было сделано

1. ✅ Установлены пакеты: `djangorestframework` и `drf-yasg`
2. ✅ Создан файл `serializers.py` с сериализаторами для всех моделей
3. ✅ Создан файл `api_views.py` с ViewSets для REST API
4. ✅ Обновлен `settings.py` - добавлены приложения и конфигурация
5. ✅ Обновлен `config/urls.py` - добавлены API routes и Swagger
6. ✅ ✅ Удалена папка `templates/`

## 🔗 Полезные ссылки

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)
- [OpenAPI Specification](https://spec.openapis.org/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
