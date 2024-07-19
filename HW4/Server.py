"""Server Side of Homework 4."""

# server will process commands and store messages in destination domain

# these email messages will be written to a domain file

# server sends a greeting message "220 {hostname of my computer}"

# read SMTP command arguments from clinet
# write this to a domain file

# check for socket errors on any read. close socket no matter the errors
# close connection socket after reading emails and return to listening socket

# server will be terminated by control+C

# Chiara Sabato - csabato - 730466575
# Honor Pledge: I will neither give nor receive aid on this assessment.

import sys
import os
from enum import Enum
from socket import *
import difflib



# Catches issues in the command of the input
class CommandSytanxException(BaseException):
    def __str__(self):
        return "500 Syntax error: command unrecognized\n"

# Catches errors in the parameter of the input
class ParamArgSytanxException(BaseException):
    def __str__(self):
        return "501 Syntax error in parameters or arguments\n"

# Catches a correct command but seen in the wrong order
class BadSequenceException(BaseException):
    def __str__(self):
        return "503 Bad sequence of commands\n"

def mail_from_cmd():
    """Examines “MAIL” <SP> “FROM:” <reverse-path> <CRLF>"""
    global index, line
    if index + 5 < len(line) and line[index] == "M" and line[index + 1] == "A" and line[index + 2] == "I" and line[index + 3] == "L":
        index = 4
        if whitespace():
            if index + 6 < len(line) and line[index] == "F" and line[index + 1] == "R" and line[index + 2] == "O" and line[index + 3] == "M" and line[index + 4] == ":":
                index += 5
                nullspace()
                if reverse_path():
                    index += 1
                    nullspace()
                    if crlf():
                        return True
    raise CommandSytanxException()

def whitespace():
    """Examines for whitespace"""
    global index
    if not sp():
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
    global index
    if index < len(line) and line[index] == "<":
        index += 1
        if index < len(line) and mailbox():
            if line[index] == ">":
                return True
        else:
            raise ParamArgSytanxException()
    raise ParamArgSytanxException()

def mailbox():
    """Examines <local-part> "@" <domain>"""
    global index
    if index < len(line) and local_part():
        if line[index] != "@":
            raise ParamArgSytanxException
        index += 1
        return domain()
    return False

def local_part():
    """Examines <string>"""
    global index
    if index < len(line) and string():
        return True
    else:
        return False
    
def string():
    """Examines <char> | <char> <string>"""
    global index
    if not char():
        raise ParamArgSytanxException()
    while char():
        index += 1
    if index < len(line):
        return True
    return False

def char():
    """Examines for ASCII characters except for <SP> or <special>"""
    global index
    if index >= len(line) or sp() or special() or not line[index].isascii():
        return False
    else:
        return True

def domain():
    """Examines <element> | <element> "." <domain>"""    
    global index
    if index < len(line):
        if element():
            if index < len(line):
                if line[index] == ".":
                    index += 1
                    return domain()
            return True
    return False

def element():
    """Examines <letter> | <name>"""
    global index
    if index < len(line):
        if name():
            return True
        elif letter():
            return True
    raise ParamArgSytanxException()

def name():
    """Examines <letter> <let-dig-str>"""
    global index
    if index < len(line):
        if letter():
            index += 1
            while index < len(line) and let_dig_str():
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
    while index < len(line) and let_dig():
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
    global index
    if index >= len(line) or line[-1] != '\n':
        raise ParamArgSytanxException()
    return True

def special():
    """Examines for > < ( ) [ ] \ . , ; : @ and three quotes"""
    global index
    if index + 2 < len(line):
        if line[index] + line[index + 1] + line[index + 2] == '"""':
            return True
    return line[index] in [">", "<", "(", ")", "[", "]", "\\", ".", ",", ";", ":", "@", '"""']

def rcpt_to_cmd():
    """Examine for “RCPT” <whitespace> “TO:” <nullspace> <forward-path> <nullspace> <CRLF>."""
    global index
    index = 0
    if line[index] == "R" and line[index + 1] == "C" and line[index + 2] == "P" and line[index + 3] == "T":
        index = 4
        if whitespace():
            if line[index] == "T" and line[index + 1] == "O" and line[index + 2] == ":":
                index += 3
                nullspace()
                if forward_path():
                    index += 1
                    nullspace()
                    if index < len(line) and line[index] != '\n':
                        raise ParamArgSytanxException()
                    if crlf():
                        return True
    raise CommandSytanxException()

