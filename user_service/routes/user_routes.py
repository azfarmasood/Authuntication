from typing import Annotated, Sequence
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.user_models import UserRES, UserREQ
from db.db import DB_SESSION
from auth_controllers.user_controller import get_all_user_data, create_users, get_login_user

router: APIRouter = APIRouter()

@router.get("/")
def hello_user():
    return {"message": "Hello User"}

@router.get("/all_users/", response_model=list[UserRES], status_code=status.HTTP_200_OK)
def get_all_users_data(db: DB_SESSION):
   data:Sequence[UserRES] = get_all_user_data(db = db)
   return data

@router.post("/signup/", response_model=UserRES, status_code=status.HTTP_201_CREATED)
def add_users(user:UserREQ, db: DB_SESSION):
    add_user_data = create_users(user = user, db = db)
    return add_user_data

@router.post("/login/", status_code=status.HTTP_200_OK)
def login_users(db: DB_SESSION, login:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_login_user(username = login.username, password = login.password, db = db)
    if not user:
        raise HTTPException(status_code=400, detail="Auth Faild")
    return 'Success full Authuntication'