import os
import logging
from pymongo import MongoClient

_client = None
_collection = None


def get_db_client():
    global _client
    if _client is None:
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            logging.warning("MONGODB_URI not set. Database features will not persist.")
            return None
        try:
            _client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000, tls=True)
            _client.admin.command("ping")
            logging.info("Connected to MongoDB successfully.")
        except Exception as e:
            logging.exception(f"Failed to connect to MongoDB: {e}")
            _client = None
    return _client


def get_user_collection():
    global _collection
    if _collection is not None:
        return _collection
    client = get_db_client()
    if client:
        try:
            db = client.get_database("finance_app")
            collection = db.get_collection("user_finances")
            collection.create_index("user_email", unique=True)
            _collection = collection
            return collection
        except Exception as e:
            logging.exception(f"Error getting collection: {e}")
    return None