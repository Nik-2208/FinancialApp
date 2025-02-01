from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.models.user import User

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

@router.post("/register/")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with hashed password"""
    hashed_password = hash_password(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}
