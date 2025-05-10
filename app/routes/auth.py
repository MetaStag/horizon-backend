from fastapi import APIRouter, HTTPException
from app.models.user import User

router = APIRouter()


@router.post("/register")
def register(user: User):
  return {"message": "Regitration successful"}

@router.post("/login")
def login(user: User):
  return {"message": "Login successful"}
