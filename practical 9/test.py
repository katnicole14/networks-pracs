import socket
import threading
import ssl
from email.mime.text import MIMEText

# Proxy server configuration
PROXY_HOST = 'localhost'
PROXY_PORT = 55555
REAL_POP3_SERVER = 'pop.gmail.com'
REAL_SMTP_SERVER = 'smtp.gmail.com'
REAL_SMTP_PORT = 465 
REAL_POP3_PORT = 995 
# Proxy credentials (used by employees to connect to the proxy)
PROXY_USERNAME = 'u22543946@tuks.co.za'
PROXY_PASSWORD = 'mxcjoptjkqmolevp'
# Real POP3 server credentials (used by the proxy to connect to the POP3 server)
REAL_POP3_USERNAME = 'u22543946@tuks.co.za'
REAL_POP3_PASSWORD = 'mxcjoptjkqmolevp'

username =REAL_POP3_USERNAME
password =REAL_POP3_PASSWORD
# Define multiple proxy credentials


# Function to send email using SMTP
def send_email(username, password):
    try:
        # Establish a TCP connection to the SMTP server
        smtp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smtp_socket = ssl.wrap_socket(smtp_socket)

        smtp_socket.connect((REAL_SMTP_SERVER, REAL_SMTP_PORT))

        # Receive the initial server response
        print(smtp_socket.recv(1024).decode())

        # Send EHLO command
        smtp_socket.send(b'EHLO localhost\r\n')
        print(smtp_socket.recv(1024).decode())

        # Send AUTH LOGIN command
        smtp_socket.send(b'AUTH LOGIN\r\n')
        print(smtp_socket.recv(1024).decode())

        # Send username
        smtp_socket.send(username.encode() + b'\r\n')
        print(f"Sent username: {username}")
        print(smtp_socket.recv(1024).decode())

        # Send password
        smtp_socket.send(password.encode() + b'\r\n')
        print("Sent password.")
        print(smtp_socket.recv(1024).decode())

        # Create the email message
        message = MIMEText("This is a test email.")
        message['Subject'] = 'Test Email'
        message['From'] = username
        message['To'] = username

        # Send the email
        smtp_socket.send(f'MAIL FROM: <{username}>\r\n'.encode())
        print(smtp_socket.recv(1024).decode())

        smtp_socket.send(f'RCPT TO: <recipient@example.com>\r\n'.encode())
        print(smtp_socket.recv(1024).decode())

        smtp_socket.send(b'DATA\r\n')
        print(smtp_socket.recv(1024).decode())

        smtp_socket.send(message.as_string().encode() + b'\r\n')
        print(smtp_socket.recv(1024).decode())

        smtp_socket.send(b'.\r\n')
        print(smtp_socket.recv(1024).decode())

        # Quit the session
        smtp_socket.send(b'QUIT\r\n')
        print(smtp_socket.recv(1024).decode())

        smtp_socket.close()

        print(f"Email sent by {username}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to handle client requests in the proxy server
def handle_client(client_socket):
    try:
        # Authentication
        client_socket.send(b'Username: ')
        username = client_socket.recv(1024).decode().strip()
        print(f"Received username: {username}")
        client_socket.send(b'Password: ')
        password = client_socket.recv(1024).decode().strip()
        print("Received password.")

        # Check if credentials are valid
        if username == PROXY_USERNAME and password == PROXY_PASSWORD:
            client_socket.send(b'Authentication successful.\n')
            print("Authentication successful.")
            send_email(username, password)
        else:
            client_socket.send(b'Authentication failed.\n')
            print("Authentication failed.")

    except Exception as e:
        print(f"Error: {e}")

# Function to interact with the proxy server as a client
def interact_with_proxy():
    try:
        # Connect to proxy server
        proxy_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_client.connect((PROXY_HOST, PROXY_PORT))
        print("Connected to proxy server.")

        # Receive authentication prompts
        print(proxy_client.recv(1024).decode())  # Username prompt
        proxy_client.send(input("Enter your username: ").encode())
        print(proxy_client.recv(1024).decode())  # Password prompt
        proxy_client.send(input("Enter your password: ").encode())

        # Receive authentication result
        auth_result = proxy_client.recv(1024).decode()
        print(auth_result)

        if "successful" in auth_result:
            print("Authentication successful. You can now send commands.")
            print("Type your command and press Enter to send.")
            print("For example: LIST, RETR 1, DELE 2, etc.")
            print("Type 'QUIT' to exit.")

            # Relay messages between client and proxy server
            while True:
                # Prompt the user to enter a command
                command = input(">> ")

                # Send command to proxy server
                proxy_client.send(command.encode())

                # Receive response from proxy server
                response = proxy_client.recv(1024).decode()
                print(response)

                if command.upper() == 'QUIT':
                    break

            # Close connection
            proxy_client.close()
            print("Disconnected from proxy server.")
        else:
            print("Authentication failed.")
            proxy_client.close()
    except Exception as e:
        print(f"Error: {e}")

# Function to start the proxy server
def start_proxy():
    # Create proxy server socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)
    print(f"Proxy server listening on {PROXY_HOST}:{PROXY_PORT}")

    while True:
        # Accept client connection
        client_socket, client_address = proxy_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Handle client request in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
# Main function
if __name__ == "__main__":
    # Start proxy server in a separate thread
    proxy_thread = threading.Thread(target=start_proxy)
    proxy_thread.start()

    # Call the function to interact with the proxy server as a client
    interact_with_proxy()
