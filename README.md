# 📌 Comments Project

A web application for creating and viewing comments with support for:

- nested comments (replies)
- captcha validation
- HTML content in comments
- pagination
- REST API (Django + DRF)

---

# 🚀 Tech Stack

- Python 3.14
- Django
- Django REST Framework
- PostgreSQL
- Docker / Docker Compose
- Pre-commit

---

# 📦 Getting Started

## 1. Clone the repository

install Docker
```bash
git clone <repo_url>
cd comments-project

## 2. Run with Docker

```bash
docker-compose up --build
docker-compose exec web uv run python manage.py migrate

The application will be available at:
http://localhost:8000

## 3. Run tests

docker-compose exec web uv run pytest -v
