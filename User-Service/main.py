from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine


app = FastAPI(
    title = "User Service",
    description = "An API to manage users and authentication.",
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