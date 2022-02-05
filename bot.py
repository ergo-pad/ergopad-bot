import os
import requests
import dotenv
import telebot
import time
from telebot import types

dotenv.load_dotenv()

messages = {
    "hello": "Hey, How's it going?",
    "faq": """
You can read the FAQ <a href=\"https://ergopad.io/faq\">here</a> ❓
""",
    "report": """
Please be aware that we will never ask for private keys over DM.
Report any suspicious activity to an admin. If you need assistance, we are able to help by checking your public key.
Keep your private keys private and never share them with anyone 🚨
""",
    "refund": """
If your transaction stuck and you have to refund your Transaction, make sure to watch our tutorial on Youtube in which Marty explains how to make a Refund.

https://www.youtube.com/watch?v=OTcCNNCnS4Q
""",
    "socials": """
<b>Ergopad socials:</b>
→ <a href=\"https://ergopad.io\">Website</a>
→ <a href=\"https://github.com/ergo-pad/ergopad/blob/dev/docs/README.md\">Whitepaper</a>
→ <a href=\"https://twitter.com/ErgoPadOfficial\">Twitter</a>
→ <a href=\"https://github.com/ergo-pad\">Github</a>
→ <a href=\"https://discord.com/invite/E8cHp6ThuZ\">Discord</a>
""",
    "welcome": """
Hello and welcome to the Ergopad community! 🥳  ErgoPad is a project incubator offering token IDOs which provide funding for new projects within the Ergo ecosystem.
Ergopad will release its own native token through an IDO and users will be able to trade Ergo or SigUSD for these tokens and stake them through smart contracts.
<b>Ergopad socials:</b>
→ <a href="https://ergopad.io">Website</a>
→ <a href="https://github.com/ergo-pad/ergopad/blob/dev/docs/README.md">Whitepaper</a>
→ <a href="https://twitter.com/ErgoPadOfficial">Twitter</a>
→ <a href="https://github.com/ergo-pad">Github</a>
→ <a href="https://discord.com/invite/E8cHp6ThuZ">Discord</a>    
""",
    "bot_love": """
Welcome fellow bot 🥰 😍, I am not sure you belong here though... 👀 👀.
"""
}

# constants
API = "https://ergopad.io/api"
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(TELEGRAM_API_KEY)


last_welcome: types.Message = None
last_welcome_user_id: int = 0
last_welcome_time: int = 0


@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def on_user_joins(message):
    global last_welcome, last_welcome_user_id, last_welcome_time
    try:
        if message.json["new_chat_member"]["is_bot"]:
            bot.reply_to(message, messages["bot_love"])
            return

        markup = types.InlineKeyboardMarkup()
        verify = types.InlineKeyboardButton(
            text='Verify Human', callback_data='verify')
        markup.add(verify)
        msg = bot.reply_to(message, messages['welcome'],
                           parse_mode="html", disable_web_page_preview=True, reply_markup=markup)
        if last_welcome:
            bot.delete_message(last_welcome.chat.id, last_welcome.id)
        last_welcome = msg
        last_welcome_user_id = message.json["new_chat_member"]["id"]
        last_welcome_time = time.time()
    except:
        pass


@bot.callback_query_handler(func=None)
def welcome_callback(call: types.CallbackQuery):
    try:
        bot.delete_message(last_welcome.chat.id, last_welcome.id)
    except:
        pass
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False)


@bot.message_handler(commands=["start", "hello"])
def greet(message):
    bot.reply_to(message, messages["hello"])


@bot.message_handler(commands=["price"])
def price(message):
    try:
        res = requests.get(f"{API}/asset/price/ergopad", verify=False)
        price = round(res.json()["price"], 4)
        bot.send_message(
            message.chat.id, f"$ERGOPAD trading at ${price} USD")
    except:
        bot.reply_to(message, "Sorry cannot get price data from ergopad api.")


@bot.message_handler(commands=["faq"])
def faq(message):
    bot.send_message(
        message.chat.id, messages["faq"], parse_mode="html")


@bot.message_handler(commands=["report"])
def report(message):
    bot.send_message(
        message.chat.id, messages["report"], parse_mode="html")


@bot.message_handler(commands=["refund"])
def refund(message):
    bot.send_message(message.chat.id, messages["refund"])


@bot.message_handler(commands=["socials"])
def socials(message):
    bot.send_message(
        message.chat.id, messages["socials"], parse_mode="html", disable_web_page_preview=True)


def listener(messages):
    for m in messages:
        print(str(m))


bot.set_update_listener(listener)
bot.polling()
