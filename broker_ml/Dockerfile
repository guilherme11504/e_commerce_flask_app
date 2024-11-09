FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 1446


CMD ["gunicorn", "--bind", "0.0.0.0:1446", "app:app"]
