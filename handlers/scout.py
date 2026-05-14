from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_ID
from utils.api_requests import get_ip_info, get_crypto_price, get_web_price
import psutil
import platform
from datetime import datetime

router = Router()

# Функция для создания главного меню (Reply-кнопки)
def get_main_kb():
    kb = [
        [KeyboardButton(text="💰 Курс Крипты"), KeyboardButton(text="📍 Пробить IP")],
        [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="📈 Мониторинг Цен")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@router.message(CommandStart()) 
async def command_start_handler(message: types.Message):
    print(f" LOG: Пользователь {message.from_user.id} нажал START") # Для отладки в консоли
    await message.answer(
        "Скаут Парсер запущен и готов к работе! 👁",
        reply_markup=get_main_kb()
    )

@router.message(F.text == "💰 Курс Крипты")
async def crypto_handler(message: types.Message):
    price = get_crypto_price("bitcoin")
    await message.answer(f"📊 Текущий курс Bitcoin: ${price}")

@router.message(F.text == "📍 Пробить IP")
async def ip_handler(message: types.Message):
    await message.answer("Отправь мне IP-адрес, и я выдам по нему справку.")

@router.message(F.text.regexp(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"))
async def ip_info_result(message: types.Message):
    data = get_ip_info(message.text)
    if data:
        res = (f"🌐 Информация по IP: {data.get('query')}\n"
               f"Страна: {data.get('country')}\n"
               f"Город: {data.get('city')}\n"
               f"Провайдер: {data.get('isp')}")
        await message.answer(res)
    else:
        await message.answer("Не удалось получить данные.")

@router.message(F.text == "⚙️ Настройки")
async def settings_handler(message: types.Message):
    # Приведение к строке для надежного сравнения
    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("⚠️ Доступ запрещен.")
        return

    cpu_usage = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    uptime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    
    stats = (
        "🖥 ПАНЕЛЬ УПРАВЛЕНИЯ СЕРВЕРОМ\n"
        "------------------------------\n"
        f"👤 Админ: {message.from_user.first_name}\n"
        f"🐧 ОС: {platform.system()} {platform.release()}\n"
        f"🔥 Процессор: {cpu_usage}%\n"
        f"💾 ОЗУ: {ram.percent}% ({round(ram.used / 10243, 1)}/{round(ram.total / 10243, 1)} GB)\n"
        f"⏱️ Система запущена: {uptime}\n"
        "------------------------------\n"
        "✅ Все системы работают штатно."
    )

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔄 Перезагрузить бота", callback_data="restart_bot"))
    builder.row(InlineKeyboardButton(text="📊 Полный лог", callback_data="get_log"))

    await message.answer(stats, reply_markup=builder.as_markup())

@router.message(F.text == "📈 Мониторинг Цен")
async def monitor_handler(message: types.Message):
    await message.answer("Пришли мне прямую ссылку на товар, и я попробую узнать его цену! 🛒")

@router.message(F.text.startswith("http"))
async def parse_url_handler(message: types.Message):
    wait_msg = await message.answer("🔍 Захожу на сайт, секунду...")
    
    price = get_web_price(message.text)
    
    await wait_msg.edit_text(
        f"✅ Результат парсинга:\n\n{price}\n\n"
        f"_Если цена некорректна, нужно настроить парсер под этот конкретный сайт._",
        parse_mode="Markdown"
    )