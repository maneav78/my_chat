import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connection established')
    send_message()

def send_message():
    predefined_message = "This is a specific message for testing."
    sio.send(predefined_message)
    print(f'Sent message: {predefined_message}')

if __name__ == '__main__':
    sio.connect('ws://localhost:5000')

