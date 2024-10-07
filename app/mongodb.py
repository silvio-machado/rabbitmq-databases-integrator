# app/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
from app.singleton_meta import SingletonMeta
from app.settings import MongoConfig

class MongoDBConnection(metaclass=SingletonMeta):
    def __init__(self):
        self._client = None
        self.config = MongoConfig()
        self._db = None
    
    def connect(self):
        if self._client is None:
            self._client = AsyncIOMotorClient(self.config.mongo_uri)
            self._db = self._client[self.config.database]
    
    def get_database(self):
        if self._db is None:
            self.connect()
        return self._db
    
    def get_collection(self):
        db = self.get_database()
        return db[self.config.collection]
    
    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
