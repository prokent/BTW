from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Хранилище сообщений
messages = []


@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()

    # Проверка наличия необходимых данных
    if not data or 'username' not in data or 'message' not in data:
        return jsonify({'msg': 'Username and message are required'}), 400

    username = data['username']
    message = data['message']

    # Добавление сообщения в список
    messages.append({'username': username, 'message': message})

    return jsonify({'msg': 'Message sent'}), 200


@app.route('/view-messages')
def view_messages():
    return render_template('messages.html', messages=messages)


if __name__ == '__main__':
    app.run(port=3000)
