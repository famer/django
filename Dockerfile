# Используем официальный образ Python как базовый
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию контейнера
COPY . .

# Выполняем команду collectstatic
#RUN python manage.py collectstatic --noinput

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
