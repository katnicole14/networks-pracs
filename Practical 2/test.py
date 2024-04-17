# Authors :
# Jaide-Maree Pastoll - 21475637
# Siyamthanda Ndlovu - 21582735

import socket
import random


BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
RESET = "\033[0m"



#variables
username = ""
tempMessage = ""

# global numQuestions 
numQuestions = 1
numCorrectAnswers = 0


questions = []
allAnswers = []
correctAnswers=[]
wrongAnswers = []


indexRandomQuestion = 0
questionArrCorrectAnswers = []
questionArrWrongAnswers = []




# Set up the server
HOST = '127.0.0.1'  # Localhost
PORT = 55555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Quiz server is running on {HOST}:{PORT}")

#======================================================================================
# START : READING FROM TEXT FILE, ASSIGNING GLOBAL ARRAYS
#======================================================================================
 
def parseAndIndexTextFile(fileName):


    import os
    
    # Check if the file exists
    if not os.path.isfile(fileName):
        print("File does not exist.")
        return

    with open(fileName, "r") as file:
        line = file.readline()
        c=0
        while line:  # Loop until the end of the file
           
            if line.startswith("?"):
                ##print(line.strip())  # Print the line, stripping any leading/trailing whitespace
                #questions.append(line[1:])
                
                formattedString =":" + str(c+1) + ": " + line[1:]
                questions.append(formattedString)
                ##print(f"{GREEN} {c} Found Question : {line[1:]} {RESET}")
                c = c+1
                #append the previous anserr

                #reset the wrong and correct arrays
              
            elif line.startswith("-") or line.startswith("+"):
                if line.startswith("-"):
                    #wrongAnswers.append(line[1:])
                    formattedString =":" + str(c) + ": " + line[1:]
                    wrongAnswers.append(formattedString)

                elif line.startswith("+"):
                    formattedString =":" + str(c) + ": " + line[1:]
                    correctAnswers.append(formattedString)
                    #wrongAnswers.append(formatted_string)



            line = file.readline()  # Read the next line
 



#correct the files by adding the 


parseAndIndexTextFile("test.txt")


      
#======================================================================================
# END : READING FROM TEXT FILE, ASSIGNING GLOBAL ARRAYS
#======================================================================================
 

#======================================================================================
# START : CORRECTING ARRAY VALUES AFTER READING FROM FILE
#======================================================================================
 

def addMoreThanOneOfTheAbove():
    # Create a dictionary to store the counts for each index
    countsPerIndex = {}

    # Count the occurrences of each index in the correctAnswers array
    for answer in correctAnswers:
        index = answer.split(":")[1].strip()
        countsPerIndex[index] = countsPerIndex.get(index, 0) + 1

    # Add "More than one of the above" for indices with multiple entries
    for index, count in countsPerIndex.items():
        if count > 1:
            additionalOption = f":{index}: More than one of the above"
            correctAnswers.append(additionalOption)

    # Sort the correctAnswers array based on index
    correctAnswers.sort(key=lambda answer: int(answer.split(":")[1].strip()))

    # Return the updated correctAnswers array
    return correctAnswers


def addNoneOfTheAbove():
    # Find the largest index in the correctAnswers array
    largestIndex = max([int(answer.split(":")[1].strip()) for answer in correctAnswers])

    # Check for missing indices and add "None of the above" items
    for index in range(1, largestIndex + 1):
        if not any(answer.startswith(f":{index}:") for answer in correctAnswers):
            noneOfTheAboveText = f":{index}: None of the above\n"
            correctAnswers.append(noneOfTheAboveText)
    
    # Sort the correctAnswers array based on index
    correctAnswers.sort(key=lambda answer: int(answer.split(":")[1].strip()))

    # Return the updated correctAnswers array
    return correctAnswers

def addNoneOfTheAboveAll(arrayValues):
    # Find the largest index in the correctAnswers array
    largestIndex = max([int(answer.split(":")[1].strip()) for answer in arrayValues])

    # Check for missing indices and add "None of the above" items
    for index in range(1, largestIndex + 1):
        if not any(answer.startswith(f":{index}:") for answer in arrayValues):
            noneOfTheAboveText = f":{index}: None of the above\n"
            arrayValues.append(noneOfTheAboveText)
    
    arrayValues.sort(key=lambda answer: int(answer.split(":")[1].strip()))

    # Return the updated correctAnswers array
    return arrayValues

correctAnswers = addMoreThanOneOfTheAbove()
correctAnswers = addNoneOfTheAbove()

#wrongAnswers = addMoreThanOneOfTheAbove()
#wrongAnswers = addNoneOfTheAboveAll(wrongAnswers)

#======================================================================================
# END : CORRECTING ARRAY VALUES
#======================================================================================
    

# Display the questions array
print("Questions Array:")
print(questions)
print()

# Display the correctAnswers array
print("Correct Answers Array:")
print(correctAnswers)
print()

# Display the wrongAnswers array
print("Wrong Answers Array:")
print(wrongAnswers)
print()


def getUsernameFull(client_socket):
    client_socket.sendall("Please enter your username: ".encode())
    username = ''
    while True:
        data = client_socket.recv(1024).decode().strip()
        if not data:  # if connection not closed by the client
            break
        username += data
        if data.endswith('\n'):  # if the input ends with a newline character
            break
    return username.strip()



def getCorrectAnswersForQuestion(correctAnswers, stringIndexOfQuestion):
    questionArrCorrectAnswers = [answer for answer in correctAnswers if answer.startswith(stringIndexOfQuestion)]
    return questionArrCorrectAnswers

def getWrongAnswersForQuestion(wrongAnswers, stringIndexOfQuestion):
    questionArrWrongAnswers = [answer for answer in wrongAnswers if answer.startswith(stringIndexOfQuestion)]
    return questionArrWrongAnswers


