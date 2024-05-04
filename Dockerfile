FROM python:3.12-slim
LABEL authors="mike tung"

WORKDIR /app
COPY ./config ./config
COPY requirements.txt .
COPY app.py .
COPY ./jainy_bot ./jainy_bot

RUN pip install -r requirements.txt
RUN rm requirements.txt

ENTRYPOINT ["python", "app.py"]