from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class FibonacciServer(BaseHTTPRequestHandler):
    """ """
    def do_GET(self):
        """ """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello! ')

    def handle_get_request(self):
        """Interpret the get request"""
        # Parse the requested URL path
        path = self.path.strip('/')
        
        if path == '':
            # If the path is '/', do nothing
            response_content = b''
        else:
            try:
                # Try to convert the path to an integer
                n = int(path)
                # If successful, calculate the nth Fibonacci number
                fibonacci_number = self.calculate_fibonacci(n)
                response_content = str(fibonacci_number).encode('utf-8')
            except ValueError:
                # If conversion to integer fails, return a 404 Not Found response
                self.send_error(404, 'Not Found')
                return
    def calculate_fibonacci(self,n):
        """calculate fib"""
        num = n + n+1
        return num
        


def run_server(host, port):
    """starting the server"""
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, FibonacciServer)
    print(f"Server started on {host}:{port}")
    httpd.serve_forever()

# Example usage
host = "localhost"
port = 8080
run_server(host, port)

