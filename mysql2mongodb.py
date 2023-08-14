#!/usr/bin/env python3
import sys

# converts Mysql Table to MongoDB Collection
## adds Validation to Collection
## all non-nullable Columns are required in the Collection
## Datatypes from mysql are converted into BSON Datatypes

from src.MysqlDatabase import MysqlDatabase
from src.Mysql2MongoConverter import Mysql2MongoConverter
from src.MongoDatabase import MongoDatabase

intSelectLimit = 100

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

# mysql connect and get Column Details
print('[MYSQL] Connect...')
objMysqlDatabase = MysqlDatabase(dictMysqlServerConnectionData)
print('[MYSQL] connected to MysqlServer at {0}, conn ID: '.format(dictMysqlServerConnectionData['host']) + str(objMysqlDatabase.objDB.connection_id))
print('[MYSQL] fetching Details for Table: ' + dictMysqlServerConnectionData['table'])
listColumnDetails = objMysqlDatabase.fetchColumnDetailsOfTable(dictMysqlServerConnectionData['table'])

objMysql2MongoConverter = Mysql2MongoConverter()
dictMongoDBCollectionValidation = objMysql2MongoConverter.createMongoDBCollectionValidationFromMysqlColumns(listColumnDetails)

print('[MONGODB] Connect...')
objMongoDatabase = MongoDatabase(dictMongoDBServerConnectionData)
print('[MONGODB] connected to MongoDB ' + str(objMongoDatabase.objDB))

print('[MONGODB] Dopping Collection: ' + dictMongoDBServerConnectionData['collection'])
objMongoDatabase.dropCollectionIfExists(dictMongoDBServerConnectionData['collection'])
# convert Mysql Table to MongoDB Collection with Validation
print('[MONGODB] creating new Collection with Validation')
objMongoDatabase.createCollectionWithValidator(dictMongoDBServerConnectionData['collection'], dictMongoDBCollectionValidation)


# only for stats, could change if data is inserted while the copy is running
intCountRowsAtStart = objMysqlDatabase.fetchTotalRowsOfTable(dictMysqlServerConnectionData['table'])

intTotalMysqlRowsCounted = 0
intSelectedMysqlRows = 0
intSelectCounter = 0

print('[MYSQL] total rows in Table: ' + str(intCountRowsAtStart))
print('')

boolDataToCopy = True

while boolDataToCopy:
    intLimitStart = intSelectCounter * intSelectLimit
    listMysqlRows = objMysqlDatabase.query(dictMysqlServerConnectionData['table'], intLimitStart, intSelectLimit)
    intSelectCounter += 1

    if len(listMysqlRows) > 0:
        objMongoDatabase.insertMulti(dictMongoDBServerConnectionData['collection'],
                                     Mysql2MongoConverter.convertMysqlListToMongoDBDict(listMysqlRows,
                                                                                        listColumnDetails))

    sys.stdout.write('copy (' + str(intLimitStart + intSelectLimit) + '/' + str(intCountRowsAtStart) + ') ' + str(round((intLimitStart + intSelectLimit) * 100 / intCountRowsAtStart)) + '%\r')

    # Number of Rows does not match the limit? we reached the end!
    if len(listMysqlRows) != intSelectLimit:
        boolDataToCopy = False
        print("all data copied!")


