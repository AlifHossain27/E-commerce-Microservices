import traceback
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..exceptions import (
    NotFoundException, 
    EntityTooLargeException
)
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

product_image_router = APIRouter()

# Product Image Endpoints 
@product_image_router.get("/product/{product_id}/images/", response_model=List[ProductImage], status_code=200)
async def get_product_images_route(product_id: int, db: Session = Depends(get_db)):
    try:
        return retrieve_product_images(product_id=product_id, db=db)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@product_image_router.get("/product/{product_id}/image/{image_id}/", response_model=ProductImage, status_code=200)
def get_product_image_route(product_id: int, image_id: int, db: Session = Depends(get_db)):
    try:
        return retrieve_product_image(product_id=product_id, image_id=image_id, db=db)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@product_image_router.post("/product/{product_id}/image/", response_model=ProductImage, status_code=201)
async def create_product_image_route(product_id: int, image: ProductImageCreate, db: Session = Depends(get_db)):
    try:
        return create_product_image(product_id=product_id, product_image=image, db=db)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except EntityTooLargeException as error:
        raise HTTPException(status_code=422, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

@product_image_router.patch("/product/{product_id}/image/{image_id}/", response_model=ProductImage, status_code=200)
async def update_product_image_route(product_id: int, image_id: int, image: ProductImageCreate, db: Session = Depends(get_db)):
    try:
        return update_product_image(product_id=product_id, image_id=image_id, updated_attributes=image, db=db)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@product_image_router.delete("/product/{product_id}/image/{image_id}/", status_code=204)
async def delete_product_image_route(product_id: int, image_id: int, db: Session = Depends(get_db)):
    try:
        return delete_product_image(product_id=product_id, image_id=image_id, db=db)
    except NotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")