
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

import random 

def parsingFile(fileName):
    questions = []
    allAnswers = []
    correctAnswers=[]
    wrongAnswers = []
    #wrongAnswers = []

    with open("test.txt", "r") as file:
        line = file.readline()  # Read the first line
        while line:
            print(f"{LIGHT_BLUE} {line} {RESET}")  # Process the line
            line = file.readline()  # Read the next line
            if line.startswith("?"):
                #question = line[1:]
                print(f"{GREEN} Found Question : {line[1:]} {RESET}")
                questions.append(line[1:])

                #get wrong answers

            if line.startswith("+"):
                correctAnswers.append(line[1:])
                print(f"{GREEN} Found Correct Answer : {line[1:]} {RESET}")
            elif line.startswith("-"):
                # Remove the hyphen from the line to get a wrong answer
                wrongAnswers.append(line[1:])
                print(f"{GREEN} Found Wrong Answer : {line[1:]} {RESET}")


            #wrong and right answers now added, lets see what we have:
                        

            # Store the question and its answers
            #questions.append(question)
            allAnswers.append({
                'correctAnswers': correctAnswers,
                'wrongAnswers': wrongAnswers
            })

            correctAnswers.clear()
            wrongAnswers.clear()
    


        # Print the parsed questions and answers


    # Display the questions array
    print("Questions Array:")
    print(questions)
    print()

    # Display the allAnswers array
    print("All Answers Array:")
    print(allAnswers)
    print()

    # Display the correctAnswers array
    print("Correct Answers Array:")
    print(correctAnswers)
    print()

    # Display the wrongAnswers array
    print("Wrong Answers Array:")
    print(wrongAnswers)
    print()



def parse_file(file_name):
    import os
    
    # Check if the file exists
    if not os.path.isfile(file_name):
        print("File does not exist.")
        return
    
    # Open the file for reading
    with open(file_name, 'r') as file:
        # Read the lines of the file
        lines = file.readlines()
        print(lines)

        # Initialize variables for storing questions and answers
        questions = []
        allAnswers = []
        correctAnswers=[]
        wrongAnswers = []

        # Iterate over each line in the file
        for line in lines:
            # Strip any leading or trailing whitespace
            #line = line.strip()

            # Check if the line is a question
            if line.startswith("?"):
                # Remove the question mark from the line
                question = line[1:]
                print(f"{GREEN} Found Question : {line[1:]} {RESET}")

                # Initialize a list to store the possible answers

                # Iterate to the next line and check if it is an answer
            elif line.startswith("-") or line.startswith("+"):

                #line = lines.pop(0).strip()
                if line.startswith("+"):
                    # Remove the plus sign from the line to get the correct answer
                    correct_answer = line[1:]
                    correctAnswers.append(line[1:])

                if line.startswith("-"):
                    # Remove the hyphen from the line to get a wrong answer
                    wrongAnswers.append(line[1:])

                # Store the question and its answers
                questions.append(question)
                allAnswers.append({
                    'correct_answer': correctAnswers,
                    'wrongAnswers': wrongAnswers
                })

        # Print the parsed questions and answers
        for i in range(len(questions)):
            print(f"Question {i+1}: {questions[i]}")
            print("Possible Answers:")
            for answer in allAnswers[i]['wrongAnswers']:
                print(f"- {answer}")
            print(f"Correct Answer: {allAnswers[i]['correct_answer']}")
            print()


        # Display the questions array
    print("Questions Array:")
    print(questions)
    print()

    # Display the allAnswers array
    print("All Answers Array:")
    print(allAnswers)
    print()

    # Display the correctAnswers array
    print("Correct Answers Array:")
    print(correctAnswers)
    print()

    # Display the wrongAnswers array
    print("Wrong Answers Array:")
    print(wrongAnswers)
    print()



