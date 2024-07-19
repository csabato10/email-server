"""Client Side of Homework 4."""

# take a user input
# generate an email message by prompting the user to type the contents of the email
# user gives an email
# send that email to the server

# needs to take some CMARG
# takes server name and port number

# send SMTP command to local server via socket


# need to implement handshaking between server
# HW2 server is waiting to receive a socket request
# when a session is established, send a 220 messages with the hostname

# client sends HELO with hostname of client machine
# 250 response to the HELO -- homework write up has more specifics

# need to change HW2 to do the 220 message
# change HW3 client side to do the HELO

# prompt the user for the components of an email
# "From: " wait for forward path
# "To:" wait for recipeints separated by commas
# Subject: 
# Message:
# User will print "\n.\n" as a way to indicate end of message
# Send this message to the server and then terminate

# Will terminate for error messages as well

# NEED TO CONFORM TO RFC 822
# after Data command we have from: To: subject: -- NOT SMTP COMMANDS, HEADERS
# then a blank line
# then the actual email


# TWO COMMAND LINE ARGUMENTS
# hostname, portnumber (14575)
# will need to ensure the socket is closed because when there are errors, it might not close these issues
# NEED TO MAKE SURE WE CLOSE AND RESET SOCKET IF AN ERROR OCCURS

# Chiara Sabato - csabato - 730466575
# Honor Pledge: I will neither give nor receive aid on this assessment.

import sys
from socket import *
import time

class SMTPException(BaseException):
    pass

class QuitException(BaseException):
    pass

def whitespace():
    """Examines for whitespace"""
    global index, error_code
    if index >= len(line) or not sp():
        error_code = "whitespace"
        return False
    
    while index < len(line) and sp():
        index += 1
    
    return True

def sp():
    """Examines for the space or tab character"""
    global index
    return line[index] == "\t" or line[index] == " "

def nullspace():
    """Examines for nullspace"""
    global index
    if index >= len(line):
        return False
    if whitespace():
        return True
    elif null():
        return True
    else:
        return False
    
def null():
    """Examines for no character"""
    global index
    return line[index] != None

def reverse_path():
    """Examines <path>"""
    return path()

def path():
    """Examines "<" <mailbox> ">" """
    global index, error_code
    if index < len(line) and line[index] == "<":
        index += 1
        if mailbox():
            if line[index] == ">":
                return True
        else:
            return False
    error_code = "path"
    return False

def mailbox():
    """Examines <local-part> "@" <domain>"""
    global index, error_code
    if local_part():
        if index >= len(line) or line[index] != "@":
            error_code = "mailbox"
            return False
        index += 1
        return domain()
    return False

def local_part():
    """Examines <string>"""
    global index
    if string():
        return True
    else:
        return False
    
def string():
    """Examines <char> | <char> <string>"""
    global index, error_code
    if not char():
        error_code = "string"
        return False
    
    while index < len(line) and char():
        index += 1
    return True

def char():
    """Examines for ASCII characters except for <SP> or <special>"""
    global index
    if sp() or special() or not line[index].isascii():
        return False
    else:
        return True

def domain():
    """Examines <element> | <element> "." <domain>"""    
    global index
    if element():
        if index < len(line) and line[index] == ".":
            index += 1
            return domain()
        return True
    return False

def element():
    """Examines <letter> | <name>"""
    global index, error_code
    if name():
        return True
    elif letter():
        return True
    error_code = "element"
    return False

def name():
    """Examines <letter> <let-dig-str>"""
    global index
    if index < len(line):
        if letter():
            index += 1
            while let_dig_str() and index < len(line):
                index += 1
            return True
    return False

def letter():
    """Examines for any one of the 52 alphabetic characters"""
    global index
    if index < len(line) and line[index].isalpha():
        return True
    return False

def let_dig_str():
    """Examines <let-dig> | <let-dig-str>"""
    global index
    while let_dig() and index < len(line):
        index += 1
    return False

def let_dig():
    """Examines <letter> | <digit>"""
    global index
    if index < len(line):
        return letter() or digit()
    return False
