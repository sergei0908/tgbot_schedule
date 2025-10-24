from google.oauth2.service_account import Credentials
import gspread
import sqlite3
from datetime import timedelta, datetime
from datetime import date as d
from threading import Timer

import re 

conn = sqlite3.connect("schedule.db")
cursor = conn.cursor()

scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1BMR4Zk3BU2Tyo7L-CYJeMfVuCxjmmT94kfz4Jp6BFAc/edit?gid=739453176#gid=739453176").worksheet("1 курс")
sheet2 = client.open_by_url("https://docs.google.com/spreadsheets/d/1pXmcgHLvxzkSkl-FgrtV2UKr_0zkAOu7EW4hR1-EbVE/edit?gid=1256432429#gid=1256432429").worksheet("1 курс")

def get_lesson(cell):
    lessons = ["Программирование C/C++", "Технологии программирования", "Дискретная математика",
               "Линейная алгебра и геометрия", "Основы российской государственности", "Математический анализ",
               "Безопасность жинедеятельности", 'НПС "Цифровая грамотность"', "История России",
               "Программирование на C++", "Алгоритмы и стуктуры данных"]
    for l in lessons:
        if l in cell: return l
    return None

def get_teacher(cell):
    teachers = ["Климов А.", "Улитин И.Б.", "Касьянов Н.Ю.",
                "Малышев Д.С.", "Беспалов П.А.", "Константинова Т.Н.",
                "Чистякова С.А.", "Савина О.Н.", "Чистяков В.В.", "Городнова А.А.",
                "Кочеров С.Н.", "Пеплин Ф.С.", "Талецкий Д.С.", "Полонецкая Н.А.",
                "Марьевичев Н.", "Шапошников В.Е.", "Логвинова К.В.", "Лупанова Е.А.",
                "Косульников Д.Д.", "Вакансия", "Марьевичев Н.", "Железин М.М."]
    for t in teachers:
        if t in cell: return t
    return None

def get_type(cell):
    types = ["лекция", "семинар", "практическое занятие"]
    for t in types:
        if t in cell: return t
    return None

