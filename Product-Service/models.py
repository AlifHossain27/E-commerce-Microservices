from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .db import Base
from datetime import datetime, timezone


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, index=True)
    category_title = Column(String(60), index=True)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc))

    product = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, index=True)
    category_title = Column(String, ForeignKey("categories.category_title"))
    product_title = Column(String(150), index=True)
    product_description = Column(String(225))
    image = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc))

    category = relationship("Category", back_populates="product")


