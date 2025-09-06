from Integration import create_app
from database import Email_Storage

print("--- Initializing Web Server ---")



# 2. Create the Flask app instance using the factory function from Integration.py.
app = create_app()

# 3. Run the web server.
if __name__ == '__main__':
    # For development, you run it like this.
    # For a live website, you would use a production-ready server like Gunicorn.
    print("Starting Flask server on http://127.0.0.1:5000...")

    app.run(host='0.0.0.0', port=5000, debug=True)

