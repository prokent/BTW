from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from YOUR_TOKEN import YOUR_BOT_TOKEN

# Создаем экземпляр бота
bot = telebot.TeleBot(YOUR_BOT_TOKEN)

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Включаем CORS для всего приложения
CORS(app)

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        # Получаем JSON данные из запроса
        data = request.get_json()

        # Извлекаем необходимые данные
        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        # Проверяем наличие chat_id и текста сообщения
        if chat_id and text:
            bot.send_message(chat_id, f"Дурак пишет: {text}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400

    except Exception as e:
        # Логируем ошибку и возвращаем статус 500
        print(f"Ошибка при получении данных: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# Запускаем приложение
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
