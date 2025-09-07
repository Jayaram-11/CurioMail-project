import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

NOTION_INTEGRATION_TOKEN = os.getenv("NOTION_INTEGRATION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
FROM_ADDR = os.getenv("FROM_ADDR")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


if not NOTION_INTEGRATION_TOKEN:
    raise ValueError("FATAL: NOTION_TOKEN is not set. Please check your environment variables.")

notion = Client(auth=NOTION_INTEGRATION_TOKEN)

