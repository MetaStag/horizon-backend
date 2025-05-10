from fastapi import FastAPI
from app.db.connect import cursor, conn

# Import routes
from app.routes import auth

app = FastAPI()
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def root():
  try:
    return {"message": "Hello World"}
  except Exception as e:
    print(e)
    return {"message": "Error occured"}