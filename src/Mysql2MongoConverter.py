class Mysql2MongoConverter:

    def createMongoDBCollectionValidationFromMysqlColumns(self, listMysqlColumnDetails):
        dictSchema = {}
        listRequiredCols = []
        dictProperties = {}

        for arrColumn in listMysqlColumnDetails:
            strColumnName = arrColumn[0]
            strIsNullable = arrColumn[1]
            strDataType = arrColumn[2]

            # if Column ist NOT Nullable on the Mysql Table, it will be "required" on the MongoDB Collection
            if strIsNullable == 'NO':
                listRequiredCols.append(strColumnName)

            dictProperties[strColumnName] = {'bsonType': self.convertMysqlDatatypesToBSON(strDataType)}

        dictSchema['title'] = 'Collection Validation'
        dictSchema['bsonType'] = 'object'
        dictSchema['required'] = listRequiredCols
        dictSchema['properties'] = dictProperties

        tmp = {}
        tmp['$jsonSchema'] = dictSchema
        return tmp

    def convertMysqlDatatypesToBSON(self, strMysqlDatatype):
        """

        :param strMysqlDatatype:
        :return:
        """
        switch = {
            'int': 'int',
            'datetime': 'date',
            'date': 'date',
            'decimal': 'double'
        }

        # switch-case with default case "string"
        return switch.get(strMysqlDatatype, 'string')
