import socket
import threading

# Configuration
POP3_UPSTREAM_SERVER = 'pop.gmail.com'
POP3_UPSTREAM_PORT = 995  # Use SSL/TLS for secure POP3 connection
POP3_PROXY_PORT = 55555  # Proxy server port

BUFFER_SIZE = 4096

def handle_client(client_socket, upstream_host, upstream_port):
    print("Handling client connection...")
    upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upstream_socket.connect((upstream_host, upstream_port))

    def forward(source, destination):
        while True:
            data = source.recv(BUFFER_SIZE)
            if not data:
                break
            destination.sendall(data)

    client_to_upstream = threading.Thread(target=forward, args=(client_socket, upstream_socket))
    upstream_to_client = threading.Thread(target=forward, args=(upstream_socket, client_socket))

    client_to_upstream.start()
    upstream_to_client.start()

    client_to_upstream.join()
    upstream_to_client.join()

    client_socket.close()
    upstream_socket.close()
    print("Client connection handled.")

def start_proxy(proxy_port, upstream_host, upstream_port):
    print(f"Starting proxy server on port {proxy_port}...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', proxy_port))
    server_socket.listen(5)
    print(f"Listening on port {proxy_port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, upstream_host, upstream_port))
        client_handler.start()

if __name__ == "__main__":
    start_proxy(POP3_PROXY_PORT, POP3_UPSTREAM_SERVER, POP3_UPSTREAM_PORT)
