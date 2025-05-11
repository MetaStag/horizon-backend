from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, JSON

class GameModel(BaseModel):
  gameID: int
  rating: int

class GameIDModel(BaseModel):
  gameID: int

meta = MetaData()

Games = Table(
  'Games', meta,
  Column('GID', Integer, primary_key=True, autoincrement=True),
  Column('USERNAME', String),
  Column('TRACKED', JSON),
  Column('WISHLIST', JSON)
)