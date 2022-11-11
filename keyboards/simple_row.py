from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

def make_keyboard(items: list[str],items2: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    row2 = [KeyboardButton(text=item) for item in items2]
    return ReplyKeyboardMarkup(keyboard=[[row],[row2]], resize_keyboard=True)