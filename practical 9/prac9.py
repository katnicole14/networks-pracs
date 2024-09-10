import socket
import threading
import ssl

# Proxy server configuration
PROXY_HOST = 'localhost'
PROXY_PORT = 55555
REAL_POP3_SERVER = 'pop.gmail.com'
REAL_POP3_PORT = 995 
# Proxy credentials (used by employees to connect to the proxy)
PROXY_USERNAME = ''
PROXY_PASSWORD = ''
# Real POP3 server credentials (used by the proxy to connect to the POP3 server)
REAL_POP3_USERNAME = ''
REAL_POP3_PASSWORD = ''

def handle_client(client_socket):
    try:
        # Authentication
        client_socket.send(b'Username: ')
        print("Sent username prompt to client.")
        username = client_socket.recv(1024).decode().strip()
        print(f"Received username: {username}")
        
        client_socket.send(b'Password: ')
        print("Sent password prompt to client.")
        password = client_socket.recv(1024).decode().strip()
        print("Received password.")

        if username == PROXY_USERNAME and password == PROXY_PASSWORD:
            # Authentication successful
            client_socket.send(b'Authentication successful.\n')
            print("Authentication successful.")
            
            # Connect to real POP3 server
            print(f"Connecting to real POP3 server at {REAL_POP3_SERVER}:{REAL_POP3_PORT}...")
            real_pop3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            real_pop3_socket = ssl.wrap_socket(real_pop3_socket, ssl_version=ssl.PROTOCOL_TLS)
            real_pop3_socket.connect((REAL_POP3_SERVER, REAL_POP3_PORT))
            print("Connected to real POP3 server.")

            # Send initial connection data to client
            initial_response = real_pop3_socket.recv(1024)
            client_socket.send(initial_response)
            print(f"Initial response from POP3 server: {initial_response.decode().strip()}")

            # Authenticate the proxy to the real POP3 server
            real_pop3_socket.send(f"USER {REAL_POP3_USERNAME}\r\n".encode())
            response = real_pop3_socket.recv(1024)
            client_socket.send(response)
            print(f"Sent USER command, received: {response.decode().strip()}")

            real_pop3_socket.send(f"PASS {REAL_POP3_PASSWORD}\r\n".encode())
            response = real_pop3_socket.recv(1024)
            client_socket.send(response)
            print(f"Sent PASS command, received: {response.decode().strip()}")

            # Relay messages between client and real POP3 server
            while True:
                # Receive command from client
                client_data = client_socket.recv(1024)
                if not client_data:
                    break
                
                command = client_data.decode().strip()
                print(f"Received command from client: {command}")
                if command.upper() == 'QUIT':
                    print("Received QUIT command. Closing connection.")
                    break

                # Send the command to the real POP3 server
                real_pop3_socket.send(client_data)
                print(f"Sent command to real POP3 server: {command}")

                # Receive response from the real POP3 server
                real_pop3_response = real_pop3_socket.recv(1024)
                print(f"Received response from real POP3 server: {real_pop3_response.decode().strip()}")

                # Send response back to the client
                client_socket.send(real_pop3_response)
                print("Sent response to client.")

            # Close connections
            real_pop3_socket.close()
            client_socket.close()
            print("Disconnected from real POP3 server and client.")
        else:
            # Authentication failed
            client_socket.send(b'Authentication failed.\n')
            print("Authentication failed.")
            client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

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


# Main function
if __name__ == "__main__":
    # Start proxy server in a separate thread
    proxy_thread = threading.Thread(target=start_proxy)
    proxy_thread.start()

    # Call the function to interact with the proxy server as a client
    interact_with_proxy()
