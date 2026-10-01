from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.callback_query(F.data == "get_subscription")
async def get_rate(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Преимущества сервиса\n\nЛегкое подключение\nБезлимитный трафик\nДо 50-ти устройств")
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="На месяц - 188₽ (-15%🔥)", callback_data="plan:1:188:15")],
        [InlineKeyboardButton(text="Три месяца - 490₽ (-25%🔥)", callback_data="plan:3:490:25")],
        [InlineKeyboardButton(text="Полгода - 990₽ (-30%🔥)", callback_data="plan:6:990:30")]
    ]))

@router.callback_query(F.data.startswith("plan:"))
async def plan(callback: CallbackQuery):
    _, month, price, discount = callback.data.split(":")

    await callback.answer()
    await callback.message.edit_text(f"Вы оплачиваете: + 4 устройства, месяцев: {month}.\nСумма: {price}₽ (Скидка: -{discount}%)\n\nВыберите удобный способ оплаты")
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="QR/СБП", callback_data="unavailable")],
        [InlineKeyboardButton(text="Международные карты", callback_data="unavailable")],
        [InlineKeyboardButton(text="Криптовалюта", callback_data="cryptowallet")],
        [InlineKeyboardButton(text="CryptoBot", callback_data="unavailable")],
        [InlineKeyboardButton(text="Банковская карта", callback_data="unavailable")]
    ]))
    

@router.callback_query(F.data == "unavailable")
async def unavailable(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Этот метод оплаты на данный момент недоступен. Выберите другой.")
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать другой способ оплаты", callback_data="get_subscription")]
    ]))
    
@router.callback_query(F.data == "cryptowallet")
async def cryptowallet(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("кайф имеется")
    await callback.message.edit_reply_markup()
    