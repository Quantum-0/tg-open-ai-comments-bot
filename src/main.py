import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from src import msg_storage, ai
from src.config import settings


bot = Bot(token=settings.tg_token.get_secret_value())
dp = Dispatcher()
bot_in_pause: bool = False


@dp.message(Command("clear_history"))
async def cmd_clear(message: Message):
    # await message.reply("История сообщений очищена")
    pass


@dp.message(Command("stop"))
async def cmd_reply(message: Message):
    if settings.tg_owner_id == message.from_user.id:
        global bot_in_pause
        bot_in_pause = True
        await message.reply("Ответы бота приостановлены")


@dp.message(Command("start"))
async def cmd_reply(message: Message):
    if settings.tg_owner_id == message.from_user.id:
        global bot_in_pause
        bot_in_pause = False
        await message.reply("Ответы бота включены")


@dp.message()
async def chat_handler(message: Message):
    global bot_in_pause
    if message.chat.id != settings.tg_chat_id:
        return
    msg_storage.save_message(message)
    if bot_in_pause:
        return
    if random.random() > settings.response_chance and not (
        message.reply_to_message and message.reply_to_message.from_user.id == message.bot.id
    ) and ("арбуз" not in message.text.lower() and me.username not in message.text):
        return
    post_bot_replying_to = msg_storage.get_message(message.message_thread_id)
    thread_history = msg_storage.get_thread(message)
    close_messages = msg_storage.get_neighbours(message)
    full_prompt = await ai.generate_prompt(message, post_bot_replying_to, thread_history, close_messages, message.bot.id)
    response_msg = await ai.get_response(full_prompt)
    response_msg = response_msg.strip()
    if not response_msg:
        return
    resp = await message.reply(text=response_msg)
    msg_storage.save_message(resp)



async def main():
    global me
    me = await bot.get_me()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())