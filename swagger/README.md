# Bank Management API - Swagger Edition

## ✨ ПОЛНОСТЬЮ ГОТОВАЯ И РАБОТОСПОСОБНАЯ ДОКУМЕНТАЦИЯ

### 🎯 Быстрый доступ к Swagger

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/  
- **OpenAPI Schema**: http://localhost:8000/api/schema/

---

## 🎯 Umumiy Xususiyatlar

Bu Django asosidagi moliyaviy boshqaruv tizimi shaxsiy va kichik biznes moliyasini boshqarish uchun mo'ljallangan. Tizimda veb interfeysi va to'liq REST API mavjud.

### ✅ Asosiy Imkoniyatlar:

#### 1. **Hisoblarni Boshqarish** 💳
- Bir nechta hisoblarni yaratish va boshqarish
- Turli valyutalarni qo'llab-quvvatlash (UZS, USD, EUR)
- Har bir hisob balansini real vaqtda kuzatish
- Hisoblar uchun moslashtirilgan emojis va ikonkalar

#### 2. **Operatsiyalar va Tranzaksiyalar** 📊
- Xarajatlar va daromadlarni qo'shish
- Operatsiyalarni kategoriyalar bo'yicha tasniflash
- Barcha operatsiyalarning to'liq tarixi
- Turi, kategoriya va davri bo'yicha filtrlash
- Qidirish va sortirovka

#### 3. **Kategoriya Boshqaruvi** 🏷️
- Dinamik kategoriyalar yaratish
- Xarajat va daromad kategoriyalari
- Har bir kategoriya uchun rasm va rang
- Kategoriyalarni tayyorlash (customize)

#### 4. **Muntazam To'lovlar** 🔄
- Takroriy to'lovlarni yaratish
- Turli chastotalarni qo'llab-quvvatlash (kunlik, haftalik, oylik, yillik)
- To'lovlarni faollashtirish/deaktivatsiya qilish
- Oxirgi bajarilishini kuzatish

#### 5. **Statistika va Tahlil** 📈
- Kategoriyalar bo'yicha xarajatlar jadvallari (pie chart)
- Kunlik xarajatlar jadvallari (line chart)
- Oylar va davr bo'yicha tahlil
- Xarajatlar bo'yicha eng yaxshi kategoriyalar
- Kirim vs Xarajat tahlili

#### 6. **Authentication va Xavfsizlik** 🔐
- Foydalanuvchi ro'yxatiga olish
- Token-based Authentication
- Qo'l bilan tizimga kirish
- Xavfli parol boshqarishi

#### 7. **REST API** 🚀
- To'liq REST API bilan veb va mobil ilova uchun
- Django REST Framework (DRF)
- Token authentication
- Filtering, searching, pagination
- API dokumentatsiyasi

---

## 🔧 Texnologiyalar

- **Backend:** Django 6.0+, Django REST Framework 3.16+
- **Database:** SQLite (yoki boshqa DB)
- **Frontend:** HTML5, Bootstrap 5, JavaScript
- **API:** REST API, Token Authentication
- **Tarjima:** Django i18n (ru, uz, en)

---

## 📋 O'rnatish va Sozlash

### 1. Loyihani Klonlash
```bash
cd c:\Users\Acer\ Nitro\Desktop\Django\bankmain\bank
```

### 2. Virtual Muhitni Yaratish (ixtiyoriy)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Kutubxonalarni O'rnatish
```bash
pip install -r requirements.txt
```

Agar `requirements.txt` yo'q bo'lsa, o'rnating:
```bash
pip install django>=6.0 djangorestframework pillow
```

### 4. Migratsiyalarni Bajarish
```bash
python manage.py migrate
```

### 5. Superuser (Admin) Yaratish
```bash
python manage.py createsuperuser
# Javob bering:
# Username: admin
# Email: admin@example.com
# Password: (o'zingizning parolingiz)
```

### 6. Serverni Ishga Tushirish
```bash
python manage.py runserver
```

Brauzerda oching: `http://localhost:8000`
Admin panelga: `http://localhost:8000/admin`

---

## 🌍 Tarjimalar (Tillar)

