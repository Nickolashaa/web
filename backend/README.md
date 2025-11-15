# Backend API на FastAPI

## Структура проекта

```
backend/
├── app/
│   ├── core/           # Конфигурация, БД, безопасность
│   ├── models/         # SQLAlchemy модели
│   ├── schemas/        # Pydantic схемы
│   ├── crud/           # CRUD операции
│   ├── routers/        # API эндпоинты
│   └── main.py         # Основное приложение
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Запуск проекта

### С помощью Docker Compose

1. Создайте `.env` файл на основе `.env.example`:
```bash
cp .env.example .env
```

2. Запустите контейнеры:
```bash
docker-compose up --build
```

API будет доступно по адресу: http://localhost:8000

Документация API (Swagger): http://localhost:8000/docs

PostgreSQL доступна на порту 5432

## API Endpoints

### Аутентификация

- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Вход в систему (получение JWT токена)

### Пользователи (требуется аутентификация)

- `GET /users/` - Получить список пользователей
- `GET /users/{user_id}` - Получить пользователя по ID
- `PUT /users/{user_id}` - Обновить пользователя
- `DELETE /users/{user_id}` - Удалить пользователя

### Типы товаров (требуется аутентификация)

- `POST /product-types/` - Создать тип товара
- `GET /product-types/` - Получить список типов товаров
- `GET /product-types/{id}` - Получить тип товара по ID
- `PUT /product-types/{id}` - Обновить тип товара
- `DELETE /product-types/{id}` - Удалить тип товара

### Товары (требуется аутентификация)

- `POST /products/` - Создать товар
- `GET /products/` - Получить список товаров
- `GET /products/{id}` - Получить товар по ID
- `PUT /products/{id}` - Обновить товар
- `DELETE /products/{id}` - Удалить товар

## Технологии

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT аутентификация
- Docker & Docker Compose
- Pydantic для валидации
- Bcrypt для хеширования паролей
