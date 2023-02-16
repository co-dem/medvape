# medvape bot - bot for vapeshop #
from aiogram.utils import executor
from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import Text

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from config import TOKEN, MAIN_MENU, METRO_STATIONS, MANAGER_ID, chek_time, ACCEPT_MENU


user_data = {}
dt = {}
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = storage)

#TODO: сделать проверку наличия жижи

class LOrder(StatesGroup):
    orderplace = State()
    ordertime = State()
    product = State()
    moderation = State()

@dp.message_handler(commands = ['start', 'order'])
async def welcome(message: types.Message):
    global user_data
    if user_data.get(message.from_user.username) == None:

        user_data[message.from_user.username] = message.from_user.username 
        user_data[message.from_user.username] = {
            'id'        : message.from_id,
            'orderplace': None,   #* place where customer is gonna buy product
            'ordertime' : None,   #* time when customer is gonna buy product
            'product'   : None    #* product that user ordered

        }
    else:
        user_data[message.from_user.username]['orderplace'] = None
        user_data[message.from_user.username]['ordertime']  = None
        user_data[message.from_user.username]['product'] = None


    print('[log]: user ->', user_data)

    if message.text == '/start':
        await bot.send_message(message.from_id, f'Привет {message.from_user.username}!\nЯ бот для medvape и это приветственный текст')
    
    await bot.send_message(message.from_id, 'я перевёл вас в главное меню', reply_markup = MAIN_MENU)    

@dp.message_handler(content_types = 'text')
async def msg_handler_func(message: types.Message):
    #* starts an ordering process
    if message.text.lower() == 'оформить заказ':
        print('order started')
        await bot.send_message(message.from_id, 'вам нужно будет указать\n1 место\n2 время\n3 товар который вы хотите купить')
        await bot.send_message(message.from_id, 'сначала укажите станцию метро или адрес\n(для доставки до дома вам нужно будет доплатить 5byn)')
        await LOrder.orderplace.set()


    #* sends a list of avilable products
    elif message.text.lower() == 'посмотреть каталог':
        print('btn1')
        await bot.send_message(message.from_id, 'вот список доступрого товаар\n...\n...\n...')
        await bot.send_message(message.from_id, 'вы также можете узнать о новинках подписавшись на нащ телеграм <a href="https://t.me/medyvape">канал</a>', parse_mode = 'HTML')

    #* sends managers username  
    elif message.text.lower() == 'менеджер':
        print('btn2')
        await bot.send_message(message.from_id, f'это телеграм аккаунт нашего иенеджера -> @MinskoeOpg1')

    else:
        await bot.send_message(message.from_id, 'выберите один из вариантов в меню')

#! ----- FSM MACHINE ----- !# 

@dp.message_handler(state = LOrder.orderplace)
async def setting_order_place(message: types.Message, state: FSMContext):
    global user_data
    
    await state.update_data(orderplace = message.text)
    data = await state.get_data()

    print('[log - orderplace]:', user_data)

    if data['orderplace'].lower() in METRO_STATIONS:
        user_data[message.from_user.username]['orderplace'] = data['orderplace']

        await bot.send_message(message.from_id, 'отлично, теперь выберите время')
        await LOrder.next()

    else:
        await bot.send_message(message.from_id, 'введите станцию метро на которой вы хотите вмтретиться по примеру.\nПример: Купаловская')
        await LOrder.orderplace.set()

@dp.message_handler(state = LOrder.ordertime)
async def setting_order_time(message: types.Message, state: FSMContext):
    await state.update_data(ordertime = message.text)
    data = await state.get_data()

    user_data[message.from_user.username]['ordertime'] = data['ordertime']

    print('[log - ordertime]:', user_data)

    try:
        if chek_time(data) == True:
            await bot.send_message(message.from_id, 'отлично, теперь выберите товар')
            await bot.send_message(message.from_id, 'каталог:\n...\n...\n...')
            
            await LOrder.next()
        else:
            await bot.send_message(message.from_id, 'введите время по примеру.\nПример: 14:00')
        print(chek_time(data))
        
    except Exception as e:
        await bot.send_message(message.from_id, 'произошла ошибка, повторите попытку позже')
        data = f'error: user_id - {data["userid"]}\n        username: {data["username"]}'
        await state.finish()


@dp.message_handler(state = LOrder.product)
async def setting_taste_func(message: types.Message, state: FSMContext):
    global data, dt

    await state.update_data(product = message.text)
    await state.update_data(username = message.from_user.username)
    data = await state.get_data()
    dt = data
    user_data[message.from_user.username]['product'] = data['product']

    print('[log - orderproduct]:', user_data)

    await bot.send_message(message.from_id, 'отлично, я отправил ваш заказ на модерацию')
    await bot.send_message(MANAGER_ID, f'username: @{message.from_user.username}\n\
    product: {user_data[message.from_user.username]["product"]}\n\
    time: {user_data[message.from_user.username]["ordertime"]}\n\
    place: {user_data[message.from_user.username]["orderplace"]}', reply_markup = ACCEPT_MENU)  
    
    await state.finish()

@dp.callback_query_handler(Text(['reject', 'accept']))
async def moderation_func(call: types.CallbackQuery):
        print(user_data)

        if call.data == 'reject':
            await bot.send_message(user_data[dt['username']]['id'], 'ваш заказ отоклонён')

        elif call.data == 'accept':
            await bot.send_message(user_data[dt['username']]['id'], 'ваш заказ одобрен и уже в доставке')
            await bot.send_message(user_data[dt['username']]['id'], f'в {user_data[dt["username"]]["ordertime"]} вам нужно будет быть на {METRO_STATIONS[user_data[dt["username"]]["orderplace"].lower()]}\nтам вас будет ждать курьер с {user_data[data["username"]]["product"]}')
            await bot.send_message(user_data[dt['username']]['id'], 'если хотите оформить ещё заказ, то вам нужно нажать на эту комманду -> /order')                                                                                                                                                                

executor.start_polling(dp)