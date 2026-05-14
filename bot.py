from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, 
    InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
)
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "8684897282:AAGYXJa5ZG4Ffv-0IAZuR4Tf2AFzSPtVMXA"

SERVICES = {
    "instruction": {
        "title": "Instrukcja jak zarabiać 1000$/miesiąc 📄",
        "description": "Plan krok po kroku, w którym dowiesz się czym jest Amerykański TikTok i jak się tu zarabiają tysiące $$$",
        "price_pln": "DARMOWY",
        "price_stars": 0,
        "content": "https://telegra.ph/1000-miesi%C4%99cznie-na-zagranicznym-TikToku-05-10-2"
    },
    "monetization": {
        "title": "Monetyzacja pod klucz 💰",
        "description": """Konto TikTok z podłączoną monetyzacją 🇺🇸

Na koncie już jest podłączona monetyzacja, możesz publikować filmy i od razu zarabiać + dostęp do mojego prywatnego kanału!!

🔐 Do konta będzie przypisany tylko Email, który jest w zestawie. Później zmieniasz wszystkie dane na swoje i konto w 100% Twoje.

W zestawie daję instrukcje po rozgrzewce konta dla dużych wyświetleń, instrukcję publikacji filmów na USA (lub dowolną inną) publiczność, oraz instrukcję weryfikacji & wypłaty pieniędzy z TikToka!

- Czyste konto ✔️
- Gwarancja 30 dni ✔️
- TikTok Shop otwarty ✔️
- 10 tys. obserwujących ✔️
- Creator Rewards Program podłączony ✔️

Pozostało kont na stanie: 1.

💳 Cena konta + instrukcji: tylko 199€

Niektórzy ludzie zarabiają cenę konta już w jeden dzień!

Po dołączeniu do prywatnego kanału z instrukcjami, automatycznie wydam dane do konta.

Wybierz wygodny sposób płatności i zacznij zarabiać na swoich 🇺🇸 filmach już dziś!""",
        "price_pln": "199€",
        "price_stars": 7500,
        "content": "Dziękujemy! Napisz do menedżera, aby podłączyć monetyzację: @twój_nick"
    },
    "accounts": {
        "title": "Konta z milionami wyświetleń 🔥",
        "description": "Prosto z Francji, gotowe do pracy",
        "price_pln": "150 PLN",
        "price_stars": 1500,
        "content": "Dziękujemy! Oto dane do konta:\nLogin: example\nHasło: 12345"
    }
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_menu():
    buttons = []
    for key, item in SERVICES.items():
        buttons.append([InlineKeyboardButton(
            text=item["title"],
            callback_data=f"service:{key}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Cześć 🤖\n\n"
        "Jestem oficjalnym botem kanału Ctrl+C Zysk, co Cię interesuje?\n\n"
        "Wybierz usługę 👇",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data.startswith("service:"))
async def show_service(call: CallbackQuery):
    key = call.data.split(":")[1]
    item = SERVICES[key]
    
    if key == "instruction":
        text = (
            f"{item['title']}\n\n"
            f"{item['description']}\n\n"
            f"🎁 Ten kurs jest DARMOWY!"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📥 Zabierz kurs", url=item["content"])],
            [InlineKeyboardButton(text="🔙 Wróć", callback_data="back")]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)
        return
    
    desc = item['description']
    if len(desc) > 250:
        desc = desc[:247] + "..."
    
    text = (
        f"{item['title']}\n\n"
        f"{item['description']}\n\n"
        f"💰 Cena: {item['price_pln']} ({item['price_stars']} ⭐)\n\n"
        f"Kliknij przycisk poniżej, aby kupić:"
    )
    
    buy_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"💳 Kup za {item['price_stars']} Stars",
            pay=True
        )],
        [InlineKeyboardButton(text="🔙 Wróć", callback_data="back")]
    ])
    
    prices = [LabeledPrice(label=item['title'], amount=item['price_stars'])]
    
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=item['title'],
        description=desc,
        payload=key,
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=buy_button
    )
    await call.message.delete()

@dp.callback_query(F.data == "back")
async def go_back(call: CallbackQuery):
    await call.message.edit_text(
        "Wybierz usługę 👇",
        reply_markup=main_menu()
    )

@dp.pre_checkout_query()
async def pre_checkout_handler(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    item = SERVICES.get(payload)
    
    if item:
        await message.answer(
            f"✅ Płatność udana!\n\n"
            f"{item['title']}\n\n"
            f"{item['content']}\n\n"
            f"Dziękujemy za zakup! 🎉"
        )
    else:
        await message.answer("Błąd! Skontaktuj się z menedżerem @twój_nick")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())