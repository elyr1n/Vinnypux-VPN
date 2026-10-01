from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"![⏺️](tg://emoji?id=5818711397860642669) Все системы работают исправно\n\n"
        "Инструкции и FAQ: [Тут](https://sup.vinnypuxvps.work/faq)\n"
        "[Политика конфиденциальности](https://vinnypux.com/privacy)",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Оформить подписку", callback_data="get_subscription")]
        ])
    )