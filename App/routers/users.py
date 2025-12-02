from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..dependencies import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(400, "Username already exists")

    hashed = auth.hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(400, "Invalid credentials")
    
    # Include both username AND user_id in the token
    token_data = {"sub": db_user.username, "user_id": db_user.id}
    token = auth.create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}