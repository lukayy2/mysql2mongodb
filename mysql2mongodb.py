#!/usr/bin/env python3

# converts Mysql Table to MongoDB Collection
## adds Validation to Collection
## all non-nullable Columns are required in the Collection
## Datatypes from mysql are converted into BSON Datatypes

from src.MysqlDatabase import MysqlDatabase
from src.Mysql2MongoConverter import Mysql2MongoConverter
from src.MongoDatabase import MongoDatabase

dictMysqlServerConnectionData = {
    'host': '192.168.178.22',
    'user': 'testuser',
    'password': 'test123',
    'database': 'testdb',
    'table': 'Log'
}

dictMongoDBServerConnectionData = {
    'host': '192.168.178.35',
    'user': 'client',
    'password': 'RTB68ZzZWs',
    'database': 'testdb',
    'collection': 'Log'
}

objMysql2MongoConverter = Mysql2MongoConverter()
objMysqlDatabase = MysqlDatabase(dictMysqlServerConnectionData)

listColumnDetails = objMysqlDatabase.fetchColumnDetailsOfTable(dictMysqlServerConnectionData['table'])

dictMongoDBCollectionValidation = objMysql2MongoConverter.createMongoDBCollectionValidationFromMysqlColumns(listColumnDetails)

#arrColumnNames = dictColumnDetails.keys()
#arrColumnDataTypes = dictColumnDetails.values()

#objMysqlDatabase.query(dictMysqlServerConnectionData['table'],0,1000)

objMongoDatabase = MongoDatabase(dictMongoDBServerConnectionData)
objMongoDatabase.dropCollectionIfExists(dictMongoDBServerConnectionData['collection'])
objMongoDatabase.createCollectionWithValidator(dictMongoDBServerConnectionData['collection'], dictMongoDBCollectionValidation)

