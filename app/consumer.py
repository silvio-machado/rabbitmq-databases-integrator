# app/consumer.py

import asyncio
import json
from aio_pika import IncomingMessage
from app.rabbitmq import RabbitMQConnection
from app.services import delete_records

QUEUE_NAME = 'device_to_clean'  # Replace with your actual queue name

async def start_consumer():
    rabbitmq_conn = RabbitMQConnection()
    await rabbitmq_conn.connect()
    channel = await rabbitmq_conn.get_channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await process_message(message)

async def process_message(message: IncomingMessage):
    async with message.process():
        try:
            message_body = json.loads(message.body.decode())
            # Extract the necessary information from the message
            # For example, assuming the message has a 'user_id' field:
            user_id = message_body.get('user_id')
            if not user_id:
                print("user_id not found in message.")
                return
            print(f"Received message: {message_body}")
            # Call the service function to delete records
            await delete_records(user_id)
            print(f"Processed user_id {user_id} successfully.")
        except Exception as e:
            print(f"Error processing message: {e}")
