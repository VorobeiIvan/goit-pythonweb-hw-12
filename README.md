# FastAPI Contacts Management API

## 🚀 Overview
This project is a **FastAPI-based REST API** designed for managing contacts. It includes features such as user authentication, email verification, JWT-based authorization, rate limiting, and avatar uploads via Cloudinary.

---

## 📌 Features
- **User Authentication & Authorization** (JWT-based)
- **Email Verification for User Registration**
- **CRUD Operations for Contacts**
- **Rate Limiting** (via SlowAPI)
- **CORS Support**
- **Cloudinary Integration for Avatar Uploads**
- **Docker & PostgreSQL Support**
- **Redis Caching**
- **Password Reset Functionality**
- **User Roles (Admin/User)**
- **Sphinx Documentation**

---

## 🛠 Tech Stack
- **Python 3.11**
- **FastAPI**
- **SQLAlchemy** (PostgreSQL)
- **JWT (PyJWT & OAuth2)**
- **Passlib** (Password Hashing)
- **Cloudinary** (Image Uploads)
- **Docker & Docker Compose**
- **SlowAPI** (Rate Limiting)
- **Redis** (Caching)
- **Sphinx** (Documentation)

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repository/your-repository
cd your-repository
```

### 2️⃣ Create a Virtual Environment & Install Dependencies
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### 3️⃣ Set Up Environment Variables
Create a `.env` file in the root directory and add the required environment variables. Example:

```env
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://user:password@localhost/dbname
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_EMAIL=your_email@example.com
SMTP_PASSWORD=your_password
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### 4️⃣ Run with Docker Compose
To start the application with Docker Compose:
```bash
docker-compose up --build
```

---

### 5️⃣ Run PostgreSQL & Redis Locally (without Docker Compose)
If using Docker manually, run the following commands:

1. Start PostgreSQL:
   ```bash
   docker run --name postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=dbname -p 5432:5432 -d postgres
   ```
2. Start Redis:
   ```bash
   docker run --name redis -p 6379:6379 -d redis
   ```

Or start existing containers:
```bash
docker start postgres redis
```

---

### 6️⃣ Run FastAPI Server
To start the FastAPI server locally:
```bash
uvicorn main:app --reload
```

The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📜 API Documentation

### Interactive Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Generated Documentation
To generate and view the Sphinx documentation:
```bash
sphinx-build -b html docs/ docs/_build/html
```
The documentation will be available at `docs/_build/html/index.html`.

---

## 🧪 Testing

### Running Tests
To run the tests with coverage reporting:
```bash
pytest --cov
```

### Test Coverage
- **Overall**: 84%
- **database.py**: 92%
- **main.py**: 69%
- **models.py**: 100%
- **tests/conftest.py**: 100%
- **tests/test_auth.py**: 100%
- **tests/test_contacts.py**: 100%

---

## 🔐 Authentication & Authorization

### User Roles
- **User**: Standard user with basic access.
- **Admin**: Administrator with additional privileges.
   - Can change their avatar.
   - Has full access to all features.

### Password Reset
1. Request password reset.
2. Check email for reset link.
3. Reset password using the token.

### Redis Caching
- User data is cached in Redis for 30 minutes.
- Cache is automatically updated when user data changes.
- Improves performance by reducing database queries.

---

## 🛠 Development

### Code Style
The project follows PEP 8 guidelines. To check code style:
```bash
flake8
```

### Documentation
All functions and classes have docstrings following Google style. To generate documentation:
```bash
sphinx-build -b html docs/ docs/_build/html
```

### Testing
To run specific test files:
```bash
pytest tests/test_file.py
```
To run a specific test:
```bash
pytest -k "test_name"
```

---

## 📦 Dependencies
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Redis**
- **JWT**
- **Passlib**
- **Cloudinary**
- **Sphinx**
- **pytest**
- **pytest-cov**
- **flake8**

---

## 🔒 Security
- JWT-based authentication.
- Password hashing with bcrypt.
- Rate limiting.
- CORS protection.
- Email verification.
- Role-based access control.

---

## 📝 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
