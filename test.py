import time
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connection established')
    send_message()

@sio.on('receive_message')
def on_receive_message(data):
    print(f'Received message: {data}')

def send_message():
    predefined_message = {
        "name": "TestUser",
        "message": "This is a specific message for testing.",
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    sio.emit('send_message', predefined_message)
    print(f'Sent message: {predefined_message["message"]}')

if __name__ == '__main__':
    connected = False
    attempts = 0
    while not connected and attempts < 5:
        try:
            sio.connect('http://localhost:5000')
            connected = True
        except socketio.exceptions.ConnectionError as e:
            print(f'Connection failed, attempt {attempts + 1}')
            attempts += 1
            time.sleep(5) 
    if connected:
        print("connected")
        sio.wait()  
    else:
        print('Failed to connect after several attempts')
