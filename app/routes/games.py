from fastapi import APIRouter, HTTPException, Request
from app.models.games import GameIDModel, GameModel, Games
from app.db.connect import conn

router = APIRouter()

def get_data(username: str) -> dict:
  data = Games.select().where(Games.c.USERNAME == username)
  result = conn.execute(data)
  result = result.fetchone()
  return result

@router.get("/tracked")
def get_tracked_games(request: Request):
  try:
    # Extract games data from username
    username = request.headers.get("username")
    result = get_data(username)

    print(result)
    return {"message": "no"}

  except Exception as e:
    print(f"Error occured in /games/tracked: {e}")
    raise HTTPException(status_code=500, detail="Error occured")

@router.post("/tracked/add")
def add_tracked_game(game: GameIDModel):
  try:
    username = request.headers.get("username")
    result = get_data(username)

    # Add game to tracked games
    result.TRACKED.append({game.gameID, 0})

    # Update tracked games
    data = Games.update().values(TRACKED=result.TRACKED).where(Games.c.USERNAME == username)
    conn.execute(data)
    conn.commit()
    return {"message": "no"}

  except Exception as e:
    print(f"Error occured in /games/tracked/add: {e}")
    raise HTTPException(status_code=500, detail="Error occured")

@router.delete("/tracked/remove")
def remove_tracked_game(game: GameModel):
  try:
    username = request.headers.get("username")

    # Get tracked games
    result = get_data(username)
    
    # Remove game from tracked games
    for game in result.TRACKED:
      if game[0] == game.gameID:
        result.TRACKED.remove(game)

    # Update tracked games
    data = Games.update().values(TRACKED=result.TRACKED).where(Games.c.USERNAME == username)
    conn.execute(data)
    conn.commit()
    return {"message": "no"}
  except Exception as e:
    print(f"Error occured in /games/tracked/remove: {e}")
    raise HTTPException(status_code=500, detail="Error occured")
    
@router.get("/wishlist")
def get_wishlist_games(request: Request):
  try:
    username = request.headers.get("username")
    result = get_data(username)
    
    print(result)
    return {"message": "no"}

  except Exception as e:
    print(f"Error occured in /games/wishlist: {e}")
    raise HTTPException(status_code=500, detail="Error occured")

@router.post("/wishlist/add")
def add_wishlist_game(game: GameModel):
  try:
    username = request.headers.get("username")

    # Get wishlist games
    result = get_data(username)

    # Add game to wishlist games
    result.WISHLIST.append(game.gameID)

    # Update wishlist games
    data = Games.update().values(WISHLIST=result.WISHLIST).where(Games.c.USERNAME == username)
    conn.execute(data)
    conn.commit()
    return {"message": "no"}
    
  except Exception as e:
    print(f"Error occured in /games/wishlist/add: {e}")
    raise HTTPException(status_code=500, detail="Error occured")

@router.delete("/wishlist/remove")
def remove_wishlist_game(game: GameModel):
  try:
    username = request.headers.get("username")

    # Get wishlist games
    result = get_data(username)

    # Remove game from wishlist games
    for game in result.WISHLIST:
      if game == game.gameID:
        result.WISHLIST.remove(game)

    # Update wishlist games
    data = Games.update().values(WISHLIST=result.WISHLIST).where(Games.c.USERNAME == username)
    conn.execute(data)
    conn.commit()
    return {"message": "no"}
  except Exception as e:
    print(f"Error occured in /games/wishlist/remove: {e}")
    raise HTTPException(status_code=500, detail="Error occured")
