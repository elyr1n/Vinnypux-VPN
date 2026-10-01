from aiogram.fsm.state import State, StatesGroup


class Subscription(StatesGroup):
    plan = State()
