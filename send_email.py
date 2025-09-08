import smtplib
from email.message import EmailMessage
from textwrap import dedent
from pickletools import read_unicodestringnl
from config import FROM_ADDR,EMAIL_PASSWORD,BASE_URL

class SendEmail:
    def send_email(self,recipients,question,answer):
        if not FROM_ADDR or not EMAIL_PASSWORD:
            print("FATAL ERROR: FROM_ADDR or EMAIL_PASSWORD not found. Check your environment variables.")
            return False
        try:
            connection = smtplib.SMTP('smtp.gmail.com', 587)
            connection.starttls()
            connection.login(FROM_ADDR, EMAIL_PASSWORD)
            print("Login success")
            with open("email_template.html", "r", encoding="utf-8") as file:
                html_template = file.read()
            for email in recipients:
                msg = EmailMessage()
                msg['From'] = FROM_ADDR
                msg['To'] = email
                safe_subject_question = question.strip().replace('\n', ' ')
                msg['Subject'] = f"Your Daily Curiosity Spark – {safe_subject_question}"

                hardcoded_html_body = f"""
                                <html>
                                <body>
                                    <h1>This is a successful test!</h1>
                                    <p>If you are seeing this email, it means the core login and sending functions are working perfectly.</p>
                                    <hr>
                                    <p><b>Question Received:</b> {question}</p>
                                </body>
                                </html>"""

                unsubscribe_url = f"{BASE_URL}/unsubscribe?email={email}"
                website_url = BASE_URL
                suggestions_url = f"{BASE_URL}/#suggestions"
                print(f"Type of unsubscribe url :{type(unsubscribe_url)}")
                print(f"Type of website url :{type(website_url)}")
                print(f"Type of suggestion url :{type(suggestions_url)}")


                msg.add_alternative(hardcoded_html_body, subtype='html')
                connection.send_message(msg)
                print(f"Successfully sent email to {email}")
            connection.quit()
            return True
        except Exception as e:
            print(f"Error occured:{e}")
            return False


