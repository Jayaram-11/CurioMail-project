import smtplib
from email.message import EmailMessage
from textwrap import dedent
from pickletools import read_unicodestringnl
from config import FROM_ADDR,EMAIL_PASSWORD

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
                msg['Subject'] = f"Your Daily Curiosity Spark – {question}"

                formatted_answer = answer.replace('\n', '<br>')
                new_template = html_template.replace("{{QUESTION}}", question).replace("{{ANSWER}}", formatted_answer)

                msg.add_alternative(new_template, subtype='html')

                connection.send_message(msg)
                print(f"Successfully sent email to {email}")
            connection.quit()
            return True
        except Exception as e:
            print(f"Error occured:{e}")
            return False


