# Dockerfile for Django backend
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY Public/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python Public/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "Public/manage.py", "runserver", "0.0.0.0:8000"]
