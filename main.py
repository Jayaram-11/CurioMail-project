from get_content import NotionContentManager
from database import Email_Storage
from send_email import SendEmail
from config import DATABASE_ID,notion


def run_daily():
    print("Fetching next scheduled content from Notion...")
    email_manager=Email_Storage()
    content_manager = NotionContentManager(notion_client=notion, database_id=DATABASE_ID)
    content_to_send = content_manager.get_next_scheduled_content()
    if not content_to_send:
        print("Process finished: No scheduled content found in Notion.")
        return

    page_id = content_to_send["page_id"]
    question = content_to_send["question"]
    answer = content_to_send["answer"]
    #print(f"Successfully fetched content from page ID: {page_id}")
    #print(f"  -> Question: {question}")
    print("Retrieving subscriber emails from the database...")

    subscribers = email_manager.get_subscribers()

    if not subscribers:
        print("Process finished: No subscribers found in the database. Will not send email.")
        return

    print(f"Found {len(subscribers)} subscribers to email.")


    print("Sending email broadcast to all subscribers...")
    # This function should handle sending the email to the list of recipients.
    # It should return True for success and False for failure.
    email_sender=SendEmail()
    email_sent_successfully = email_sender.send_email(
        recipients=subscribers,
        question=question,
        answer=answer
    )

    # --- Step 4: Update Notion status ONLY if emails were sent successfully ---
    if email_sent_successfully:
        print("\nEmail broadcast successful. Updating Notion status to 'Sent'...")
        content_manager.update_content_status_to_sent(page_id)
    else:
        print("\nEmail broadcast failed. The Notion status will NOT be updated, so it can be retried.")

    print("--- Daily CurioMail Process Finished ---")



# --- Main execution block ---
if __name__ == '__main__':
    temp_email_manager=Email_Storage()
    temp_email_manager.initialize_db()

    run_daily()



