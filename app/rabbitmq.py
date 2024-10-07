# app/rabbitmq.py

import asyncio
from aio_pika import connect_robust, Channel
from app.singleton_meta import SingletonMeta  # We'll create this metaclass
from app.settings import RabbitMQConfig

class RabbitMQConnection(metaclass=SingletonMeta):
    def __init__(self):
        self._connection = None
        self._channel = None
        self.config = RabbitMQConfig()
    
    async def connect(self):
        if self._connection is None or self._connection.is_closed:
            rabbitmq_url = f"amqp://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/"
            self._connection = await connect_robust(rabbitmq_url)
            self._channel = await self._connection.channel()
    
    async def get_channel(self) -> Channel:
        if self._channel is None or self._channel.is_closed:
            await self.connect()
        return self._channel
    
    async def close(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
