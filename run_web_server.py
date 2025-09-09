import os

from Integration import create_app
from database import Email_Storage

print("--- Initializing Web Server ---")


app = create_app()

if __name__ == '__main__':
    port=int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0', port=port)

