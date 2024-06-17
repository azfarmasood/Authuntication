from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

# Create Users Base Start: 
# ======================================================

class UserBase(SQLModel):
    first_name: str = Field(default = str, regex = r'^[A-Za-z]*$' ,max_length = 20, nullable = False, index=True)
    last_name: str = Field(default = str, regex = r'^[A-Za-z]*$' ,max_length = 20, nullable = False, index=True)
    username: str = Field(default = str, regex = r'^[A-Za-z0-9]*$' ,max_length = 30, nullable=False, unique=True)
    email: str = Field(default = str, regex = r'^(.+)@(gmail\.com|outlook\.com|yahoo\.com)$', max_length = 50, nullable=False, unique=True)
    password: str = Field(default = str, max_length = 100, nullable=False)
    phone_number: str = Field(default = str, regex = r'^\+92\d{10}$', max_length = 11, nullable = False)
    

# Create Users Base End:
# ======================================================



# Create Users Res Body Start:
# ======================================================

class UserRES(UserBase, table=True):
    id: Optional[int] = Field(default = None, primary_key = True)
    is_verified: bool = Field(default = False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Create Users Res Body End:
# ======================================================



# Create Users Req Body Start:
# ======================================================

class UserREQ(SQLModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    phone_number: str
    is_verified: bool = False
    
# Create Users Req Body End:
# ======================================================


# Request Login Start:
# ======================================================

class LoginREQ(SQLModel):
    email: str
    username: str
    password: str
    
# Request Login END:
# ======================================================