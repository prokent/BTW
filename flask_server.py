from flask import Flask, request, jsonify
import telebot
import sqlite3
import os

YOUR_NEW_BOT_TOKEN = '7112295260:AAFpQ1Cqo31Odq-69t54stivkoJ21eTJkug'
bot = telebot.TeleBot(YOUR_NEW_BOT_TOKEN)

app = Flask(__name__)

# Функция для создания таблицы сообщений, если она не существует
def create_table():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                message TEXT,
                chat_id TEXT
            )
        ''')
        conn.commit()

# Вызов функции создания таблицы при запуске приложения
create_table()

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()
        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if chat_id and text:
            # Сохранение сообщения в базе данных
            with sqlite3.connect('messages.db') as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO messages (username, message, chat_id)
                    VALUES (?, ?, ?)
                ''', (username, text, chat_id))
                conn.commit()

            # Отправка сообщения через бота
            bot.send_message(chat_id, f"Сообщение от сервера: {text}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run()
