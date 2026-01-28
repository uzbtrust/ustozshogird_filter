import asyncio
import logging
from typing import Optional

from pyrogram import Client, filters
from pyrogram.types import Message

from config import API_ID, API_HASH, BOT_TOKEN, CHANNELS, POST_TYPES
from database import get_users_with_filter

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Userbot (kanallarni kuzatish uchun)
userbot = Client(
    "channel_monitor",
    api_id=API_ID,
    api_hash=API_HASH
)

# Bot client (xabar yuborish uchun)
from aiogram import Bot
bot = Bot(token=BOT_TOKEN)


def detect_post_type(text: str) -> Optional[str]:
    """Post turini aniqlash"""
    if not text:
        return None
    
    text_lower = text.lower().strip()
    
    for filter_type, data in POST_TYPES.items():
        keyword = data["keyword"].lower()
        if keyword in text_lower[:150]:
            return filter_type
    
    return None


@userbot.on_message(filters.chat(CHANNELS) & ~filters.edited)
async def handle_channel_post(client: Client, message: Message):
    """Kanal postini olish va bot orqali yuborish"""
    
    text = message.text or message.caption or ""
    
    if not text:
        return
    
    # Post turini aniqlash
    post_type = detect_post_type(text)
    
    if not post_type:
        return
    
    post_info = POST_TYPES[post_type]
    chat_name = message.chat.username or message.chat.title or "Kanal"
    
    logger.info(f"📨 {post_info['label']} - @{chat_name}")
    
    # Bu filter yoqilgan foydalanuvchilarni olish
    users = get_users_with_filter(post_type)
    
    if not users:
        logger.info(f"⚠️ Hech kim {post_type} filterini yoqmagan")
        return
    
    logger.info(f"👥 {len(users)} ta foydalanuvchiga yuboriladi")
    
    # Bot orqali yuborish
    notification = (
        f"{post_info['emoji']} <b>Yangi post: {post_info['label']}</b>\n"
        f"📢 Kanal: @{chat_name}\n\n"
        f"{'─' * 30}\n\n"
        f"{text}"
    )
    
    for user_id in users:
        try:
            await bot.send_message(user_id, notification, parse_mode="HTML")
            logger.info(f"✅ {user_id} ga yuborildi")
        except Exception as e:
            logger.error(f"❌ {user_id} ga xato: {e}")
        
        await asyncio.sleep(0.05)


async def main():
    """Userbotni ishga tushirish"""
    logger.info("🔍 Userbot ishga tushmoqda...")
    logger.info(f"📢 Kanallar: {CHANNELS}")
    
    await userbot.start()
    logger.info("✅ Userbot tayyor! Kanallarni kuzatmoqda...")
    
    # Cheksiz kutish
    await asyncio.Event().wait()


if __name__ == "__main__":
    userbot.run(main())
