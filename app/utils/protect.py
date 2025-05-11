from fastapi import HTTPException, Request
import jwt
from dotenv import load_dotenv
import os
from app.models.user import Users
from datetime import datetime, timedelta
from functools import lru_cache

load_dotenv()

# Cache user verification for 5 minutes
@lru_cache(maxsize=1000)
def verify_user(username: str, timestamp: int) -> bool:
  try:
    result = Users.select().where(Users.c.USERNAME == username)
    if result.fetchone() is None:
      return False
    return True
  except Exception as e:
    print(f"Error occured in verify_user: {e}")
    return False

def protect_route(request: Request):
  try:
    # Get auth header
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
      raise HTTPException(status_code=401, detail="Unauthorized")

    # Extract and decode jwt
    token = auth_header.split(" ")[1]
    token = jwt.decode(token, os.environ.get("JWT_KEY"), algorithms="HS256")

    # Check if token is expired
    if datetime.fromtimestamp(token["exp"]) < datetime.utcnow():
      raise HTTPException(status_code=401, detail="Token expired")
    
    # Verify user
    current_window = int(datetime.utcnow().timestamp() / 300)
    if not verify_user(token["username"], current_window):
      raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Update request headers
    request.headers.update({"username": token["username"]})
    return True
  except Exception as e:
    print(f"Error occured in protect_route: {e}")
    raise HTTPException(status_code=500, detail="Error occured")