def get_day(start, end):
    day_pairs_up = []
    day_pairs_low = []
    n = 1
    if d(year=2025, month=9, day=1) < d.today() < d(year=2025, month=11, day=1):
        cell = sheet.get_all_values(f'{start}:{end}')
    elif d(year=2025, month=11, day=1) <= d.today() < d(year=2026, month=1, day=1):
        cell = sheet2.get_all_values(f'{start}:{end}')
    i = 0
    for pair in cell:
        
        if len(cell[i]) > 0:
            if len(cell[i][0]) > 0:
                disciplines = cell[i][0]
                building = cell[i][2]
                if n == 1: time = '8:00-9:20'
                elif n == 2: time = '9:30-10:50'
                elif n == 3: time = '11:10-12:30'
                elif n == 4: time = '13:00-14:20'
                elif n == 5: time = '14:40-16:00'
                elif n == 6: time = '16:20-17:40'
                elif n == 7: time = '18:10-19:30'
                elif n == 8: time = '19:40-21:00'
                auditories = cell[i][1]

                if "---------------------" in disciplines:
                    upper_week_discipline, lower_week_discipline = disciplines.replace("\n", "").split("---------------------")

                    if "----" in auditories:
                        upper_week_auditories, lower_week_auditories = auditories.replace("\n", "").split("----")
                    elif "---" in auditories:
                        upper_week_auditories, lower_week_auditories = auditories.replace("\n", "").split("---")
                    else:
                        upper_week_auditories = auditories.replace("\n", "")
                        lower_week_auditories = auditories.replace("\n", "")

                    if "----" in building:
                        upper_week_building, lower_week_building = building.replace("\n", "").split("----")
                    elif "---" in building:
                        upper_week_building, lower_week_building = building.replace("\n", "").split("---")
                    else:
                        upper_week_building = building.replace("\n", "")
                        lower_week_building = building.replace("\n", "")

                    type_lesson_up = get_type(upper_week_discipline)
                    type_lesson_low = get_type(lower_week_discipline)
                    teacher_up = get_teacher(upper_week_discipline)
                    lesson_up = get_lesson(upper_week_discipline)
                    teacher_low = get_teacher(lower_week_discipline)
                    lesson_low = get_lesson(lower_week_discipline)

                    data_up = [time, lesson_up, type_lesson_up, teacher_up, upper_week_auditories, upper_week_building, upper_week_discipline]
                    data_low = [time, lesson_low, type_lesson_low, teacher_low, lower_week_auditories, lower_week_building, lower_week_discipline]
                    
                    if data_up[4] == '': data_up[4] = '-'
                    if data_low[4] == '': data_low[4] = '-'
                    if data_up[2] == None: data_up[2] = 'семинар'
                    if data_low[2] == None: data_low[2] = 'семинар'


                    if data_up[1] != None:
                        day_pairs_up += [data_up]
                    if data_low[1] != None:
                        day_pairs_low += [data_low]
                else:
                    lower_week_discipline = disciplines.replace("\n", "")
                    upper_week_discipline = disciplines.replace("\n", "")

                    upper_week_auditories = auditories.replace("\n", "")
                    lower_week_auditories = auditories.replace("\n", "")

                    upper_week_building = building.replace("\n", "")
                    lower_week_building = building.replace("\n", "")
                    
                    teacher = get_teacher(lower_week_discipline)
                    lesson = get_lesson(lower_week_discipline)
                    type_lesson = get_type(lower_week_discipline)

                    data_up = [time, lesson, type_lesson, teacher, upper_week_auditories, upper_week_building, upper_week_discipline]
                    data_low = [time, lesson, type_lesson, teacher, lower_week_auditories, lower_week_building, lower_week_discipline]
                    
                    if data_up[4] == '': data_up[4] = '-'
                    if data_low[4] == '': data_low[4] = '-'
                    if data_up[2] == None: data_up[2] = 'семинар'
                    if data_low[2] == None: data_low[2] = 'семинар'

                    day_pairs_up += [data_up]
                    day_pairs_low += [data_low]
            n += 1   
        i += 1

    return [day_pairs_up, day_pairs_low]

rows = ([12, 19], [21, 28], [30, 37], [48, 57])

def get_week(list):
    week_schedule = []
    for el in rows:
        week_schedule += get_day(f'{list[0]}{el[0]}', f'{list[1]}{el[1]}')
    return week_schedule

upper_week_days = ['01.09', '02.09', '03.09', '04.09', '05.09', '06.09', '15.09', '16.09', '17.09', '18.09', '19.09', '20.09', '29.09', '30.09', \
                   '01.10', '02.10', '03.10', '04.10', '13.10', '14.10', '15.10', '16.10', '17.10', '18.10', '03.11', '04.11', '05.11', '06.11', \
                    '07.11', '08.11', '21.11', '22.11', '17.11', '18.11', '19.11', '20.11', '01.12', '02.12', '03.12', '04.12', '05.12', '06.12', \
                     '15.12', '16.12', '17.12', '18.12', '19.12']
lower_week_days = ['08.09', '09.09', '10.09', '11.09', '12.09', '13.09', '22.09', '23.09', '24.09', '25.09', '26.09', '27.09', '06.10', '07.10', \
                   '08.10', '09.10', '10.10', '11.10', '20.10', '21.10', '22.10', '23.10', '24.10', '01.11', '10.11', '11.11', '12.11', '13.11', \
                    '14.11', '15.11', '24.11', '25.11', '26.11', '27.11', '28.11', '29.11', '08.12', '09.12', '10.12', '11.12', '12.12', '13.12']
weekend_days = ['07.09', '14.09', '21.09', '28.09', '05.10', '12.10', '19.10', '03.11', '02.11', '09.11', '16.11', '23.11', '30.11', '07.12', '14.12', '31.12']
session_days = ['25.10', '26.10', '27.10', '28.10', '29.10', '30.10', '31.10', '20.12', '21.12', '22.12', '23.12', '24.12', '25.12', '26.12', '27.12', '28.12', '29.12', '30.12']

