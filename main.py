import telegram.ext
from telegram.ext import CommandHandler
import requests
import json
import time
from tracker import get_prices


print('bot is starting...')
time.sleep(2)

# enter below your telegram bot token you find in the "botfather".
bot_token = '5829520085:AAGTk0Kp49fJ1_MA9LQhcs6s4-cRYwfY1KM'
updater = telegram.ext.Updater(token=bot_token, use_context=True)
print("API loaded correctly...") 

dispatcher = updater.dispatcher


# function responsible for take by API coin price you want to get to know.
def get_price(symbol):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        if "USD" in data:
            return data["USD"]
        else:
            return None
    else:
        return None

def start(update, context):
    chat_id = update.effective_chat.id
    message = ""

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"

    context.bot.send_message(chat_id=chat_id, text=message)


dispatcher.add_handler(CommandHandler("raport", start))
updater.start_polling()

# function that takes your message from telegram e.g if you write /eth function takes it and send it to the symbol.
def handle_message(update, context):
    if update.message:
        message = update.message.text
        if message.startswith("/"):
            symbol = message.split(" ")[0][1:].upper()
            price = get_price(symbol)
            if price:
                chat_id = update.message.chat_id
                context.bot.send_message(chat_id=chat_id, text=f"{symbol} ${price}")
                print(f"{symbol} ${price}")
                print(chat_id)
            else:
                chat_id = update.message.chat_id
                context.bot.send_message(chat_id=chat_id, text=f"Sorry, I couldn't find the coin you wrote, please write again correctly")
                print(chat_id)
        else:
            pass

# Add the error handler to the dispatcher
dp = updater.dispatcher

# main function.
# remember if bot at the start printing "Timed out, trying again..." please remove your bot from a telegram group. 
def main():
    dp.add_handler(telegram.ext.CommandHandler("start", start))
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


