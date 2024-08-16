import socket
import threading

# Proxy server details
proxy_host = 'localhost'
proxy_port = 55555

# POP3 server details
pop3_server = 'localhost'
pop3_port = 110
real_username = 'katnicole'
real_password = 'katnicole14'

# SMTP server details
smtp_server = 'localhost'
smtp_port = 25

# Authentication details for proxy users
proxy_users = {
    'user1@example.com': 'password1',
    'user2@example.com': 'password2',
    'user3@example.com': 'password3'
}
delete_allowed_user = 'user2@example.com'

def handle_client(client_socket):
    pop_conn = None
    smtp_conn = None
    try:
        while True:
            # Receive client request
            request = client_socket.recv(1024).decode().strip()

            # Check if it is a POP3 or SMTP request
            if request.startswith('USER'):
                handle_pop3_request(client_socket, request)
            else:
                client_socket.send(b'-ERR Invalid command\r\n')

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client_socket:
            client_socket.close()
        if pop_conn:
            pop_conn.close()
        if smtp_conn:
            smtp_conn.close()

def handle_pop3_request(client_socket, request):
    global pop_conn
    # Connect to the real POP3 server
    pop_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pop_conn.connect((pop3_server, pop3_port))
    client_socket.send(pop_conn.recv(1024))  # Welcome message from the real server

    # Authenticate client to proxy
    client_socket.send(b'+OK Proxy POP3 server ready\r\n')
    user_authenticated = False
    proxy_username = None

    while not user_authenticated:
        user_cmd = client_socket.recv(1024).decode().strip()
        if user_cmd.startswith('USER'):
            proxy_username = user_cmd.split()[1]
            client_socket.send(b'+OK User accepted\r\n')
        elif user_cmd.startswith('PASS'):
            proxy_password = user_cmd.split()[1]
            if proxy_users.get(proxy_username) == proxy_password:
                user_authenticated = True
                client_socket.send(b'+OK Proxy authentication successful\r\n')
            else:
                client_socket.send(b'-ERR Invalid credentials\r\n')

    # Authenticate to the real POP3 server
    pop_conn.sendall(b'USER ' + bytes(real_username, 'utf-8') + b'\r\n')
    client_socket.send(pop_conn.recv(1024))
    pop_conn.sendall(b'PASS ' + bytes(real_password, 'utf-8') + b'\r\n')
    client_socket.send(pop_conn.recv(1024))

    # Relay messages between client and server with enhancements
    while True:
        command = client_socket.recv(1024)
        if not command:
            break
        if command.startswith(b'RETR'):
            msg_id = command.split()[1]
            pop_conn.sendall(command)
            response = b""
            while True:
                part = pop_conn.recv(1024)
                response += part
                if b'\r\n.\r\n' in part:
                    break

            if b'Subject: Confidential' in response:
                response = (b'From: test@example.com\r\n'
                            b'Subject: Just testing\r\n'
                            b'\r\n'
                            b'This is a cover email.\r\n'
                            b'\r\n'
                            b'.\r\n')
            else:
                response = response.replace(b'\r\n', b'\r\nHandled by ' + bytes(proxy_username, 'utf-8') + b'\r\n', 1)

            client_socket.send(response)
        elif command.startswith(b'DELE') and proxy_username != delete_allowed_user:
            client_socket.send(b'-ERR You are not allowed to delete emails\r\n')
        else:
            pop_conn.sendall(command)
            response = pop_conn.recv(1024)
            client_socket.send(response)

def handle_smtp_request(client_socket, request):
    global smtp_conn
    # Connect to the real SMTP server
    smtp_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    smtp_conn.connect((smtp_server, smtp_port))
    client_socket.send(smtp_conn.recv(1024))  # Welcome message from the real server

    # Relay HELO/EHLO command to the real SMTP server
    smtp_conn.sendall(request.encode())
    response = smtp_conn.recv(1024)
    client_socket.send(response)

    # Forward remaining commands and responses between client and server
    while True:
        command = client_socket.recv(1024)
        if not command:
            break

        smtp_conn.sendall(command)
        response = smtp_conn.recv(1024)
        client_socket.send(response)

    smtp_conn.close()  # Close the SMTP connection after the session ends


def start_proxy():
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.bind((proxy_host, proxy_port))
    proxy_server.listen(5)
    print(f"Proxy server listening on {proxy_host}:{proxy_port}")

    while True:
        client_socket, addr = proxy_server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()
