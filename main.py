from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base, engine
from app.routers import auth, contacts, users

# Ініціалізація FastAPI
app = FastAPI()


# Подія для створення таблиць у базі даних під час запуску
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


# Додавання CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
