import socket

# Calculate the next fibonnaci number 
def next_fibonacci():
    try:
        # Open the file
        with open("fibonacci.txt", 'r+') as file:
            # Read the numbers from the file 
            numbers = list(map(int, file.readline().strip().split()))

            # Calculate the next Fibonacci number
            next_fib = numbers[1] + numbers[2]

            # write new numbers into the file
            file.seek(0)
            file.write("{} {} {}".format(numbers[1], numbers[2], next_fib))

    except FileNotFoundError:
        print("Error: Unable to open file", "fibonacci.txt")
        return -1
    except IOError:
        print("Error: Unable to open file", "fibonacci.txt", "for writing")
        return -1

    return next_fib

#cgi responce couldnt import the cgi file 
def generate_html(sequence_before, next_fib, sequence_after):
    html_content = """\
<!DOCTYPE html>
<html>
<head>
<title>Next Fibonacci Number</title>
</head>
<body>
<h1>Next Fibonacci Number:</h1>
<p>Sequence Before: {}</p>
<p>Next Fibonacci Number: {}</p>
<p>Sequence After: {}</p>
<a href="/next">Next</a>
</body>
</html>
""".format(sequence_before, next_fib, sequence_after)

    #headers added
    http_response = "HTTP/1.1 200 OK\r\n"
    http_response += "Content-Type: text/html\r\n"
    http_response += "Content-Length: {}\r\n".format(len(html_content))
    http_response += "\r\n" 
    http_response += html_content

    return http_response

# 
def main():
    server_host = "localhost"
    server_port = 55555

   #socket creation
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    print("Fibonacci server is listening on {}:{}".format(server_host, server_port))

    while True:
       #clients connection
        client_socket, address = server_socket.accept()
        print("Connection from:", address)

        #client requests
        request_data = client_socket.recv(1024).decode("utf-8")

        # process rewuests 
        if request_data.startswith("GET /next"):
           #before modifying the request
            with open("fibonacci.txt", 'r') as file:
                sequence_before = file.readline().strip()
              #next number
            next_fib = next_fibonacci()

            # updated file
            with open("fibonacci.txt", 'r') as file:
                sequence_after = file.readline().strip()

            html_response = generate_html(sequence_before, next_fib, sequence_after)
            client_socket.sendall(html_response.encode("utf-8"))

       
        client_socket.close()

if __name__ == "__main__":
    main()
