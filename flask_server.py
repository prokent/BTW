from flask import Flask, request, jsonify
import telebot
import requests
import asyncio
from YOUR_TOKEN import YOUR_BOT_TOKEN

bot = telebot.TeleBot(YOUR_BOT_TOKEN)

app = Flask(__name__)

# Создаем словарь для хранения данных
stored_messages = []

@app.route('/send-message', methods=['POST'])
async def receive_message():
    try:
        data = request.get_json()
        print(f"Полученные данные для отправки сообщения: {data}")

        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if chat_id and text:
            await asyncio.to_thread(bot.send_message, chat_id, f"Дурак пишет: {text}")
            return jsonify({"status": "success"}), 200
        else:
            error_msg = "Invalid data provided: chat_id or text is missing"
            print(error_msg)
            return jsonify({"status": "error", "message": error_msg}), 400
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/save-message', methods=['POST'])
async def save_message():
    try:
        data = request.get_json()
        print(f"Полученные данные для сохранения сообщения: {data}")

        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if username and text and chat_id:
            # Сохраняем данные в словарь
            stored_messages.append({
                'username': username,
                'message': text,
                'chatid': chat_id
            })
            print(f"Сообщение сохранено: {stored_messages[-1]}")
            return jsonify({"status": "success", "message": "Message saved"}), 200
        else:
            error_msg = "Invalid data provided: username, text or chat_id is missing"
            print(error_msg)
            return jsonify({"status": "error", "message": error_msg}), 400
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/get-messages', methods=['GET'])
def get_messages():
    return jsonify(stored_messages), 200

def send_message_to_server(username, message, chat_id):
    url = "https://kent12-64aba4c14b55.herokuapp.com/save-message"
    data = {
        "username": username,
        "message": message,
        "chatid": chat_id
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Отправка сообщения: {data} на {url} с результатом: {response.status_code}, {response.text}")
        return response.status_code, response.text
    except Exception as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None, str(e)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    # Отправка данных на сервер
    status_code, response_text = send_message_to_server(username, text, chat_id)
    bot.send_message(chat_id, f"Ваше сообщение: {text} (отправлено на сервер с результатом: {status_code})")

if __name__ == '__main__':
    app.run(debug=True)
    bot.polling()
