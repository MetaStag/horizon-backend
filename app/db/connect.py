import os
from dotenv import load_dotenv
import urllib.parse
from sqlalchemy import create_engine

load_dotenv()

try:
  connection_string = os.environ.get("AZURE_SQL_CONNECTIONSTRING")

  # Some string manipulation to make it work with sqlalchemy
  params = urllib.parse.quote(connection_string)
  url = f"mssql+pyodbc:///?odbc_connect={params}"

  # Create sqlalchemy engine and connection
  engine = create_engine(url, echo=True)
  conn = engine.connect()
except Exception as e:
  print(e)
  exit()