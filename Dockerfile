FROM python:3.12-slim
LABEL authors="mike tung"

WORKDIR /app
COPY ./config ./config
COPY requirements.txt .
COPY app.py .
COPY ./jainy_bot ./jainy_bot

ENV DISCORD_BOT_TOKEN=DISCORD_TOKEN_HERE
ENV LOG_LEVEL=LOG_LEVEL_HERE
ENV BOT_GUILD_ID=BOT_GUILD_ID_HERE

RUN pip install -r requirements.txt
RUN rm requirements.txt

ENTRYPOINT ["python", "app.py"]