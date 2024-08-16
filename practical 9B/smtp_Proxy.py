import socket
import ssl
import base64
import os

def smtp_proxy(proxy_host, proxy_port, smtp_server, smtp_port, gmail_username, gmail_password):
    def recv_until(socket, delimiter=b'\n'):
        data = b''
        while not data.endswith(delimiter):
            more = socket.recv(1)
            if not more:
                raise EOFError("Socket closed")
            data += more
        return data

    # Create a socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the proxy host and port
    proxy_socket.bind((proxy_host, proxy_port))

    # Listen for incoming connections
    proxy_socket.listen(1)

    print(f"Proxy server listening on {proxy_host}:{proxy_port}...")

    while True:
        # Accept incoming connection from Thunderbird
        client_socket, client_address = proxy_socket.accept()
        print(f"Connection established from {client_address}")

        try:
            # Connect to the actual SMTP server (Gmail)
            smtp_socket = socket.create_connection((smtp_server, smtp_port))
            smtp_file = smtp_socket.makefile('rb')
            print(f"Connected to SMTP server {smtp_server}:{smtp_port}")

            # Upgrade the connection to SSL/TLS
            context = ssl.create_default_context()
            smtp_socket = context.wrap_socket(smtp_socket, server_hostname=smtp_server)
            smtp_file = smtp_socket.makefile('rb')
            print("Connection upgraded to SSL/TLS")

            # Initial greeting from SMTP server
            initial_response = recv_until(smtp_socket)
            print(f"Initial response from SMTP server: {initial_response.decode()}")

            # Send EHLO to SMTP server
            smtp_socket.sendall(b"EHLO example.com\r\n")
            ehlo_response = recv_until(smtp_socket)
            print(f"EHLO response from SMTP server: {ehlo_response.decode()}")
            # Send AUTH LOGIN
            smtp_socket.sendall(b"AUTH LOGIN\r\n")
            auth_response = recv_until(smtp_socket, b"334")
            print(f"AUTH LOGIN response from SMTP server: {auth_response.decode()}")

            # Send base64 encoded username
            smtp_socket.sendall(base64.b64encode(gmail_username.encode()) + b"\r\n")
            user_response = recv_until(smtp_socket, b"334")
            print(f"Username response from SMTP server: {user_response.decode()}")

            # Send base64 encoded password
            smtp_socket.sendall(base64.b64encode(gmail_password.encode()) + b"\r\n")
            pass_response = recv_until(smtp_socket)
            print(f"Password response from SMTP server: {pass_response.decode()}")

        
         # Handle communication from Thunderbird and forward to SMTP server
            while True:
                client_data = client_socket.recv(4096)
                if not client_data:
                    break

                # Print data received from Thunderbird
                print(f"Received data from Thunderbird: {client_data.decode('utf-8')}")

                # Forward data to SMTP server
                smtp_socket.sendall(client_data)

                # Receive response from SMTP server
                smtp_response = recv_until(smtp_socket)

                # Print response received from SMTP server
                print(f"Received response from SMTP server: {smtp_response.decode('utf-8')}")

                # Send response back to Thunderbird
                client_socket.sendall(smtp_response)



        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()
            smtp_socket.close()


smtp_proxy('localhost', 2500, 'smtp.gmail.com', 465, '', 'mxcjop')
