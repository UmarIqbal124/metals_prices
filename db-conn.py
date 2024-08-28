import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root' ,
    password = '',
    database = 'metals_prices'
)
print(mydb)