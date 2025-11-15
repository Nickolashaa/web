import os
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.product_type import ProductType
from app.models.product import Product
from app.core.security import get_password_hash


def create_test_data(db: Session):
    """
    Создает тестовые данные при первом запуске приложения.
    Проверяет наличие записей в таблицах и добавляет их, если таблицы пустые.
    """

    # Проверяем наличие пользователей
    user_count = db.query(User).count()
    if user_count == 0:
        print("Создание тестового администратора...")
        admin_user = User(
            login="admin",
            password=get_password_hash("admin"),
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        print("Администратор создан: login=admin, password=admin")

    # Проверяем наличие типов товаров
    product_type_count = db.query(ProductType).count()
    if product_type_count == 0:
        print("Создание типов товаров...")

        ring_type = ProductType(name="Кольца")
        earring_type = ProductType(name="Серьги")
        brooch_type = ProductType(name="Броши")

        db.add(ring_type)
        db.add(earring_type)
        db.add(brooch_type)
        db.commit()
        db.refresh(ring_type)
        db.refresh(earring_type)
        db.refresh(brooch_type)

        print(f"Типы товаров созданы: {ring_type.id}, {earring_type.id}, {brooch_type.id}")
    else:
        ring_type = db.query(ProductType).filter(ProductType.name == "Кольца").first()
        earring_type = db.query(ProductType).filter(ProductType.name == "Серьги").first()
        brooch_type = db.query(ProductType).filter(ProductType.name == "Броши").first()

    # Проверяем наличие товаров
    product_count = db.query(Product).count()
    if product_count == 0:
        print("Создание товаров...")

        # Путь к папке с изображениями
        images_dir = os.path.join(os.path.dirname(__file__), "..", "static", "images")

        # Функция для чтения изображения
        def read_image(filename):
            path = os.path.join(images_dir, filename)
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    return f.read()
            return None

        # Кольца
        rings = [
            {
                "name": "Кольцо 'Изумрудная элегантность'",
                "description": "Роскошное золотое кольцо с крупным изумрудом огранки 'кушон' и россыпью бриллиантов",
                "price": 125000.00,
                "image": "ring1.png"
            },
            {
                "name": "Кольцо 'Вечная классика'",
                "description": "Классическое обручальное кольцо из белого золота 585 пробы с бриллиантом",
                "price": 85000.00,
                "image": "ring2.png"
            },
            {
                "name": "Кольцо 'Сапфировая мечта'",
                "description": "Элегантное кольцо с синим сапфиром и бриллиантовой дорожкой в платине",
                "price": 210000.00,
                "image": "ring3.png"
            },
            {
                "name": "Кольцо 'Розовая нежность'",
                "description": "Изысканное кольцо из розового золота с морганитом и паве из бриллиантов",
                "price": 95000.00,
                "image": "ring4.png"
            }
        ]

        # Серьги
        earrings = [
            {
                "name": "Серьги 'Бриллиантовый каскад'",
                "description": "Роскошные висячие серьги с бриллиантами общим весом 2 карата в белом золоте",
                "price": 185000.00,
                "image": "earrings1.png"
            },
            {
                "name": "Серьги 'Жемчужная элегантность'",
                "description": "Классические серьги-гвоздики с культивированным жемчугом Акойя и золотом",
                "price": 45000.00,
                "image": "earrings2.png"
            },
            {
                "name": "Серьги 'Изумрудный шик'",
                "description": "Длинные серьги с колумбийскими изумрудами и бриллиантами в платине",
                "price": 320000.00,
                "image": "earrings3.png"
            }
        ]

        # Броши
        brooches = [
            {
                "name": "Брошь 'Цветочная фантазия'",
                "description": "Винтажная брошь в виде цветка с разноцветными сапфирами и бриллиантами",
                "price": 145000.00,
                "image": "brooch1.png"
            },
            {
                "name": "Брошь 'Королевская бабочка'",
                "description": "Изящная брошь-бабочка с эмалью, рубинами и бриллиантами из белого золота",
                "price": 175000.00,
                "image": "brooch2.png"
            },
            {
                "name": "Брошь 'Арт-деко'",
                "description": "Геометрическая брошь в стиле Арт-деко с ониксом, бриллиантами и платиной",
                "price": 230000.00,
                "image": "brooch3.png"
            }
        ]

        # Добавляем кольца
        for ring_data in rings:
            image_data = read_image(ring_data["image"])
            product = Product(
                product_type_id=ring_type.id,
                name=ring_data["name"],
                description=ring_data["description"],
                price=ring_data["price"],
                image=image_data
            )
            db.add(product)

        # Добавляем серьги
        for earring_data in earrings:
            image_data = read_image(earring_data["image"])
            product = Product(
                product_type_id=earring_type.id,
                name=earring_data["name"],
                description=earring_data["description"],
                price=earring_data["price"],
                image=image_data
            )
            db.add(product)

        # Добавляем броши
        for brooch_data in brooches:
            image_data = read_image(brooch_data["image"])
            product = Product(
                product_type_id=brooch_type.id,
                name=brooch_data["name"],
                description=brooch_data["description"],
                price=brooch_data["price"],
                image=image_data
            )
            db.add(product)

        db.commit()
        print(f"Создано {len(rings) + len(earrings) + len(brooches)} товаров")

    print("Инициализация тестовых данных завершена!")
