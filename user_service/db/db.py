from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy import Engine
from starlette.config import Config
from sqlmodel import Session, SQLModel, create_engine

try:
    config: Config = Config(".env")
except FileNotFoundError as error:
    print(error)
    

db: str = config("DATABASE_URL", cast = str)
algorithem: str = config("ALGORITHEM", cast = str)
secret_key: str = config("SECRET_KEY", cast = str)
access_token: timedelta = timedelta(minutes=int(config("ACCESS_TOKEN", cast = int)))
refresh_token: timedelta = timedelta(days=int(config("REFRESH_TOKEN", cast=int)))

connection_string: str = str(db).replace("postgresql", "postgresql+psycopg")

engine: Engine = create_engine(connection_string, pool_pre_ping = True, echo = True, pool_recycle = 300, max_overflow = 0)


async def create_tables(app:FastAPI):
    print(f"create_tables...{app}")
    SQLModel.metadata.create_all(bind = engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session
        
DB_SESSION = Annotated[Session, Depends(get_session)]