from sqlalchemy.orm import Session
from datetime import datetime, timezone
from .models import Category, Product, ProductImage
from .schemas import (CategoryCreate,
                      ProductCreate, 
                      ProductUpdate,
                      ProductImageCreate
)
from .exceptions import (
    CategoryAlreadyTakenException, 
    NotFoundException, 
    EntityTooLargeException,
    BadRequestException
)

# Category services
def create_category(category: CategoryCreate, db: Session):
    if db.query(Category).filter(Category.category_title == category.category_title).first():
        raise CategoryAlreadyTakenException(f"Category with title '{category.category_title}' already taken")
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def retrieve_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Category).offset(skip).limit(limit).all()

def retrieve_category_by_name(category_name: str, db: Session):
    category = db.query(Category).filter(Category.category_title == category_name).first()
    if category is None:
        raise NotFoundException(f"Category with title '{category_name}' not found")
    return category

def update_category(category_id: int, updated_attributes: CategoryCreate, db: Session):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if db_category is None:
        raise NotFoundException(f"Category with ID {category_id} not found")
    if db_category:
        db_category.category_title = updated_attributes.category_title
        db_category.updated_at = datetime.now(tz=timezone.utc)
        db.commit()
        db.refresh(db_category)
        return db_category

def delete_category(category_id: int, db: Session):
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if category is None:
        raise NotFoundException(f"Category with ID {category_id} not found")
    
    products = db.query(Product).filter(Product.category_id == category_id).all()
    if products:
        raise BadRequestException("Cannot delete category as it has associated products")
    
    db.delete(category)
    db.commit()
    return {"success": True, "message": f"Category with ID {category_id} deleted successfully"}

# Product services
def create_product(product: ProductCreate, db: Session):
    category = db.query(Category).filter(Category.category_title == product.category_title).first()
    if category is None:
        raise NotFoundException(f"Category with title '{product.category_title}' not found")
    if len(product.images) > 5:
        raise EntityTooLargeException("You can upload a maximum of 5 images")
    # Creating a new product
    db_product = Product(
        product_title = product.product_title,
        product_description = product.product_description,
        category=category,
        price=product.price,
        quantity=product.quantity,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Adding images to the product
    for image in product.images:
        db_image = ProductImage(
            image_url=image.image_url,
            product_id=db_product.product_id
        )
        db.add(db_image)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(product_id: int, updated_attributes: ProductUpdate, db: Session):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise NotFoundException(f"Product with ID {product_id} not found")
    else:
        db_product.product_title = updated_attributes.product_title
        db_product.product_description = updated_attributes.product_description
        db_product.price = updated_attributes.price
        db_product.quantity = updated_attributes.quantity
        db_product.updated_at = datetime.now(tz=timezone.utc)
        
        db.commit()
        db.refresh(db_product)

        return db_product
    
def retrieve_products(db: Session, skip: int = 0, limit: int = 10):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

def retrieve_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise NotFoundException(f"Product with ID {product_id} not found")
    return product

def delete_product(product_id: int, db: Session):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product is None:
        raise NotFoundException(f"Product with ID {product_id} not found")
    db.delete(product)
    db.commit()
    return {"success": True, "message": f"Product with ID {product_id} deleted successfully"}

# Product Image service
def retrieve_product_images(product_id: int, db: Session):
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    return images

def retrieve_product_image(product_id: int, image_id:int, db: Session):
    image = db.query(ProductImage).filter(ProductImage.product_id == product_id, ProductImage.image_id == image_id).first()
    if image is None:
        raise NotFoundException(f"Product image with ID {image_id} not found")
    return image

def update_product_image(product_id: int, image_id: int, updated_attributes: ProductImageCreate, db: Session):
    db_image = db.query(ProductImage).filter(ProductImage.product_id == product_id, ProductImage.image_id == image_id).first()
    if db_image is None:
        raise NotFoundException(f"Product image with ID {image_id} not found")
    db_image.image_url = updated_attributes.image_url

    db.commit()
    db.refresh(db_image)

    return db_image

def delete_product_image(product_id: int, image_id: int, db: Session):
    db_image = db.query(ProductImage).filter(ProductImage.product_id == product_id, ProductImage.image_id == image_id).first()
    if db_image is None:
        raise NotFoundException(f"Product image with ID {image_id} not found")
    db.delete(db_image)
    db.commit()
    return {"success": True, "message": f"Product Image with ID {image_id} deleted successfully"}