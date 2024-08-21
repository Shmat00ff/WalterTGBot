import asyncio
from datetime import datetime
import logging
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from New_bot import config
from bot_promts import program_promt, nutrition_promt
from database import ChatHistory, session
from collections import deque

client = openai.AsyncOpenAI(api_key=config.api)
bot = Bot(token=config.bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(text=f'Hello, {message.from_user.full_name}!'
                              f'\nYou are using a chatGPT. I am helpful sports nutrition specialist. '
                              f'Text me dishes that you eat today and theirs quantity in grams '
                              f'and I calculate the calorie content.')


@dp.message()
async def message_handler(message: types.Message):
    messages = program_promt

    user_message = ChatHistory(user_id=message.from_user.id, role='user', msg=message.text,
                               username=message.from_user.username, first_name=message.from_user.first_name,
                               last_interaction=datetime.now())
    session.add(user_message)
    session.commit()

    chat_history = session.query(ChatHistory).filter_by(user_id=message.from_user.id, role='user').all()

    for item in deque(chat_history, maxlen=4):
        if str(message.from_user.id) == str(item.user_id):
            messages.append({'role': item.role, 'content': item.msg})
            print(message.from_user.id, item.user_id)

    response = await client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    assistant_response = response.choices[0].message.content

    bot_message = ChatHistory(user_id=message.from_user.id, role='assistant', msg=assistant_response)
    session.add(bot_message)
    session.commit()

    await bot.send_message(message.chat.id, assistant_response)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
