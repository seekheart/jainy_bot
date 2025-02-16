FROM python:3.12-slim
LABEL authors="mike tung"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN rm requirements.txt

ENTRYPOINT ["python", "app.py"]
