import json
import os
from typing import Dict, Set, List

DATABASE_FILE = "users.json"


def load_data() -> dict:
    """Ma'lumotlarni yuklash"""
    if not os.path.exists(DATABASE_FILE):
        return {"users": {}}
    
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"users": {}}


def save_data(data: dict) -> None:
    """Ma'lumotlarni saqlash"""
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_user_filters(user_id: int) -> Set[str]:
    """Foydalanuvchi filterlarini olish"""
    data = load_data()
    user_key = str(user_id)
    
    if user_key not in data["users"]:
        # Yangi foydalanuvchi - hamma filter yoqiq
        data["users"][user_key] = ["job", "worker", "partner", "mentor"]
        save_data(data)
    
    return set(data["users"][user_key])


def toggle_filter(user_id: int, filter_type: str) -> bool:
    """Filterni yoqish/o'chirish"""
    data = load_data()
    user_key = str(user_id)
    
    if user_key not in data["users"]:
        data["users"][user_key] = ["job", "worker", "partner", "mentor"]
    
    filters = set(data["users"][user_key])
    
    if filter_type in filters:
        filters.discard(filter_type)
        result = False
    else:
        filters.add(filter_type)
        result = True
    
    data["users"][user_key] = list(filters)
    save_data(data)
    return result


def get_users_with_filter(filter_type: str) -> List[int]:
    """Berilgan filter yoqilgan foydalanuvchilar"""
    data = load_data()
    users = []
    
    for user_id, filters in data["users"].items():
        if filter_type in filters:
            users.append(int(user_id))
    
    return users


def get_all_users() -> List[int]:
    """Barcha foydalanuvchilar"""
    data = load_data()
    return [int(uid) for uid in data["users"].keys()]
