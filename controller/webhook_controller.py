from flask import request, jsonify
from service.github_webhook_service import GitHubWebhookService
from utils.logger import logger

def register_routes(app):
    @app.route('/api/v1/github-webhook', methods=['POST'])
    def handle_webhook():
        try:
            event_type = request.headers.get('x-github-event')
            payload = request.json
            service = GitHubWebhookService()

            if event_type == 'push':
                return service.handle_push_event(payload)
            elif event_type == 'pull_request':
                return service.handle_pull_request_event(payload)
            else:
                return jsonify({"error": f"Unsupported event type: {event_type}"}), 400

        except Exception as e:
            logger.error(f"An error occurred while processing the webhook: {e}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/api/v1/latest-events', methods=['GET'])
    def get_latest_events():
        try:
            service = GitHubWebhookService()
            return service.get_latest_events()
        except Exception as e:
            logger.error(f"An error occurred while fetching the latest events: {e}", exc_info=True)
            return jsonify({"error": "Internal Server Error"}), 500
