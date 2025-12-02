from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Create a transaction
@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if category exists
    category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Validate transaction type
    if transaction.type not in ["income", "expense"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction type must be either 'income' or 'expense'"
        )

    new_transaction = models.Transaction(
        amount=transaction.amount,
        type=transaction.type,
        category_id=transaction.category_id,
        user_id=current_user.id  # Use authenticated user's ID
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    # Fetch the category relationship
    db.refresh(new_transaction, ['category'])
    return new_transaction

# List all transactions for the current user
@router.get("/", response_model=list[schemas.TransactionOut])
def list_transactions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(models.Transaction)\
        .filter(models.Transaction.user_id == current_user.id)\
        .all()
    return transactions