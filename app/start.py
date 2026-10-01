from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Все системы работают исправно\n\n"
        "Инструкции и FAQ: Тут (https://sup.vinnypuxvps.work/faq)\n"
        "Политика конфиденциальности (https://vinnypux.com/privacy)",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Оформить подписку", callback_data="get_podpiska")]
        ])
    )