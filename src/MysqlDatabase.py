import mysql.connector


class MysqlDatabase:

    def __init__(self, dictConnectionData):
        self.objDB = mysql.connector.connect(
            host=dictConnectionData['host'],
            user=dictConnectionData['user'],
            password=dictConnectionData['password'],
            database=dictConnectionData['database']
        )

    def fetchColumnDetailsOfTable(self, strTableName):
        """
        Load Column Details of given Table

        :param strTableName:
        :return:
        """
        objCursor = self.objDB.cursor(buffered=True)
        objCursor.execute("SELECT COLUMN_NAME, IS_NULLABLE, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{0}' AND TABLE_NAME = '{1}';".format(self.objDB.database, strTableName))

        listColumnDetails = []

        for arrRow in objCursor:
            listColumnDetails.append(arrRow)

        return listColumnDetails

    def fetchTotalRowsOfTable(self, strTableName):
        objCursor = self.objDB.cursor()
        objCursor.execute('SELECT COUNT(*) FROM {0}'.format(strTableName))

        dictResult = objCursor.fetchone()

        return dictResult[0]

    def query(self, strTableName, intLimitStart, intLimitEnd):
        objCursor = self.objDB.cursor(buffered=True)
        objCursor.execute('SELECT * FROM {0} LIMIT {1},{2}'.format(strTableName, intLimitStart, intLimitEnd))

        listResult = []

        for row in objCursor:
            listResult.append(row)

        return listResult