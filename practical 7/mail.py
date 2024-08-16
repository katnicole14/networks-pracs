import ssl
import socket
import base64

def get_welcome_message(sock):
    response = sock.recv(4096).decode('utf-8')
    return response

def send_command(sock, command):
    sock.sendall(command.encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    return response

def connect_to_pop3_server(pop_server, pop_port):
    context = ssl.create_default_context()
    pop_conn = socket.create_connection((pop_server, pop_port))
    pop_conn = context.wrap_socket(pop_conn, server_hostname=pop_server)
    return pop_conn

def parse_email_headers(email_content):
    headers = {}
    lines = email_content.split(b'\r\n')
    for line in lines:
        if line == b'':
            break
        key, value = line.split(b':', 1)
        headers[key.strip()] = value.strip()
    return headers

def retrieve_emails(pop_conn, username, password):
    # Send USER command
    response_user = send_command(pop_conn, f'USER {username}\r\n')
    print("Response after USER command:", response_user)

    # Send PASS command
    response_pass = send_command(pop_conn, f'PASS {password}\r\n')
    print("Response after PASS command:", response_pass)

    # Request message list
    response_list = send_command(pop_conn, 'LIST\r\n')
    print("Response after LIST command:", response_list)

    # Retrieve messages
    num_messages = int(response_list.split(' ')[1])
    for i in range(num_messages):
        response_retr = send_command(pop_conn, f'RETR {i+1}\r\n')
        print("Response after RETR command:", response_retr)

        # Parse email content
        email_content = b''
        while True:
            data = pop_conn.recv(4096)
            if not data:
                break
            email_content += data

        headers = parse_email_headers(email_content)
        if b'Bcc' in headers:
            print("You were BCC'ed in this email.")

        # Added a timeout of 5 seconds to the recv call
        data = pop_conn.recv(4096, socket.MSG_DONTWAIT)
        if not data:
            break
        email_content += data


        headers = parse_email_headers(email_content)
        if b'Bcc' in headers:
            print("You were BCC'ed in this email.")

def main():
    pop_server = 'pop.gmail.com'
    pop_port = 995
    username = ''

    pop_conn = connect_to_pop3_server(pop_server, pop_port)

    # Get the server greeting
    print("Server greeting:", get_welcome_message(pop_conn))

    # Retrieve emails
    retrieve_emails(pop_conn, username, password)

    # Quit
    response_quit = send_command(pop_conn, 'QUIT\r\n')
    print("Response after QUIT command:", response_quit)

    pop_conn.close()

if __name__ == "__main__":
    main()
