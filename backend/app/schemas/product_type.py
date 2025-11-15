from pydantic import BaseModel


class ProductTypeCreate(BaseModel):
    name: str


class ProductTypeUpdate(BaseModel):
    name: str


class ProductTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
