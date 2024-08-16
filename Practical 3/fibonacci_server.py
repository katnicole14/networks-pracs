import socket

# Function to calculate the next Fibonacci number
def next_fibonacci():
    try:
        # Open the file containing the last two Fibonacci numbers
        with open("fibonacci.txt", "r+") as file:
            # Read the last two numbers
            numbers = list(map(int, file.readline().strip().split()))

            # Calculate the next Fibonacci number
            next_fib = numbers[1] + numbers[2]

            # Update the file with the new Fibonacci sequence
            file.seek(0)
            file.write("{} {}".format(numbers[1], next_fib))

    except FileNotFoundError:
        print("Error: Unable to open file fibonacci.txt")
        return -1
    except IOError:
        print("Error: Unable to open file fibonacci.txt for writing")
        return -1

    return next_fib

# Function to generate HTML response with the next Fibonacci number
def generate_html(next_fib):
    html_content = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
<title>Next Fibonacci Number</title>
</head>
<body>
<h1>Next Fibonacci Number:</h1>
<p>{}</p>
<a href="/next">Next</a>
</body>
</html>
""".format(next_fib)

    return html_content

# Main function to start the Fibonacci server
def main():
    server_host = socket.gethostname()
    server_port = 55555

    # Create a TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print("Fibonacci server is listening on {}:{}".format(server_host, server_port))

    while True:
        # Accept incoming client connection
        client_socket, address = server_socket.accept()
        print("Connection from:", address)

        # Receive request from client
        request = client_socket.recv(1024).decode("utf-8")

        # Process request and calculate next Fibonacci number
        if request.startswith("GET /next"):
            next_fib = next_fibonacci()
            html_response = generate_html(next_fib)
            client_socket.sendall(html_response.encode("utf-8"))

        # Close client connection
        client_socket.close()

if __name__ == "__main__":
    main()
