# -1001578820122 барахолка минск
#* program to send messages to the supergroups *#

from telethon.sync import TelegramClient
from telethon import TelegramClient
from telethon.errors import SlowModeWaitError
from config import TOKEN, api_id, api_hash

print('loading...')

client = TelegramClient('anon', api_id, api_hash)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=TOKEN)

async def add1():
    with open('others\\visit_card\\final\\types\\back2.jpg', 'rb') as file:                #! insert path of the necessary file
        await client.send_file(-1001588344829, file = file, caption = 'photo description1') #! write necessary text and id here

async def add2():
    with open('others\\visit_card\\final\\types\\back2.jpg', 'rb') as file:                #! insert path of the necessary file
        await client.send_file(-1001588344829, file = file, caption = 'photo description2') #! write necessary text and id here
    
async def add3():
    with open('others\\visit_card\\final\\types\\back2.jpg', 'rb') as file:                #! insert path of the necessary file
        await client.send_file(-1001588344829, file = file, caption = 'photo description3') #! write necessary text and id here

add_choose = input('введи номер рекламы(1 - 3): ')

try:
    with client:
        if add_choose == '1':
                client.loop.run_until_complete(add1())
        elif add_choose == '2':
                client.loop.run_until_complete(add2())
        elif add_choose == '3':
                client.loop.run_until_complete(add3())
except SlowModeWaitError:
    print('ограничение рассылки сообщений: 1 час')