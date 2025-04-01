import traceback
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from ..db import get_db
from ..schemas import (
    Category,
    CategoryCreate
)
from ..services import (
    create_category,
    retrieve_categories,
    retrieve_category_by_name,
    update_category,
    delete_category
)
from ..exceptions import (
    NotFoundException,
    EntityTooLargeException,
    BadRequestException,
    ConflictException,
    InternalServerErrorException
)

category_router = APIRouter()

# Category endpoints
@category_router.get("/categories/", response_model=List[Category], status_code=200)
async def get_categories_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return retrieve_categories(db=db, skip=skip, limit=limit)
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@category_router.get("/category/{category_title}/", response_model=Category, status_code=200)
async def get_category_by_name_route(category_title: str, db: Session = Depends(get_db)):
    try:
        return retrieve_category_by_name(category_name=category_title, db=db)
    except NotFoundException as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()


@category_router.post("/category/create/", response_model=Category, status_code=201)
async def create_category_route(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category(category=category, db=db)
    except (NotFoundException, EntityTooLargeException, BadRequestException, ConflictException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
@category_router.patch("/category/{category_id}/", response_model=Category, status_code=200)
async def update_category_route(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return update_category(category_id=category_id, updated_attributes=category, db=db)
    except (NotFoundException, EntityTooLargeException, BadRequestException, ConflictException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
    
    
@category_router.delete("/category/{category_id}/", status_code=204)
async def delete_category_route(category_id: int, db: Session = Depends(get_db)):
    try:
        delete_category(category_id=category_id, db=db)
        return {"detail": "Category deleted successfully"}
    except (NotFoundException, BadRequestException) as error:
        raise error
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestException()
