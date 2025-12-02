from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a transaction
@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Check if category exists
    category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_transaction = models.Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category_id=transaction.category_id,
        # For now, we assume a single user (user_id=1) until we add JWT auth dependency
        user_id=1  
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# List all transactions
@router.get("/", response_model=list[schemas.TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return transactions
