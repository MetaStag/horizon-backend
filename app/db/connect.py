import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_conn():
  return pyodbc.connect(connection_string)

try:
  connection_string = os.environ.get("AZURE_SQL_CONNECTIONSTRING")
  conn = get_conn()
  cursor = conn.cursor()
except Exception as e:
  print(e)
  exit()