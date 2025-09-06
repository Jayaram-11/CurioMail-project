from flask import Flask, request, jsonify
from flask_cors import CORS
# Assuming your database functions are now in database.py
from database import Email_Storage


def create_app():
    """Creates and configures the Flask application."""
    email_manager=Email_Storage()
    email_manager.initialize_db()

    app = Flask(__name__)


    CORS(app)
    @app.route('/subscribe', methods=['POST'])
    def subscribe():
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"status": "error", "message": "Email is required"}), 400

        email = data['email']
        success = email_manager.add_email(email)

        if success:
            return jsonify({"status": "success", "message": "Subscription successful!"})
        else:
            return jsonify({"status": "error", "message": "Could not save email"}), 500

    @app.route('/suggest', methods=['POST'])
    def suggest():
        data = request.get_json()
        if not data or 'suggestion' not in data:
            return jsonify({"status": "error", "message": "Suggestion text is required"}), 400

        suggestion_text = data['suggestion']
        success = email_manager.add_suggestion(suggestion_text)

        if success:
            return jsonify({"status": "success", "message": "Suggestion received!"})
        else:
            return jsonify({"status": "error", "message": "Could not save suggestion"}), 500

    # At the end of the function, return the configured app object
    return app
