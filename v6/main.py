# medvape bot - bot for vapeshop #
import schedule
import datetime

from aiogram.utils import executor
from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from commands import set_bot_commands
from config import TOKEN, MAIN_MENU, METRO_STATIONS, MANAGER_ID, catalog,\
                   ADMIN_PANEL, check_time, DEVELOPERID, DEVELOPER_PANEL, clear_stats_mrk
from db import update_database, check_product, changestats, upload_products, showstats, clear_stats

from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

#$ new feature: bot can show selling stats
#TODO: make bot to write all stat info to the svg/excel file and clear it at the end of the month

now = datetime.datetime.now()           #* datetime object
orders = []                             #* variable to store orders (for developer only)
dt = {}                                 #* dt and           are created to make oder process exactlyer
user_data = {}                          #*        user_data
storage = MemoryStorage()               #* memory object
bot = Bot(TOKEN)                        #* bot object
dp = Dispatcher(bot, storage = storage) #* Dispatcher object

class LOrder(StatesGroup):   
    orderplace = State()
    ordertime = State()
    product = State()
    moderation = State()


#* function to create an account for user
# userid | username | orderplace | ordertime | product
def login_func(user) -> None:
    global user_data

    # if user doesn't exist, add him 
    if user_data.get(user.from_user.username) == None:

        user_data[user.from_user.username] = user.from_user.username 
        user_data[user.from_user.username] = {
            'id'        : user.from_id,
            'username'  : user.from_user.username,
            'orderplace': None,   #* place where customer is gonna buy product
            'ordertime' : None,   #* time when customer is gonna buy product
            'product'   : None    #* product that user ordered
        }
        #* if user already exists, setall data to none
    else:
        user_data[user.from_user.username]['orderplace'] = None
        user_data[user.from_user.username]['ordertime']  = None
        user_data[user.from_user.username]['product'] = None

#* starting function
'''
here we set the access level for user:
basic user | manager | developer

and creating an account for user
'''
@dp.message_handler(commands = ['start', 'order'])
async def welcome(message: types.Message):
    
    await set_bot_commands(bot = bot)   # setting hot commands
    login_func(user = message)          # creating an account
    upload_products()                   # uploading products for stats

    print('[log]: new user ->', user_data)

    #* developer access level
    if message.text == '/start' and message.from_id == 798330024:
        await bot.send_message(message.from_id, f'Привет {message.from_user.username}!❤️\nЯ бот, который сделает процесс оформления заказа приятным\nуровень доступа: developer', reply_markup = DEVELOPER_PANEL)
    #* manager access level
    elif message.text == '/start' and message.from_user.id == MANAGER_ID:
        await bot.send_message(message.from_id, f'Привет {message.from_user.username}!❤️\nЯ бот, который сделает процесс оформления заказа приятным\nуровень доступа: manager', reply_markup = ADMIN_PANEL)
    #* basic user access level
    elif message.text == '/start' and message.from_user.id != MANAGER_ID:
        await bot.send_message(message.from_id, f'Привет {message.from_user.username}!❤️\nЯ бот, который сделает процесс оформления заказа приятным', reply_markup = MAIN_MENU)

    # same
    elif message.text == '/order' and message.from_id == 798330024:
        await bot.send_message(message.from_id, 'Я перевёл вас в главное меню', reply_markup = DEVELOPER_PANEL)    
    
    elif message.text == '/order' and message.from_id == MANAGER_ID:
        await bot.send_message(message.from_id, 'Я перевёл вас в главное меню', reply_markup = ADMIN_PANEL)    
    elif message.text == '/order' and message.from_id != MANAGER_ID:
        await bot.send_message(message.from_id, 'Я перевёл вас в главное меню', reply_markup = MAIN_MENU)    
    login_func(user = message)