week_1 = [f'{x}.09' for x in ('01', '02', '03', '04', '05', '06', '07')]
week_2 = [f'{x}.09' for x in ('08', '09', '10', '11', '12', '13', '14')]
week_3 = [f'{x}.09' for x in ('15', '16', '17', '18', '19', '20', '21')]
week_4 = [f'{x}.09' for x in ('22', '23', '24', '25', '26', '27', '28')]
week_5 = ['29.09', '30.09',  '01.10', '02.10', '03.10', '04.10', '05.10']
week_6 = [f'{x}.10' for x in ('06', '07', '08', '09', '10', '11', '12')]
week_7 = [f'{x}.10' for x in ('13', '14', '15', '16', '17', '18', '19')]
week_8 = [f'{x}.10' for x in ('20', '21', '22', '23', '24', '25', '26')]
week_9 = ['27.10', '28.10', '29.10', '30.10', '31.10', '01.11', '02.11']

week_10 = [f'{x}.11' for x in ('03', '04', '05', '06', '07', '08', '09')]
week_11 = [f'{x}.11' for x in ('10', '11', '12', '13', '14', '15', '16')]
week_12 = [f'{x}.11' for x in ('17', '18', '19', '20', '21', '22', '23')]
week_13 = [f'{x}.11' for x in ('24', '25', '26', '27', '28', '29', '30')]
week_14 = [f'{x}.12' for x in ('01', '02', '03', '04', '05', '06', '07')]
week_15 = [f'{x}.12' for x in ('08', '09', '10', '11', '12', '13', '14')]
week_16 = [f'{x}.12' for x in ('15', '16', '17', '18', '19', '20', '21')]
week_17 = [f'{x}.11' for x in ('22', '23', '24', '25', '26', '27', '28')]

weeks = [week_1, week_2, week_3, week_4, week_5, week_6, week_7, week_8, week_9, week_10, week_11, week_12, week_13, week_13, week_14, week_15, week_16, week_17]

def which_week(date):
    if date in upper_week_days:
        return True
    if date in lower_week_days:
        return False

knt_1 =[]
knt_2 = [] 
knt_3 = [] 
knt_4 = [] 
knt_5 = []
knt_6 = []
knt_7 = []

# в списке расписания кнт
# [0] - пн, верхняя  [1] - пн, нижняя
# [2] - вт, верхняя  [3] - вт, нижняя
# [4] - ср, верхняя  [5] - ср, нижняя
# [6] - пт, верхняя  [7] - пт, нижняя
# а уже в этом списке - набор списков всех пар дня





#      ---------------------------- ТГ БОТ ---------------------------------

import asyncio

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()

temple_value = knt_1
pattern = re.compile(r"[0-9][0-9].[0-9][0-9]")
cancel = r"(?:[0-9][0-9].[0-9][0-9]. - отмена занятий)"
pat = r"(?:с [0-9][0-9].[0-9][0-9])"

async def get_weeks():
    while True:
        global knt_1, knt_2, knt_3, knt_4, knt_5, knt_6, knt_7
        # a, b, c, dd, e, f, g = knt_1, knt_2, knt_3, knt_4, knt_5, knt_6, knt_7
        knt_1 = get_week(['E', 'G'])
        knt_2 = get_week(['I', 'K'])
        knt_3 = get_week(['M', 'O'])
        knt_4 = get_week(['Q', 'S'])
        knt_5 = get_week(['U', 'W'])
        knt_6 = get_week(['Y', 'AA'])
        knt_7 = get_week(['AC', 'AE'])
        # if a != (knt_1 or b != knt_2 or c != knt_3 or dd != knt_4 or e != knt_5 or f != knt_6 or knt_7 != g) and a != []:
        #     await bot.send_message()
        print('============= списки найдены ===============')
        await asyncio.sleep(7200)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Здравствуйте!\n \nЭтот бот предназначен для просмотра расписания групп 25КНТ в ВШЭ 📅\n✏️ Чтобы узнать расписание — \n/schedule\nУзнать информацию о дисциплинах - \n/disciplines \nℹ️ Для справки используйте - /help", reply_markup=kb_start)

