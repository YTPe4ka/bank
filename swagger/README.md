# Mening Bankim-moliyaviy boshqaruv tizimi

## Funktsionallik

### ✅ Asosiy imkoniyatlar:

1. ** Hisoblarni boshqarish**
   - Bir nechta hisoblarni yaratish va boshqarish
   - Turli valyutalarni qo'llab-quvvatlash (UZS, USD, EUR)
   - Har bir hisob balansini kuzatish
   - Hisoblar uchun moslashtirilgan piktogrammalar

2. ** Operatsiyalar va operatsiyalar**
   - Xarajatlar va daromadlarni qo'shish
   - Operatsiyalarni tasniflash
   - Barcha operatsiyalar tarixi
   - Turi, toifasi va davri bo'yicha filtrlash

3. ** Muntazam to'lovlar**
   - Takroriy to'lovlarni yaratish
   - Turli chastotalarni qo'llab-quvvatlash (kunlik, haftalik, oylik, yillik)
   - To'lovlarni faollashtirish/o'chirish
   - Oxirgi bajarilishini kuzatish

4. ** Statistika va tahlil**
   - Toifalar bo'yicha xarajatlar jadvallari (pirog diagrammasi)
   - Kunlik xarajatlar jadvallari (chiziqli grafik)
   - Oylar va davrlar bo'yicha tahlil
   - Xarajatlar bo'yicha eng yaxshi toifalar

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

## Texnologiya

- **Backend**: Django 6.0+
- **Ma'lumotlar bazasi**: SQLite (sukut bo'yicha PostgreSQL/MySQL bilan almashtirilishi mumkin)
- **Frontend**: Bootstrap 5
- **Charts**: Chart.js
- **i18n**: Django Internationalization

## Mumkin kengaytmalar

- Ma'lumotlarni import/eksport qilish (CSV, Excel)
- Toifalar bo'yicha byudjetlashtirish
- Byudjetdan tashqari bildirishnomalar
- Qurilmalar o'rtasida sinxronizatsiya
- Mobil ilova uchun API
- Hisobotlar va ma'lumotlarni eksport qilish
- Operatsiyalar uchun teglar
- Qo'shma hisoblar

## Qo'llab-quvvatlash

Savollar yoki takliflar uchun ishlab chiquvchi bilan bog'laning.