@dp.message_handler(content_types = 'text')
async def msg_handler_func(message: types.Message):
    global orders
    
    #* ----- commands for all users
    #* starts an ordering process
    if message.text.lower() == 'оформить заказ💨':
        print('order started')
        await bot.send_message(message.from_id, 'Вам нужно будет указать\n1️⃣ место\n2️⃣ время\n3️⃣ товар который вы хотите купить', reply_markup = ReplyKeyboardRemove())
        await bot.send_message(message.from_id, 'Сначала укажите станцию метро или адрес\n🔴для доставки до дома вам нужно будет доплатить 5byn🔴')
        # last check for having an account
        login_func(user = message)
        await LOrder.orderplace.set()


    #* sends a list of avilable products
    elif message.text.lower() == 'посмотреть каталог📋':
        print('btn1')
        await bot.send_message(message.from_id, 'Список товаров📋', reply_markup = catalog)
        await bot.send_message(message.from_id, 'Вы также можете узнать о новинках подписавшись на наш телеграм <a href="https://t.me/medyvape">канал</a>', parse_mode = 'HTML')

    #* sends managers username  
    elif message.text.lower() == 'менеджер👷‍♂️':
        print('btn2')
        await bot.send_message(message.from_id, f'Это телеграм нашего <a href = "https://t.me/MinskoeOpg1">👷‍♂️менеджера👷‍♂️</a>', parse_mode = 'HTML')

    elif message.text.lower() == '⭐️оставить отзыв⭐️':
        await bot.send_message(message.from_id, 'Написать своё мнение о боте вы можете его 🧑‍💻<a href="https://t.me/c0dem">создателю</a>🧑‍💻\n', parse_mode = 'HTML')


    #* ----- manager commands 
    elif message.text.lower() == 'перезагрузить каталог🔄' and message.from_id == (MANAGER_ID or DEVELOPERID):
        print('[log]: updating catalog')
        try:
            update_database()
            await bot.send_message(message.from_user.id, 'готово')
            print('success')
        except Exception as e:
            await bot.send_message(message.from_user.id, 'ошибка в обновлении данных\nперед тем как пытаться решить проблему самому обратитесь <a href = "https://t.me/c0dem">создателю бота</a>', parse_mode = 'HTML')
            print('ошибка в обновлении базы данных: ', e)

    elif message.text.lower() == '📊показать статистику📊' and message.from_id == (MANAGER_ID or DEVELOPERID):
        stat_string = ''
        for i in showstats().items():
            stat_string += f'{i[0]}: {i[1]}\n'
        await bot.send_message(message.from_id, stat_string, reply_markup = clear_stats_mrk)

    #* ----- developer commands
    elif message.from_id == 798330024 and message.text == '🚫выключить бота🚫':
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id)
        quit()

    
    elif message.from_id == 798330024 and message.text == 'очистить заказы':
        await bot.send_message(DEVELOPERID, orders)
        orders = []
        print(f'[log]: orders cleared successfully | orders list --> {orders}')

    elif message.text.lower() == '🧹очистить статистику🧹' and message.from_user.id == (DEVELOPERID or MANAGER_ID):
        print(clear_stats())
        await bot.send_message(message.from_id, "статистика очищена")

    elif message.from_id == DEVELOPERID or MANAGER_ID and message.text.lower() == '◀️назад':
        if message.from_id == DEVELOPERID:
            await bot.send_message(message.from_id, 'перевожу вас в главное меню', reply_markup = DEVELOPER_PANEL)
        elif message.from_id == MANAGER_ID:
            await bot.send_message(message.from_id, 'перевожу вас в главное меню', reply_markup = ADMIN_PANEL)

    else:
        await bot.send_message(message.from_id, '‼️выберите один из вариантов в меню‼️')


#! -------- FSM -------- !#  
@dp.message_handler(state = LOrder.orderplace)
async def setting_order_place(message: types.Message, state: FSMContext):
    global user_data
    
    await state.update_data(orderplace = message.text)
    data = await state.get_data()

    print('[log - orderplace]:', user_data)

    user_data[message.from_user.username]['orderplace'] = data['orderplace']

    await bot.send_message(message.from_id, '✅отлично, теперь выберите время, пример 14:00', reply_markup = ReplyKeyboardRemove())
    await LOrder.next()

@dp.message_handler(state = LOrder.ordertime)
async def setting_order_time(message: types.Message, state: FSMContext):
    await state.update_data(ordertime = message.text)
    data = await state.get_data()

    user_data[message.from_user.username]['ordertime'] = data['ordertime']

    print('[log - ordertime]:', user_data)

    #* cheking for entering the time correctly
    if check_time(data) == True:
        print('passing the time check: ', check_time(data))
        await bot.send_message(message.from_id, '✅отлично, теперь выберите товар.\nпример: банан, клубника, лёд')
        await bot.send_message(message.from_id, 'каталог ниже', reply_markup = catalog)
        
        await LOrder.next()
    else:
        await bot.send_message(message.from_id, '‼️введите время по примеру‼️\nПример: 14:00')
        await LOrder.ordertime.set()

