from google.oauth2.service_account import Credentials
import gspread
import sqlite3
from datetime import date, time, timedelta, datetime


conn = sqlite3.connect("schedule.db")
cursor = conn.cursor()

scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1rsTLgy-7ZTEDXc_GZeOglTJyIbT80KszZzb2kXiGf88/edit?gid=739453176#gid=739453176").worksheet("1 курс")

def get_lesson(cell):
    lessons = ["Программирование C/C++", "Технологии программирования", "Дискретная математика",
               "Линейная алгебра и геометрия", "Основы российской государственности", "Математический анализ",
               "Безопасность жинедеятельности", 'НПС "Цифровая грамотность"', "История России",
               "Программирование на C++"]
    for l in lessons:
        if l in cell: return l
    return None

def get_teacher(cell):
    teachers = ["Климов А.", "Улитин И.Б.", "Касьянов Н.Ю.",
                "Малышев Д.С.", "Беспалов П.А.", "Константинова Т.Н.",
                "Чистякова С.А.", "Савина О.Н.", "Чистяков В.В.", "Городнова А.А.",
                "Кочеров С.Н.", "Пеплин Ф.С.", "Талецкий Д.С.", "Полонецкая Н.А.",
                "Марьевичев Н.", "Шапошников В.Е.", "Логвинова К.В.", "Лупанова Е.А.",
                "Косульников Д.Д."]
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
    cell = sheet.get_all_values(f'{start}:{end}')
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

                if "------------------" in disciplines:
                    upper_week_discipline, lower_week_discipline = disciplines.replace("\n", "").split("------------------")

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

                    data_up = [time, lesson_up, type_lesson_up, teacher_up, upper_week_auditories, upper_week_building]
                    data_low = [time, lesson_low, type_lesson_low, teacher_low, lower_week_auditories, lower_week_building]
                    
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

                    data_up = [time, lesson, type_lesson, teacher, upper_week_auditories, upper_week_building]
                    data_low = [time, lesson, type_lesson, teacher, lower_week_auditories, lower_week_building]
                    
                    if data_up[4] == '': data_up[4] = '-'
                    if data_low[4] == '': data_low[4] = '-'
                    if data_up[2] == None: data_up[2] = 'семинар'
                    if data_low[2] == None: data_low[2] = 'семинар'
                    # print(data_up, data_low)
                    day_pairs_up += [data_up]
                    day_pairs_low += [data_low]
            n += 1   
        i += 1

    return [day_pairs_up, day_pairs_low]

rows = ([12, 19], [21, 28], [30, 37], [48, 55])

def get_week(list):
    week_schedule = []
    for el in rows:
        week_schedule += get_day(f'{list[0]}{el[0]}', f'{list[1]}{el[1]}')
    return week_schedule

upper_week_days = ['01.09', '02.09', '03.09', '04.09', '05.09', '06.09', '15.09', '16.09', '17.09', '18.09', '19.09', '20.09', '29.09', '30.09', \
                   '01.10', '02.10', '03.10', '04.10', '13.10', '14.10', '15.10', '16.10', '17.10', '18.10']
lower_week_days = ['08.09', '09.09', '10.09', '11.09', '12.09', '13.09', '22.09', '23.09', '24.09', '25.09', '26.09', '27.09', '06.10', '07.10', \
                   '08.10', '09.10', '10.10', '11.10', '20.10', '21.10', '22.10', '23.10', '24.10']
weekend_days = ['07.09', '14.09', '21.09', '28.09', '05.10', '12.10', '19.10']
session_days = ['25.10', '26.10', '27.10', '28.10', '29.10', '30.10', '31.10']

week_1 = [f'{x}.09' for x in ('01', '02', '03', '04', '05', '06', '07')]
week_2 = [f'{x}.09' for x in ('08', '09', '10', '11', '12', '13', '14')]
week_3 = [f'{x}.09' for x in ('15', '16', '17', '18', '19', '20', '21')]
week_4 = [f'{x}.09' for x in ('22', '23', '24', '25', '26', '27', '28')]
week_5 = ['29.09', '30.09',  '01.10', '02.10', '03.10', '04.10', '05.10']
week_6 = [f'{x}.10' for x in ('06', '07', '08', '09', '10', '11', '12')]
week_7 = [f'{x}.10' for x in ('13', '14', '15', '16', '17', '18', '19')]
week_8 = [f'{x}.10' for x in ('20', '21', '22', '23', '24', '25', '26')]
week_9 = ['27.10', '28.10', '29.10', '30.10', '31.10', '01.11', '02.11']


