# Python Web Application with FastAPI

## Опис проекту

Цей проект є веб-додатком, створеним за допомогою **FastAPI**. Він включає функціонал для роботи з базою даних, аутентифікації, кешування, інтеграції з Cloudinary, SMTP-сервером та іншими сервісами.

---

## Основні функції

- **Аутентифікація**: Реалізовано за допомогою JWT-токенів для забезпечення безпеки.
- **Робота з базою даних**: Використовується SQLAlchemy для роботи з PostgreSQL або SQLite, що забезпечує гнучкість у виборі бази даних.
- **Кешування**: Інтеграція з Redis для зменшення навантаження на базу даних і підвищення швидкості роботи.
- **Завантаження файлів**: Інтеграція з Cloudinary для зберігання та обробки зображень, таких як аватари користувачів.
- **Відправка email**: Використовується SMTP для відправки листів, наприклад, для підтвердження реєстрації.
- **Документація API**: Автоматично генерується за допомогою Swagger UI та ReDoc для зручності розробників.

---

## Вимоги

- **Python**: Версія 3.10 або новіша.
- **Docker та Docker Compose**: Для запуску проекту в контейнерах.
- **PostgreSQL**: Рекомендується для продакшн-середовища.
- **Redis**: Для кешування даних.

---

## Установка

### 1. Клонування репозиторію
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Створення та активація віртуального середовища
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
```

### 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 4. Налаштування змінних середовища
- Створіть файл `.env` на основі `.env.example`.
- Заповніть змінні середовища у файлі `.env`.

---

## Запуск проекту

### Локально
1. Запустіть сервер:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Відкрийте документацію API:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Через Docker
1. Запустіть Docker-контейнери:
   ```bash
   docker-compose up --build
   ```
2. Відкрийте документацію API:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Тестування

### Запуск всіх тестів
```bash
pytest
```

### Запуск тестів з покриттям коду
```bash
pytest --cov=app
```

### Запуск тестів для конкретної папки
```bash
pytest tests/
```

---

## Структура проекту

```plaintext
.
├── .env
├── Dockerfile
│   # Defines the instructions to build the Docker image for the application.
├── README.md
│   # Documentation file with project overview, setup, and usage instructions.
├── __pycache__
│   # Directory for Python bytecode cache files.
├── app
│   # Main application directory containing core logic and structure.
│   ├── database
│   │   # Database connection and initialization logic.
│   ├── models
│   │   # ORM models for database tables.
│   ├── routers
│   │   # API route definitions for various functionalities.
│   ├── schemas
│   │   # Pydantic models for request and response validation.
│   ├── services
│   │   # Business logic and service layer implementations.
│   └── utils
│       # Utility functions and helper modules.
├── docker-compose.yml
│   # Configuration for orchestrating multi-container Docker setups.
├── docker-entrypoint.sh
│   # Script for initializing the Docker container.
├── main.py
│   # Entry point for the FastAPI application.
├── requirements.txt
│   # List of Python dependencies for the project.
├── test.db
│   # SQLite database file for testing purposes.
└── tests
   # Directory containing test cases for the application.
   ├── cache
   │   # Tests for caching functionality.
   ├── cloudinary
   │   # Tests for Cloudinary integration.
   ├── database
   │   # Tests for database-related functionality.
   ├── docker
   │   # Tests for Docker-related functionality.
   ├── integration
   │   # Integration tests for application modules.
   ├── models
   │   # Tests for ORM models.
   ├── routers
   │   # Tests for API route handlers.
   ├── schemas
   │   # Tests for Pydantic schemas.
   ├── services
   │   # Tests for service layer logic.
   ├── smtp
   │   # Tests for SMTP email functionality.
   ├── utils
   │   # Tests for utility modules.
   └── pytest.ini
      # Configuration file for pytest settings.
```

---

## Залежності

Перелік основних бібліотек:
- **FastAPI**: Фреймворк для створення веб-додатків.
- **SQLAlchemy**: ORM для роботи з базою даних.
- **Pydantic**: Валідація даних.
- **Redis**: Кешування.
- **python-jose**: Робота з JWT.
- **pytest**: Тестування.

---

## Автор

- **Ваше ім'я**: [Ваш GitHub профіль](https://github.com/your-username)

---

## Ліцензія

Цей проект ліцензований під [MIT License](LICENSE).
