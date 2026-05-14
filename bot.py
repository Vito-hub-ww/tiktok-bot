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
        "photo": "https://i.pinimg.com/736x/c4/50/98/c45098f00cee7ddb754db7aa71b6decf.jpg",
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
        "title": "Konto TikTok + instrukcja 🇺🇸",
        "description_part1": """Konto TikTok + instrukcja 🇺🇸

Konto do monetyzacji, zarejestrowane prosto we Francji, z maksymalnym zaufaniem od TikToka + dostęp do mojego Prywatnego Kanału!

🧹 Czyste konto, nikt i nigdy nie robił na nim filmów, pasuje pod każdą Twoją tematykę.

🔐 Do konta będzie przypisany tylko Email, który oddajemy w zestawie. Później zmieniasz dane na swoje i konto w 100% Twoje.

📖 W zestawie dołączam instrukcje po prawidłowej rozgrzewce konta dla dobrych wyświetleń, instrukcje publikacji filmów na USA (lub dowolną inną) publiczność, instrukcje weryfikacji, wypłaty pieniędzy i nie tylko!!""",
        "description_part2": """💳 Cena konta + instrukcji: tylko 30€

Po dołączeniu do mojego prywatnego kanału z instrukcjami, automatycznie wydam dane do konta.

Wybierz wygodny sposób płatności i wkręć się w 🇺🇸 TikTok razem z nami!""",
        "price_pln": "30€",
        "price_stars": 1200,
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
    
    # --- PŁATNE USŁUGI ---
    await call.message.delete()
    
    # Крок 1: ФОТО тільки якщо є (для monetization є, для accounts — немає)
    if 'photo' in item:
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=item['photo'],
            caption=f"{item['title']}\n\nPrzykład konta 👆"
        )
    
    # Крок 2: Текст опису
    if 'description_part1' in item:
        # Для accounts — два окремі повідомлення
        await call.message.answer(item['description_part1'])
        await call.message.answer(item['description_part2'])
    else:
        # Для monetization — один довгий текст
        await call.message.answer(item['description'])
    
    # Крок 3: Рахунок з кнопкою оплати
    desc_short = f"{item['title']} - {item['price_pln']}"
    if len(desc_short) > 250:
        desc_short = desc_short[:247] + "..."
    
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
        description=desc_short,
        payload=key,
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=buy_button
    )

@dp.callback_query(F.data == "back")
async def go_back(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(
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