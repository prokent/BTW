import telebot
import requests
import json

YOUR_BOT_TOKEN = '7112295260:AAFpQ1Cqo31Odq-69t54stivkoJ21eTJkug'
FLASK_SERVER_URL = 'https://kent12-64aba4c14b55.herokuapp.com/send-message'  # URL вашего Flask сервера

bot = telebot.TeleBot(YOUR_BOT_TOKEN)

chat_ids = {}
loading_message_ids = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"chat_id: {chat_id}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    # Сохранение chat_id
    if chat_id not in chat_ids:
        chat_ids[chat_id] = username

    data = {"username": username, "message": text, "chatid": chat_id}
    send_data_to_flask_server(data)
    print(f"chat_id:{chat_id}. Username:{username}. Message:{text}. Успех")

def send_data_to_flask_server(data):
    json_data = json.dumps(data, ensure_ascii=False)
    try:
        response = requests.post(FLASK_SERVER_URL, data=json_data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"ошибка  {e}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
