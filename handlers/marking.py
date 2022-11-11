from aiogram import Router, F
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

router = Router()

available_subjects = ["Математике", "Информатике",]

id_group = 0

class OrderGroup(StatesGroup):
    choosing_subjects = State()



@router.message(Command(commands=["groups"]))
async def cmd_subject(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите предмет:",
        reply_markup=make_row_keyboard(available_subjects)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderGroup.choosing_subjects)
