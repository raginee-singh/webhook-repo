from flask import jsonify
from model.github_webhook_model import GitHubWebhookModel
from utils.logger import logger
from datetime import datetime

class GitHubWebhookService:
    
    def __init__(self):
        self.model = GitHubWebhookModel()

    def handle_push_event(self, payload):
        try:
            author = payload.get('head_commit', {}).get('author', {}).get('name', 'Unknown')
            to_branch = payload.get('ref', '').split('/')[-1]
            timestamp = payload.get('head_commit', {}).get('timestamp', '')

            data = {
                "author": author,
                "to_branch": to_branch,
                "timestamp": timestamp
            }
            saved_entry = self.model.save_to_mongo("PUSH", data)
            logger.info("Push event processed successfully")
            return jsonify({"message": "Push event processed successfully", "data": saved_entry}), 200
        except Exception as e:
            logger.error(f"Error processing push event: {e}", exc_info=True)
            raise

    def handle_pull_request_event(self, payload):
        try:
            pr_data = payload.get("pull_request", {})
            action = payload.get("action")
            author = pr_data.get("user", {}).get("login", "Unknown")
            from_branch = pr_data.get("head", {}).get("ref", "Unknown")
            to_branch = pr_data.get("base", {}).get("ref", "Unknown")

            if action == "opened":
                timestamp = pr_data.get("created_at", "")
                data = {
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": timestamp
                }
                saved_entry = self.model.save_to_mongo("PULL REQUEST", data)
                logger.info("Pull Request event processed successfully")
                return jsonify({"message": "Pull Request event processed successfully", "data": saved_entry}), 200
            
            elif action == "closed" and pr_data.get("merged", False):
                timestamp = pr_data.get("merged_at", "")
                data = {
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": timestamp
                }
                saved_entry = self.model.save_to_mongo("MERGE", data)
                logger.info("Merge event processed successfully")
                return jsonify({"message": "Merge event processed successfully", "data": saved_entry}), 200
        except Exception as e:
            logger.error(f"Error processing pull request event: {e}", exc_info=True)
            raise
    
    def get_latest_events(self):
        try:
            events = self.model.fetch_latest_events()
            event_messages = self.format_event_messages(events)
            logger.info("Fetching latest events successfully")
            return jsonify({"messages": event_messages}), 200
        except Exception as e:
            logger.error(f"Error fetching latest events: {e}", exc_info=True)
            raise

    def format_event_messages(self, events):
        event_messages = []
        for event in events:
            event_type = event.get("type", "UNKNOWN")
            author = event.get("author", "Unknown")
            to_branch = event.get("to_branch", "Unknown")
            timestamp = event.get("timestamp", "Unknown")

            # Format timestamp
            try:
                dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
                formatted_timestamp = dt.strftime("%d %B %Y - %I:%M %p %Z")
            except Exception:
                formatted_timestamp = timestamp  # Fallback

            # Format message based on event type
            if event_type == "PUSH":
                message = f'"{author}" pushed to "{to_branch}" on {formatted_timestamp}'
            elif event_type == "PULL REQUEST":
                from_branch = event.get("from_branch", "Unknown")
                message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {formatted_timestamp}'
            elif event_type == "MERGE":
                from_branch = event.get("from_branch", "Unknown")
                message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {formatted_timestamp}'
            else:
                message = f"Unknown event type: {event_type}"

            event_messages.append(message)
        return event_messages
