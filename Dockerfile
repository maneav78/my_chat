# FROM python:3.10.14-alpine3.20
FROM python:3.12-alpine
WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install --upgrade python-socketio flask-socketio


COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
