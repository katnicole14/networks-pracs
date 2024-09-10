import ssl
import socket


# Function to decode email headers
def decode_email_header(header):
    parts = header.split(b'?')
    if len(parts) == 5:
        charset = parts[1].decode()
        encoding = parts[2]
        text = parts[3]
        return text.decode(charset)
    return header.decode()

# Function to connect to POP3 server
def connect_to_pop3_server(pop_server, pop_port):
    context = ssl.create_default_context()
    pop_conn = socket.create_connection((pop_server, pop_port))
    pop_conn = context.wrap_socket(pop_conn, server_hostname=pop_server)

    # Print response after connecting
    print(pop_conn.recv(4096).decode('utf-8'))

    return pop_conn

# Function to retrieve emails
# Function to retrieve emails
def retrieve_emails(pop_conn, username, password):
    pop_conn.sendall(b'USER ' + bytes(username, 'utf-8') + b'\r\n')
    pop_conn.sendall(b'PASS ' + bytes(password, 'utf-8') + b'\r\n')

    # Read and discard the initial server greeting
    pop_conn.recv(4096).decode('utf-8')

    pop_conn.sendall(b'LIST\r\n')
    response = pop_conn.recv(4096).decode('utf-8')

    print("Response after LIST command:", response)  # Print response for debugging

    # Check if response contains "Welcome", indicating no emails
    if "Welcome" in response:
        print("No emails to retrieve.")
        return

    num_messages = 0
    for line in response.split('\r\n'):
        if line.isdigit():
            num_messages = int(line)
            break

    print("Number of messages:", num_messages)  # Print number of messages for debugging

    for i in range(num_messages):
        pop_conn.sendall(b'RETR ' + bytes(str(i + 1), 'utf-8') + b'\r\n')
        email_content = b''
        while True:
            data = pop_conn.recv(4096)
            if not data:
                break
            email_content += data

        # Parse email content
        lines = email_content.split(b'\r\n')
        headers = {}
        for line in lines:
            if line == b'':
                break
            key, value = line.split(b':', 1)
            headers[key.strip()] = value.strip()

        # Check for BCC header
        if b'Bcc' in headers:
            bcc_header = headers[b'Bcc']
            decoded_bcc_header = decode_email_header(bcc_header)
            # Send warning email
            send_warning_email(username, password, decoded_bcc_header)


def send_warning_email(username, password, bcc_recipient):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Construct the warning email
    warning_subject = '[BCC Warning] You received an email as a blind carbon copy'
    warning_body = 'Hello,\n\nYou received an email as a blind carbon copy.'
    warning_message = f'Subject: {warning_subject}\n\n{warning_body}'

    # Create SMTP connection
    context = ssl.create_default_context()
    with socket.create_connection((smtp_server, smtp_port)) as server_socket:
        with context.wrap_socket(server_socket, server_hostname=smtp_server) as secure_socket:
            secure_socket.sendall(b'EHLO example.com\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(b'STARTTLS\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(b'EHLO example.com\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(b'AUTH LOGIN\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(base64.b64encode(bytes(username, 'utf-8')) + b'\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(base64.b64encode(bytes(password, 'utf-8')) + b'\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(b'MAIL FROM:<' + bytes(username, 'utf-8') + b'>\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(b'RCPT TO:<' + bytes(bcc_recipient, 'utf-8') + b'>\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(b'DATA\r\n')
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(warning_message.encode('utf-8') + b'\r\n.\r\n')  # Fix subject placement
            print(secure_socket.recv(1024).decode())
            secure_socket.sendall(b'QUIT\r\n')
            print(secure_socket.recv(1024).decode())



# Main function
def main():
    pop_server = 'pop.gmail.com'
    pop_port = 995
    username = ''
    password = ''

    pop_conn = connect_to_pop3_server(pop_server, pop_port)
    retrieve_emails(pop_conn, username, password)
    pop_conn.close()

if __name__ == "__main__":
    main()
