from pydantic import BaseModel, field_serializer, model_serializer, field_validator, model_validator
from typing import Optional, Union
import base64


class ProductCreate(BaseModel):
    product_type_id: int
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[Union[str, bytes]] = None

    @model_validator(mode='before')
    @classmethod
    def decode_image_field(cls, values):
        if isinstance(values, dict) and 'image' in values:
            img = values['image']
            if img and isinstance(img, str):
                try:
                    values['image'] = base64.b64decode(img)
                except Exception:
                    raise ValueError('Invalid base64 image')
        return values


class ProductUpdate(BaseModel):
    product_type_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image: Optional[Union[str, bytes]] = None

    @model_validator(mode='before')
    @classmethod
    def decode_image_field(cls, values):
        if isinstance(values, dict) and 'image' in values:
            img = values['image']
            if img and isinstance(img, str):
                try:
                    values['image'] = base64.b64decode(img)
                except Exception:
                    raise ValueError('Invalid base64 image')
        return values


class ProductResponse(BaseModel):
    id: int
    product_type_id: int
    name: str
    description: Optional[str]
    price: float
    image: Optional[bytes] = None

    @model_serializer
    def ser_model(self):
        return {
            'id': self.id,
            'product_type_id': self.product_type_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': base64.b64encode(self.image).decode('utf-8') if self.image else None
        }

    class Config:
        from_attributes = True