@dp.message(Command('schedule'))
async def schedule(message: Message):
    await message.answer("Выбери ниже необходимую группу ⬇️", reply_markup=keybord_inline)

@dp.message(Command('disciplines'))
async def schedule(message: Message):
    await message.answer("В этом разделы Вы можете узнать инфомацию о дисциплинах!\n \nВыберите интересующую Вас дисциплину ниже ⬇️", reply_markup=kb_disciplines)

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Если у Вас возникли вопросы, обращайтесь @lebsergei \nПо вопросам сотрудничества - @longerxo")

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
# ⏹️⏩⏪
keybord_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='КНТ-1', callback_data='knt-1'), InlineKeyboardButton(text='КНТ-2', callback_data='knt-2')],
    [InlineKeyboardButton(text='КНТ-3', callback_data='knt-3'), InlineKeyboardButton(text='КНТ-4', callback_data='knt-4')],
    [InlineKeyboardButton(text='КНТ-5', callback_data='knt-5'), InlineKeyboardButton(text='КНТ-6', callback_data='knt-6')],
    [InlineKeyboardButton(text='КНТ-7', callback_data='knt-7')]
])

kb_english = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расписание', url='https://docs.google.com/spreadsheets/d/1RB9AWtrYm6Y9m8NSy6On7Zk3byws8RonAGBqeneSxOo/edit?gid=23993546#gid=23993546')]
])


@dp.callback_query(F.data == 'knt-1')
async def knt__1(callback: CallbackQuery):
    global temple_value
    global knt_1
    temple_value = knt_1
    await callback.answer('выбрана группа КНТ-1')
    await callback.message.answer('Выбери нужные дни ниже:', reply_markup=keybord_reply)



@dp.callback_query(F.data == 'knt-2')
async def knt__2(callback: CallbackQuery):
    global temple_value
    global knt_2
    temple_value = knt_2
    await callback.answer('выбрана группа КНТ-2')
    await callback.message.answer('Выбери нужные дни ниже:', reply_markup=keybord_reply)

@dp.callback_query(F.data == 'knt-3')
async def knt__3(callback: CallbackQuery):
    global temple_value
    global knt_3
    temple_value = knt_3
    await callback.answer('выбрана группа КНТ-3')
    await callback.message.answer('Выбери нужные дни ниже:', reply_markup=keybord_reply)

@dp.callback_query(F.data == 'knt-4')
async def knt__4(callback: CallbackQuery):
    global temple_value
    global knt_4
    temple_value = knt_4
    await callback.answer('выбрана группа КНТ-4')
    await callback.message.answer('Выбери нужные дни ниже:', reply_markup=keybord_reply)

@dp.callback_query(F.data == 'knt-5')
async def knt__5(callback: CallbackQuery):
    global temple_value
    global knt_5
    temple_value = knt_5
    await callback.answer('выбрана группа КНТ-5')
    await callback.message.answer('Выбери нужные дни ниже:', reply_markup=keybord_reply)

@dp.callback_query(F.data == 'knt-6')
async def knt__6(callback: CallbackQuery):
    global temple_value
    global knt_6
    temple_value = knt_6
    await callback.answer('выбрана группа КНТ-6')
    await callback.message.answer('Выбери нужные дни ниже:', reply_markup=keybord_reply)

@dp.callback_query(F.data == 'knt-7')
async def knt__7(callback: CallbackQuery):
    global temple_value
    global knt_7
    temple_value = knt_7
    await callback.answer('выбрана группа КНТ-7')
    await callback.message.answer('Выбери нужные дни ниже:', reply_markup=keybord_reply)

