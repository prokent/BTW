from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from YOUR_TOKEN import YOUR_BOT_TOKEN

bot = telebot.TeleBot(YOUR_BOT_TOKEN)
app = Flask(__name__)
CORS(app)

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()
        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if chat_id and text:
            bot.send_message(chat_id,  {text})
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400
    except Exception as e:
        print(f"Ошибка при получении: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run()
