from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

# Category Schemas
class CategoryBase(BaseModel):
    category_title: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Product Schemas
class ProductBase(BaseModel):
    product_title: str
    product_description: str
    category_title: str
    image: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    product_title: Optional[str]
    product_description: Optional[str]
    image: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

class Product(ProductBase):
    product_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
