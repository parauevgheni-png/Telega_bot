from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Menu")],
        [KeyboardButton(text="Favorite")],
        [KeyboardButton(text="Send")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# ===================== FAVORITE KEYBOARD =====================

fav_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Favorite")],
        [KeyboardButton(text="Menu")],
        [KeyboardButton(text="Send")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# ===================== SEND KEYBOARD =====================

send_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send")],
        [KeyboardButton(text="Menu")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# ===================== ADMIN INLINE KEYBOARD =====================

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Add film",
                callback_data="add_film"
            )
        ]
    ]
)