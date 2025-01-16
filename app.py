from flask import Flask, render_template, jsonify
from controller.webhook_controller import register_routes

def create_app():
    # Initialize Flask app with correct paths for template and static
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Register routes
    register_routes(app)

    # Route for the root URL ("/")
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)