import random
from datetime import date

class NotionContentManager:
    def __init__(self, notion_client, database_id):
        """
        Initializes the manager with the Notion client and database ID.
        """
        self.notion = notion_client
        self.database_id = database_id

    def get_next_scheduled_content(self):
        """
        Queries Notion for the first item with the status "Scheduled",
        ordered by the 'ID' property.

        Returns a dictionary with page_id, question, and answer, or None if none are found.
        """
        try:
            # This query asks the Notion API to do the filtering and sorting for us.
            # It's much more efficient than fetching everything.
            response = self.notion.databases.query(
                database_id=self.database_id,
                # Filter 1: Only get pages where the 'Status' is 'Scheduled'
                filter={"property": "Status", "select": {"equals": "Scheduled"}},
                # Sort by the 'ID' column to ensure we get them in order (1, 2, 3...)
                sorts=[{"property": "ID", "direction": "ascending"}],
                # We only need the very next one, so we set page_size to 1
                page_size=1
            )
            #print(response)
            if not response["results"]:
                print("No scheduled content found.")
                return None

            # --- Parse the single result ---
            page_data = response["results"][0]
            page_id = page_data["id"]

            properties = page_data.get("properties", {})

            # Safely extract question
            question_title = properties.get("Question", {}).get("title", [])
            question = question_title[0].get("text", {}).get("content") if question_title else "No Question"

            # Safely extract answer
            answer_blocks = properties.get("Answer", {}).get("rich_text", [])

            # This list will hold our HTML-formatted text parts
            html_answer_parts = []

            # Loop through each block of text from Notion
            for block in answer_blocks:
                text_content = block.get("plain_text", "")
                annotations = block.get("annotations", {})

                # Check for bold formatting
                if annotations.get("bold"):
                    # If bold, wrap the text in HTML <strong> tags
                    text_content = f"<strong>{text_content}</strong>"

                # You can add more checks here for italics, underlines, etc. in the future
                # if annotations.get("italic"):
                #     text_content = f"<em>{text_content}</em>"

                html_answer_parts.append(text_content)

            # Join all the formatted parts into a single string.
            # This string now contains HTML tags for formatting.
            answer = "".join(html_answer_parts)

            return {
                "page_id": page_id,
                "question": question,
                "answer": answer
            }

        except Exception as e:
            print(f"An error occurred while fetching content: {e}")
            return None

    def update_content_status_to_sent(self, page_id: str):
        """
        Updates a specific Notion page to set its status to "Sent"
        and fills in today's date in the "Schedule Date" field.
        """
        try:
            today_iso = date.today().isoformat()

            self.notion.pages.update(
                page_id=page_id,
                properties={
                    "Status": {"select": {"name": "Sent"}},
                    "Schedule Date": {"date": {"start": today_iso}}
                }
            )
            print(f"Successfully updated page {page_id} to 'Sent' for date {today_iso}.")
        except Exception as e:
            print(f"An error occurred while updating page {page_id}: {e}")


