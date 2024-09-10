import ssl
import socket


BLACK = '\033[0;30m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
BROWN = '\033[0;33m'
BLUE = '\033[0;34m'
PURPLE = '\033[0;35m'
CYAN = '\033[0;36m'
LIGHT_GRAY = '\033[0;37m'
DARK_GRAY = '\033[1;30m'
LIGHT_RED = '\033[1;31m'
LIGHT_GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
LIGHT_BLUE = '\033[1;34m'
LIGHT_PURPLE = '\033[1;35m'
LIGHT_CYAN = '\033[1;36m'
LIGHT_WHITE = '\033[1;37m'
BOLD = '\033[1m'
FAINT = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
NEGATIVE = '\033[7m'
CROSSED = '\033[9m'
RESET = '\033[0m'

import email
import base64 

# POP3 server settings
POP3_SERVER = 'pop.gmail.com'
POP3_PORT = 995 
USERNAME = ''
PASSWORD = ''


WARNING_SUBJECT = '[BCC Warning]'

def send_warning_email(subject, body):
   
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    
   
    # email content
    message = f'Subject: {subject}\r\n\r\n{body}'
    
    # connect to SMTP server 
    # ssl
    context = ssl.create_default_context()
    with socket.create_connection((smtp_server, smtp_port)) as server_socket:
        with context.wrap_socket(server_socket, server_hostname=smtp_server) as secure_socket:
            # Receive greeting message
            print(f'{GREEN}Receive greeting message :\r\n{RESET}{secure_socket.recv(1024).decode()}')
            
            # ehlo command
            secure_socket.sendall(b'EHLO example.com\r\n')
            print(secure_socket.recv(1024).decode())
            
            #  authentication command
            secure_socket.sendall(b'AUTH LOGIN\r\n')
            print(secure_socket.recv(1024).decode())
            
            print(f'{GREEN} Sending over variables {RESET}')
            #encoded username 
            secure_socket.sendall(base64.b64encode(bytes(USERNAME, 'utf-8')) + b'\r\n')
            print(secure_socket.recv(1024).decode())
            
              #encoded password base64
            secure_socket.sendall(base64.b64encode(bytes(PASSWORD, 'utf-8')) + b'\r\n')
            print(secure_socket.recv(1024).decode())
            
            #  mail from command
            secure_socket.sendall(b'MAIL FROM:<' + bytes(USERNAME, 'utf-8') + b'>\r\n')
            print(secure_socket.recv(1024).decode())
            
            #  rcpt to
            secure_socket.sendall(b'RCPT TO:<' + bytes(USERNAME, 'utf-8') + b'>\r\n')
            print(secure_socket.recv(1024).decode())
            
            #  send data
            secure_socket.sendall(b'DATA\r\n')
            print(secure_socket.recv(1024).decode())
            
            # send email content
            secure_socket.sendall(bytes(message, 'utf-8') + b'\r\n.\r\n')
            print(secure_socket.recv(1024).decode())
            print(f'{GREEN} Finishing {RESET}')

            #  QUIT 
            secure_socket.sendall(b'QUIT\r\n')
            print(secure_socket.recv(1024).decode())

def check_bcc(email_msg):
    if email_msg.get_all('bcc'):
        print("BCC found. Sending warning email...")
        send_warning_email(WARNING_SUBJECT + email_msg['Subject'], 'You received an email as a blind carbon copied recipient.')

def main():
    print("Connecting to POP3 server...")
    pop_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pop_ssl = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    with pop_ssl.wrap_socket(pop_conn, server_hostname=POP3_SERVER) as pop_server:
        pop_server.connect((POP3_SERVER, POP3_PORT))
        print(pop_server.recv(1024).decode())  # Print welcome message

        pop_server.sendall(b'USER ' + bytes(USERNAME, 'utf-8') + b'\r\n')
        print(pop_server.recv(1024).decode())  # Print response

        pop_server.sendall(b'PASS ' + bytes(PASSWORD, 'utf-8') + b'\r\n')
        print(pop_server.recv(1024).decode())  # Print response

        pop_server.sendall(b'LIST\r\n')
        response = pop_server.recv(1024).decode()
        print(response)  # Print response

        num_messages = len(response.split('\n')) - 2
        print(f"Number of emails: {num_messages}")

        for i in range(num_messages):
            pop_server.sendall(b'RETR ' + bytes(str(i + 1), 'utf-8') + b'\r\n')
            msg_content = b''
            while True:
                response = pop_server.recv(1024)
                msg_content += response
                lines = msg_content.decode('utf-8').split('\r\n')
                if '.' in lines[-2]:
                    break

            email_msg = email.message_from_bytes(msg_content)

            check_bcc(email_msg)

    print("Disconnected from POP3 server.")

if __name__ == "__main__":
    main()
