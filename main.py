from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from pymongo import MongoClient
import openai 
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env.credentials")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) #changed
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

openai.api_key = os.getenv('OPENAI_API_KEY')
print("Loaded API Key:", openai.api_key)

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client.chat_db
messages_col = db.messages
users_col = db.users

@socketio.on('connect')
def handle_connect(auth=None):
    messages = list(messages_col.find({}, {'_id': 0}))  # already excluding _id here
    for message in messages:
        emit('receive_message', message)
    update_users_online()

@socketio.on('send_message')
def handle_send_message(data):
    user_message = data["message"]
    if user_message.startswith("/ask"):
        query = user_message[5:].strip()
        user_message_doc = {'name': data['name'], 'message': user_message, 'time': data["time"]}
        print(user_message_doc)
        result = messages_col.insert_one(user_message_doc)
        user_message_doc['_id'] = str(result.inserted_id) 
        emit('receive_message', user_message_doc, broadcast=True)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": query}],
                max_tokens=400,
                temperature=0.5
            )
            output = response.choices[0].message['content'].strip()
            bot_message = {
                'name': "ChatGPT",
                'message': output,
                'time': data["time"]
            }
            result = messages_col.insert_one(bot_message)
            bot_message['_id'] = str(result.inserted_id)
            emit('receive_message', bot_message, broadcast=True)
            emit('bot_answer', broadcast=True)
        except openai.error.RateLimitError as e:
            emit('receive_message', {'name': 'System', 'message': 'Rate limit exceeded, please try again later.'}, broadcast=True)
        except openai.error.APIError as e:
            emit('receive_message', {'name': 'System', 'message': 'An API error occurred: ' + str(e)}, broadcast=True)
        except Exception as e:
            emit('receive_message', {'name': 'System', 'message': 'An unexpected error occurred: ' + str(e)}, broadcast=True)
    else:
        user_message_doc = {'name': data['name'], 'message': user_message, 'time': data["time"]}
        result = messages_col.insert_one(user_message_doc)
        user_message_doc['_id'] = str(result.inserted_id) 
        emit('receive_message', user_message_doc, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_left = users_col.find_one_and_delete({'sid': request.sid})
    if user_left:
        emit('user_left', {'name': user_left['name']}, broadcast=True)
    update_users_online()

@socketio.on('register_user')
def handle_register_user(name):
    if users_col.find_one({'name': name}):
        emit('registration_failed', {'message': 'Name already exists'})
    else:
        users_col.insert_one({'name': name, 'sid': request.sid})
        emit('user_joined', name)
        update_users_online()

def update_users_online():
    users_online = list(users_col.find({}, {'_id': 0, 'name': 1}))
    emit('users_online', users_online, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
