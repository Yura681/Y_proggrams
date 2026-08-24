import os
import json
from http.server import BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8969404900:AAFRX3s1VpATqniz345McVU_nS3eAOw7-pg"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатуры оставляем твои
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть пример программы/сайта", callback_data="show_examples")],
        [InlineKeyboardButton(text="Лицензионное соглашение", callback_data="license_agreement")],
        [InlineKeyboardButton(text="Связаться с создателем", url="https://t.me/Yura_2202")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_menu")]
    ])

@dp.message(F.text == "/start")
async def cmd_start(message):
    user_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    text = (
        f"Здравствуйте, {user_display}! "
        f"Если вы хотите посмотреть пример работ, нажмите кнопку «Посмотреть пример программы/сайта», "
        f"если вы хотите заказать сайт или программу .exe, нажмите «Связаться с создателем».\n\n"
        f"💡 Цена зависит от качества и размеров проекта, а средняя составляет 190–700 рублей.\n\n"
        f"⚠️ Покупая товар или оформляя заказ, вы автоматически соглашаетесь с условиями "
        f"лицензионного соглашения.\n\n"
        f"Пожалуйста, не ведитесь на поддельных ботов, это единственный оригинальный бот Y_Proggrams, "
        f"мой оригинальный юзернейм — @Yura_2202."
    )
    await message.answer(text, reply_markup=get_main_keyboard())

@dp.callback_query(F.data == "show_examples")
async def show_examples_callback(callback):
    await callback.answer("Загружаю примеры...")
    videos = [
        ("BAACAgIAAxkBAAM5aor0An7rrOzmSrFeT6u_urL3Q-4AAheoAALxnlhIYgKcpHYMWT09BA", "700 рублей за этот проект"),
        ("BAACAgIAAxkBAAM7aor0GD2Nw4yVf1BWSvSrRe1jXOwAAhmoAALxnlhIOhECkCf5jDM9BA", "400 рублей за этот проект"),
        ("BAACAgIAAxkBAAM9aor0LYdnAn5n9eRKIjFK1GLdShoAAhuoAALxnlhIEmcsh7368Tc9BA", "190 рублей за этот проект")
    ]
    for vid, caption in videos:
        await callback.message.answer_video(video=vid, caption=caption)

@dp.callback_query(F.data == "license_agreement")
async def license_callback(callback):
    await callback.answer()
    license_text = (
        "📜 Лицензионное соглашение и правила сервиса Y_Proggrams\n\n"
        "1. Общие положения: Оформляя заказ или совершая покупку, вы безоговорочно принимаете условия данного соглашения.\n\n"
        "2. Условия возврата: Возврат средств возможен исключительно до начала активной разработки.\n\n"
        "3. Комиссии и платежи: Все комиссии создатель берет на себя. Перевод осуществляется исключительно на указанную банковскую карту. Попытки взлома или подбора паролей пресекаются по статье 272 УК РФ.\n\n"
        "4. Ответственность: Заказчик несет полную личную ответственность за использование ПО."
    )
    await callback.message.answer(license_text, reply_markup=get_back_keyboard())

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback):
    await callback.answer()
    user_display = f"@{callback.from_user.username}" if callback.from_user.username else callback.from_user.first_name
    text = (
        f"Здравствуйте, {user_display}! "
        f"Если вы хотите посмотреть пример работ, нажмите кнопку «Посмотреть пример программы/сайта», "
        f"если вы хотите заказать сайт или программу .exe, нажмите «Связаться с создателем».\n\n"
        f"💡 Цена зависит от качества и размеров проекта, а средняя составляет 190–700 рублей."
    )
    await callback.message.answer(text, reply_markup=get_main_keyboard())

# Обработчик для Vercel (ловит запросы от Telegram)
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update_data = json.loads(post_data.decode('utf-8'))
            update = Update.model_validate(update_data, context={"bot": bot})
            
            # Запуск асинхронного диспетчера для обработки апдейта
            import asyncio
            asyncio.run(dp.feed_update(bot, update))
        except Exception as e:
            print(f"Error: {e}")

        self.send_response(200)
        self.end_headers()