def forward_path():
    """Examine for the forward-path for the RCPT command."""
    return path()

def data_cmd():
    """Examines for the <data-cmd>"""
    global index
    index = 0
    if line[index] == "D" and line[index + 1] == "A" and line[index + 2] == "T" and line[index + 3] == "A":
        index = 4
        nullspace()
        if crlf():
            return True
        raise ParamArgSytanxException()
    raise CommandSytanxException()

class state(Enum):
    MAIL = "mail"
    RCPT = "rcpt"
    DATA = "data"

def state_checker(connectionSocket: socket):
    global current, message, recipients, finished, line, host_name
    if state.MAIL == current:
        # expecting a mail command
        try:
            # tesing mail command and continues to change state and pass if correct
            mail_from_cmd()
            current = state.RCPT
            connectionSocket.send("250 OK\n".encode())
        except CommandSytanxException as e:
            # catches and error in the Command Syntax meaning the command does not match MAIL FROM
            try:
                # test to see if the command matches a RCPT TO and if so, it is in the wrong order
                rcpt_to_cmd()
                raise BadSequenceException()
            except ParamArgSytanxException as e:
                # if RCPT TO throws a paramarg exception then it's Command passed, so it is still in the wrong order
                raise BadSequenceException()
            except CommandSytanxException as e:
                # if the RCPT TO issue is in the command, test the DATA command
                if line[:4] == "HELO":
                    raise BadSequenceException()
                
                try:
                    # test to see if the command matches a DATA and if so, it is in the wrong order
                    data_cmd()
                    raise BadSequenceException()
                except ParamArgSytanxException as e:
                    # if DATA throws a paramarg exception then it's Command passed, so it is still in the wrong order
                    raise BadSequenceException()
                except CommandSytanxException as e:
                    # if DATA fails then the problem is only with the command of MAIL and thus should rethrow CommandError
                    raise CommandSytanxException()
        except ParamArgSytanxException as e:
            current = state.MAIL
            raise ParamArgSytanxException()
        # failing to catch a ParameterException because it will be caught later down in the looping block
    elif state.RCPT == current:
        # testing RCPT TO command because the state is currently RCPT
        try:
            # test RCPT TO and if a successful message, passes, adds to recipients and is prepared to run again if necessary
            rcpt_to_cmd()
            recipients.append(line[9:-1])
            connectionSocket.send("250 OK\n".encode())
        except CommandSytanxException as e:
            # catches an error in the command of RCPT and checks if a different command was given
            try:
                # checks for MAIL FROM command and if success throws and order error
                mail_from_cmd()
                raise BadSequenceException()
            except ParamArgSytanxException as e:
                # if a ParamArg is caught then Command passed thus the order is wrong again
                raise BadSequenceException()
            except CommandSytanxException as e:
                # if a commandexception is caught for MAIL FROM then check DATA
                if line[:4] == "HELO":
                    raise BadSequenceException()
                if len(recipients) > 0:
                    try:
                        # checks data command for passing
                        data_cmd()
                        current = state.DATA
                        connectionSocket.send("354 Start mail input; end with <CRLF>.<CRLF>\n".encode())
                    except ParamArgSytanxException as e:
                        # if a Param arg is caught with DATA then it is not properly formatted as a DATA command
                        raise ParamArgSytanxException()
                    except CommandSytanxException as e:
                    # if DATA fails then the problem is only with the command of MAIL and thus should rethrow CommandError
                        raise CommandSytanxException
                else:
                    try: 
                        data_cmd()
                        raise BadSequenceException() 
                    except ParamArgSytanxException as e:
                        raise BadSequenceException()
                    except CommandSytanxException as e:
                    # if DATA fails then the problem is only with the command of MAIL and thus should rethrow CommandError
                        raise CommandSytanxException()   
        # not accounting for parameter exception as it will be caught in the original loop because it is not caught here      
    elif state.DATA == current:
        # only enters if there has been a successful data command retreieved after RCPT TO
        folder = "forward"
        try:
            path = os.path.dirname(__file__)
            folder = os.path.join(path, folder)
            if not os.path.exists(folder):
                os.mkdir(folder)
            # creates a file for each recipient
            domains = []
            for recipient in recipients:
                file: str = recipient.replace("<", "") # gets the address of the recipient without brackets for file name
                file = recipient.replace(">", "")
                file = file.split("@")
                domains.append(file[1])
            domains = set(domains)

            for domain in domains:
                destination = os.path.join(folder, domain) # creates file path
                if os.path.exists(destination):
                    with open(destination, 'a') as serv: # append if file exists
                        serv.write(line)
                else: # write to new file if not
                    with open(destination, 'w') as serv: 
                        serv.write(line)
            # reset for next message
            finished = True
            connectionSocket.send("250 OK\n".encode())

        # error catching for I/O issues
        except PermissionError() as e:
            pass
        except FileNotFoundError() as e:
            pass


