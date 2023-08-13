import pymongo


class MongoDatabase:

    def __init__(self, dictConnectionData):
        self.objClient = pymongo.MongoClient(
            "mongodb://{1}:{2}@{0}:27017/?authMechanism=DEFAULT".format(
                dictConnectionData['host'],
                dictConnectionData['user'],
                dictConnectionData['password']
            )
        )

        self.objDB = self.objClient[dictConnectionData['database']]
        print(self.objDB)

    def createCollection(self, strCollectionName):
        """
        Creates Collection (drops it, if it exists already)

        :param strCollectionName:
        :return:
        """
        listCollectionNames = self.objDB.list_collection_names()

        if strCollectionName in listCollectionNames:
            objCollection = self.objDB[strCollectionName]
            objCollection.drop()

        objCollection = self.objDB[strCollectionName]

    def insertMulti(self, strCollectionName, listDocuments):
        """

        :param strCollectionName:
        :param listDocuments: -> List of Dictionaries
        :return:
        """
        objCollection = self.objDB[strCollectionName]
        objResult = objCollection.insert_many(listDocuments, True)

        return objResult.inserted_ids
