from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.product_router import product_router
from .routers.category_router import category_router
from .db import Base, engine, get_db


app = FastAPI()

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

