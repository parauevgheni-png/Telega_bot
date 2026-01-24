from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="О нас"),
            KeyboardButton(text="Контакты"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

menu_kbjj = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Главное меню"),
            KeyboardButton(text="Далее")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

contacts_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Номер телефона"),
            KeyboardButton(text="Адрес")
        ],
        [
            KeyboardButton(text="Главное меню"),
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

order_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Заказать")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

cart_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Корзина")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

cart_order_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Корзина"),
            KeyboardButton(text="Заказать")
        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


main_kb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Меню", callback_data="menu"),
            InlineKeyboardButton(text="О нас", callback_data="about"),
            InlineKeyboardButton(text="Контакты", callback_data="contacts")
        ]
    ]
)

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить", callback_data="add"),
            InlineKeyboardButton(text="Удалить", callback_data="del"),
            InlineKeyboardButton(text="Изменить", callback_data="change")
        ]
    ]
)