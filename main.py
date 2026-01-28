import asyncio
import logging

from pyrogram import Client
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import API_ID, API_HASH, BOT_TOKEN, CHANNELS, POST_TYPES
from database import get_user_filters, toggle_filter, get_users_with_filter
from keyboards import get_filters_keyboard

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
#                         BOT (Aiogram)
# ═══════════════════════════════════════════════════════════════
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start komandasi"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    filters = get_user_filters(user_id)
    
    text = (
        f"👋 <b>Assalomu alaykum, {user_name}!</b>\n\n"
        f"🤖 Men <b>UstozShogird Filter Bot</b>man.\n\n"
        f"📢 Quyidagi kanallardan postlarni filterlash xizmati:\n"
        f"   • @UstozShogird\n"
        f"   • @UstozShogirdSohalar\n\n"
        f"⚙️ <b>Kerakli post turlarini tanlang:</b>\n\n"
        f"   ✅ — Sizga yuboriladi\n"
        f"   ❌ — Sizga yuborilmaydi"
    )
    
    await message.answer(text, reply_markup=get_filters_keyboard(filters), parse_mode="HTML")
    logger.info(f"👤 Yangi foydalanuvchi: {user_id}")


@router.callback_query(F.data.startswith("toggle:"))
async def toggle_callback(callback: CallbackQuery):
    """Filter tugmasi"""
    user_id = callback.from_user.id
    filter_type = callback.data.split(":")[1]
    
    new_state = toggle_filter(user_id, filter_type)
    filters = get_user_filters(user_id)
    
    status = "yoqildi ✅" if new_state else "o'chirildi ❌"
    await callback.answer(f"{POST_TYPES[filter_type]['label']} {status}")
    await callback.message.edit_reply_markup(reply_markup=get_filters_keyboard(filters))


# ═══════════════════════════════════════════════════════════════
#                      USERBOT (Pyrogram)
# ═══════════════════════════════════════════════════════════════
userbot = Client(
    "channel_monitor",
    api_id=API_ID,
    api_hash=API_HASH
)


def detect_post_type(text: str):
    """Post turini aniqlash"""
    if not text:
        return None
    
    text_lower = text.lower().strip()
    
    for filter_type, data in POST_TYPES.items():
        if data["keyword"].lower() in text_lower[:150]:
            return filter_type
    return None


@userbot.on_message()
async def handle_channel_post(client, message):
    """Kanal postini olish"""
    
    # Faqat belgilangan kanallardan
    chat_username = message.chat.username
    if not chat_username or chat_username not in CHANNELS:
        return
    
    text = message.text or message.caption or ""
    if not text:
        return
    
    post_type = detect_post_type(text)
    if not post_type:
        return
    
    post_info = POST_TYPES[post_type]
    logger.info(f"📨 {post_info['label']} - @{chat_username}")
    
    # Foydalanuvchilarni olish
    users = get_users_with_filter(post_type)
    if not users:
        logger.info(f"⚠️ Hech kim {post_type} yoqmagan")
        return
    
    logger.info(f"👥 {len(users)} ta userga yuboriladi")
    
    # Bot orqali yuborish
    notification = (
        f"{post_info['emoji']} <b>Yangi post: {post_info['label']}</b>\n"
        f"📢 Kanal: @{chat_username}\n\n"
        f"{'─' * 30}\n\n"
        f"{text}"
    )
    
    for user_id in users:
        try:
            await bot.send_message(user_id, notification, parse_mode="HTML")
            logger.info(f"✅ {user_id}")
        except Exception as e:
            logger.error(f"❌ {user_id}: {e}")
        await asyncio.sleep(0.05)


# ═══════════════════════════════════════════════════════════════
#                           MAIN
# ═══════════════════════════════════════════════════════════════
async def main():
    """Hammani ishga tushirish"""
    
    # Routerni qo'shish
    dp.include_router(router)
    
    # Userbotni boshlash
    await userbot.start()
    logger.info("🔍 Userbot tayyor - kanallarni kuzatmoqda")
    logger.info(f"📢 Kanallar: {CHANNELS}")
    
    # Botni boshlash
    logger.info("🤖 Bot tayyor - foydalanuvchilar kutilmoqda")
    
    # Ikkalasini parallel ishga tushirish
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
