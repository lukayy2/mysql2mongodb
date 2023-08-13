import mysql.connector

objSourceDB = mysql.connector.connect(
    host="192.168.178.22",
    user="testuser",
    password="test123",
    database="testdb"
)

strDatabase = "testdb"
strTable = "Log"

print(objSourceDB)
objCursor = objSourceDB.cursor()

objCursor.execute("SHOW CREATE TABLE `{0}`.`{1}`".format(strDatabase, strTable))

objResultCreateTable = objCursor.fetchone()

print(objResultCreateTable)