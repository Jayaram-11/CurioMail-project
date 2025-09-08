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

                unsubscribe_url = f"{BASE_URL}/unsubscribe?email={email}"
                website_url = f"{BASE_URL}"
                suggestions_url = f"{BASE_URL}/#suggestions"

                formatted_answer = answer.replace('\n', '<br>')

                populated_html = html_template.replace("{{QUESTION}}", question)
                populated_html = populated_html.replace("{{ANSWER}}", formatted_answer)
                populated_html = populated_html.replace("{{WEBSITE_URL}}", website_url)
                populated_html = populated_html.replace("{{SUGGESTIONS_URL}}", suggestions_url)
                populated_html = populated_html.replace("{{UNSUBSCRIBE_URL}}", unsubscribe_url)

                msg.add_alternative(populated_html, subtype='html')
                connection.send_message(msg)
                print(f"Successfully sent email to {email}")
            connection.quit()
            return True
        except Exception as e:
            print(f"Error occured:{e}")
            return False


