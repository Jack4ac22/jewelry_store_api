from fastapi import FastAPI
from db import models
from db.database import database_engine
from routers import user, image, auth, address_router

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(address_router.router)
app.include_router(image.router)


models.Base.metadata.create_all(bind=database_engine)
