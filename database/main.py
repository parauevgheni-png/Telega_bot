import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from kb import main_kb, admin_kb, fav_kb, send_kb
from db2 import init_db, get_films, add_film



BOT_TOKEN = "8298563896:AAGmnGmm1CSbRGxCU-rofLiUsFP9waYUC0c"


ADMIN_ID = 123456789

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()




class FavoriteFSM(StatesGroup):
    choosing = State()


class SubmitFSM(StatesGroup):
    name = State()
    comment = State()


class AddFilmFSM(StatesGroup):
    title = State()
    year = State()



@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "🎬 Welcome to the films bot!",
        reply_markup=main_kb
    )



@dp.message(F.text == "Menu")
async def show_films(message: Message):
    films = get_films()

    if not films:
        await message.answer("We add your favorite movies. /start for start; /menu for menu; /send for sending favorite film")
        return

    for title, year in films:
        await message.answer(f"<b>{title}</b> ({year})")



@dp.message(F.text == "Favorite")
async def favorite_start(message: Message, state: FSMContext):
    films = get_films()

    if not films:
        await message.answer("The most favorite films of all humanity are here: https://m.imdb.com/chart/top/")
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=title)]
            for title, _ in films
        ] + [
            [InlineKeyboardButton(text=" Finish", callback_data="finish")]
        ]
    )

    await state.set_state(FavoriteFSM.choosing)
    await message.answer("Choose your favorite films:", reply_markup=kb)


@dp.callback_query(FavoriteFSM.choosing)
async def favorite_choose(call: CallbackQuery, state: FSMContext):
    if call.data == "finish":
        favs = (await state.get_data()).get("favs", [])

        if not favs:
            await call.message.answer("You didn't choose any films.", reply_markup=main_kb)
        else:
            text = "<b>Your favorites:</b>\n" + "\n".join(f"• {f}" for f in favs)
            await call.message.answer(text, reply_markup=send_kb)

        await state.clear()
        await call.answer()
        return

    data = await state.get_data()
    favs = data.get("favs", [])

    if call.data not in favs:
        favs.append(call.data)
        await state.update_data(favs=favs)
        await call.answer("Added to favorites!")
    else:
        await call.answer("Already added")


@dp.message(F.text == "Send")
async def submit_start(message: Message, state: FSMContext):
    await message.answer("Your name?")
    await state.set_state(SubmitFSM.name)


@dp.message(SubmitFSM.name)
async def submit_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("What is your favorite film?")
    await state.set_state(SubmitFSM.comment)


@dp.message(SubmitFSM.comment)
async def submit_finish(message: Message, state: FSMContext):
    data = await state.get_data()

    conn = sqlite3.connect("films.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO submissions (name, comment, films) VALUES (?, ?, ?)",
        (
            data["name"],
            message.text,
            ", ".join(data.get("favs", []))
        )
    )

    conn.commit()
    conn.close()

    await message.answer("Thank you for your feedback!", reply_markup=main_kb)
    await state.clear()



@dp.message(Command("admin"))
async def admin_cmd(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("Admin panel", reply_markup=admin_kb)


@dp.callback_query(F.data == "add_film")
async def admin_add_film(call: CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return

    await call.message.answer("Film title?")
    await state.set_state(AddFilmFSM.title)
    await call.answer()

@dp.message(AddFilmFSM.title)
async def admin_film_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Release year?")
    await state.set_state(AddFilmFSM.year)


@dp.message(AddFilmFSM.year)
async def admin_film_year(message: Message, state: FSMContext):
    try:
        year = int(message.text)
    except ValueError:
        await message.answer("Enter a valid year (number).")
        return

    data = await state.get_data()
    add_film(data["title"], year)

    await message.answer("Film added successfully!", reply_markup=main_kb)
    await state.clear()


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
