import telebot
import requests
from YOUR_TOKEN import YOUR_BOT_TOKEN,FLASK_SERVER_URL

bot = telebot.TeleBot(YOUR_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Придумал: https://t.me/vladyslavbtw")
    bot.send_message(chat_id, "Создал: https://t.me/prokent676")

@bot.message_handler(commands=['help'])
def handle_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Пшёл вон!")

@bot.message_handler(commands=['id'])
def handle_id(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"chat_id: {chat_id}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    data = {"username": username, "message": text, "chatid": chat_id}
    send_data_to_flask_server(data)
    print(f"chat_id: {chat_id}. Username: {username}. Message: {text}. Успех")

def send_data_to_flask_server(data):
    try:
        response = requests.post(FLASK_SERVER_URL, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при отправке данных: {e}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
