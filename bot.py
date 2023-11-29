import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InputFile, URLInputFile, Message
from requests import ReadTimeout

import requests


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6180484344:AAGyBQJEtOZ1ZRU4GrRj08olO6oynDnAfD0")
# Диспетчер
dp = Dispatcher()






# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Available: \n/cats\n/dogs\n\n/meme")

def get_url(count:int):
    print("Выполняю запрос")
    try:
        resp = requests.get(f"http://shibe.online/api/shibes?count={count}&urls=true&httpsUrls=true", timeout=10)
        print(resp)

        a = resp.json()
        print(resp.json())
        print("Done")
        return a
    except ReadTimeout as e:
        print(f"АШИБКА {e}")

@dp.message(Command("dogs"))
async def cmd_dog(message: types.Message):

    number = 1
    try:
        number = int(message.text.split()[1])
    except (ValueError, IndexError):
        await message.answer('Если хочешь много псов вводи команду с цифрой /dogs 1-10')

    await message.answer(f'Количество псин {number}, не считая тебя')


    await message.answer(f"Щас будет псина")
    try:
        count = number
        URL = get_url(count)
        if count==1:
            url = str(URL[0])
            photo = URLInputFile(url=url)
            await bot.send_photo(chat_id=message.from_user.id, photo=photo)
        elif count>1 and count<11:
            a = 0
            while a<len(URL):
                url = str(URL[a])
                photo = URLInputFile(url=url)
                await bot.send_photo(chat_id=message.from_user.id, photo=photo)
                a+=1
        else:
            raise Exception
    except Exception as e:
        await message.answer(f"Не будет псины, потому шо ты сам псина \n{e}")


@dp.message(Command("cats"))
async def cmd_cat(message: types.Message):

    await message.answer(f"Щас покажу киску")
    try:
        url = "https://cataas.com/cat?position=centre"
        photo = URLInputFile(url=url)
        await bot.send_photo(chat_id=message.from_user.id, photo=photo)

    except Exception as e:
        await message.answer(f"Не будет киски, потому шо ты псина \n{e}")


@dp.message(Command("meme"))
async def cmd_meme(message: types.Message):

    await message.answer(f"Щас покажу MEM")
    try:
        url = "http://127.0.0.1:8000/memes"
        photo = URLInputFile(url=url)
        await bot.send_photo(chat_id=message.from_user.id, photo=photo)

    except Exception as e:
        await message.answer(f"Не будет МЕМА, потому шо ты сам сука МЕМ ходячий \n{e}")



@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    await message.answer(f"Щас загружу МЕМ")
    filename = f"{message.photo[-1].file_id}.jpg"
    try:
        await bot.download(
            message.photo[-1],
            destination=f"./{filename}"
        )
        await message.answer(f"Щас загружу МЕМ через API")

        url = 'http://127.0.0.1:8000/memes/upload'

        with open(filename, 'rb') as f:
            files = {'file': (filename, f)}
            response = requests.post(url, files=files)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            await message.reply('Файл успешно отправлен на удаленный сервер.')
        else:
            await message.reply('Произошла ошибка при отправке файла на удаленный сервер.')
        os.remove(filename)
    except Exception as e:
        await message.answer(f"Не будет МЕМА, потому шо ты сам сука МЕМ ходячий \n{e}")






# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())






