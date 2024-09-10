import poplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText

# POP3 server settings
POP3_SERVER = 'pop.gmail.com'
POP3_PORT = 995  # Use port 995 for POP3 over SSL
USERNAME = ''
PASSWORD = ''

# Email settings
FROM_EMAIL = ''
TO_EMAIL = ''
WARNING_SUBJECT = '[BCC Warning]'

def send_warning_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    print("Connecting to SMTP server...")
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Use port 587 for SMTP with TLS
    smtp_server.starttls()  # Start TLS encryption
    smtp_server.login(USERNAME, PASSWORD)
    smtp_server.send_message(msg)
    print("Email sent.")
    smtp_server.quit()

def check_bcc(email_msg):
    if email_msg.get('bcc'):
        print("BCC found. Sending warning email...")
        send_warning_email(WARNING_SUBJECT + email_msg['Subject'], 'You received an email as a blind carbon copied recipient.')

def main():
    print("Connecting to POP3 server...")
    pop_conn = poplib.POP3_SSL(POP3_SERVER, POP3_PORT)
    pop_conn.user(USERNAME)
    pop_conn.pass_(PASSWORD)
    print("Connected to POP3 server.")

    num_messages = len(pop_conn.list()[1])
    print(f"Number of emails: {num_messages}")
    num_ = 3
    for i in range(3):
        print(f"Retrieving email {i + 1}...")
        _, msg_lines, _ = pop_conn.retr(i + 1)
        msg_content = b'\r\n'.join(msg_lines).decode('utf-8', errors='ignore')
        email_msg = email.message_from_string(msg_content)

        check_bcc(email_msg)

    pop_conn.quit()
    print("Disconnected from POP3 server.")

if __name__ == "__main__":
    main()
