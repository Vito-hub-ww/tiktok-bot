from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "8684897282:AAGYXJa5ZG4Ffv-0IAZuR4Tf2AFzSPtVMXA"

# --- TWOJE USŁUGI (ТВОЇ ПОСЛУГИ) ---
SERVICES = {
    "instruction": {
        "title": "Instrukcja jak zarabiać 1000$/miesiąc 📄",
        "description": "Plan krok po kroku, w którym dowiesz się czym jest Amerykański TikTok i jak się tu zarabiają tysiące $$$",
        "price": "299 PLN"
    },
    "monetization": {
        "title": "Monetyzacja pod klucz 💰",
        "description": "Podłącz monetyzację na TikToku przez 10 000 obserwujących w 5 minut",
        "price": "499 PLN"
    },
    "accounts": {
        "title": "Konta z milionami wyświetleń 🔥",
        "description": "Prosto z Francji, gotowe do pracy",
        "price": "150 PLN"
    }
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- GŁÓWNE MENU ---
def main_menu():
    buttons = []
    for key, item in SERVICES.items():
        buttons.append([InlineKeyboardButton(
            text=item["title"],
            callback_data=f"service:{key}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- PRZYCISK POWRÓT ---
def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Wróć", callback_data="back")]
    ])

# --- KOMENDA /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Cześć 🤖\n\n"
        "Jestem oficjalnym botem kanału <b>Ctrl+C Zysk</b>, co Cię interesuje?\n\n"
        "Wybierz usługę 👇",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

# --- KLIKNIĘCIE USŁUGI ---
@dp.callback_query(F.data.startswith("service:"))
async def show_service(call: CallbackQuery):
    key = call.data.split(":")[1]
    item = SERVICES[key]
    
    text = (
        f"<b>{item['title']}</b>\n\n"
        f"{item['description']}\n\n"
        f"💰 Cena: <b>{item['price']}</b>\n\n"
        f"Aby kupić — napisz do menedżera @VitossW"
    )
    await call.message.edit_text(text, reply_markup=back_button())

# --- PRZYCISK POWRÓT ---
@dp.callback_query(F.data == "back")
async def go_back(call: CallbackQuery):
    await call.message.edit_text(
        "Wybierz usługę 👇",
        reply_markup=main_menu()
    )

# --- START ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())