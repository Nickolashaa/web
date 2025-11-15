from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.crud import product as crud_product
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, summary="Create product")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_product.create_product(db=db, product=product)


@router.get("/", response_model=List[ProductResponse], summary="Get all products")
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    products = crud_product.get_products(db, skip=skip, limit=limit)
    return products


@router.get(
    "/{product_id}", response_model=ProductResponse, summary="Get product by ID"
)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}", response_model=ProductResponse, summary="Update product")
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = crud_product.update_product(
        db, product_id=product_id, product_update=product
    )
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}", summary="Delete product")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product = crud_product.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
