import os
import requests
import dotenv
import telebot

dotenv.load_dotenv()

# constants
API = "https://ergopad.io/api"
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(TELEGRAM_API_KEY)


@bot.message_handler(commands=["start", "hello"])
def greet(message):
    bot.reply_to(message, "Hey, How's it going?")


@bot.message_handler(commands=["price"])
def price(message):
    try:
        res = requests.get(f"{API}/asset/price/ergopad", verify=False)
        price = round(res.json()["price"], 4)
        bot.send_message(
            message.chat.id, f"$ERGOPAD trading at ${price} USD")
    except:
        bot.reply_to(message, "Sorry cannot get price data from ergopad api.")


bot.polling()
