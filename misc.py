import json, os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

USER_DATA_FILE = "userData.json"
RAZORPAY_KEYS_FILE = "razorpay_keys.txt"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return []


# Function to save updated user data to the JSON file
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def load_razorpay_credentials():
    try:
        with open(RAZORPAY_KEYS_FILE, 'r') as file:
            lines = file.readlines()
            # Extract key_id and secret from the file
            key_id = lines[0].strip().split('=')[1]
            secret = lines[1].strip().split('=')[1]
            return key_id, secret
    except Exception as e:
        raise Exception(f"Error loading Razorpay credentials: {str(e)}")
    
def load_email_credentials():
    try:
        with open(RAZORPAY_KEYS_FILE, 'r') as file:
            lines = file.readlines()
            # Extract key_id and secret from the file
            email = lines[4].strip().split('=')[1]
            passw = lines[5].strip().split('=')[1]
            bccem = lines[6].strip().split('=')[1]
            return email, passw, bccem
    except Exception as e:
        raise Exception(f"Error loading email credentials: {str(e)}")
    


# def send_preorder_confirmation(user_email: str, user_name: str, preorder_id: str, bcc_emails=None):
#     """
#     Sends an email confirmation for a successful preorder, with optional BCC recipients.

#     Args:
#         user_email (str): The recipient's email address.
#         user_name (str): The recipient's name.
#         preorder_id (str): The preorder ID to include in the email.
#         bcc_emails (list): Optional list of email addresses to BCC.
#     """
#     sender_email, sender_password, bcc = load_email_credentials()
#     sender_name = "Infinity AR"
#     smtp_server = "smtpout.secureserver.net"
#     smtp_port_ssl = 465
#     smtp_port_tls = 587

#     # Default BCC list to empty if not provided
#     bcc_emails = bcc_emails or [bcc]

#     subject = "Preorder Confirmation"
#     body = f"""
#     Hi {user_name},

#     Thank you for your preorder with us! 
#     Your preorder ID is: {preorder_id}

#     We will notify you once your item is ready for shipment.

#     Best regards,
#     {sender_name}
#     """

#     try:
#         # Create the email message
#         message = MIMEMultipart()
#         message["From"] = formataddr((sender_name, sender_email))
#         message["To"] = user_email
#         message["Subject"] = subject
#         message.attach(MIMEText(body, "plain"))

#         # Combine all recipients: To + BCC
#         all_recipients = [user_email] + bcc_emails

#         # Attempt SSL connection
#         try:
#             with smtplib.SMTP_SSL(smtp_server, smtp_port_ssl) as server:
#                 server.login(sender_email, sender_password)
#                 server.sendmail(sender_email, all_recipients, message.as_string())
#             print(f"Email sent successfully to {user_email} (BCC: {', '.join(bcc_emails)})")
#         except smtplib.SMTPException as e_ssl:
#             print(f"SSL connection failed: {e_ssl}. Trying STARTTLS...")
#             # Retry with STARTTLS
#             with smtplib.SMTP(smtp_server, smtp_port_tls) as server:
#                 server.starttls()
#                 server.login(sender_email, sender_password)
#                 server.sendmail(sender_email, all_recipients, message.as_string())
#             print(f"Email sent successfully to {user_email} (BCC: {', '.join(bcc_emails)})")

#     except smtplib.SMTPException as e:
#         print(f"Failed to send email to {user_email}: {e}")
#         raise
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         raise

# send_preorder_confirmation("katariavishal888@gmail.com","vishal","Asdasdasda")


import requests

def send_preorder_confirmation(user_email: str, user_name: str, preorder_id: str, bcc_emails=None):
    """
    Sends an email confirmation for a successful preorder, using GoDaddy's REST API.

    Args:
        user_email (str): The recipient's email address.
        user_name (str): The recipient's name.
        preorder_id (str): The preorder ID to include in the email.
        bcc_emails (list): Optional list of email addresses to BCC.
    """
    # Load email credentials and API details
    bcc, api_key, api_secret = load_email_credentials()
    sender_email = "support@infinityar.in"
    sender_name = "Infinity AR"
    domain = "infinityar.in"  # Replace with your domain
    api_url = f"https://api.godaddy.com/v1/email/accounts/{domain}/messages"

    # Default BCC list to empty if not provided
    bcc_emails = bcc_emails or []

    subject = "Preorder Confirmation"
    body = f"""
    Hi {user_name},

    Thank you for your preorder with us! 
    Your preorder ID is: {preorder_id}

    We will notify you once your item is ready for shipment.

    Best regards,
    {sender_name}
    """

    # Prepare the API request payload
    payload = {
        "from": sender_email,
        "to": [user_email],
        "bcc": bcc_emails,
        "subject": subject,
        "textBody": body
    }

    # Add API headers for authentication
    headers = {
        "Authorization": f"sso-key {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    try:
        # Make the API POST request
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code in (200, 202):  # 202 Accepted indicates email is queued for delivery
            print(f"Email sent successfully to {user_email}")
        else:
            print(f"Failed to send email: {response.status_code}, {response.text}")
            response.raise_for_status()

    except requests.RequestException as e:
        print(f"An error occurred while sending email: {e}")
        raise


send_preorder_confirmation("katariavishal888@gmail.com","vishal","Asdasdasda")