@dp.message_handler(state = LOrder.product)
async def setting_taste_func(message: types.Message, state: FSMContext):
    global data, dt, orders

    await state.update_data(product = message.text.strip())
    await state.update_data(username = message.from_user.username)
    data = await state.get_data()

    #* cheking if product that user choosed is available
    available_product = check_product(data['product'].lower()) == True

    print('passing product check: ', available_product)

    if available_product == True:
        dt = data
        user_data[message.from_user.username]['product'] = data['product']

        changestats(data['product'])

        print('[log - orderproduct]:', user_data)

        #* creating inline menu with username
        ACCEPT_MENU = InlineKeyboardMarkup(
            inline_keyboard = [
                [InlineKeyboardButton(text = f'отклонить {user_data[message.from_user.username]["username"]}', callback_data = f'reject'), 
                InlineKeyboardButton(text = f'одобрить {user_data[message.from_user.username]["username"]}', callback_data = f'accept')]
            ]
        ) 

        #* sending all info that user sended to the manager 
        await bot.send_message(message.from_id, '📤отлично, я отправил ваш заказ на модерацию📤\nожидайт, в течении 5 минут, вам придёт сообщение')
        await bot.send_message(MANAGER_ID, f'@{message.from_user.username}\n\
product: {user_data[message.from_user.username]["product"]}\n\
time: {user_data[message.from_user.username]["ordertime"]}\n\
place: {user_data[message.from_user.username]["orderplace"]}📥', reply_markup = ACCEPT_MENU)
        
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, '‼️выберите товар из списка‼️')
        await LOrder.product.set()


@dp.callback_query_handler()
async def moderation_func(call: types.CallbackQuery):
    global orders

    print(user_data)

    if call.data == 'reject':
        for name in user_data:
            if name in call.message.text:
                print(name)
                await bot.send_message(user_data[name]['id'], '❌ваш заказ отоклонён❌\nпо вопросам обращяйтесь к \n<a href = "https://t.me/MinskoeOpg1">👷‍♂️менеджеру👷‍♂️</a>', parse_mode = 'HTML')
                await bot.send_message(user_data[name]['id'], '🔄если хотите оформить ещё заказ, то вам нужно использывать эту комманду: /order')                                                                                                                                                                

    elif call.data == 'accept':
        orders.append(user_data[data["username"]]["product"])
        print(orders)

        for name in user_data:
            if name in call.message.text:
                metrostation = METRO_STATIONS.get(user_data[dt["username"]]["orderplace"].lower())
                if metrostation == None:
                    await bot.send_message(user_data[name]['id'], f'✨ваш заказ одобрен и уже в доставке✨\nв {user_data[dt["username"]]["ordertime"]} вам нужно будет быть на {user_data[dt["username"]]["orderplace"].lower()}\nтам вас будет ждать курьер с {user_data[data["username"]]["product"]}\n\nесли вам есть что добавить, обращяйтесь к <a href = "https://t.me/MinskoeOpg1">👷‍♂️менеджеру👷‍♂️</a>', parse_mode = 'HTML')
                elif metrostation != None:
                    await bot.send_message(user_data[name]['id'], f'✨ваш заказ одобрен и уже в доставке✨\nв {user_data[dt["username"]]["ordertime"]} вам нужно будет быть на {METRO_STATIONS[user_data[dt["username"]]["orderplace"].lower()]}\nтам вас будет ждать курьер с {user_data[data["username"]]["product"]}\n\nесли вам есть что добавить, обращяйтесь к <a href = "https://t.me/MinskoeOpg1">👷‍♂️менеджеру👷‍♂️</a>', parse_mode = 'HTML')

                await bot.send_message(user_data[name]['id'], '🔄если хотите оформить ещё заказ, то вам нужно использывать эту комманду: /order')                                                                                                                                                                

if __name__ == '__main__':
    executor.start_polling(dp)
#| coded by codem