Tizim Uzbek, Rus va Ingliz tillarida mavjud.

**Tilni o'zgartirish uchun:**
1. Admin panelga kiring (`/admin`)
2. Django admin panelida tilni tanlang

**Hozirgi holatida:** Tarjimalar mavjud, lekin `USE_I18N = False` bo'lsa tarjimalar ishlamaydi.

**Tarjimalarni faollashtirish uchun:**
1. `config/settings.py` ochib `USE_I18N = True` qiling
2. Terminal'da jarayoni tugatib qayta ishga tushiring

---

## 🚀 REST API Dokumentatsiyasi

### Asosiy Endpoints

#### 1. **Foydalanuvchini Ro'yxatga Olish**
```bash
POST /api/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}
```

#### 2. **Tizimga Kirish (Login)**
```bash
POST /api-token-auth/
Content-Type: application/json

{
  "username": "admin",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### 3. **Kategoriyalarni Olish**
```bash
GET /api/categories/?type=expense
Authorization: Token <your_token>
```

#### 4. **Hisoblarni Olish**
```bash
GET /api/accounts/
Authorization: Token <your_token>
```

#### 5. **Tranzaksiya Qo'shish**
```bash
POST /api/transactions/
Authorization: Token <your_token>
Content-Type: application/json

{
  "account": 1,
  "category": 3,
  "type": "expense",
  "amount": "50.00",
  "description": "Xaridlar"
}
```

**To'liq API dokumentatsiyasi:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 📂 Loyiha Strukturasi

```
bank/
├── config/                 # Django sozlamalari
│   ├── settings.py        # Asosiy sozlamalar
│   ├── urls.py            # URL routing
│   └── wsgi.py
├── configapp/             # Asosiy ilovasi
│   ├── models.py          # Database modellari
│   ├── views.py           # Web views
│   ├── api_views.py       # API ViewSets
│   ├── serializers.py     # API Serializers
│   ├── forms.py           # Django Forms
│   ├── urls.py            # App URLs
│   ├── migrations/        # DB migratsiyalari
│   └── templates/         # HTML shablonlari
├── locale/                # Tarjimalar (i18n)
│   ├── en/LC_MESSAGES/
│   ├── ru/LC_MESSAGES/
│   └── uz/LC_MESSAGES/
├── manage.py              # Django boshqaruv skripti
├── db.sqlite3             # Database fayli
├── README.md              # Bu fayl
└── API_DOCUMENTATION.md   # API dokumentatsiyasi
```

---

## 🔒 Xavfsizlik Bo'yicha Eslatmalar

1. **Hayvon Parolingizni O'zgaritring**: Loyihani ishlatishdan oldin admin parolini o'zgartiring
2. **Secret Keyni O'zgartiring**: `config/settings.py` da `SECRET_KEY` ni o'zgartiring
3. **DEBUG Rejimini O'chiring**: Ishlab chiqarish uchun `DEBUG = False` qiling
4. **Allowed Hosts**: `ALLOWED_HOSTS` da o'z domeningizni ko'rsating

---

## 🐛 Muammolarni Hal Qilish

### Muammo: "No module named 'rest_framework'"
**Yechimi:** 
```bash
pip install djangorestframework
```

### Muammo: "No such table: configapp_account"
**Yechimi:** 
```bash
python manage.py migrate
```

### Muammo: "Port 8000 already in use"
**Yechimi:** 
```bash
python manage.py runserver 8001
```

---

## 📚 Qo'shimcha Resurslar

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5](https://getbootstrap.com/)

---

## 👨‍💻 Rivojlantirilgan Tomonidan

Foydalanuvchi tomonidan yaratilgan

## 📝 Litsenziya

MIT License - Erkin foydalanish va o'zgartirish uchun

---

## 🤝 Hissa Qo'shish

Taklif va xatoliklarni bildir:
1. Muammoni bildir
2. Yechimni taklif et
3. Pull request yubor

---

**Oxirgi O'zgartirilgan:** 2026-01-22

5. **Ko'p tilli qo'llab-quvvatlash**
   - Rus (ru) 🇺 🇿 
   - Ingliz tili (EN) 🇬 🇧 
   - O'zbek (uz) 🇺🇿
   - To'g'ridan-to'g'ri interfeysda tillarni almashtirish

6. ** Administrator paneli**
   - Django Admin orqali ma'lumotlarni to'liq boshqarish
   - Kategoriyalar, hisoblar, operatsiyalarni boshqarish

## Loyihaning tuzilishi

```
bank/
─ ─ - config / # Django-ning asosiy sozlamalari
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
configapp / # asosiy dastur
- models.py # ma'lumotlar modellari
- views.py # taqdimotlar
- forms.py # shakllar
- admin.py # boshqaruv paneli
- urls.py # URL yo'nalishlari
│   └── templates/    # HTML shablonlari
─ ─ - locale / # tarjimalar
│   ├── en/
│   ├── ru/
│   └── uz/
└── manage.py
```

## Ma'lumotlar modellari

### Hisob (Hisob)
- Hisob nomi
- Balans
- Valyuta (UZS, USD, EUR)
- Belgi
- Yaratilgan sana

### Kategoriya (Kategoriya)
- Nomi
- Turi (Daromad / Xarajat)
- Belgi
- Rang

### Transaction (Operatsiya)
- Hisob
- Kategoriya
- Turi (Daromad / Xarajat / Transfer)
- Miqdori
- Tavsif
- Sana

### Takroriy to'lov (muntazam to'lov)
- Hisob
- Kategoriya
- Miqdori
- Tavsif
- Chastota
- Boshlanish/tugash sanasi
- Faoliyat holati

## O'rnatish va ishga tushirish

### 1. Bog'liqliklarni o'rnatish
```bash
pip install django
```

### 2. Migratsiyalar yaratish
```bash
python manage.py migrate
```

### 3. Superuser yaratish
```bash
python manage.py createsuperuser
```

### 4. Serverni ishga tushirish
```bash
python manage.py runserver
```

### 5. Ilovaga kirish
- Bosh sahifa: http://localhost:8000/
- Ruscha versiyasi: http://localhost:8000/ru/
- Inglizcha versiyasi: http://localhost:8000/en/
- O'zbekcha versiyasi: http://localhost:8000/uz/
-Administrator paneli: http://localhost:8000/admin/

## Interfeys tillari

Yuqori o'ng burchakdagi tugmalar yordamida tilni almashtiring:
- **EN** - English
- **Ru * * - rus Tili
- **UZ * * - O'zbek

Ilovadagi barcha matnlar tanlangan tilga qarab tarjima qilinadi.

## Foydalanish misollari

### Hisob-fakturani qo'shish
1. Hisoblar bo'limiga o'ting
2. "Hisob-Fakturani Qo'shish"Tugmasini Bosing
3. Ismni, boshlang'ich balansni va valyutani to'ldiring
4. Belgini tanlang (kulgichlar)

### Operatsiyani qo'shish
1. Bosh sahifada yoki hisob tafsilotlarida "+"tugmasini bosing
2. Turini tanlang (iste'mol/Daromad)
3. Toifani tanlang
4. Miqdor va tavsifni ko'rsating
5. Sanani tanlang

### Muntazam to'lovlar
1. "To'lovlar" ga o'ting
2. "To'lovni Qo'shish" tugmasini bosing
3. Parametrlarni o'rnating: hisob, miqdor, chastota
4. Saqlash

### Statistikani ko'rish
1. Statistikaga o'ting
2. Xarajatlar jadvallarini toifalar va kunlar bo'yicha ko'rib chiqing
3. Xarajatlar bo'yicha eng yaxshi toifalarni tahlil qiling

---

## 🚀 SWAGGER API DOKUMENTATSIYA

### ✅ Swagger Sozlamalari Yangilandi

**Barcha zarur o'zgartirishlar o'rnatildi:**
- ✓ `drf-spectacular` konfiguratsiyasi takomillashtirildi
- ✓ Barcha API eadpointlari to'liq hujjatlashtirildi
- ✓ "Try It Out" funksiyasi to'liq ishlaydi
- ✓ Token autentifikatsiyasi sozlandi
- ✓ Taydagilgan boshlang'ich ma'lumotlar yaratildi

### Swagger'ni Ishlatish

#### 1. **Serverini Ishga Tushirish**
```bash
python manage.py runserver
```

#### 2. **Boshlang'ich Ma'lumotlarni Yaratish (Birinchi Marta)**
```bash
python manage.py init_data
```

Bu quyidagilarni yaratadi:
- Test foydalanuvchisi: `testuser`
- Parol: `testpass123`
- Token: Ko'rsatiladi ekranda
- 6 xarajat toifasi
- 4 daromad toifasi
- 3 test hisobi (UZS, USD, EUR)

#### 3. **Swagger'ni Ochish**
Quyidagi manzillardan birini ochish:
- http://localhost:8000/api/docs/ (Swagger UI)
- http://localhost:8000/api/redoc/ (ReDoc)
- http://localhost:8000/api/schema/ (OpenAPI Schema JSON)

#### 4. **Avtorizatsiya**
1. Swagger UI'da o'ng yuqori burchakdagi **"Authorize"** tugmasini bosing
2. Token qiymatini kiriting: `Token eb6e7c56ebda08b049e3758c6cd49967650b08c9`
3. **"Authorize"** tugmasini bosing
4. Hozir siz barchasini ishlatishingiz mumkin!

#### 5. **"Try It Out" Ishlatish**
1. Har qanday API eadpointni kengaytiring
2. **"Try It Out"** tugmasini bosing
3. Kerakli parametrlarni to'ldiring
4. **"Execute"** tugmasini bosing
5. Javobni real vaqtda ko'ring!

### API Endpoints

**Autentifikatsiya (yo'q avtorización kerak):**
- `POST /api/register/` - Ro'yxatga olish
- `POST /api-token-auth/` - Token olish

**Foydalanuvchilar (avtorización kerak):**
- `GET /api/users/` - Foydalanuvchilar ro'yxati
- `GET /api/users/me/` - Hozirgi foydalanuvchi
- `POST /api/users/logout/` - Tizimdan chiqish

**Hisoblar:**
- `GET /api/accounts/` - Hisoblar ro'yxati
- `POST /api/accounts/` - Hisob yaratish
- `GET /api/accounts/{id}/` - Hisob tafsilotlari
- `GET /api/accounts/summary/` - Barcha hisoblar qisqasi
- `GET /api/accounts/{id}/transactions/` - Hisob operatsiyalari

**Toifalar:**
- `GET /api/categories/` - Toifalar ro'yxati
- `POST /api/categories/` - Toifa yaratish
- `GET /api/categories/by_type/?type=expense` - Toifalarni turga bo'lish

**Tranzaksiyalar:**
- `GET /api/transactions/` - Operatsiyalar ro'yxati
- `POST /api/transactions/` - Operatsiya qo'shish
- `GET /api/transactions/statistics/` - Statistika

**Muntazam To'lovlar:**
- `GET /api/recurring-payments/` - To'lovlar ro'yxati
- `POST /api/recurring-payments/` - To'lov yaratish
- `POST /api/recurring-payments/{id}/deactivate/` - O'chirib tashlash
- `POST /api/recurring-payments/{id}/activate/` - Aktivlash

---

## Texnologiya

- **Backend**: Django 6.0+
- **REST Framework**: Django REST Framework
- **API Dokumentatsiya**: drf-spectacular (OpenAPI 3.0)
- **Ma'lumotlar bazasi**: SQLite (sukut bo'yicha PostgreSQL/MySQL bilan almashtirilishi mumkin)
- **Charts**: Chart.js
- **i18n**: Django Internationalization

## Mumkin kengaytmalar

- Ma'lumotlarni import/eksport qilish (CSV, Excel)
- Toifalar bo'yicha byudjetlashtirish
- Mobil aplikatsiya
- Email xabarlari
- Byudjetdan tashqari bildirishnomalar
- Qurilmalar o'rtasida sinxronizatsiya
- Mobil ilova uchun API
- Hisobotlar va ma'lumotlarni eksport qilish
- Operatsiyalar uchun teglar
- Qo'shma hisoblar

## Qo'llab-quvvatlash

Savollar yoki takliflar uchun ishlab chiquvchi bilan bog'laning.