from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.transaction import Transaction
from app.services.fraud_detection import predict_fraud
import time

router = APIRouter()

@router.post("/transactions/")
def create_transaction(amount: float, account_balance: float, db: Session = Depends(get_db)):
    """Handles transactions and performs fraud detection"""
    transaction_time = int(time.time() % 86400)

    # Fraud detection
    is_fraudulent = predict_fraud(amount, account_balance, transaction_time)

    if is_fraudulent:
        raise HTTPException(status_code=403, detail="Fraudulent transaction detected")

    # Create and store the transaction
    new_transaction = Transaction(amount=amount, account_balance=account_balance)
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {"message": "Transaction successful"}
