import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MySQLConfig:
    def __init__(self):
        logger.info("Loading MySQL configuration")
        self.user = os.getenv("MYSQL_USER", "root")
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.password = os.getenv("MYSQL_PASSWORD", "root")
        self.database = os.getenv("MYSQL_DATABASE", "test")


class MongoConfig:
    def __init__(self):
        logger.info("Loading Mongo configuration")
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.database = os.getenv("MONGO_DATABASE", "test")
        self.collection = os.getenv("MONGO_ACCESS_COLLECTION", "access")


class RabbitMQConfig:
    def __init__(self):
        logger.info("Loading RabbitMQ configuration")
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.port = os.getenv("RABBITMQ_PORT", 5672)