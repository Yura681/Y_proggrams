import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8969404900:AAFRX3s1VpATqniz345McVU_nS3eAOw7-pg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть пример программы/сайта", callback_data="show_examples")],
        [InlineKeyboardButton(text="Лицензионное соглашение", callback_data="license_agreement")],
        [InlineKeyboardButton(text="Связаться с создателем", url="https://t.me/Yura_2202")]
    ])
    return keyboard

def get_back_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_menu")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: Message):
    username = message.from_user.username
    user_display = f"@{username}" if username else message.from_user.first_name
    
    text = (
        f"Здравствуйте, {user_display}! "
        f"Если вы хотите посмотреть пример работ, нажмите кнопку «Посмотреть пример программы/сайта», "
        f"если вы хотите заказать сайт или программу .exe, нажмите «Связаться с создателем».\n\n"
        f"💡 Цена зависит от качества и размеров проекта, а средняя составляет 190–700 рублей.\n\n"
        f"⚠️ Покупая товар или оформляя заказ, вы автоматически соглашаетесь с условиями "
        f"лицензионного соглашения.\n\n"
        f"Пожалуйста, не ведитесь на поддельных ботов, это единственный оригинальный бот Y_Proggrams, "
        f"мой оригинальный юзернейм — @Yura_2202.\n\n"
        f"Кстати этот бот тоже создан мной."
    )
    
    await message.answer(text, reply_markup=get_main_keyboard())

# Отправка примеров с индивидуальными ценами для каждого видео
@dp.callback_query(F.data == "show_examples")
async def show_examples_callback(callback: CallbackQuery):
    await callback.answer("Загружаю примеры...")
    
    videos_with_captions = [
        ("BAACAgIAAxkBAAM5aor0An7rrOzmSrFeT6u_urL3Q-4AAheoAALxnlhIYgKcpHYMWT09BA", "700 рублей за этот проект"),
        ("BAACAgIAAxkBAAM7aor0GD2Nw4yVf1BWSvSrRe1jXOwAAhmoAALxnlhIOhECkCf5jDM9BA", "400 рублей за этот проект"),
        ("BAACAgIAAxkBAAM9aor0LYdnAn5n9eRKIjFK1GLdShoAAhuoAALxnlhIEmcsh7368Tc9BA", "190 рублей за этот проект")
    ]
    
    for vid, caption in videos_with_captions:
        await callback.message.answer_video(
            video=vid,
            caption=caption
        )

# Лицензионное соглашение с условиями оплаты на карту и статьей 272 УК РФ
@dp.callback_query(F.data == "license_agreement")
async def license_callback(callback: CallbackQuery):
    await callback.answer()
    
    license_text = (
        "📜 Лицензионное соглашение и правила сервиса Y_Proggrams\n\n"
        "1. Общие положения: Оформляя заказ или совершая покупку, вы безоговорочно принимаете условия данного соглашения.\n\n"
        "2. Условия возврата: Возврат денежных средств возможен исключительно до начала активной разработки программы или сайта. После передачи готового исходного кода или исполняемого файла (.exe) возврат средств не производится.\n\n"
        "3. Комиссии и платежи: Все комиссии за перевод средств (банки, платежные системы, криптокошельки и т.д.) создатель берет полностью на себя. Вы платите ровно ту сумму, о которой договорились. Перевод средств осуществляется исключительно на указанную мной банковскую карту. Любые попытки несанкционированного доступа, подбора паролей, взлома или совершения противоправных действий в отношении платежных реквизитов и инфраструктуры сервиса пресекаются и подпадают под действие статьи 272 УК РФ (Неправомерный доступ к компьютерной информации).\n\n"
        "4. Ответственность: Заказчик несет полную личную ответственность за дальнейшее использование приобретенного программного обеспечения."
    )
    
    await callback.message.answer(
        license_text, 
        reply_markup=get_back_keyboard()
    )

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery):
    await callback.answer()
    
    username = callback.from_user.username
    user_display = f"@{username}" if username else callback.from_user.first_name
    
    text = (
        f"Здравствуйте, {user_display}! "
        f"Если вы хотите посмотреть пример работ, нажмите кнопку «Посмотреть пример программы/сайта», "
        f"если вы хотите заказать сайт или программу .exe, нажмите «Связаться с создателем».\n\n"
        f"💡 Цена зависит от качества и размеров проекта, а средняя составляет 190–700 рублей."
    )
    
    await callback.message.answer(text, reply_markup=get_main_keyboard())

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())