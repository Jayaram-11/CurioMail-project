from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
# Assuming your database functions are now in database.py
from database import Email_Storage


def create_app():

    email_manager=Email_Storage()
    email_manager.initialize_db()
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def serve_index():

        return send_from_directory(app.static_folder, 'index.html')


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

    @app.route('/unsubscribe', methods=['GET'])
    def unsubscribe():

        email_to_remove = request.args.get('email')

        if not email_to_remove:
            return "<h1>Error: No email address provided.</h1><p>Please contact support if you continue to have issues.</p>", 400


        success = email_manager.remove_email(email_to_remove)

        if success:

            return "<h1>You have been unsubscribed.</h1><p>You will no longer receive daily emails from CurioMail.</p>"
        else:
            return "<h1>Error</h1><p>There was a problem unsubscribing your email. Please try again later .</p>", 500


    return app
