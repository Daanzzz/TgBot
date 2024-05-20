FROM python

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV BOT_TOKEN=bot_token

CMD ["python3", "TeleBot.py"]
