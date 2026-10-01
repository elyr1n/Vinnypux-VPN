from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.callback_query(F.data == "get_podpiska")
async def get_tarif(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Преимущества сервиса\n\nЛегкое подключение\nБезлимитный трафик\nДо 50-ти устройств")
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="На месяц - 188₽ (-15%🔥)", callback_data="plan:1:188:15")],
        [InlineKeyboardButton(text="Три месяца - 490₽ (-25%🔥)", callback_data="plan:3:490:25")],
        [InlineKeyboardButton(text="Полгода - 990₽ (-30%🔥)", callback_data="plan:6:990:30")],
        [InlineKeyboardButton(text="Назад", callback_data="nazad")],
    ]))