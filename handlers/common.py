from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    from config import ADMIN_ID

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    
    # Кнопки для всех
    builder.row(types.KeyboardButton(text="📍 Пробить IP"))
    builder.row(types.KeyboardButton(text="💰 Курс Крипты"))
    
    # Кнопка настроек появится ТОЛЬКО у тебя
    if str(message.from_user.id) == str(ADMIN_ID):
        builder.row(types.KeyboardButton(text="⚙️ Настройки"))
    
    await message.answer(
        "Разведчик готов к работе!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

