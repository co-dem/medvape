from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = '5999439436:AAGcSDlI3gfEFkdk1HC9dfYwkW3CHLzvj7Y'
MANAGER_ID = 798330024

METRO_STATIONS = {'каменная горка': 'каменной горке', 'кунцевщина': 'кунцевщине', 'спортивная': 'спортивной', 'пушкинская': 'пушкинской', 'молодежная': 'молодежной',
                  'фрунзенская': 'фрунзенской', 'немига': 'немига', 'купаловская': 'купаловской', 'первомайская': 'первомайской', 'пролетарская': 'пролетарской', 
                  'тракторный завод': 'тракторном заводе', 'партизанская': 'партизанской', 'автозаводская': 'автозаводской', 'могилёвская': 'могилёвской',
                  
                  'малиновка': 'малиновке', 'петровщина': 'петровщине', 'михалово': 'михалово', 'грушевка' : 'грушевке', 'институт культуры': 'институте культуры', 
                  'площадь ленина': 'площади ленина', 'октяборская': 'октяборской', 'площадь победы': 'площади победы', 'площадь якуба коласа': 'площади якуба коласа', 
                  'академия наук': 'академии наук', 'парк челюскинцев': 'парке челюскинцева', 'московская': 'московской', 'восток': 'востоке', 'борисовский тракт': 'борисовском тракте', 'уручье': 'уручье', 
                  
                  'ковальская свобода': 'ковальскаой свободы', 'вокзальная': 'вокзальной', 'площядь франтишка богулевича': 'площяди франтишка богулевича', 'юбилейная площадь': 'юбилейной площади'}


MAIN_MENU = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('Оформить заказ💨')],
        [KeyboardButton('Посмотреть каталог📋'), KeyboardButton('Менеджер👷‍♂️')]
    ],
    resize_keyboard = True
)

ADMIN_PANEL = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton('Оформить заказ💨')],
        [KeyboardButton('Посмотреть каталог📋'), KeyboardButton('Менеджер👷‍♂️')],
        [KeyboardButton('Перезагрузить каталог🔄')]
    ],
    resize_keyboard = True
)

ACCEPT_MENU = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'отклонить', callback_data = 'reject'), InlineKeyboardButton(text = 'одобрить', callback_data='accept')]
    ]
) 

catalog = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = 'прайс лист', url = 'https://docs.google.com/spreadsheets/d/1Iq6nU3yDAA2r_X179tC5cKhL98syIRljY1XhLJalP38/edit?usp=sharing')]
    ]
)

def check_time(data):
    otime = data['ordertime'].replace(':', ' ').split()
    if len(otime) != 2:
        return False
    elif int(otime[0]) <= 23 and int(otime[0]) >= 8 and int(otime[1]) >= 0 and int(otime[1]) <= 60:
        return True
    else:
        return False