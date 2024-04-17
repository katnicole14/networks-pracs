def previous_fibonacci(fib_file):
    try:
        # Open the Fibonacci file in read mode
        with open(fib_file, 'r') as file:
            # Read the current Fibonacci numbers
            fib_numbers = [int(num) for num in file.readline().split()]

        # Calculate the previous Fibonacci number
        prev_fib = fib_numbers[1] - fib_numbers[0]

        # Handle special case when the file contains (0, 1, 1)
        if fib_numbers == [0, 1, 1]:
            prev_fib = -1

        # Update the file with the new Fibonacci sequence
        with open(fib_file, 'w') as outFile:
            outFile.write("{} {} {}".format(prev_fib, fib_numbers[0], fib_numbers[1]))

    except FileNotFoundError:
        print("Error: Unable to open file:", fib_file)
        return -1
    except IOError:
        print("Error: Unable to open file for writing:", fib_file)
        return -1

    return prev_fib


def generate_html(prev_fib):
    # Generate HTML content
    print("Content-type: text/html\n")
    print("<!DOCTYPE html>")
    print("<html>")
    print("<head>")
    print("<title>Previous Fibonacci Number</title>")
    print("</head>")
    print("<body>")
    print("<h1>Previous Fibonacci Number:</h1>")
    print("<p>", prev_fib, "</p>")
    print('<a href="/cgi-bin/next.cgi">Next</a>')
    print("</body>")
    print("</html>")

if __name__ == "__main__":
    # Path to the Fibonacci file
    fib_file = "fibonacci.txt"

    # Calculate the previous Fibonacci number
    prev_fib = previous_fibonacci(fib_file)

    # Generate HTML output
    generate_html(prev_fib)
