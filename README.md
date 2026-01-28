# 🤖 UstozShogird Filter Bot

Telegram kanallaridagi postlarni filterlash tizimi. Userbot kanallarni kuzatadi, bot foydalanuvchilarga yuboradi.

## 📋 Qanday ishlaydi?

```
@UstozShogird ──► Userbot ──► Bot ──► Foydalanuvchilar
   (kanal)        (oladi)   (yuboradi)  (filter bo'yicha)
```

**Afzalligi:** Kanalga admin bo'lish shart emas! Faqat a'zo bo'lsangiz kifoya.

## 🚀 O'rnatish

### 1. Reponi clone qilish

```bash
git clone https://github.com/uzbtrust/ustozshogird_filter.git
cd ustozshogird_filter
```

### 2. Virtual environment yaratish

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. API kalitlarini olish

**Telegram API (userbot uchun):**
1. https://my.telegram.org ga kiring
2. "API development tools" bo'limiga o'ting
3. App yarating
4. **API ID** va **API Hash** ni ko'chirib oling

**Bot Token:**
1. Telegram'da @BotFather ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username'ini kiriting
4. Token'ni ko'chirib oling

### 5. `.env` faylini sozlash

`.env` fayl yarating va quyidagilarni yozing:

```env
API_ID=12345678
API_HASH=your_api_hash_here
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 6. Ishga tushirish

```bash
python main.py
```

Birinchi marta ishga tushirganda telefon raqam va SMS kod so'raydi (userbot uchun).

## 📱 Foydalanish

1. Botni Telegram'da toping
2. `/start` bosing
3. Kerakli filterlarni tanlang (✅/❌)
4. Kanalda yangi post chiqqanda bot sizga yuboradi!

## 🔧 Filter turlari

| Filter | Tavsif |
|--------|--------|
| 👨‍💼 Ish joyi kerak | Ish izlovchilar postlari |
| 🏢 Xodim kerak | Ishga yollash e'lonlari |
| 🏅 Sherik kerak | Hamkorlik takliflari |
| 🎓 Ustoz kerak | Mentorlik so'rovlari |

## 📢 Kuzatiladigan kanallar

- [@UstozShogird](https://t.me/UstozShogird)
- [@UstozShogirdSohalar](https://t.me/UstozShogirdSohalar)

Boshqa kanal qo'shish uchun `config.py` da `CHANNELS` ro'yxatini tahrirlang.

## 📁 Loyiha tuzilishi

```
ustozshogird_filter/
├── main.py          # Asosiy fayl (bot + userbot)
├── bot.py           # Bot handlerlari
├── userbot.py       # Userbot handlerlari
├── config.py        # Sozlamalar
├── database.py      # Ma'lumotlar bazasi
├── keyboards.py     # Inline tugmalar
├── requirements.txt # Kutubxonalar
├── .env             # API kalitlari (gitignore'da)
└── README.md
```

## ⚠️ Muhim eslatmalar

- `.env` faylini hech kimga bermang!
- `*.session` fayllarini hech kimga bermang!
- Userbot sizning shaxsiy akkauntingiz orqali ishlaydi
- Kanalga a'zo bo'lishingiz kerak (admin emas)

## 📝 Litsenziya

MIT License

## 👨‍💻 Muallif

[@uzbtrust](https://github.com/uzbtrust)
