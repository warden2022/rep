import json

from aiogram import Router, F
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard
from data.data_1 import *
router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_subjects = ["Математике", "Информатике",]
available_levels = ["Среднюю", "Старшую", ]
#available_datas = ["Начать","Участники","Баланс"]
id_group = 0

class OrderGroup(StatesGroup):
    choosing_subjects = State()
    choosing_levels = State()
    #choosing_datas = State()


@router.message(Command(commands=["groups"]))
async def cmd_subject(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите предмет:",
        reply_markup=make_row_keyboard(available_subjects)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderGroup.choosing_subjects)
#
# Этап выбора направления #
#
#
@router.message(OrderGroup.choosing_subjects, F.text.in_(available_subjects))
async def subject_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_subject=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите уровень:",
        reply_markup=make_row_keyboard(available_levels)
    )
    await state.set_state(OrderGroup.choosing_levels)

@router.message(OrderGroup.choosing_subjects)
async def subject_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такой группы.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_subjects)
    )
#
# Этап выбора группы и отображение сводной информации #
#
#
@router.message(OrderGroup.choosing_levels, F.text.in_(available_levels))
async def level_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    
    # Определяем Id Группы
    lev = message.text.lower()
    subj = user_data['chosen_subject']
    if lev == available_levels[0].lower() and subj == available_subjects[0].lower():
        id_group = "1"
        less = "ОГЭ математика"
    elif lev == available_levels[0].lower() and subj == available_subjects[1].lower():
        id_group = "2"
    elif lev == available_levels[1].lower() and subj == available_subjects[0].lower():
        id_group = "3"
    elif lev == available_levels[1].lower() and subj == available_subjects[1].lower():
        id_group = "4"
    else:
        id_group = "not found"
    
    # Открываем database 
    with open("./data/data.json", "r", encoding="utf-8") as f:
        item = json.load(f)[id_group]
        
    zoom = item["zoom"]
    tm_gr = item["tm_gr"]
    for i in item["participants"]:
        name = i["name"]
        nick = i["nick"]
        balance = i["balance"]
        # Создаем карточку и выводим данные
        await message.answer(
            text=f"{name} {nick}\n"
                 f"Осталось занятий: {balance}\n"
        )
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} группу по {user_data['chosen_subject']}.\n"
             f"zoom: {zoom}\n"
             f"telegram: {tm_gr}\n"
             f"Начать урок: /start_lesson\n"
             f"открыть список участников: /participants\n"
             f"отметить отсутствующих: /marking\n",
        #reply_markup=make_row_keyboard(available_datas)
        reply_markup=ReplyKeyboardRemove()
    )

    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(OrderGroup.choosing_levels)
async def level_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого уровня.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_levels)
    )
#
# Этап просмотра участников #
#
#
'''
@router.message(OrderGroup.choosing_datas, F.text.in_(available_datas))
async def group_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    with await open("data_1.py", "r", encoding="utf-8") as f:
        item = f.read()

    await message.answer(
        text=f"Вы выбрали {message.text.lower()} группу по {user_data['chosen_subject']}.\n"
             f"{item}\n"
             f"Начать урок: /start_lesson\n"
             f"открыть список участников: /participants\n"
             f"отметить присутствующих: /marking\n",
        reply_markup=ReplyKeyboardRemove()
    )

    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()


@router.message(OrderGroup.choosing_datas)
async def group_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого уровня.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_datas)
    )

'''
