import socket
import threading
import ssl

REAL_SMTP_SERVER = 'smtp.gmail.com'
REAL_SMTP_PORT = 587

def handle_smtp_client(client_socket):
    try:
        # Connect to the real SMTP server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((REAL_SMTP_SERVER, REAL_SMTP_PORT))
        print('[*] Connected to real SMTP server')

        # Initial server response
        server_response = server_socket.recv(4096)
        print(f'Server: {server_response.decode("utf-8")}', flush=True)
        client_socket.send(server_response)

        while True:
            client_data = client_socket.recv(4096)
            if not client_data:
                break

            print(f'Client: {client_data.decode("utf-8")}', flush=True)

            if b'STARTTLS' in client_data:
                server_socket.send(client_data)
                server_response = server_socket.recv(4096)
                print(f'Server: {server_response.decode("utf-8")}', flush=True)
                client_socket.send(server_response)

                # Wrap the client socket with SSL
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                client_socket = context.wrap_socket(client_socket, server_side=True)
                print('[*] Upgraded connection to SSL/TLS', flush=True)
            else:
                server_socket.send(client_data)
                server_response = server_socket.recv(4096)
                print(f'Server: {server_response.decode("utf-8")}', flush=True)
                client_socket.send(server_response)
    except Exception as e:
        print(f'Error: {e}', flush=True)
    finally:
        client_socket.close()
        server_socket.close()
        print('[*] Closed client and server sockets', flush=True)

def main():
    bind_ip = '0.0.0.0'
    bind_port = 1025

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    print(f'[*] Listening on {bind_ip}:{bind_port}')

    while True:
        client_socket, addr = server.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

        client_handler = threading.Thread(target=handle_smtp_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
