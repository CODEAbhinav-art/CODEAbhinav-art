import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# It's recommended to set these environment variables with your Gmail address and an app password.
# Do NOT use your regular Gmail password here, generate an app password from your Google Account security settings:
# https://support.google.com/accounts/answer/185833
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_email_password")

if SENDER_EMAIL == "your_email@gmail.com" or SENDER_PASSWORD == "your_email_password":
    print("WARNING: Using default placeholder email credentials. Please set environment variables SENDER_EMAIL and SENDER_PASSWORD with your Gmail address and app password.")

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        raise e

def send_booking_notification(user_email, property_name, owner_email):
    subject = f"Booking Confirmation for {property_name}"
    body = f"Dear user,\n\nYour booking for the property '{property_name}' has been confirmed.\n\nOwner contact: {owner_email}\n\nThank you for using Renters."
    send_email(user_email, subject, body)
    send_email(owner_email, f"New Booking for {property_name}", f"A new booking has been made by {user_email} for your property '{property_name}'.")


