import os

from Integration import create_app
from database import Email_Storage

print("--- Initializing Web Server ---")



# 2. Create the Flask app instance using the factory function from Integration.py.
app = create_app()

# 3. Run the web server.
if __name__ == '__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)