def which_week(date):
    if date in upper_week_days:
        return True
    if date in lower_week_days:
        return False

knt_1 = get_week(['E', 'G'])
knt_2 = get_week(['I', 'K'])
knt_3 = get_week(['M', 'O'])
knt_4 = get_week(['Q', 'S'])
knt_5 = get_week(['U', 'W'])
knt_6 = get_week(['Y', 'AA'])
knt_7 = get_week(['AC', 'AE'])

# когда выведется это сообщение - бот полностью работает

print('============================= списки найдены =============================')

# в списке расписания кнт
# [0] - пн, верхняя  [1] - пн, нижняя
# [2] - вт, верхняя  [3] - вт, нижняя
# [4] - ср, верхняя  [5] - ср, нижняя
# [6] - пт, верхняя  [7] - пт, нижняя
# а уже в этом списке - набор списков всех пар дня





#      ---------------------------- ТГ БОТ ---------------------------------

import re 
import asyncio

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

bot = Bot(token='8406562267:AAFDp-EKv2UosY6r-GH7ugbGy8L8qHJAFlA')
dp = Dispatcher()

temple_value = knt_1
pattern = re.compile(r"[0-9][0-9].[0-9][0-9]")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, первокурсник! \nЗдесь ты можешь узнать расписание на направление Компьютерные науки и технологии!\n \nВыбери ниже Вашу группу  ", reply_markup=keybord_inline)

keybord_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сегодня'), KeyboardButton(text='Завтра')],
    [KeyboardButton(text='Послезавтра'), KeyboardButton(text='Текущая неделя')],
    [KeyboardButton(text='Следующая неделя')]
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
    message = f'{get_weekday(date.weekday())} - {date_today}\n'
    for el in temple_value[index]:
        message += f'\nВремя: {el[0]}\nДисциплина: {el[1]}\nТип занятия: {el[2]}\nПреподаватель: {el[3]}\nАудитория: {el[4]}\nЗдание: {el[5]}\n'
    return message

