"""SMTP Server Construction - Final Step"""
# Chiara Sabato - csabato - 730466575
# Honor Pledge: I will neither give nor receive aid on this assessment.

import sys

class CommandException(Exception):
    # exception for command based errors
    pass

def read_SMTP():
    global line
    # enter MAIL FROM segment, which will terminate immediately and go to RCPT TO once complete
    if line[:6] == "From: ":
        print("MAIL FROM: " + line[6:-1])
        response = input()
        response_code(response, "250")
        print(response.strip('\n'), file=sys.stderr)

    # Enter RCPT TO segment, terminate when there is no more "To:"
    line = messages.readline()
    while line[0:4] == "To: ":
        print("RCPT TO: " + line[4:-1])
        response = input()
        response_code(response, "250")
        print(response.strip('\n'), file=sys.stderr)
        line = messages.readline()

    # enter Data segment, expect 354
    print("DATA")
    response = input()
    response_code(response, "354")
    print(response.strip('\n'), file=sys.stderr)

    # print out lines that are not "From:" or "To:" in order as the body text
    while line[0:5] != "From:":
        print(line.strip('\n'))
        line = messages.readline()
        if line == "":
            break

    # encountered the end of the email
    print(".")
    response = input()
    response_code(response, "250")
    print(response.strip('\n'), file=sys.stderr)
    if line == "":
        return False
    return True


def response_code(response: str, expected: str):
    """Checks for response code matching and failure - responds accordingly."""
    if response[:3] == expected:
        if whitespace_and_arbitrary(response, 3):
            return
    if response[:3] == "500" or response[:3] == "501" or response[:3] == "503" or response[:3] == "354" or response[:3] == "250":
        raise CommandException(response)
    raise CommandException(response)


    
def whitespace_and_arbitrary(response, index):
    """Examines for whitespace and arbritrary printable characters after."""
    if not sp(response, index):
        return False
    while sp(response, index):
        index += 1

    if response[index].isprintable():
        while  index < len(response) and response[index].isprintable():
            index += 1
        if index == len(response):  
            return True
    return False 

def sp(response, index):
    """Examines for the space or tab character"""
    return response[index] == "\t" or response[index] == " "

try:
    # get file from argv and read it
    messages = open(sys.argv[1], "r")
    line = messages.readline()
    reading = True
    # loop to keep reading 
    while reading:
        reading = read_SMTP()
    # quit upon success and termination of reading file
    print("QUIT")
except CommandException as e:
    # catching errors and sending to stand error and printing QUIT
    print(e, file=sys.stderr)
    print("QUIT")
except Exception as e:
    # catching any random errors and exiting with no QUIT
    pass