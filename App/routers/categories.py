from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

# Create a new category
@router.post("/", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get all categories
@router.get("/", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories