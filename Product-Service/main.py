from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.product_router import product_router
from .routers.category_router import category_router
from .routers.product_image_router import product_image_router
from .db import Base, engine


app = FastAPI(
    title = "Product Service",
    description = "An API to manage products",
    version = "1.0.0",
    contact = {
        "name": "API Support",
        "url": "https://github.com/AlifHossain27/E-commerce-Microservices",
        "email": "alifh044@gmail.com"
    }
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Category router
app.include_router(category_router, tags=["Categories"], prefix="/api")
# Product router
app.include_router(product_router, tags=["Products"], prefix="/api")
# Product Image router
app.include_router(product_image_router, tags=["Product Image"], prefix="/api")