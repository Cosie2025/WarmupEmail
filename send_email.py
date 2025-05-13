import os
import csv
from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from jinja2 import Template

# Load env vars
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")  # Should be warmup@entugo.in

app = Flask(__name__)

# Load HTML template
def load_template():
    with open("email_template.html", "r", encoding='utf-8') as f:
        return Template(f.read())

# Load CSV email list
def load_emails():
    with open("emails.csv", newline='') as csvfile:
        return list(csv.DictReader(csvfile))

# Send one email
def send_email(to_email, subject, html_content):
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Sent to {to_email}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending to {to_email}: {e}")

# Root endpoint for health check
@app.route("/")
def home():
    return "Entugo Mailer is Running"

# POST endpoint to send emails
@app.route("/send", methods=["POST"])
def trigger_send():
    template = load_template()
    recipients = load_emails()
    for user in recipients:
        html = template.render()
        send_email(user["email"], "Entugo Warmup - Email Campaign.", html)
    return jsonify({"status": "Emails sent"}), 200

# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
