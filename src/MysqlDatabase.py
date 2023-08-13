import mysql.connector


class MysqlDatabase:

    def __init__(self, dictConnectionData):
        self.objDB = mysql.connector.connect(
            host=dictConnectionData['host'],
            user=dictConnectionData['user'],
            password=dictConnectionData['password'],
            database=dictConnectionData['database']
        )

    def fetchCreateCode(self, strTableName):
        objCursor = self.objDB.cursor()
        objCursor.execute("SHOW CREATE TABLE `{0}`.`{1}`;".format(self.objDB.database, strTableName))

        objResultCreateTable = objCursor.fetchone()

        return objResultCreateTable[1]
