# 🤖 UstozShogird Filter Bot + Userbot

Userbot kanallarni kuzatadi, bot foydalanuvchilarga yuboradi.

## 📋 Qanday ishlaydi?

```
@UstozShogird ──► Userbot ──► Bot ──► Foydalanuvchilar
   (kanal)        (oladi)   (yuboradi)  (filter bo'yicha)
```

## 🚀 O'rnatish

### 1. API olish

**Telegram API (userbot uchun):**
1. https://my.telegram.org ga kiring
2. API development tools → App yarating
3. API ID va API Hash ni oling

**Bot Token:**
1. @BotFather ga yozing
2. /newbot → Bot yarating
3. Token ni oling

### 2. Config sozlash

`config.py` ni to'ldiring:
```python
API_ID = 12345678
API_HASH = "your_api_hash"
BOT_TOKEN = "123456:ABC..."
```

### 3. O'rnatish va ishga tushirish

```bash
pip install -r requirements.txt
python main.py
```

Birinchi marta telefon raqam va SMS kod so'raydi (userbot uchun).

## 📱 Foydalanish

1. Botni toping va /start bosing
2. Kerakli filterlarni tanlang (✅/❌)
3. Kanalda yangi post chiqqanda bot sizga yuboradi

## 📁 Fayllar

```
├── main.py         # Asosiy - bot + userbot
├── config.py       # Sozlamalar
├── database.py     # Foydalanuvchilar
├── keyboards.py    # Tugmalar
└── requirements.txt
```

## ⚠️ Muhim

- `channel_monitor.session` faylini hech kimga bermang!
- Userbot sizning akkauntingiz orqali ishlaydi
- Kanalga a'zo bo'lishingiz kerak (admin emas)
