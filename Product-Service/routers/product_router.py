import traceback
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..schemas import (
    Product,
    ProductCreate,
    ProductUpdate
)
from ..services import (
    create_product,
    update_product,
    retrieve_products,
    retrieve_product_by_id,
    delete_product
)
from ..exceptions import (
    ProductNotFoundException,
    CategoryNotFoundException,
    EntityTooLargeException
)

product_router = APIRouter()

# Product endpoints
@product_router.get("/products/", response_model=List[Product], status_code=200)
async def get_products_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return retrieve_products(skip=skip, limit=limit, db=db)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")

@product_router.post("/product/create/", response_model=Product, status_code=201)
async def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        return create_product(product, db)
    except CategoryNotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except EntityTooLargeException as error:
        raise HTTPException(status_code=422, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")   

@product_router.get("/product/{product_id}/", response_model=Product, status_code=200)
async def get_product_route(product_id: int, db: Session = Depends(get_db)):
    try:
        return retrieve_product_by_id(product_id=product_id, db=db)
    except ProductNotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@product_router.patch("/product/{product_id}/", response_model=Product, status_code=200)
async def update_product_route(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        return update_product(product_id, product, db)
    except ProductNotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@product_router.delete("/product/{product_id}/", status_code=204)
async def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    try:
        return delete_product(product_id, db)
    except ProductNotFoundException as error:
        raise HTTPException(status_code=404, detail=str(error))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")