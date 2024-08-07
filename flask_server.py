from flask import Flask, request, jsonify
import telebot
import asyncio
from YOUR_TOKEN import YOUR_BOT_TOKEN

bot = telebot.TeleBot(YOUR_BOT_TOKEN)
app = Flask(__name__)

# Создаем список для хранения сообщений
stored_messages = []

@app.route('/send-message', methods=['POST'])
async def receive_message():
    try:
        data = request.get_json()
        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if chat_id and text:
            # Отправка сообщения с использованием asyncio для асинхронного выполнения
            await asyncio.to_thread(bot.send_message, chat_id, f"Дурак пишет: {text}")

            # Сохранение сообщения
            stored_messages.append({
                'username': username,
                'message': text,
                'chatid': chat_id
            })
            return jsonify({"status": "success", "message": "Message sent"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# Эндпоинт для получения сохраненных сообщений
@app.route('/get-messages', methods=['GET'])
def get_messages():
    return jsonify(stored_messages), 200

if __name__ == '__main__':
    app.run(debug=True)
