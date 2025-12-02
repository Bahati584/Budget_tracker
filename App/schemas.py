from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

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
    type: str   # “income” or “expense”
    category_id: int

class TransactionOut(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: datetime
    category: CategoryOut
    class Config:
        orm_mode = True
