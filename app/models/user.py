from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer, String

class UserModel(BaseModel):
  username: str
  password: str

meta = MetaData()

Users = Table(
  'Users', meta,
  Column('UID', Integer, primary_key=True, autoincrement=True),
  Column('USERNAME', String),
  Column('PASSWORD', String),
)
