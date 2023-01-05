from db import models
from db.database import database_engine
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import user, image, auth, address_router, product


app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(address_router.router)
app.include_router(product.router)
app.include_router(image.router)


models.Base.metadata.create_all(bind=database_engine)
app.mount('/images', StaticFiles(directory='images'), name='images')
################# CORS resolving ##################
origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)
