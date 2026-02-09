# Geeks Andijan IQ Test Onlayn Platformasi

Ta'limiy MVP — o'quvchilar uchun oddiy, tez va qulay onlayn IQ test platformasi.

## Xususiyatlar

- **Ro'yxatdan o'tishsiz** — faqat ism, yosh, jinsi va telefon
- **Landing sahifa** — qisqa tavsif va "IQ Testni boshlash" tugmasi
- **Ma'lumotlar formasi** — tekshiruv va do'stona xato xabarlari
- **Test interfeysi** — har bir savol alohida, taymer, progress bar, o'tkazib yuborish
- **Natijalar** — IQ ball, nishon (Bronza/Kumush/Oltin), reyting
- **O'qituvchi paneli** — statistika, grafiklar, eksport (CSV, Excel)

## Texnologiyalar

- **Frontend:** HTML, CSS, Tailwind CSS (CDN), JavaScript
- **Backend:** Django, SQLite

## O'rnatish

```bash
# Virtual muhit (ixtiyoriy)
python -m venv venv
venv\Scripts\activate  # Windows

# To'g'ridan-to'g'ri
pip install -r requirements.txt
python manage.py migrate
python manage.py load_sample_questions

# Administrator yaratish
python manage.py createsuperuser

# Server ishga tushirish
python manage.py runserver
```

## Ishlatish

1. **Asosiy sahifa:** http://127.0.0.1:8000/
2. **O'qituvchi paneli:** http://127.0.0.1:8000/dashboard/
3. **Admin:** http://127.0.0.1:8000/admin/

## Savollarni boshqarish

Admin panel orqali savollarni qo'shing, tahrirlang, yoqing/o'chiring. Qiyinlik darajasi: Oson, O'rta, Qiyin.

---

Geeks Andijan © 2025 — Ta'limiy MVP
