import random

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from app.storage import blockchain_networks, price_devices

router = Router()


@router.callback_query(F.data == "get_subscription")
async def get_rate(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.update_data(devices=4)

    await callback.message.edit_text(
        "![💫](tg://emoji?id=5931621672846103580) Преимущества сервиса\n\n"
        "![⚡️](tg://emoji?id=5843553939672274145) Легкое подключение\n"
        "![⚡️](tg://emoji?id=5843553939672274145) Безлимитный трафик\n"
        "![⚡️](tg://emoji?id=5843553939672274145) До 50 устройств",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔼", callback_data="device:add"),
            InlineKeyboardButton(text=str((await state.get_data())["devices"]), callback_data="count_devices"),
            InlineKeyboardButton(text="🔽", callback_data="device:delete")
        ],
        [InlineKeyboardButton(text=f"На месяц - {price_devices["one_months"]}₽ (-15%🔥)", callback_data=f"plan:1:{price_devices["one_months"]}:15")],
        [InlineKeyboardButton(text=f"Три месяца - {price_devices["three_months"]}₽ (-25%🔥)", callback_data=f"plan:3:{price_devices["three_months"]}:25")],
        [InlineKeyboardButton(text=f"Полгода - {price_devices["six_months"]}₽ (-30%🔥)", callback_data=f"plan:6:{price_devices["six_months"]}:30")]
    ]))


@router.callback_query(F.data.startswith("device:"))
async def devices(callback: CallbackQuery, state: FSMContext):
    _, action = callback.data.split(":")
    count_devices = (await state.get_data())["devices"]

    if action == "add":
        await state.update_data(devices=count_devices + 1)
    else:
        await state.update_data(devices=count_devices - 1)

    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔼", callback_data="device:add"),
            InlineKeyboardButton(text=str((await state.get_data())["devices"]), callback_data="count_devices"),
            InlineKeyboardButton(text="🔽", callback_data="device:delete")
        ],
        [InlineKeyboardButton(text=f"На месяц - {price_devices["one_months"] + random.randint(10, 30)}₽ (-15%🔥)", callback_data=f"plan:1:{price_devices["one_months"] + random.randint(10, 30)}:15")],
        [InlineKeyboardButton(text=f"Три месяца - {price_devices["three_months"] + random.randint(10, 30)}₽ (-25%🔥)", callback_data=f"plan:3:{price_devices["three_months"] + random.randint(10, 30)}:25")],
        [InlineKeyboardButton(text=f"Полгода - {price_devices["six_months"] + random.randint(10, 30)}₽ (-30%🔥)", callback_data=f"plan:6:{price_devices["six_months"] + random.randint(10, 30)}:30")]
    ]))


@router.callback_query(F.data.startswith("plan:"))
async def plan(callback: CallbackQuery, state: FSMContext):
    _, month, price, discount = callback.data.split(":")

    await state.update_data(month=month, price=price)

    await callback.answer()
    await callback.message.edit_text(
        "![👛](tg://emoji?id=5769403330761593044) Вы оплачиваете: \\+ 4 устройства, месяцев: "
        f"{month}\\.\n"
        "![👛](tg://emoji?id=5769403330761593044) Сумма: "
        f"{price}₽ \\(Скидка: \\-{discount}%\\)\n\n"
        "![📷](tg://emoji?id=5987917196469213507) Выберите удобный способ оплаты",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="QR/СБП", callback_data="unavailable")],
        [InlineKeyboardButton(text="Международные карты", callback_data="unavailable")],
        [InlineKeyboardButton(text="Криптовалюта", callback_data="cryptowallet")],
        [InlineKeyboardButton(text="Банковская карта", callback_data="unavailable")],
        [InlineKeyboardButton(text="Назад", callback_data="get_subscription")]
    ]))


@router.callback_query(F.data == "unavailable")
async def unavailable(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("[Обратитесь в поддержку для получения нужных реквизитов\\.](https://t.me/Vinnypux_VPN?direct)", parse_mode=ParseMode.MARKDOWN_V2)
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать другой способ оплаты", callback_data="get_subscription")]
    ]))


@router.callback_query(F.data == "cryptowallet")
async def cryptowallet(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "![👛](tg://emoji?id=5769403330761593044) Выберите сеть по которой хотите оплатить подписку",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="GRAM", callback_data="network_GRAM")],
        [InlineKeyboardButton(text="USDT-Ton", callback_data="network_USDT-Ton")],
        [InlineKeyboardButton(text="USDT-TRC20", callback_data="network_USDT-TRC20")],
    ]))


@router.callback_query(F.data.startswith("network_"))
async def send_address_network(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    try:
        data = await state.get_data()
        month, price = data["month"], data["price"]
        _, network = callback.data.split("_")

        await callback.message.edit_text(
            "![👛](tg://emoji?id=5769403330761593044) Сеть: "
            f"{network.replace("-", "\\-")}\n"
            "![👛](tg://emoji?id=5769403330761593044) Адрес: "
            f"`{blockchain_networks[network]["address"]}`\n"
            "![👛](tg://emoji?id=5769403330761593044) Сумма: "
            f"`${int(price) / blockchain_networks[network]["rate"]:.4f}`\n\n"
            "![⚡️](tg://emoji?id=5843553939672274145) Ожидаем оплату, после чего вернемся к Вам с уведомлением о подписке",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="get_subscription")]
        ]))
    except KeyError:
        await callback.message.edit_text("Произошла ошибка с оплатой. Повторите попытку.")
        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Повторить попытку", callback_data="get_subscription")]
        ]))
