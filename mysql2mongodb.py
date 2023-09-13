#!/usr/bin/env python3
import sys

from src.CliInputParser import CliInputParser
from src.MysqlDatabase import MysqlDatabase
from src.Mysql2MongoConverter import Mysql2MongoConverter
from src.MongoDatabase import MongoDatabase

# converts Mysql Table to MongoDB Collection
## adds Validation to Collection
## all non-nullable Columns are required in the Collection
## Datatypes from mysql are converted into BSON Datatypes

objInputParser = CliInputParser()
config = objInputParser.parse()

intSelectLimit = int(config['default']['selectlimit'])

# mysql connect and get Column Details
print('[MYSQL] Connect...')
objMysqlDatabase = MysqlDatabase(config['mysql'])
print('[MYSQL] connected to MysqlServer at {0}, conn ID: '.format(config['mysql']['host']) + str(objMysqlDatabase.objDB.connection_id))
print('[MYSQL] fetching Details for Table: ' + config['mysql']['table'])
listColumnDetails = objMysqlDatabase.fetchColumnDetailsOfTable(config['mysql']['table'])

objMysql2MongoConverter = Mysql2MongoConverter()
dictMongoDBCollectionValidation = objMysql2MongoConverter.createMongoDBCollectionValidationFromMysqlColumns(listColumnDetails)

print('[MONGODB] Connect...')
objMongoDatabase = MongoDatabase(config['mongodb'])
print('[MONGODB] connected to MongoDB ' + str(objMongoDatabase.objDB))

print('[MONGODB] Dopping Collection: ' + config['mongodb']['collection'])
objMongoDatabase.dropCollectionIfExists(config['mongodb']['collection'])
# convert Mysql Table to MongoDB Collection with Validation
print('[MONGODB] creating new Collection with Validation')
objMongoDatabase.createCollectionWithValidator(config['mongodb']['collection'], dictMongoDBCollectionValidation)


# only for stats, could change if data is inserted while the copy is running
intCountRowsAtStart = objMysqlDatabase.fetchTotalRowsOfTable(config['mysql']['table'])

intTotalMysqlRowsCounted = 0
intSelectedMysqlRows = 0
intSelectCounter = 0

print('[MYSQL] total rows in Table: ' + str(intCountRowsAtStart))
print('')

boolDataToCopy = True

while boolDataToCopy:
    intLimitStart = intSelectCounter * intSelectLimit
    listMysqlRows = objMysqlDatabase.query(config['mysql']['table'], intLimitStart, intSelectLimit)
    intSelectCounter += 1

    if len(listMysqlRows) > 0:
        objMongoDatabase.insertMulti(config['mongodb']['collection'],
                                     Mysql2MongoConverter.convertMysqlListToMongoDBDict(listMysqlRows,
                                                                                        listColumnDetails))

    sys.stdout.write('copy (' + str(intLimitStart + intSelectLimit) + '/' + str(intCountRowsAtStart) + ') ' + str(round((intLimitStart + intSelectLimit) * 100 / intCountRowsAtStart)) + '%\r')

    # Number of Rows does not match the limit? we reached the end!
    if len(listMysqlRows) != intSelectLimit:
        boolDataToCopy = False
        print('')
        print("all data copied!")