def confirm_helo():
    """Confirm HELO message."""
    global index, line
    client_name = ""
    if line[:4] == "HELO":
        index += 4
        if whitespace():
            start_index = index
            client_name = line[start_index: -2]
            if client_name.isprintable():
                if crlf():
                    return client_name, True
        connectionSocket.send(f"501 Syntax error in parameters or arguments\n".encode())
        return client_name, False
    connectionSocket.send(f"500 Syntax error: command unrecognized\n".encode())
    return client_name, False
    
# message = []
# recipients = []
# sender = ""
# address = ""
# finished = False

try:
    serverPort = int(sys.argv[1]) # single command line argument - port number to listen for connections
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    connectionSocket = None

    while True:
        # create connection to the socket
        try:
            current: state = state.MAIL
            recipients: list[str] = []
            finished: bool = False
            message: str = ""
            connectionSocket, addr = serverSocket.accept()
            # send approval connection
            connectionSocket.send(f"220 {gethostname()}\n".encode())
            line: str = connectionSocket.recv(1024).decode()
            # check HELO
            index: int = 0
            host_name, valid = confirm_helo()

            while not valid:
                index = 0
                line: str = connectionSocket.recv(1024).decode()
                host_name, valid = confirm_helo()
            
            connectionSocket.send(f"250 Hello {host_name} pleased to meet you\n".encode())
            while True:
                try:
                    line = connectionSocket.recv(1024).decode()
                    if not line:
                        break
                    if line == "QUIT\n" or line.strip('\r\n') == "QUIT":
                        break 
                    index = 0
                    state_checker(connectionSocket)
                except timeout as e:
                    print("Timeout Error")
                    if connectionSocket:
                        connectionSocket.send(f"Timeout Error: {e}\n".encode())
                    break
                except CommandSytanxException as e:
                    current = state.MAIL
                    if connectionSocket:
                        connectionSocket.send(str(e).encode())
                except BadSequenceException as e:
                    current = state.MAIL
                    if connectionSocket:
                        connectionSocket.send(str(e).encode())
                except ParamArgSytanxException as e:
                    current = state.MAIL
                    if connectionSocket:
                        connectionSocket.send(str(e).encode())

            connectionSocket.send(f"221 {host_name} closing connection\n".encode())

            connectionSocket.close()
        except TimeoutError as e:
            print("Timeout Error")
            if connectionSocket:
                connectionSocket.send(f"Timeout Error: {e}\n".encode())
        except PermissionError as e:
            print("Permissions Error")
            if connectionSocket:
                connectionSocket.send(f"Permission Error: {e}\n".encode())
        except FileNotFoundError as e:
            print("File Not Found Error")
            if connectionSocket:
                connectionSocket.send(f"Connection Error: {e}\n".encode())
        except ConnectionError as e:
            print("Connection Error")
            if connectionSocket:
                connectionSocket.send(f"Connection Error: {e}\n".encode())
        except OSError as e:
            print("OSError")
            if connectionSocket:
                connectionSocket.send(f"OS Error: {e}\n".encode())
        finally:
            if connectionSocket is not None:
                connectionSocket.close()
except error as e:
    print("Port in use")
except KeyboardInterrupt as e:
    print("Keyboard interupt")
except Exception as e:
    print(f"Exception Occurred: {e}")
finally:
    if serverSocket:
        serverSocket.close()