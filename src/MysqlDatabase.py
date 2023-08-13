import mysql.connector


class MysqlDatabase:

    def __init__(self, dictConnectionData):
        self.objSourceDB = mysql.connector.connect(
            host=dictConnectionData['host'],
            user=dictConnectionData['user'],
            password=dictConnectionData['password'],
            database=dictConnectionData['database']
        )

    def fetchCreateCode(self, strTableName):
        objCursor = self.objSourceDB.cursor()
        objCursor.execute("SHOW CREATE TABLE `{0}`.`{1}`;".format(self.objSourceDB.database, strTableName))

        objResultCreateTable = objCursor.fetchone()

        return objResultCreateTable[1]