def digit():
    """Examines any one of the ten digits 0 through 9"""
    global index
    if index < len(line):
        return line[index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    return False

def crlf():
    """Examines for the newline character"""
    global index, error_code
    if index >= len(line) or line[index] != '\n':
        error_code = "CRLF"
        return False
    return True

def special():
    """Examines for > < ( ) [ ] \ . , ; : @ and three quotes"""
    global index
    if index + 2 < len(line):
        if line[index] + line[index + 1] + line[index + 2] == '"""':
            return True
    return line[index] in [">", "<", "(", ")", "[", "]", "\\", ".", ",", ";", ":", "@", '"""']

def forward_path():
    """Examine for the forward-path for the RCPT command."""
    return path()

def data_cmd():
    """Examines for the <data-cmd>"""
    global index, error_code
    index = 0
    if line[index] == "D" and line[index + 1] == "A" and line[index + 2] == "T" and line[index + 3] == "A":
        index = 4
        nullspace()
        if crlf():
            return True
    error_code = "DATA"
    return False

def read_SMTP(clientSocket: socket, email: str):
    global passed
    valid = True
    # enter MAIL FROM segment, which will terminate immediately and go to RCPT TO once complete
    lines = email.split('\n')
    line = lines[0]
    if line[:6] == "From: ":
        message = f"MAIL FROM: {line[6:]}\n"
        clientSocket.send(message.encode())
    response = clientSocket.recv(1024).decode()
    if not response_code(response.strip('\n'), "250"):
        valid = False
    
    # Enter RCPT TO segment, terminate when there is no more "To:"
    line = lines[1]
    if line[0:4] == "To: ":
        line = line[3:]
    recipients = line.split(",")
    for recipient in recipients:
        clientSocket.send(f"RCPT TO:{recipient}\n".encode())
        response = clientSocket.recv(1024).decode()
        if not response_code(response.strip('\n'), "250"):
            valid = False

    # enter Data segment, expect 354
    clientSocket.send("DATA\n".encode())
    response = clientSocket.recv(1024).decode()
    if not response_code(response.strip('\n'), "354"):
        valid = False

    clientSocket.send(email.encode())
    response = clientSocket.recv(1024).decode()
    if not response_code(response.strip('\n'), "250"):
        valid = False

    
    # encountered the end of the email

def response_code(response: str, expected: str):
    """Checks for response code matching and failure - responds accordingly."""
    if response[:3] == expected:
        if whitespace_and_arbitrary(response, 3):
            return True
    if response[:3] == "500" or response[:3] == "501" or response[:3] == "503" or response[:3] == "354" or response[:3] == "250":
        raise SMTPException()
    
    return False
    
def whitespace_and_arbitrary(response: str, index: int):
    """Examines for whitespace and arbritrary printable characters after."""
    if not space(response, index):
        return False
    while space(response, index):
        index += 1

    if response[index].isprintable():
        while index < len(response) and response[index].isprintable():
            index += 1
        if index == len(response):  
            return True
    return False 

def space(response, index):
    """Examines for the space or tab character"""
    return response[index] == "\t" or response[index] == " "

def getemail():
    global line, index, error_code
    email = ""

    # get From: command
    valid = False
    index = 0
    line = input(f"From:\n").strip()
    line = f"<{line}>"
    while not reverse_path():
        print(f"ERROR -- {error_code}")
        line = input(f"From:\n")
        line = f"<{line}>"
        index = 0
    fromClause = f"{line}"
    email += f"From: {fromClause}\n"

    valid = False
    while not valid:
        recipients = []
        line = input(f"To:\n")
        toClause = line.split(',')
        valid = True
        for recipient in toClause:
            line = recipient
            whitespace()
            line = line.strip()
            line = f"<{line}>"
            index = 0
            if not forward_path():
                print(f"ERROR -- {error_code}")
                valid = False
            else:
                recipients.append(f"{line}")

    email += "To:"
    for i in range(0, len(recipients)):
        if i == len(recipients) - 1:
            email += f" {recipients[i]}\n"
        else:
            email += f" {recipients[i]},"
    

    line = input(f"Subject:\n")
    subjectClause = line.strip('\n')
    email += f"Subject: {subjectClause}\n\n"

    messageClause = []
    line = input(f"Message:\n")
    while line.strip('\n') != ".":
        messageClause.append(line.strip('\n'))
        line = input()

    for i in range(0, len(messageClause)):
        email += f"{messageClause[i]}\n"

    return email
    

try:
    # get file from argv and read it
    serverName=sys.argv[1]
    serverPort=int(sys.argv[2])


    line = ""
    index = 0
    recipients = []
    error_code = ""
    email = getemail()
    passed = False
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        
        modifiedSentence = clientSocket.recv(1024).decode()
        ## need to confirm this is a valid greeting message
        clientSocket.send(f'HELO {gethostname()}\n'.encode())
        
        modifiedSentence = clientSocket.recv(1024).decode()

        read_SMTP(clientSocket=clientSocket, email=email)
        clientSocket.send("QUIT\n".encode())
        modifiedSentence = clientSocket.recv(1024).decode()
    except TimeoutError as e:
        print(f"Timeout Error: {e}")
        clientSocket.send("timeout error".encode())
    except PermissionError as e:
        print(f"Permission Error: {e}")
    except ConnectionError as e:
        print(f"Connection Error: {e}")
    except OSError as e:
        print(f"OS Error: {e}")
    except SMTPException as e:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if clientSocket:
            clientSocket.close()
except error as e:
    print("Port in use")
except SMTPException as e:
    pass
except EOFError as e:
    pass