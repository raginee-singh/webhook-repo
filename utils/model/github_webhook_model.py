from pymongo import MongoClient
from utils.logger import logger

class GitHubWebhookModel:

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client.github_webhooks
        self.collection = self.db.events

    def save_to_mongo(self, entry_type, data):
        try:
            formatted_entry = {"type": entry_type, **data}
            result = self.collection.insert_one(formatted_entry)
            formatted_entry["_id"] = str(result.inserted_id)
            return formatted_entry
        except Exception as e:
            logger.error(f"Failed to save data to MongoDB: {e}", exc_info=True)
            raise

    def fetch_latest_events(self):
        try:
            events = self.collection.find().sort("timestamp", -1).limit(10)
            return list(events)
        except Exception as e:
            logger.error(f"Failed to fetch events: {e}", exc_info=True)
            raise
