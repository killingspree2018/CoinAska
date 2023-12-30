import mysql.connector
from settings import database_password

config = {
  'user': 'admin',
  'password': database_password,
  'host': 'localhost',
  'database': 'CoinAska',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()
# cnx.close()