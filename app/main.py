from fastapi import FastAPI, Depends
from app.routes.auth import router as auth_router
from app.routes.games import router as games_router
from app.utils.protect import protect_route

app = FastAPI()
app.include_router(auth_router, prefix="/auth") 
app.include_router(games_router, prefix="/games"
  # dependencies=[Depends(protect_route)]
)

@app.get("/")
def root():
  return {"message": "Hello World"}