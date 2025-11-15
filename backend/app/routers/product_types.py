from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.product_type import (
    ProductTypeCreate,
    ProductTypeUpdate,
    ProductTypeResponse,
)
from app.crud import product_type as crud_product_type
from app.models.user import User

router = APIRouter(prefix="/product_types", tags=["product-types"])


@router.post("/", response_model=ProductTypeResponse, summary="Create product type")
def create_product_type(
    product_type: ProductTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_product_type.create_product_type(db=db, product_type=product_type)


@router.get(
    "/", response_model=List[ProductTypeResponse], summary="Get all product types"
)
def read_product_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    product_types = crud_product_type.get_product_types(db, skip=skip, limit=limit)
    return product_types


@router.get(
    "/{product_type_id}",
    response_model=ProductTypeResponse,
    summary="Get product type by ID",
)
def read_product_type(
    product_type_id: int,
    db: Session = Depends(get_db),
):
    db_product_type = crud_product_type.get_product_type(
        db, product_type_id=product_type_id
    )
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="Product type not found")
    return db_product_type


@router.put(
    "/{product_type_id}",
    response_model=ProductTypeResponse,
    summary="Update product type",
)
def update_product_type(
    product_type_id: int,
    product_type: ProductTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product_type = crud_product_type.update_product_type(
        db, product_type_id=product_type_id, product_type_update=product_type
    )
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="Product type not found")
    return db_product_type


@router.delete("/{product_type_id}", summary="Delete product type")
def delete_product_type(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_product_type = crud_product_type.delete_product_type(
        db, product_type_id=product_type_id
    )
    if db_product_type is None:
        raise HTTPException(status_code=404, detail="Product type not found")
    return {"message": "Product type deleted successfully"}
