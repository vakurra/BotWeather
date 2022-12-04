import requests
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города, где узнать погоду)")

@dp.message_handler()
async def get_weather(message: types.Message):
    global emoji
    check_emoji = {
    "01d": "\U00002600", "01n": "\U0001F319",
    "02d": "\U0001F324", "02n": "\U0001F324",
    "03d": "\U000026C5", "03n": "\U000026C5",
    "04d": "\U00002601", "04n": "\U00002601",
    "09d": "\U0001F327", "09n": "\U0001F327",
    "10d": "\U0001F326", "10n": "\U0001F326",
    "11d": "\U000026C8", "11n": "\U000026C8",
    "13d": "\U00002744", "13n": "\U00002744",
    "50d": "\U0001F32B", "50n": "\U0001F32B",
    }

    try:
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
        )
        data = req.json()

        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = int(data["main"]["pressure"] * 0.75006375541921)
        wind_speed = data["wind"]["speed"]
        weather = data["weather"][0]["description"]
        type_emoji = data["weather"][0]["icon"]
        if type_emoji in check_emoji:
            emoji = check_emoji[type_emoji]

        await message.reply(
            f"Погода в городе '{city}' сейчас:\nТемпература: {cur_temp}°C\n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind_speed} м/с\n"
            f"За окном {weather}.{emoji}\n"
            f"*****Удачи тебе!*****"
        )

    except:
        await message.reply("Проверь правильность написания города.")

if __name__ == '__main__':
    executor.start_polling(dp)