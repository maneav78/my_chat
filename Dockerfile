FROM python:3.10.14-alpine3.20
# FROM python:3.8-alpine

WORKDIR /app

# RUN apt update && apt install -y python3  python3-pip

COPY requirements.txt .

RUN pip --version
RUN cat requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade python-socketio flask-socketio


COPY main.py .
COPY .env.credentials .

EXPOSE 5000

CMD ["python", "main.py"]
