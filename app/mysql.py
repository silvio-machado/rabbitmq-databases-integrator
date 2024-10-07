# app/mysql.py

import aiomysql
from app.singleton_meta import SingletonMeta
from app.settings import MySQLConfig

class MySQLConnection(metaclass=SingletonMeta):
    def __init__(self):
        self._pool = None
        self.config = MySQLConfig()
    
    async def connect(self):
        if self._pool is None:
            self._pool = await aiomysql.create_pool(
                host=self.config.host,
                port=3306,
                user=self.config.user,
                password=self.config.password,
                db=self.config.database,
                minsize=1,
                maxsize=5,
            )
    
    async def get_connection(self):
        if self._pool is None:
            await self.connect()
        return await self._pool.acquire()
    
    async def close(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None
