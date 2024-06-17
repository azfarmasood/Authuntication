from typing import Sequence
from db.db import DB_SESSION
from sqlmodel import select
from models.user_models import UserRES, UserREQ
from fastapi import HTTPException
from sqlmodel import select
from security.secrets import (hash_password, verify_password, strong_password, phone_number_strict, strict_email_methods)

# This will genrate all user data
def get_all_user_data(db:DB_SESSION):
    all_users:Sequence[UserRES] = db.exec(select(UserRES)).all()
    return all_users

# This will create user data
def create_users(user: UserREQ, db: DB_SESSION):
    user_exists: UserRES | None = db.exec(select(UserRES).where(UserRES.username == user.username).where(UserRES.email == user.email)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Some one with this Email and User name is already exists")
    
    if not strict_email_methods(user.email):
        raise HTTPException(status_code=400, detail="Your Email is not valid")
    
    if not strong_password(user.password):
        raise HTTPException(status_code=400, detail="Your password is not strong enough please recreate your password and your password must be in (upper, lower, number, special characters)")
    
    if not phone_number_strict(user.phone_number):
        raise HTTPException(status_code=400, detail="please use only pakistani number")
    
    create_user: UserRES = UserRES()
    create_user.first_name = user.first_name
    create_user.last_name = user.last_name
    create_user.username = user.username
    create_user.email = user.email
    create_user.password =  hash_password(user.password)
    create_user.phone_number = user.phone_number
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user



# This Will Login User With Correct Credentials:

def get_login_user(username: str, password: str, db: DB_SESSION):
    user = db.exec(select(UserRES).where(UserRES.username == username)).first()

    if not user:
        raise HTTPException(status_code=400, detail="Your Email or User name is not correct")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Your Password is not correct")
    
    return user