def get_wrong_answers(random_index):
    question_index_prefix = ":" + str(random_index + 1) + ":"

    questionArrWrongAnswers.clear()
    for item in wrongAnswers:
        if item.startswith(question_index_prefix):
            questionArrWrongAnswers.append(item)

    return questionArrWrongAnswers


def get_right_answers(random_index):
    question_index_prefix = ":" + str(random_index + 1) + ":"

    questionArrCorrectAnswers.clear()
    for item in correctAnswers:
        if item.startswith(question_index_prefix):
            questionArrCorrectAnswers.append(item)

    return questionArrCorrectAnswers



questionArrWrongAnswers = get_wrong_answers(5)
questionArrRightAnswers = get_right_answers(5)

print(questionArrWrongAnswers)
print(questionArrRightAnswers)




def get_answer_choice():
    client_socket.sendall("Enter the index of your answer: ".encode())
    answer_choice = client_socket.recv(1024).decode().strip()
    answer_choice = answer_choice.strip()
    answer_choice.replace(" ", "")

    if not answer_choice.isdigit():
        answer_choice = 10

    print(f"Received answer choice: {answer_choice}")
    return answer_choice


def getContinueWithQuiz():
    client_socket.sendall("\r\nDo you want to continue with the quiz? (y/n): \r\n".encode())
    answer = client_socket.recv(1024).decode().strip()
    answer = answer.strip().lower()

    print(f"User wants to continue with quiz? {answer}")
    if answer == "y":
        return True
    else:
        return False



def loopSendingQuestion():
    messageToSend = ""

    temp_message = f"{GREEN} ========================== NEW QUESTION ============================== {RESET} \r\n"
    client_socket.send(temp_message.encode())

    random_index = random.choice(range(len(questions)))

    c = random_index+1
    
    questionArrWrongAnswers = get_wrong_answers(random_index)
    questionArrRightAnswers = get_right_answers(random_index)

    formattedQuestionToSend = f"{questions[random_index]}\r\n"
    for index, item in enumerate(questionArrWrongAnswers):
        formattedQuestionToSend += f"{index + 1}. {item.split(':')[-1]}"
        formattedQuestionToSend += "\r\n"


    print(f"formattedQuestionToSend : {formattedQuestionToSend}")
    client_socket.send(formattedQuestionToSend.encode())


    #user_input = input("Enter the index of your answer: ")
    answer = get_answer_choice()
    answer = int(answer) 

    #check if answer is correct
    messageToSend = ""
    #print(f"Answer For Quiz {answer}")

    if answer <= len(questionArrWrongAnswers) :
        global numQuestions
        numQuestions += 1
        answerToCheck = questionArrWrongAnswers[answer-1]
        print(f"Answer For Quiz {answerToCheck} vs Correct Answer for Quiz {questionArrRightAnswers[0]}")
        if answerToCheck in questionArrRightAnswers:
            messageToSend = f"\r\nCongratulations {username} on the correct answer\r\n"
            global numCorrectAnswers
            numCorrectAnswers +=1

        else:
            correctAns = questionArrRightAnswers[0].split(': ', 1)[1].strip()
            messageToSend = f"\r\nThe correct answer was {correctAns}\r\n"
    else:
        messageToSend="\r\n Invalid Index Given\r\n"

    client_socket.send(messageToSend.encode())

    #check if they want to continue with the quiz
    if getContinueWithQuiz() == False:
        calculateMark()
        #client_socket.send(messageToSend.encode())
    else:
        loopSendingQuestion()

    



def calculateMark():    
    mark = (numCorrectAnswers / (numQuestions)) * 100

    markMessage = f"Your mark is: {mark}%"
    print(f"{username} 's mark is: {mark}% , they got {numCorrectAnswers} correct out of {numQuestions}")
    client_socket.send(markMessage.encode())


def loopSendingQuestionBackup(indexForRandomQuestion):
    #indexOfQuestion == :3:
    indexForRandomQuestion = random.choice(questions)
    c = indexForRandomQuestion+1
    stringIndexOfQuestion = ":"+str(c)+":" # eg :6:

#    questionArrCorrectAnswers.clear()
#    questionArrWrongAnswers.clear()


    #stringIndexOfQuestion = random.choice(questionArrCorrectAnswers)
    #questionArrCorrectAnswers = getCorrectAnswersForQuestion(correctAnswers,stringIndexOfQuestion)
    #questionArrWrongAnswers = getWrongAnswersForQuestion(correctAnswers,stringIndexOfQuestion)


#======================================================================================
# MAIN LOOP
#======================================================================================
    
while True:
    # Accept client connections
    client_socket, address = server_socket.accept()
    print(f"New connection from {address}")

    # Send a welcome message to the client
    welcomeMessage = "Welcome to the quiz server!"
    client_socket.send(welcomeMessage.encode())
    

    username = getUsernameFull(client_socket)
    tempMessage = (f"Good to have you here {BLUE}{username}{RESET}. Lets start the quiz :\r\n")
    client_socket.send(tempMessage.encode())

    # questionArrCorrectAnswers = getCorrectAnswersForQuestion(correctAnswers,":2:")
    # questionArrWrongAnswers = getWrongAnswersForQuestion(correctAnswers,":2:")


    # stringArray = ''.join(questionArrCorrectAnswers)

    # client_socket.send(stringArray.encode())

    # client_socket.send(tempMessage.encode())

    
    numQuestions = 1
    numCorrectAnswers = 0
    #start sending questions
    loopSendingQuestion()
         
    # Close the connection
    client_socket.close()



#======================================================================================
# END : MAIN LOOP
#======================================================================================