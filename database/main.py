from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
import asyncio
import sqlite3
from kb import (
    main_kb, admin_kb, order_kb, cart_kb, 
    cart_order_kb, menu_kbjj, contacts_kb
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db2 import food_insert, food_del, food_change
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#Importa neccesary biblaties



bot = Bot(
    token='8298563896:AAGq8Kqfl-6n4gSq3Q2t8GFM40ik_x8oV58',
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

#Import our bot

class add_product(StatesGroup):
    name = State()
    price = State()

class del_prod(StatesGroup):
    namee = State()

class change_prod(StatesGroup):
    prod_name = State()
    name = State()
    price = State()

class OrderFSM(StatesGroup):
    name = State()
    address = State()
    final = State()

#Import spetial tasks(classes)


@dp.message(Command("start"))
async def start_com(message: Message):
    await message.answer("Привет, это бот для заказа еды", reply_markup=main_kb)

#command start



@dp.message(F.text == "Меню")
async def show_menu(message: Message):
    await message.answer("\U0001F37D️ Вот ваше меню:", reply_markup=cart_order_kb)

    conn_f = sqlite3.connect("food.db")
    cursor_f = conn_f.cursor()
    cursor_f.execute("SELECT name, price FROM food")
    result = cursor_f.fetchall()
    conn_f.close()

    if not result:
        await message.answer("Меню пока пустое \U0001FAE4")
        return

    for item in result:
        nameq, priceq = item
        text = f"*{nameq}*\nЦена: *{priceq}* лей."

        product_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add:{nameq}")]
            ]
        )
        await message.answer(text, parse_mode="Markdown", reply_markup=product_kb)


#Main menu


@dp.callback_query(F.data.startswith("add:"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    food_name = callback.data.split("add:")[1]
    data = await state.get_data()
    cart = data.get("cart", [])
    cart.append(food_name)
    await state.update_data(cart=cart)
    await callback.answer(f"{food_name} добавлено в корзину ✅")

#Add to trach cane


@dp.message(F.text == "Корзина")
async def show_cart(message: Message, state: FSMContext):
    data = await state.get_data()
    cart = data.get("cart", [])
    if not cart:
        await message.answer("Ваша корзина пуста \U0001F9FA", reply_markup=cart_kb)
    else:
        text = "\U0001F6D2 Ваша корзина:\n" + "\n".join(f"• {item}" for item in cart)
        await message.answer(text, reply_markup=order_kb)

#Command to thash cane


@dp.message(F.text == "Заказать")
async def start_order(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(OrderFSM.name)

#Command to order


@dp.message(OrderFSM.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите адрес доставки:")
    await state.set_state(OrderFSM.address)

#Adress order


@dp.message(OrderFSM.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    name = data.get("name")
    address = data.get("address")
    cart = data.get("cart", [])

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, address TEXT, items TEXT)")
    cursor.execute("INSERT INTO orders (name, address, items) VALUES (?, ?, ?)", (name, address, ", ".join(cart)))
    conn.commit()
    conn.close()

    await message.answer("Ваш заказ оформлен и отправлен в доставку! \U0001F680", reply_markup=main_kb)
    await state.clear()

#Name, adress and other


@dp.message(F.text == "О нас")
async def ec(message: Message):
    await message.answer("Тут о нас)", reply_markup=menu_kbjj)

@dp.message(F.text == "Контакты")
async def e(message: Message):
    await message.answer("Наш номер телефона: +373 600 00 00", reply_markup=contacts_kb)

@dp.message(F.text == "Назад")
@dp.message(F.text == "Главное меню")
async def back_to_main(message: Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=main_kb)

@dp.message(Command("admin"))
async def admin_handler(message: Message):
    await message.answer("Введи паоль: ")

@dp.message(F.text == "13211")
async def admin_handler(message: Message):
    await message.answer("Ты в админке", reply_markup=admin_kb)

@dp.callback_query(F.data == "add")
async def add_name(message: CallbackQuery, state: FSMContext):
    await message.message.answer("Привет! Чтобы добваить новый продукт напиши тут название: ")
    await state.set_state(add_product.name)


#Some administrative shit


@dp.message(add_product.name)
async def add_price(message: Message, state: FSMContext):
    await message.answer("Мне ещё нужна цена этого продукта: ")
    await state.update_data(name=message.text)
    await state.set_state(add_product.price)

@dp.message(add_product.price)
async def all_data(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    food_insert(data["name"], data["price"])
    await message.answer("Данные сохраненны в базе данных")

@dp.callback_query(F.data == "change")
async def change_by_name(message: CallbackQuery, state: FSMContext):
    await state.set_state(change_prod.prod_name)
    await message.message.answer("Напишите имя продукта который вы хотите изменить")

@dp.message(change_prod.prod_name)
async def change_name(message: Message, state: FSMContext):
    await state.update_data(prod_name=message.text)
    await message.answer("Напишите новое имя для данного продукта")
    await state.set_state(change_prod.name)

@dp.message(change_prod.name)
async def change_price(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введи новую цену")
    await state.set_state(change_prod.price)

@dp.message(change_prod.price)
async def get_a_data(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    food_change(data["prod_name"], data["name"], data["price"])
    await message.answer("Данные изменены")

@dp.callback_query(F.data == "del")
async def pred_del(message: CallbackQuery, state: FSMContext):
    await message.message.answer("Напишите имя продукта который вы хотите удалить")
    await state.set_state(del_prod.namee)

@dp.message(del_prod.namee)
async def dell(message: Message, state: FSMContext):
    await state.update_data(namee=message.text)
    name = await state.get_data()
    food_del(name["namee"])
    await message.answer("Удалили успешно")


#product



async def main():
    await dp.start_polling(bot)

#bot function

if __name__ == "__main__":
    asyncio.run(main())


#end of the code