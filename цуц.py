import requests
import json

data = {
    "username": "example_user",
    "message": "Hello, World!",
    "chatid": 5433647570
}

response = requests.post(
    'https://mystic-sky12-b0fa2a6ddde6.herokuapp.com/send-message',
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'}
)
print(response.text)
