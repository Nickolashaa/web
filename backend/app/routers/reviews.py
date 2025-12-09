from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.review import ReviewCreate, ReviewResponse
from app.crud import review as crud_review
from app.models.user import User

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/latest", response_model=List[ReviewResponse], summary="Get latest reviews")
def read_latest_reviews(
    db: Session = Depends(get_db),
):
    """Получить последние 5 отзывов для слайдера на главной странице"""
    reviews = crud_review.get_reviews(db, skip=0, limit=5)
    result = []
    for review in reviews:
        response = ReviewResponse.model_validate(review)
        response.user_login = review.user.login if review.user else None
        result.append(response)
    return result


@router.post("/", response_model=ReviewResponse, summary="Create review")
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_review = crud_review.create_review(db=db, review=review, user_id=current_user.id)
    # Добавляем логин пользователя в ответ
    response = ReviewResponse.model_validate(db_review)
    response.user_login = current_user.login
    return response


@router.get("/", response_model=List[ReviewResponse], summary="Get all reviews")
def read_reviews(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    reviews = crud_review.get_reviews(db, skip=skip, limit=limit)
    # Добавляем логины пользователей
    result = []
    for review in reviews:
        response = ReviewResponse.model_validate(review)
        response.user_login = review.user.login if review.user else None
        result.append(response)
    return result


@router.get("/{review_id}", response_model=ReviewResponse, summary="Get review by ID")
def read_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    db_review = crud_review.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    response = ReviewResponse.model_validate(db_review)
    response.user_login = db_review.user.login if db_review.user else None
    return response
