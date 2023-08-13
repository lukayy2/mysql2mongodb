#!/usr/bin/env python3

from src.MysqlDatabase import MysqlDatabase
from src.Mysql2MongoConverter import Mysql2MongoConverter

dictMysqlServerConnectionData = {
    'host': '192.168.178.22',
    'user': 'testuser',
    'password': 'test123',
    'database': 'testdb',
    'table': 'Log'
}

# dictMongoDBServerConnectionData = {
#     'host': '192.168.178.35',
#     'user': 'client',
#     'password': 'RTB68ZzZWs',
#     'database': 'testdb',
#     'collection': 'Log'
# }

objMysqlDatabase = MysqlDatabase(dictMysqlServerConnectionData)
strSourceTableCreateCode = objMysqlDatabase.fetchCreateCode(dictMysqlServerConnectionData['table'])

