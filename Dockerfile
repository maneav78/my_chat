FROM python:3.10.14-alpine3.20

WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install --upgrade python-socketio flask-socketio


COPY main.py .
COPY .env.credentials .

EXPOSE 5000

CMD ["python", "main.py"]
