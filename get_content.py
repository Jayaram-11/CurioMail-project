
from datetime import date

class NotionContentManager:
    def __init__(self, notion_client, database_id):

        self.notion = notion_client
        self.database_id = database_id

    def get_next_scheduled_content(self):

        try:

            response = self.notion.databases.query(
                database_id=self.database_id,

                filter={"property": "Status", "select": {"equals": "Scheduled"}},

                sorts=[{"property": "ID", "direction": "ascending"}],

                page_size=1
            )
            #print(response)
            if not response["results"]:
                print("No scheduled content found.")
                return None


            page_data = response["results"][0]
            page_id = page_data["id"]

            properties = page_data.get("properties", {})

            #default question
            question = "A Spark of Curiosity"
            question_title_list = properties.get("Question", {}).get("title", [])
            if question_title_list:

                question = question_title_list[0].get("text", {}).get("content", question)


            html_answer_parts = []
            answer_blocks = properties.get("Answer", {}).get("rich_text",[])

            for block in answer_blocks:
                text_content = block.get("plain_text", "")
                annotations = block.get("annotations", {})
                if annotations.get("bold"):
                    text_content = f"<strong>{text_content}</strong>"
                html_answer_parts.append(text_content)


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