def get_weekday(i):
    if i == 0:
        return 'Понедельник'
    elif i == 1:
        return 'Вторник'
    elif i == 2:
        return 'Среда'
    elif i == 3:
        return 'Четверг'
    elif i == 4:
        return 'Пятница'
    elif i == 5:
        return 'Суббота'
    elif i == 6:
        return 'Воскресенье'

def get_message(index, date_today, date):
    message = f'<b>🗓 {get_weekday(date.weekday())} - {date_today}</b>\n'
    for el in temple_value[index]:
        find = re.findall(cancel, el[6])
        find_2 = re.findall(pat, el[6])
        find_3 = re.findall(pattern, el[6])
        if len(find) > 0:
            if f'{find[0][0:2]}.{find[0][3:5]}' == date.strftime("%d.%m"):
                continue
            else:
                if el[5] == 'Л':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Львовская, 1В\n'
                if el[5] == 'БП':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Большая Печёрская, 25/12\n'
                if el[5] == 'Р' or el[5] == 'р':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Родионова, 136\n'
        elif len(find_2) == 0 and len(find_3) > 0:
            if date.strftime("%d.%m") in find_3:
                if el[5] == 'Л':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Львовская, 1В\n'
                if el[5] == 'БП':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Большая Печёрская, 25/12\n'
                if el[5] == 'Р' or el[5] == 'р':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Родионова, 136\n'
        elif len(find_2) > 0:
            if el[5] == 'Л':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Львовская, 1В\n'
            if el[5] == 'БП':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Большая Печёрская, 25/12\n'
            if el[5] == 'Р' or el[5] == 'р':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Родионова, 136\n'
        else:
            if el[5] == 'Л':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Львовская, 1В\n'
            if el[5] == 'БП':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Большая Печёрская, 25/12\n'
            if el[5] == 'Р' or el[5] == 'р':
                    message += f'\n<b>⏰ Время:</b> <u>{el[0]}</u>\n<b>Дисциплина:</b> {el[1]}\n<b>Тип занятия:</b> {el[2]}\n<b>Преподаватель:</b> {el[3]}\n<b>Аудитория:</b> {el[4]}\n<b>Здание:</b> Родионова, 136\n'
    if message == f'<b>🗓 {get_weekday(date.weekday())} - {date_today}</b>\n':
        message += '\nПар нет, можно отдохнуть! 💆'
    return message

