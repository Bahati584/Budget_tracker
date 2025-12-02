from pydantic import BaseModel, validator
from datetime import datetime
import re

class UserCreate(BaseModel):
    username: str
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric (letters and numbers only)')
        return v

class UserOut(BaseModel):
    id: int
    username: str
    
    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    amount: float
    type: str  # "income" or "expense"
    category_id: int
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['income', 'expense']:
            raise ValueError('Type must be either "income" or "expense"')
        return v

class TransactionOut(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: datetime
    category: CategoryOut
    
    class Config:
        orm_mode = True