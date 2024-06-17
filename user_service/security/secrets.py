from fastapi import HTTPException
from passlib.context import CryptContext
import re

# This Will Strict Email Domains While Creating Emails
def strict_email_methods(email: str) -> bool:
    pattern = r'^(.+)@(gmail\.com|outlook\.com|yahoo\.com)$'
    if not re.match(pattern, email):
        raise HTTPException(status_code=400, detail="Your domain name is incorrect please use the following email patterns (gmail.com/outlook.com/yahoo.com)")
    return True

def phone_number_strict(phone_number: str) -> bool:
    if len(phone_number) != 11:
        raise HTTPException(status_code=400, detail="Use only pakistani number that used for only 11 digits")
    return True

# This Will ask the user to create strong password
def strong_password(password: str) -> bool:
    SPECIAL_CHARACTER = ['!', '@', '#', '$', '%', '^', '&', '*', '=', ':', '?', '.', '/', '~', '<', '>']
    if len(password) < 8 or len(password) > 20:   
        raise HTTPException(status_code=400, detail="Your Password must be between 8 or 20 characters")
    
    if not any(character.isupper() for character in password) or not any(character.islower() for character in password) or not any(character.isdigit() for character in password) or not any(character in SPECIAL_CHARACTER for character in password):
        raise HTTPException(status_code=400, detail="Your password must be upper, lower, number and special characters")
    
    return True
    
# Convert string password in to hashing password
def hash_password(password: str):
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password: str = pwd_context.hash(password)
    return hashed_password

# This will verify plain password in to hashpassword and converting in to hash digits
def verify_password(plain_password:str, hash_password: str):
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hash = hash_password)