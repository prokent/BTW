from flask import Flask, request, jsonify
import telebot
import os

YOUR_BOT_TOKEN = '7112295260:AAFpQ1Cqo31Odq-69t54stivkoJ21eTJkug'
bot = telebot.TeleBot(YOUR_BOT_TOKEN)

app = Flask(__name__)

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()
        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if chat_id and text:
            bot.send_message(chat_id, f"Сообщение от сервера: {text}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run()
