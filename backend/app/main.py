from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base, SessionLocal
from app.routers import auth, users, product_types, products, reviews
from app.core.init_data import create_test_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Products API", version="1.0.0")

# Инициализация тестовых данных при старте
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        create_test_data(db)
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(product_types.router)
app.include_router(products.router)
app.include_router(reviews.router)


@app.get("/", summary="Health check")
def health_check():
    return {"status": "ok"}
