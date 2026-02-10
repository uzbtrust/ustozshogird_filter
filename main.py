import asyncio
import logging

from pyrogram import Client
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message as AioMessage, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import API_ID, API_HASH, BOT_TOKEN, CHANNELS, POST_TYPES
from database import get_user_filters, toggle_filter, get_users_with_filter
from keyboards import get_filters_keyboard

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

last_message_ids = {}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: AioMessage):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    filters_data = get_user_filters(user_id)
    
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
    
    await message.answer(text, reply_markup=get_filters_keyboard(filters_data), parse_mode="HTML")
    logger.info(f"👤 Yangi foydalanuvchi: {user_id}")


@router.callback_query(F.data.startswith("toggle:"))
async def toggle_callback(callback: CallbackQuery):
    """Filter tugmasi"""
    user_id = callback.from_user.id
    filter_type = callback.data.split(":")[1]
    
    new_state = toggle_filter(user_id, filter_type)
    filters_data = get_user_filters(user_id)
    
    status = "yoqildi ✅" if new_state else "o'chirildi ❌"
    await callback.answer(f"{POST_TYPES[filter_type]['label']} {status}")
    await callback.message.edit_reply_markup(reply_markup=get_filters_keyboard(filters_data))


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


async def process_message(message, chat_username):
    """Xabarni qayta ishlash"""
    
    text = message.text or message.caption or ""
    if not text:
        return
    
    post_type = detect_post_type(text)
    if not post_type:
        return
    
    post_info = POST_TYPES[post_type]
    logger.info(f"🏷️ Yangi post: {post_info['label']} - @{chat_username}")
    
    users = get_users_with_filter(post_type)
    if not users:
        logger.info(f"⚠️ Hech kim {post_type} yoqmagan")
        return
    
    logger.info(f"👥 {len(users)} ta userga yuboriladi")
    
    post_link = f"https://t.me/{chat_username}/{message.id}"
    
    notification = (
        f"┏━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"   {post_info['emoji']} <b>{post_info['label'].upper()}</b>\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"{text}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📢 <b>Kanal:</b> @{chat_username}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📎 Postga o'tish", url=post_link)]
    ])
    
    for user_id in users:
        try:
            await bot.send_message(
                user_id, 
                notification, 
                parse_mode="HTML",
                reply_markup=keyboard
            )
            logger.info(f"✅ {user_id} ga yuborildi")
        except Exception as e:
            logger.error(f"❌ {user_id}: {e}")
        await asyncio.sleep(0.05)


async def check_channels():
    global last_message_ids
    
    while True:
        try:
            for channel in CHANNELS:
                try:
                    async for message in userbot.get_chat_history(channel, limit=1):
                        msg_id = message.id
                        
                        if channel not in last_message_ids:
                            last_message_ids[channel] = msg_id
                            logger.info(f"📢 {channel} - oxirgi ID: {msg_id}")
                        elif msg_id > last_message_ids[channel]:
                            logger.info(f"📩 Yangi xabar: @{channel}")
                            last_message_ids[channel] = msg_id
                            await process_message(message, channel)
                        
                        break
                        
                except Exception as e:
                    logger.error(f"❌ {channel}: {e}")
            
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"❌ Polling xatosi: {e}")
            await asyncio.sleep(10)


async def main():
    """Hammani ishga tushirish"""
    
    dp.include_router(router)
    
    await userbot.start()
    logger.info("🔍 Userbot tayyor")
    logger.info(f"📢 Kanallar: {CHANNELS}")
    
    asyncio.create_task(check_channels())
    logger.info("⏱️ Polling boshlandi (har 5 soniyada)")
    
    logger.info("🤖 Bot tayyor")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