questions = []
allAnswers = []
correctAnswers=[]
wrongAnswers = []

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
                print(line.strip())  # Print the line, stripping any leading/trailing whitespace
                #questions.append(line[1:])
                
                formatted_string =":" + str(c+1) + ": " + line[1:]
                questions.append(formatted_string)
                print(f"{GREEN} {c} Found Question : {line[1:]} {RESET}")
                c = c+1
                #append the previous anserr

                #reset the wrong and correct arrays
              
            elif line.startswith("-") or line.startswith("+"):
                if line.startswith("-"):
                    #wrongAnswers.append(line[1:])
                    formatted_string =":" + str(c) + ": " + line[1:]
                    wrongAnswers.append(formatted_string)
                    print(f"{PURPLE} {c} Found Wrong Answer : {line[1:]} {RESET}")

                elif line.startswith("+"):
                    formatted_string =":" + str(c) + ": " + line[1:]
                    correctAnswers.append(formatted_string)
                    print(f"{YELLOW} {c} Found Correct Answer : {line[1:]} {RESET}")                
            line = file.readline()  # Read the next line
 

    print("Questions Array:")
    print(questions)
    print()

    # Display the allAnswers array
    print("All Answers Array:")
    print(allAnswers)
    print()

    # Display the correctAnswers array
    print("Correct Answers Array:")
    print(correctAnswers)
    print()

    # Display the wrongAnswers array
    print("Wrong Answers Array:")
    print(wrongAnswers)
    print()

   

# Example usage:
#parseAndIndexTextFile("test.txt")


# Example usage
parseAndIndexTextFile("test.txt")
#parse_file("test.txt")
#parsingFile("test.txt")

indexRandomQuestion = random.choice(questions)
questionArrCorrectAnswers = []
questionArrWrongAnswers = [] 

def addNoneOfTheAbove(correctAnswers):
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



# Example usage
#correctAnswers = [':1: Port 80\n', ':2: SMTP\n', ':4: HTTPS\n', ':7: HTTPS\n']
#correctAnswers = addNoneOfTheAbove(correctAnswers)

# Display the updated correctAnswers array
#print("Updated Correct Answers Array:")
#print(correctAnswers)






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


# Example usage
correctAnswers = [':1: Port 80\n', ':1: SMTP\n', ':4: HTTPS\n', ':6: HTTPS\n', ':4: HTTPS\n', ':6: HTTPS\n']
correctAnswers = addMoreThanOneOfTheAbove()

# Display the updated correctAnswers array
print("Updated Correct Answers Array:")
print(correctAnswers)






def get_wrong_answers(random_index):
    questionIndexPrefix = random_index + 1
    questionArrWrongAnswers = []

    for answer in wrongAnswers:
        if answer.startswith(f':{questionIndexPrefix}:'):
            questionArrWrongAnswers.append(answer)
    
    return questionArrWrongAnswers

random_index = 5
wrongAnswers = [':1: Port 53\n', ':1: Port 80\n', ':1: Port 443\n', ':1: Port 8080\n', ':2: FTP\n', ':2: SMTP\n', ':2: SSH\n', ':2: HTTP\n', ':3: Physical layer\n', ':3: Network layer\n', ':3: Transport layer\n', ':3: Data link layer\n', ':4: FTP\n', ':4: HTTP\n', ':4: HTTPS\n', ':4: SMTP\n', ':5: 16 bits\n', ':5: 32 bits\n', ':5: 64 bits\n', ':5: 128 bits\n', ':6: A record\n', ':6: MX record\n', ':6: NS record\n', ':6: CNAME record\n', ':7: HTTP\n', ':7: FTP\n', ':7: SSH\n', ':7: SMTP\n', ':8: Transport layer\n', ':8: Network layer\n', ':8: Physical layer\n', ':8: Data link layer\n', ':9: HTTP\n', ':9: FTP\n', ':9: SIP\n', ':9: SMTP\n', ':10: A record\n', ':10: MX record\n', ':10: NS record\n', ':10: CNAME record\n', ':11: DNS\n', ':11: SNMP\n', ':11: FTP\n', ':12: Routing data packets between networks\n', ':12: Encrypting network traffic\n', ':12: Allocating IP addresses to devices\n', ':13: Physical Layer\n', ':13: Data Link Layer\n', ':13: Session Layer']

questionArrWrongAnswers = get_wrong_answers(random_index)
print(questionArrWrongAnswers)
