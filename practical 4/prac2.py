import socket
import random

# Read questions from file
def read_questions(filename):
    questions = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        question = ''
        correct_answer = ''
        answers = []
        for line in lines:
            if line.startswith('?'):
                if question:
                    questions.append((question, answers, correct_answer))
                question = line.strip()[1:]
                answers = []
            elif line.startswith('+'):
                correct_answer = line.strip()[1:]
                answers.append(correct_answer)
            elif line.startswith('-'):
                answers.append(line.strip()[1:])
        if question:
            questions.append((question, answers, correct_answer))
    return questions

# Select a random question
def select_question(questions):
    return random.choice(questions)

# Handle client connection
def handle_client(client_socket, address):
    # Read client request

    if client_socket.recv(1024).decode().startswith("GET /quiz"):
        questions = read_questions("questions.txt")
        
        question, answers, correct_answer = select_question(questions)

        # HTTP response for quiz page
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        response += f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quiz</title>
        </head>
        <body>
            <h1>Quiz</h1>
            <p>{question}</p>
            <form method="POST" action="/answer.html">
                <input type="hidden" name="correct_answer" value="{correct_answer}">
        """
        for i, answer in enumerate(answers):
            response += f"""
                <input type="radio" id="answer_{i}" name="answer" value="{answer}">
                <label for="answer_{i}">{answer}</label><br>
            """
        response += """
                <button type="submit">Submit</button>
            </form>
            <form action="/quit" method="get">
                <button type="submit">Quit</button>
            </form>
        </body>
        </html>
        """
        client_socket.send(response.encode())

    elif client_socket.recv(1024).decode().startswith("POST /answer.html"):
        # Extract submitted answer and correct answer
        data = client_socket.recv(1024).decode().split('\r\n')[-1]  # Extract data from the last line
        submitted_answer = data.split('&')[0].split('=')[-1]  # Extract submitted answer
        correct_answer = data.split('&')[1].split('=')[-1]  # Extract correct answer

        # Compare answers
        if submitted_answer == correct_answer:
            feedback = "Correct!"
        else:
            feedback = f"Incorrect. The correct answer is: {correct_answer}"

        # Construct HTTP response with feedback
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        response += f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quiz Feedback</title>
        </head>
        <body>
            <h1>Quiz Feedback</h1>
            <p>{feedback}</p>
            <form action="/quiz" method="get">
                <button type="submit">Next Question</button>
            </form>
            <form action="/quit" method="get">
                <button type="submit">Quit</button>
            </form>
        </body>
        </html>
        """
        client_socket.send(response.encode())

    # Close connection
    client_socket.close()

# Set up server
HOST = '127.0.0.1'
PORT = 55555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

# Accept incoming connections
while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from: {address} has been established")
    handle_client(client_socket, address)
