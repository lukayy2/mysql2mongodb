import datetime

import bson

class Mysql2MongoConverter:

    def createMongoDBCollectionValidationFromMysqlColumns(self, listMysqlColumnDetails):
        dictSchema = {}
        listRequiredCols = []
        dictProperties = {}

        for arrColumn in listMysqlColumnDetails:
            strColumnName = arrColumn[0]
            strIsNullable = arrColumn[1]
            strDataType = arrColumn[2]
            strColumnType = arrColumn[3]

            # if Column ist NOT Nullable on the Mysql Table, it will be "required" on the MongoDB Collection
            if strIsNullable == 'NO':
                listRequiredCols.append(strColumnName)

            dictProperties[strColumnName] = {'bsonType': self.__convertMysqlDatatypesToBSON(strDataType)}

        dictSchema['title'] = 'Collection Validation'
        dictSchema['bsonType'] = 'object'
        dictSchema['required'] = listRequiredCols
        dictSchema['properties'] = dictProperties

        tmp = {}
        tmp['$jsonSchema'] = dictSchema
        return tmp

    @staticmethod
    def convertMysqlListToMongoDBDict(listMysqlRows, listMysqlColumnDetails):
        """
        Converts List of Columns from Mysql to Dict for insert into Mongo

        :param listMysqlColumnDetails:
        :param listMysqlRows:
        :return:
        """

        listMongoDBMultiInsert = []

        for listMysqlRow in listMysqlRows:
            dictMongoDBDocument = {}

            for i in range(len(listMysqlColumnDetails)):
                strMysqlDataType = listMysqlColumnDetails[i][2]
                mysqlColumnValue = listMysqlRow[i]

                if mysqlColumnValue is not None:

                    # convertion of "set" Value into a string (using first Value from SET-Field)
                    if type(mysqlColumnValue) is set:
                        mysqlColumnValue = mysqlColumnValue.pop()

                    # convert mysql unsinged int to 64bit Int for MongoDB
                    if strMysqlDataType == 'uint':
                        mysqlColumnValue = bson.int64.Int64(mysqlColumnValue)

                    # Date values come in "Datetime" Object from Mysql-Library, convert to normal date, without the Time-part
                    if strMysqlDataType == 'date':
                        mysqlColumnValue = datetime.datetime.strptime(mysqlColumnValue.isoformat(), "%Y-%m-%d")

                    dictMongoDBDocument[listMysqlColumnDetails[i][0]] = mysqlColumnValue

            listMongoDBMultiInsert.append(dictMongoDBDocument)

        return listMongoDBMultiInsert

    @staticmethod
    def __convertMysqlDatatypesToBSON(strMysqlDatatype):
        """

        :param strMysqlDatatype:
        :return:
        """
        switch = {
            'int': 'int',
            'tinyint': 'int',
            'smallint': 'int',
            'mediumint': 'int',
            'uint': 'long',
            'bigint': 'long',
            'datetime': 'date',
            'date': 'date',
            'decimal': 'double',
            'double': 'double'
        }

        # switch-case with default case "string"
        return switch.get(strMysqlDatatype, 'string')