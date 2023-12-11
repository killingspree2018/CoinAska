import mysql.connector

database_password = '12345'
http_api_key = b'95a609b954ab2e7f235843ed452e3f97'
http_secret_key = b'f724b35459d93f92e93c0c5e1cbe239c'

# http_api_key = b'd44b34ef0e43e3ddc0791a8bd9dc7d6d'
# http_secret_key = b'f7bf170e77f2e67e9116bf42ca7617c6'

# f7bf170e77f2e67e9116bf42ca7617c6
# d44b34ef0e43e3ddc0791a8bd9dc7d6d

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