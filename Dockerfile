FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # --no-cache-dir reduces image size

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]