from sqlalchemy.orm import Session, joinedload
from app.models.review import Review
from app.schemas.review import ReviewCreate


def create_review(db: Session, review: ReviewCreate, user_id: int):
    db_review = Review(
        user_id=user_id,
        rating=review.rating,
        text=review.text,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review(db: Session, review_id: int):
    return db.query(Review).options(joinedload(Review.user)).filter(Review.id == review_id).first()


def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Review).options(joinedload(Review.user)).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
