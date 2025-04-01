import traceback
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..db import get_db
from ..schemas import (
    ProductImage,
    ProductImageCreate
)
from ..services import (
    retrieve_product_images,
    retrieve_product_image,
    create_product_image,
    update_product_image,
    delete_product_image
)
from ..exceptions import (
    NotFoundException,
    EntityTooLargeException,
    BadRequestException,
    ConflictException,
    InternalServerErrorException
)

product_image_router = APIRouter()

# Product Image Endpoints 
@product_image_router.get("/product/{product_id}/images/", response_model=List[ProductImage], status_code=200)
async def get_product_images_route(product_id: int, db: Session = Depends(get_db)):
    try:
        return retrieve_product_images(product_id=product_id, db=db)
    except NotFoundException as error:
        raise error
    except Exception:
        print(traceback.format_exc())
        raise BadRequestException()
    
@product_image_router.get("/product/{product_id}/image/{image_id}/", response_model=ProductImage, status_code=200)
async def get_product_image_route(product_id: int, image_id: int, db: Session = Depends(get_db)):
    try:
        return retrieve_product_image(product_id=product_id, image_id=image_id, db=db)
    except NotFoundException as error:
        raise error
    except Exception:
        print(traceback.format_exc())
        raise BadRequestException()
    
@product_image_router.post("/product/{product_id}/image/", response_model=ProductImage, status_code=201)
async def create_product_image_route(product_id: int, image: ProductImageCreate, db: Session = Depends(get_db)):
    try:
        return create_product_image(product_id=product_id, product_image=image, db=db)
    except (NotFoundException, EntityTooLargeException, BadRequestException, ConflictException) as error:
        raise error
    except Exception:
        print(traceback.format_exc())
        raise BadRequestException()

@product_image_router.patch("/product/{product_id}/image/{image_id}/", response_model=ProductImage, status_code=200)
async def update_product_image_route(product_id: int, image_id: int, image: ProductImageCreate, db: Session = Depends(get_db)):
    try:
        return update_product_image(product_id=product_id, image_id=image_id, updated_attributes=image, db=db)
    except (NotFoundException, EntityTooLargeException, BadRequestException, ConflictException) as error:
        raise error
    except Exception:
        print(traceback.format_exc())
        raise BadRequestException()
    
@product_image_router.delete("/product/{product_id}/image/{image_id}/", status_code=204)
async def delete_product_image_route(product_id: int, image_id: int, db: Session = Depends(get_db)):
    try:
        return delete_product_image(product_id=product_id, image_id=image_id, db=db)
    except (NotFoundException, BadRequestException) as error:
        raise error
    except Exception:
        print(traceback.format_exc())
        raise BadRequestException()