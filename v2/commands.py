from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

async def set_bot_commands(bot: Bot):
    commands = [
            BotCommand(command = "/manager", description = "получить контакты манеджера"),
            BotCommand(command = "/order", description = "сделать новый заказ")
        ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())