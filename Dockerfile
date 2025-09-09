FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV WORKERS=4
ENV REDIS_URL=redis://redis:6379

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 --workers ${WORKERS} application:application