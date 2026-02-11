import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.my_email = os.environ.get("my_email")
        self.password = os.environ.get("password")

    def send_alert(self, msg_body, email_list):  # Changed users_email to email_list
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=self.my_email, password=self.password)
                connection.sendmail(from_addr=self.my_email,
                                    to_addrs=email_list,  # Send to the whole list at once
                                    msg=msg_body
                                    )
                print(f"Alert sent to {len(email_list)} users.")
        except smtplib.SMTPException as e:
            print(f"Error: Unable to send emails. {e}")
