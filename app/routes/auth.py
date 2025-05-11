from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import datetime
import jwt
import os
from app.models.user import UserModel, Users
from app.models.games import Games
from app.db.connect import conn
from app.utils.hash import hash_password, verify_password

load_dotenv()

router = APIRouter()

@router.post("/register")
def register(user: UserModel):
  try:
    # check for unique username
    s = Users.select().where(Users.c.USERNAME == user.username)
    result = conn.execute(s)
    if result.fetchone() is not None:
      raise HTTPException(status_code=400, detail="Error: Username already exists")

    hashed_password = hash_password(user.password)

    u_ins = Users.insert().values(USERNAME=user.username, PASSWORD=hashed_password)
    g_ins = Games.insert().values(USERNAME=user.username, TRACKED=[], WISHLIST=[])
    conn.execute(u_ins)
    conn.execute(g_ins)
    conn.commit()

    payload = {
      "iss": "horizon-backend",
      "aud": "horizon-frontend",
      "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
      "username": user.username
    }
    encoded = jwt.encode(payload, os.environ.get('JWT_KEY'), algorithm="HS256")
    return {"token": encoded}
  except Exception as e:
    print(f"Error occured in /auth/register: {e}")
    raise HTTPException(status_code=500, detail="Error occured")

@router.post("/login")
def login(user: UserModel):
  try:
    # select row with username
    s = Users.select().where(Users.c.USERNAME == user.username)
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
      raise HTTPException(status_code=404, detail="Error: Username not found")

    # match passwords (hashed)
    if not verify_password(user.password, row.PASSWORD):
      raise HTTPException(status_code=400, detail="Error: Invalid Password")

    payload = {
      "iss": "horizon-backend",
      "aud": "horizon-frontend",
      "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
      "username": user.username
    }
    encoded = jwt.encode(payload, os.environ.get('JWT_KEY'), algorithm="HS256")
    return {"token": encoded}
  except Exception as e:
    print(f"Error occured in /auth/login: {e}")
    raise HTTPException(status_code=500, detail="Error occured")
