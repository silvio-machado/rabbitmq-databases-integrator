# app/main.py

import asyncio
from fastapi import FastAPI
from app.consumer import start_consumer
from app.mysql import MySQLConnection
from app.mongodb import MongoDBConnection
from app.rabbitmq import RabbitMQConnection

app = FastAPI()
consumer_task = None

@app.on_event("startup")
async def startup_event():
    global consumer_task
    # Initialize connections
    mysql_conn = MySQLConnection()
    await mysql_conn.connect()
    mongo_conn = MongoDBConnection()
    mongo_conn.connect()
    rabbitmq_conn = RabbitMQConnection()
    await rabbitmq_conn.connect()
    # Start the consumer task
    consumer_task = asyncio.create_task(start_consumer())
    print("Application started.")

@app.on_event("shutdown")
async def shutdown_event():
    global consumer_task
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass
    # Close connections
    mysql_conn = MySQLConnection()
    await mysql_conn.close()
    mongo_conn = MongoDBConnection()
    mongo_conn.close()
    rabbitmq_conn = RabbitMQConnection()
    await rabbitmq_conn.close()
    print("Application shutdown.")

@app.get("/health")
async def health_check():
    return {'status': 'ok'}
