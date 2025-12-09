from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):
    rating: int
    text: str

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Text cannot be empty')
        if len(v) > 1000:
            raise ValueError('Text is too long (max 1000 characters)')
        return v


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    rating: int
    text: str
    created_at: datetime
    user_login: Optional[str] = None

    class Config:
        from_attributes = True
