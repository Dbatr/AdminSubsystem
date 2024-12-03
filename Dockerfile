# Базовый образ с Python
FROM python:3.11-slim

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем зависимости проекта
COPY requirements2.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements2.txt

# Копируем весь проект в контейнер
COPY . /app/

# Настраиваем переменные среды для Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE StPractice.settings

# Открываем порт для сервера разработки
EXPOSE 8000

# Команда по умолчанию для запуска проекта
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
