from sqlalchemy.orm import Session
from app.models.product_type import ProductType
from app.schemas.product_type import ProductTypeCreate, ProductTypeUpdate


def create_product_type(db: Session, product_type: ProductTypeCreate):
    db_product_type = ProductType(name=product_type.name)
    db.add(db_product_type)
    db.commit()
    db.refresh(db_product_type)
    return db_product_type


def get_product_type(db: Session, product_type_id: int):
    return db.query(ProductType).filter(ProductType.id == product_type_id).first()


def get_product_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductType).offset(skip).limit(limit).all()


def update_product_type(
    db: Session, product_type_id: int, product_type_update: ProductTypeUpdate
):
    db_product_type = (
        db.query(ProductType).filter(ProductType.id == product_type_id).first()
    )
    if db_product_type:
        db_product_type.name = product_type_update.name
        db.commit()
        db.refresh(db_product_type)
    return db_product_type


def delete_product_type(db: Session, product_type_id: int):
    db_product_type = (
        db.query(ProductType).filter(ProductType.id == product_type_id).first()
    )
    if db_product_type:
        db.delete(db_product_type)
        db.commit()
    return db_product_type