@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == 'сегодня':
        
        date_today = datetime.today().strftime("%d.%m")
        date = datetime.today()

        if date_today in session_days:
            await message.answer(f'<b>🗓 {get_weekday(datetime.today().weekday())} - {date_today}</b>\n \nВ этот день у тебя сессия!\nУдачи!', parse_mode='HTML')
        elif date_today in weekend_days:
            await message.answer(f'<b>🗓 {get_weekday(datetime.today().weekday())} - {date_today}</b>\n \nВ этот день у тебя выходной', parse_mode='HTML')
        else:
            if datetime.today().weekday() == 3 or datetime.today().weekday() == 5:
                await message.answer(f'🗓 <b>{get_weekday(datetime.today().weekday())} - {date_today}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
            elif datetime.today().weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date), parse_mode='HTML')
            elif datetime.today().weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date), parse_mode='HTML')
            elif datetime.today().weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date), parse_mode='HTML')
            elif datetime.today().weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date), parse_mode='HTML')
            elif datetime.today().weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date), parse_mode='HTML')
            elif datetime.today().weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date), parse_mode='HTML')
            elif datetime.today().weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date), parse_mode='HTML')
            elif datetime.today().weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date), parse_mode='HTML')

    if msg == 'завтра':
        
        delta = timedelta(days=1)
        date_today = (datetime.today() + delta).strftime("%d.%m")
        date = datetime.today() + delta

        if date_today in session_days:
            await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя сессия!\nУдачи!', parse_mode='HTML')
        elif date_today in weekend_days:
            await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя выходной', parse_mode='HTML')
        else:
            if (datetime.today() + delta).weekday() == 3 or (datetime.today() + delta).weekday() == 5:
                await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date), parse_mode='HTML')

    if msg == 'послезавтра':

        delta = timedelta(days=2)
        date_today = (datetime.today() + delta).strftime("%d.%m")
        date = datetime.today() + delta

        if date_today in session_days:
            await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя сессия!\nУдачи!', parse_mode='HTML')
        elif date_today in weekend_days:
            await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя выходной', parse_mode='HTML')
        else:
            if (datetime.today() + delta).weekday() == 3 or (datetime.today() + delta).weekday() == 5:
                await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date), parse_mode='HTML')
            elif (datetime.today() + delta).weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date), parse_mode='HTML')
    

    # расписание по маске ДД.ММ
    if pattern.fullmatch(msg):
        
        date_today = msg
        date = datetime(year=2025, day=int(msg[0:2]), month=int(msg[-2:]))

        if date_today in session_days:
            await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя сессия!\nУдачи!', parse_mode='HTML')
        elif date_today in weekend_days:
            await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя выходной', parse_mode='HTML')
        else:
            if date.weekday() == 3 or date.weekday() == 5:
                await message.answer(f'🗓 <b>{get_weekday(date.weekday())} - {date_today}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
            elif date.weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date), parse_mode='HTML')
            elif date.weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date), parse_mode='HTML')
            elif date.weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date), parse_mode='HTML')
            elif date.weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date), parse_mode='HTML')
            elif date.weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date), parse_mode='HTML')
            elif date.weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date), parse_mode='HTML')
            elif date.weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date), parse_mode='HTML')
            elif date.weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date), parse_mode='HTML')

    if msg == 'текущая неделя':
        
        date_today = datetime.today().strftime("%d.%m")

        for week in weeks:
            if date_today in week:
                cnt = 0
                for day in week:
                    if day in session_days:
                        cnt += 1
                if cnt >= 5:
                    await message.answer(f'Указанная неделя - зачётная!\nУдачи! ☦️', parse_mode='HTML')
                if date_today in upper_week_days:
                    await message.answer(get_message(0, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(2, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(4, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                    await message.answer(get_message(6, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                elif date_today in lower_week_days:
                    await message.answer(get_message(1, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(3, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(5, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                    await message.answer(get_message(7, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')

    if msg == 'след. неделя ⏩':

        delta = timedelta(weeks=1)
        date_today = (datetime.today() + delta).strftime("%d.%m")

        for week in weeks:
            if date_today in week:
                cnt = 0
                for day in week:
                    if day in session_days:
                        cnt += 1
                if cnt >= 5:
                    await message.answer(f'Указанная неделя - зачётная!\nУдачи! ☦️', parse_mode='HTML')
                elif date_today in upper_week_days:
                    await message.answer(get_message(0, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(2, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(4, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                    await message.answer(get_message(6, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                elif date_today in lower_week_days:
                    await message.answer(get_message(1, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(3, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(5, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                    await message.answer(get_message(7, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
    if msg == '⏪ пред. неделя':

        delta = timedelta(weeks=1)
        date_today = (datetime.today() - delta).strftime("%d.%m")

        for week in weeks:
            if date_today in week:
                cnt = 0
                for day in week:
                    if day in session_days:
                        cnt += 1
                if cnt >= 5:
                    await message.answer(f'Указанная неделя - зачётная!\nУдачи! ☦️', parse_mode='HTML')
                elif date_today in upper_week_days:
                    await message.answer(get_message(0, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(2, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(4, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                    await message.answer(get_message(6, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                elif date_today in lower_week_days:
                    await message.answer(get_message(1, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(3, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))), parse_mode='HTML')
                    await message.answer(get_message(5, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')
                    await message.answer(get_message(7, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))), parse_mode='HTML')
                    await message.answer(f'🗓 <b>{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}</b>\n \nВ этот день у тебя Английский язык, расписание своей группы можешь узнать по ссылке ниже.', reply_markup=kb_english, parse_mode='HTML')

async def main():
    task2 = asyncio.create_task(get_weeks())
    task1 = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
