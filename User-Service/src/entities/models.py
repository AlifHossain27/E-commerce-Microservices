import uuid
import enum
from ..database.db import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone



class Roles(enum.Enum):
    Admin = 'admin'
    Seller = 'seller'
    Buyer = 'buyer'


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    password_hash = Column(String, nullable=False)
    is_enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    role = Column(Enum(Roles), nullable=False, default=Roles.Buyer)

    address = relationship('Address', back_populates='user')

    def __repr__(self):
        return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"
    
class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey('users.user_id'))
    full_address = Column(String)
    postal_code = Column(String)
    city = Column(String)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc))

    user = relationship('User', back_populates='address')

    def __repr__(self):
        return f"<Address(full_address='{self.full_address}', postal_code='{self.postal_code}', city='{self.city}', country='{self.country}')>"