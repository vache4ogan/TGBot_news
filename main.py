from aiogram import Dispatcher, types, Bot
import logging
import asyncio
import requests
from bs4 import BeautifulSoup


token = 'TOKEN'

logging.basicConfig(level=logging.INFO)


bot = Bot(token=token)

dp = Dispatcher(bot)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
click_last = types.KeyboardButton(text='Последние новости')
keyboard.add(click_last)


hrefs = []


async def get_news(count, message: types.Message,  url = 'https://tass.ru/'):
    i = 0
    r = requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    news = soup.find_all('span', class_ = 'tass_pkg_title-xVUT1 tass_pkg_title--inline-9iqZC tass_pkg_title--font_weight_medium-5SS-v tass_pkg_title--variant_h3_default-lNWLU tass_pkg_title--color_tass-IRRCy')
    o = -1
    r1 = requests.get(url)
    soup1 = BeautifulSoup(r1.text, 'html.parser')
    news_href = soup1.find_all('a')


    for hr in news_href:
        o += 1
        if o < 3:
            continue
        elif o >= 3 and o <= 7:
            if hr['href'] == '/politika/19031377':
                o = o -1
                continue
            hrefs.append(hr['href'])
        else:
            break

    
    for new in news:
        if len(new.text.split()) <= 3:
            continue



        inl_keyboard = types.InlineKeyboardMarkup()
        adress = types.InlineKeyboardButton(text='Переход на страницу', callback_data='addres', url='https://tass.ru/' + str(hrefs[i]))
        inl_keyboard.add(adress)


        await message.answer(new.text, reply_markup=inl_keyboard)
        i += 1

        del inl_keyboard

        if i == count:
            break
            
    i = 0
    o = -1

    del hrefs[:]

                
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет, я бот, который отправляет последние новости, при нажатии на кнопку', reply_markup=keyboard)


@dp.message_handler()
async def message(message: types.Message):

    if message.text == 'Последние новости':
        await get_news(count=5, message=message)


async def main():
    await dp.start_polling()



if __name__ == '__main__':
    asyncio.run(main())
