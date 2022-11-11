import json

from aiogram import Router, types, F
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove


from keyboards.simple_row import make_row_keyboard#, make_keyboard
from data.data_1 import *
from func import get_date_now, create_conference
from data_base.data_childs import set_balance

#from data_base.data_curent import curent

router = Router()

curent = {}
# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_subjects = ["Математике", "Информатике",]
available_levels = ["Среднюю", "Старшую", ]
available_begin = ["/begin",]

id_group = 0

class OrderGroup(StatesGroup):
    choosing_subjects = State()
    choosing_levels = State()
    choosing_begin = State()



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
    elif lev == available_levels[0].lower() and subj == available_subjects[1].lower():
        id_group = "2"
    elif lev == available_levels[1].lower() and subj == available_subjects[0].lower():
        id_group = "3"
    elif lev == available_levels[1].lower() and subj == available_subjects[1].lower():
        id_group = "4"
    else:
        id_group = "not found"
    # Открываем database
    now = get_date_now()
    #print(d_groups["1"])
    with open(f"./data_base/data_groups.json", "r", encoding="utf-8") as f:
        groups = json.load(f)
    teams = groups[id_group]["participants"]
    zoom = groups[id_group]["zoom"]
    tm_gr = groups[id_group]["tm_gr"]
    for i in teams:
        if i["user_id"] == 0:
            continue
        else:
            name = i["name"]
            nick = i["nick"]
            balance = i["balance"]
            # Создаем карточку и выводим данные
            await message.answer(
                text=f"{name} {nick}\n"
                    f"Осталось занятий: {balance}\n"
            )
    # Сохраняем id группы
    curent_group = {"id":id_group}
    with open(f"data/date/curent.json", "w", encoding="utf-8") as f:
        json.dump(curent_group, f, indent=4, ensure_ascii=False)
    
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} группу по {user_data['chosen_subject']}.\n"
             f"zoom: {zoom}\n"
             f"telegram: {tm_gr}\n\n"
             f"Начать урок: /begin\n"
             f"открыть список участников: /participants\n"
             f"отметить отсутствующих: /marking\n",
        reply_markup=make_row_keyboard(available_begin)
        # reply_markup=ReplyKeyboardRemove()
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
@router.message(Command(commands=["begin"]))
async def cmd_begin(message: Message):
    # Текущая дата
    now = get_date_now()
    # считываем данные о группах 
    with open(f"./data_base/data_groups.json", "r", encoding="utf-8") as f:
        groups = json.load(f)
        # Считываем данные id текущей группы
        with open(f"./data/date/curent.json", "r", encoding="utf-8") as f:
            group_id = json.load(f)["id"] # id группы
            # Снимаем с баланс абонемент каждого участника текущей группы
            for i in groups[group_id]["participants"]:
                id_item = i["user_id"]
                set_balance(id_item, now,-1)
            # Считываем данные учеников
            with open(f"./data_base/data_childs.json", "r", encoding="utf-8") as f:
                child = json.load(f)
                # Сохраняем обновленные данные учеников в группе
                groups[group_id]["participants"] = child
                with open(f"./data_base/data_groups.json", "w", encoding="utf-8") as f:
                    json.dump(groups, f, indent=4, ensure_ascii=False)
            
            # Начинаем конференцию
            zoom = groups[group_id]["zoom"]    # url zoom conference
            tm_gr = groups[group_id]["tm_gr"]  # url telegram conference
            '''
            try:
                if tm_gr:
                    create_conference(tm_gr)
            except:
                create_conference(zoom)
            '''

    # addBalance
    # marking
    #
    await message.answer(
        text=f"Началось\n",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    #await state.clear()

@router.message(OrderGroup.choosing_begin)
async def begin_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_begin)
    )

