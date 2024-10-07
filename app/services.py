# app/services.py

import asyncio
from app.mysql import MySQLConnection
from app.mongodb import MongoDBConnection

async def delete_records(user_id):
    await asyncio.gather(
        delete_from_mysql(user_id),
        delete_from_mongodb(user_id)
    )

async def delete_from_mysql(user_id):
    mysql_conn = MySQLConnection()
    conn = await mysql_conn.get_connection()
    try:
        async with conn.cursor() as cursor:
            # Replace 'devices' with your actual table name
            # await cursor.execute("DELETE FROM devices WHERE user_id = %s", (user_id,))
            result = await cursor.execute("SELECT * FROM userDevice ud WHERE ud.user_id = %s", (user_id,))
            result = await cursor.fetchall()
            print("MYSQL Result: ", result)
            await conn.commit()
            print(f"Deleted records from MySQL for user_id {user_id}")
    except Exception as e:
        print(f"MySQL deletion error: {e}")
    finally:
        conn.close()

async def delete_from_mongodb(user_id):
    mongo_conn = MongoDBConnection()
    collection = mongo_conn.get_collection()
    try:
        print("User_id: ", user_id)
        # Replace 'devices' with your actual collection name
        # result = await collection.devices.sel({"user_id": user_id})
        result = collection.find({"user_id": user_id})
        documents = await result.to_list(length=None)
        print("MONGODB Result: ", documents)
        # print(f"Deleted {result.deleted_count} documents from MongoDB for user_id {user_id}")
    except Exception as e:
        print(f"MongoDB deletion error: {e}")
