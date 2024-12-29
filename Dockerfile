FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE StPractice.settings

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
