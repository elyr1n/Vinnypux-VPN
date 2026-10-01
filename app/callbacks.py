from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

router = Router()


@router.callback_query(F.data == "get_subscription")
async def get_rate(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("![💫](tg://emoji?id=5931621672846103580) Преимущества сервиса\n\n![⚡️](tg://emoji?id=5843553939672274145) Легкое подключение\n![⚡️](tg://emoji?id=5843553939672274145) Безлимитный трафик\n![⚡️](tg://emoji?id=5843553939672274145) До 4 устройств", parse_mode=ParseMode.MARKDOWN_V2)
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="На месяц - 188₽ (-15%🔥)", callback_data="plan:1:188:15")],
        [InlineKeyboardButton(text="Три месяца - 490₽ (-25%🔥)", callback_data="plan:3:490:25")],
        [InlineKeyboardButton(text="Полгода - 990₽ (-30%🔥)", callback_data="plan:6:990:30")]
    ]))

@router.callback_query(F.data.startswith("plan:"))
async def plan(callback: CallbackQuery):
    _, month, price, discount = callback.data.split(":")

    await callback.answer()
    await callback.message.edit_text(f"![👛](tg://emoji?id=5769403330761593044) Вы оплачиваете: \\+ 4 устройства, месяцев: {month}\\.\n![👛](tg://emoji?id=5769403330761593044) Сумма: {price}₽ \\(Скидка: \\-{discount}%\\)\n\n![📷](tg://emoji?id=5987917196469213507) Выберите удобный способ оплаты", parse_mode=ParseMode.MARKDOWN_V2)
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="QR/СБП", callback_data="unavailable")],
        [InlineKeyboardButton(text="Международные карты", callback_data="unavailable")],
        [InlineKeyboardButton(text="Криптовалюта", callback_data="cryptowallet")],
        [InlineKeyboardButton(text="CryptoBot", callback_data="unavailable")],
        [InlineKeyboardButton(text="Банковская карта", callback_data="unavailable")],
        [InlineKeyboardButton(text="Назад", callback_data="get_subscription")]
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
    