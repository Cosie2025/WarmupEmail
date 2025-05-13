import os
import csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from jinja2 import Template

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')

def load_template():
    with open("email_template.html", "r", encoding='utf-8') as file:
        return Template(file.read())

def load_emails(file_path):
    with open(file_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def send_email(to_email, subject, html_content):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Sent to {to_email}: {response.status_code}")
    except Exception as e:
        print(f"Error sending to {to_email}: {e}")

def main():
    template = load_template()
    recipients = load_emails("emails.csv")

    for user in recipients:
        html = template.render()  # no name needed
        send_email(user["email"], "Hello from SendGrid", html)

if __name__ == "__main__":
    main()
