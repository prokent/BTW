from flask import Flask, request, jsonify
import telebot
from YOUR_TOKEN import YOUR_BOT_TOKEN

bot = telebot.TeleBot(YOUR_BOT_TOKEN)
app = Flask(__name__)

# Список для хранения сообщений
stored_messages = []

@app.route('/send-message', methods=['POST'])
def receive_message():
    try:
        data = request.get_json()
        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if chat_id and text:
            bot.send_message(chat_id, f"Турок Успешно отправил на сервер: {text}")
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400
    except Exception as e:
        print(f"Error receiving data: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/save-message', methods=['POST'])
def save_message():
    try:
        data = request.get_json()
        username = data.get('username')
        text = data.get('message')
        chat_id = data.get('chatid')

        if username and text and chat_id:
            stored_messages.append({
                'username': username,
                'message': text,
                'chatid': chat_id
            })
            print(f"Message saved: {stored_messages[-1]}")
            return jsonify({"status": "success", "message": "Message saved"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400
    except Exception as e:
        print(f"Error saving data: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/get-messages', methods=['GET'])
def get_messages():
    return jsonify(stored_messages), 200

if __name__ == '__main__':
    app.run(debug=True)
