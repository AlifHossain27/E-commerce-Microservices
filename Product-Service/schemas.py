from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from .exceptions import EntityTooLargeException

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

# Product Images
class ProductImageBase(BaseModel):
    image_url: str

class ProductImageCreate(ProductImageBase):
    pass

class ProductImage(ProductImageBase):
    image_id: int
    product_id: int
    model_config = ConfigDict(from_attributes=True)

# Product Schemas
class ProductBase(BaseModel):
    product_title: str
    product_description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    category_title: str
    images: Optional[List[ProductImageCreate]] = []


class ProductUpdate(ProductBase):
    product_title: Optional[str]
    product_description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

class Product(ProductBase):
    product_id: int
    category: Category
    images: List[ProductImage] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
