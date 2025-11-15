from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        product_type_id=product.product_type_id,
        name=product.name,
        description=product.description,
        price=product.price,
        image=product.image,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        if product_update.product_type_id is not None:
            db_product.product_type_id = product_update.product_type_id
        if product_update.name is not None:
            db_product.name = product_update.name
        if product_update.description is not None:
            db_product.description = product_update.description
        if product_update.price is not None:
            db_product.price = product_update.price
        if product_update.image is not None:
            db_product.image = product_update.image
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product
