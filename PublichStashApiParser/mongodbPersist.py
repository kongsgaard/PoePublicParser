from pymongo import MongoClient
import atexit

class MongoDbPersist:
    def __init__(self, host, port, db_name, collection_name, logger=None):
        self.logger=logger
        self.client = MongoClient(host,port)
        self.conn_params = host + ':' + str(port) + '/' + db_name + '.' + collection_name  
        db = self.client[db_name]

        self.collection = db[collection_name]
        atexit.register(self.cleanup)

    def cleanup(self):
        self.client.close()

    def persist_json(self, json):
        if self.logger is not None:
            self.logger.info('Writing to mongoDb: %s' % self.conn_params)
        self.collection.insert_one(json)
