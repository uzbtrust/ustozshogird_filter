import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN, POST_TYPES
from database import get_user_filters, toggle_filter
from keyboards import get_filters_keyboard

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
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
    logger.info(f"👤 Yangi foydalanuvchi: {user_id} - {user_name}")


@router.callback_query(F.data.startswith("toggle:"))
async def toggle_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    filter_type = callback.data.split(":")[1]
    
    new_state = toggle_filter(user_id, filter_type)
    filters = get_user_filters(user_id)
    
    status = "yoqildi ✅" if new_state else "o'chirildi ❌"
    await callback.answer(f"{POST_TYPES[filter_type]['label']} {status}")
    
    await callback.message.edit_reply_markup(reply_markup=get_filters_keyboard(filters))


async def send_post_to_users(user_ids: list, post_type: str, text: str, chat_name: str):
    post_info = POST_TYPES[post_type]
    
    notification = (
        f"{post_info['emoji']} <b>Yangi post: {post_info['label']}</b>\n"
        f"📢 Kanal: @{chat_name}\n\n"
        f"{'─' * 30}\n\n"
        f"{text}"
    )
    
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, notification, parse_mode="HTML")
            logger.info(f"✅ {user_id} ga yuborildi")
        except Exception as e:
            logger.error(f"❌ {user_id} ga xato: {e}")
        
        await asyncio.sleep(0.05)


async def run_bot():
    dp.include_router(router)
    logger.info("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
