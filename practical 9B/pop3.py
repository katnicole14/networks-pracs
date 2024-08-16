import socket
import ssl
import base64
import re
import datetime


# Configuration
PROXY_HOST = 'localhost'
PROXY_PORT = 55555
REAL_POP3_HOST = 'localhost'
REAL_POP3_PORT = 143
REAL_POP3_USERNAME = 'katnicole@katnicole.localdomain'
REAL_POP3_PASSWORD = 'katnicole'

def handle_client(client_socket):
    # Receive client greeting
    client_greeting = client_socket.recv(1024).decode()
    print("Client Greeting:", client_greeting)
    
    # Send server greeting
    server_greeting = "+OK POP3 Proxy Ready\r\n"
    client_socket.send(server_greeting.encode())
    print("Server Greeting Sent")

    # Receive client authentication
    client_auth = client_socket.recv(1024).decode()
    print("Client Authentication:", client_auth)
    if not client_auth.startswith("USER") or not client_auth.endswith("\r\n"):
        client_socket.send("-ERR Invalid command\r\n".encode())
        client_socket.close()
        return
    client_socket.send("+OK\r\n".encode())
    print("User OK Sent")

    # Receive password
    client_password = client_socket.recv(1024).decode()
    print("Client Password:", client_password)
    if not client_password.startswith("PASS") or not client_password.endswith("\r\n"):
        client_socket.send("-ERR Invalid command\r\n".encode())
        client_socket.close()
        return
    client_socket.send("+OK\r\n".encode())
    print("Password OK Sent")

    # Connect to real POP3 server
    real_pop3_socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    real_pop3_socket.connect((REAL_POP3_HOST, REAL_POP3_PORT))
    real_pop3_socket.recv(1024)  # Receive server greeting from real POP3 server
    print("Connected to Real POP3 Server")

    # Send authentication to real POP3 server
    real_pop3_socket.sendall("USER {}\r\n".format(REAL_POP3_USERNAME).encode())
    real_pop3_socket.recv(1024)  # Receive response
    real_pop3_socket.sendall("PASS {}\r\n".format(REAL_POP3_PASSWORD).encode())
    real_pop3_socket.recv(1024)  # Receive response
    print("Authenticated with Real POP3 Server")

    # Relay commands and responses between client and real POP3 server
    while True:
        client_data = client_socket.recv(1024)
        if not client_data:
            break

        # Check for confidential emails
        if "Subject: Confidential" in client_data.decode():
            print("Confidential Email Detected")
            client_socket.sendall(b"-ERR Email is confidential\r\n")
            continue

        # Insert user information
        username = "john_doe"  # Placeholder username for demonstration
        user_info = "\n\nHandled by {}\n".format(username)
        client_data = client_data.replace(b"\r\n\r\n", user_info.encode())

        real_pop3_socket.sendall(client_data)
        real_pop3_response = real_pop3_socket.recv(1024)
        client_socket.sendall(real_pop3_response)
        print("Relayed Data")

        # Log events
        log_event("Client request: " + client_data.decode())
        log_event("Server response: " + real_pop3_response.decode())

    # Close connections
    real_pop3_socket.close()
    client_socket.close()
    print("Connections Closed")

def log_event(event_message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[{}] {}".format(timestamp, event_message))

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)
    print("Proxy server listening on {}:{}".format(PROXY_HOST, PROXY_PORT))
    
    while True:
        client_socket, client_address = proxy_socket.accept()
        print("Connection established from:", client_address)
        handle_client(client_socket)

if __name__ == "__main__":
    start_proxy()
