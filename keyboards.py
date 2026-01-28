from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Set

from config import POST_TYPES


def get_filters_keyboard(active_filters: Set[str]) -> InlineKeyboardMarkup:
    """Filter tugmalarini yaratish"""
    
    def status(filter_type: str) -> str:
        return "✅" if filter_type in active_filters else "❌"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # 1-qator: Ish joyi va Xodim
        [
            InlineKeyboardButton(
                text=f"{POST_TYPES['job']['emoji']} {POST_TYPES['job']['label']} {status('job')}",
                callback_data="toggle:job"
            ),
            InlineKeyboardButton(
                text=f"{POST_TYPES['worker']['emoji']} {POST_TYPES['worker']['label']} {status('worker')}",
                callback_data="toggle:worker"
            ),
        ],
        # 2-qator: Sherik va Ustoz
        [
            InlineKeyboardButton(
                text=f"{POST_TYPES['partner']['emoji']} {POST_TYPES['partner']['label']} {status('partner')}",
                callback_data="toggle:partner"
            ),
            InlineKeyboardButton(
                text=f"{POST_TYPES['mentor']['emoji']} {POST_TYPES['mentor']['label']} {status('mentor')}",
                callback_data="toggle:mentor"
            ),
        ],
        # 3-qator: Shogird
        [
            InlineKeyboardButton(
                text=f"{POST_TYPES['student']['emoji']} {POST_TYPES['student']['label']} {status('student')}",
                callback_data="toggle:student"
            ),
        ],
    ])
    
    return keyboard