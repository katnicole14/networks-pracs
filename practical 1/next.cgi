import os

def next_fibonacci(fib_file):
    try:
        # Open the file
        with open(fib_file, 'r+') as file:
            # Read the numbers
            numbers = list(map(int, file.readline().strip().split()))

            # Calculate the next Fibonacci number
            next_fib = numbers[1] + numbers[2]

            # Update the file with the new Fibonacci sequence
            file.seek(0)
            file.write("{} {} {}".format(numbers[1], numbers[2], next_fib))

    except FileNotFoundError:
        print("Error: Unable to open file", fib_file)
        return -1
    except IOError:
        print("Error: Unable to open file", fib_file, "for writing")
        return -1

    return next_fib


def generate_html(next_fib):
    # Generate HTML content
    print("Content-type: text/html\n")
    print("<!DOCTYPE html>")
    print("<html>")
    print("<head>")
    print("<title>Next Fibonacci Number</title>")
    print("</head>")
    print("<body>")
    print("<h1>Next Fibonacci Number:</h1>")
    print("<p>", next_fib, "</p>")
    print('<a href="/cgi-bin/prev.cgi">Previous</a>')
    print("</body>")
    print("</html>")

if __name__ == "__main__":
    fib_file = "fibonacci.txt"
    next_fib = next_fibonacci(fib_file)
    generate_html(next_fib)