@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == 'сегодня':
        
        date_today = datetime.today().strftime("%d.%m")
        date = datetime.today()

        if date_today in session_days:
            await message.answer(f'{get_weekday(datetime.today().weekday())} - {date_today}\n \nВ этот день у тебя сессия!\nУдачи!')
        elif date_today in weekend_days:
            await message.answer(f'{get_weekday(datetime.today().weekday())} - {date_today}\n \nВ этот день у тебя выходной')
        else:
            if datetime.today().weekday() == 3 or datetime.today().weekday() == 5:
                await message.answer(f'{get_weekday(datetime.today().weekday())} - {date_today}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
            elif datetime.today().weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date))
            elif datetime.today().weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date))
            elif datetime.today().weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date))
            elif datetime.today().weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date))
            elif datetime.today().weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date))
            elif datetime.today().weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date))
            elif datetime.today().weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date))
            elif datetime.today().weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date))

    if msg == 'завтра':
        
        delta = timedelta(days=1)
        date_today = (datetime.today() + delta).strftime("%d.%m")
        date = datetime.today() + delta

        if date_today in session_days:
            await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя сессия!\nУдачи!')
        elif date_today in weekend_days:
            await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя выходной')
        else:
            if (datetime.today() + delta).weekday() == 3 or (datetime.today() + delta).weekday() == 5:
                await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
            elif (datetime.today() + delta).weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date))
            elif (datetime.today() + delta).weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date))
            elif (datetime.today() + delta).weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date))
            elif (datetime.today() + delta).weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date))
            elif (datetime.today() + delta).weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date))
            elif (datetime.today() + delta).weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date))
            elif (datetime.today() + delta).weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date))
            elif (datetime.today() + delta).weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date))

    if msg == 'послезавтра':

        delta = timedelta(days=2)
        date_today = (datetime.today() + delta).strftime("%d.%m")
        date = datetime.today() + delta

        if date_today in session_days:
            await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя сессия!\nУдачи!')
        elif date_today in weekend_days:
            await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя выходной')
        else:
            if (datetime.today() + delta).weekday() == 3 or (datetime.today() + delta).weekday() == 5:
                await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
            elif (datetime.today() + delta).weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date))
            elif (datetime.today() + delta).weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date))
            elif (datetime.today() + delta).weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date))
            elif (datetime.today() + delta).weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date))
            elif (datetime.today() + delta).weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date))
            elif (datetime.today() + delta).weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date))
            elif (datetime.today() + delta).weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date))
            elif (datetime.today() + delta).weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date))
    

    # расписание по маске ДД.ММ
    if pattern.fullmatch(msg):
        
        date_today = msg
        date = datetime(year=2025, day=int(msg[0:2]), month=int(msg[-2:]))

        if date_today in session_days:
            await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя сессия!\nУдачи!')
        elif date_today in weekend_days:
            await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя выходной')
        else:
            if date.weekday() == 3 or date.weekday() == 5:
                await message.answer(f'{get_weekday(date.weekday())} - {date_today}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
            elif date.weekday() == 0 and date_today in upper_week_days:
                await message.answer(get_message(0,date_today, date))
            elif date.weekday() == 0 and date_today in lower_week_days:
                await message.answer(get_message(1,date_today, date))
            elif date.weekday() == 1 and date_today in upper_week_days:
                await message.answer(get_message(2,date_today, date))
            elif date.weekday() == 1 and date_today in lower_week_days:
                await message.answer(get_message(3,date_today, date))
            elif date.weekday() == 2 and date_today in upper_week_days:
                await message.answer(get_message(4,date_today, date))
            elif date.weekday() == 2 and date_today in lower_week_days:
                await message.answer(get_message(5,date_today, date))
            elif date.weekday() == 4 and date_today in upper_week_days:
                await message.answer(get_message(6,date_today, date))
            elif date.weekday() == 4 and date_today in lower_week_days:
                await message.answer(get_message(7,date_today, date))

    if msg == 'текущая неделя':
        
        date_today = datetime.today().strftime("%d.%m")

        for week in (week_1, week_2, week_3, week_4, week_5, week_6, week_7, week_8, week_9):
            if date_today in week:
                if date_today in upper_week_days:
                    await message.answer(get_message(0, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))))
                    await message.answer(get_message(2, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))))
                    await message.answer(get_message(4, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
                    await message.answer(get_message(6, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
                elif date_today in lower_week_days:
                    await message.answer(get_message(1, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))))
                    await message.answer(get_message(3, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))))
                    await message.answer(get_message(5, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
                    await message.answer(get_message(7, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)

    if msg == 'следующая неделя':

        delta = timedelta(weeks=1)
        date_today = (datetime.today() + delta).strftime("%d.%m")

        for week in (week_1, week_2, week_3, week_4, week_5, week_6, week_7, week_8, week_9):
            if date_today in week:
                if date_today in upper_week_days:
                    await message.answer(get_message(0, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))))
                    await message.answer(get_message(2, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))))
                    await message.answer(get_message(4, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
                    await message.answer(get_message(6, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
                elif date_today in lower_week_days:
                    await message.answer(get_message(1, week[0], datetime(year=2025, day=int(week[0][0:2]), month=int(week[0][-2:]))))
                    await message.answer(get_message(3, week[1], datetime(year=2025, day=int(week[1][0:2]), month=int(week[1][-2:]))))
                    await message.answer(get_message(5, week[2], datetime(year=2025, day=int(week[2][0:2]), month=int(week[2][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[3][0:2]), month=int(week[3][-2:])).weekday())} - {week[3]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)
                    await message.answer(get_message(7, week[4], datetime(year=2025, day=int(week[4][0:2]), month=int(week[4][-2:]))))
                    await message.answer(f'{get_weekday(datetime(year=2025, day=int(week[5][0:2]), month=int(week[5][-2:])).weekday())} - {week[5]}\n \nВ этот день у тебя Английский язык, расписание свое группы можешь узнать по ссылке ниже.', reply_markup=kb_english)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
