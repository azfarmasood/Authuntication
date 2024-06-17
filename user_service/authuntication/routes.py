from fastapi import FastAPI
from db.db import create_tables
from routes.user_routes import router

app: FastAPI = FastAPI(lifespan=create_tables)

app.include_router(router=router)