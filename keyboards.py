from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

kb_start = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text= 'Информация о боте', url='https://longerx00.github.io/site/')]])

kb_disciplines = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Программирование C/C++', callback_data='c++')],
    [InlineKeyboardButton(text='Технологии программирования', callback_data='tp')],
    [InlineKeyboardButton(text='Дискретная математика', callback_data='discra')],
    [InlineKeyboardButton(text='Основы российской государственности', callback_data='org')],
    [InlineKeyboardButton(text='Математический анализ', callback_data='mathan')],
    [InlineKeyboardButton(text='Безопасность жинедеятельности', callback_data='bzhd')],
    [InlineKeyboardButton(text='НПС "Цифровая грамотность"', callback_data='cg')],
    [InlineKeyboardButton(text='Алгоритмы и структуры данных', callback_data='c++')]
])

keybord_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сегодня'), KeyboardButton(text='Завтра')],
    [KeyboardButton(text='Послезавтра'), KeyboardButton(text='Текущая неделя')],
    [KeyboardButton(text='⏪ Пред. неделя'), KeyboardButton(text='След. неделя ⏩')]
], resize_keyboard=True, input_field_placeholder='Выберите день:')

keybord_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='КНТ-1', callback_data='knt-1'), InlineKeyboardButton(text='КНТ-2', callback_data='knt-2')],
    [InlineKeyboardButton(text='КНТ-3', callback_data='knt-3'), InlineKeyboardButton(text='КНТ-4', callback_data='knt-4')],
    [InlineKeyboardButton(text='КНТ-5', callback_data='knt-5'), InlineKeyboardButton(text='КНТ-6', callback_data='knt-6')],
    [InlineKeyboardButton(text='КНТ-7', callback_data='knt-7')]
])

kb_english = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расписание', url='https://docs.google.com/spreadsheets/d/1RB9AWtrYm6Y9m8NSy6On7Zk3byws8RonAGBqeneSxOo/edit?gid=23993546#gid=23993546')]
])
