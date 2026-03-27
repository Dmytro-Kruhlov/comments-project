FROM python:3.11-slim
ENV UV_PROJECT_ENVIRONMENT=/tmp/venv
# Системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install uv

WORKDIR /app

# Копируем только зависимости (для кеша)
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости через uv
RUN uv sync --frozen

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Запуск
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
