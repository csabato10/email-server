"""Parsing Email Command - Chiara Sabato"""
# Chiara Sabato - csabato - 730466575
# Honor Pledge: I will neither give nor receive aid on this assessment.


import sys, os
from error_objects import CommandSytanxException, BadSequenceException, ParamArgSytanxException
from enum import Enum

def mail_from_cmd():
    """Examines “MAIL” <SP> “FROM:” <reverse-path> <CRLF>"""
    global index
    if line[index] == "M" and line[index + 1] == "A" and line[index + 2] == "I" and line[index + 3] == "L":
        index = 4
        if whitespace():
            if line[index] == "F" and line[index + 1] == "R" and line[index + 2] == "O" and line[index + 3] == "M" and line[index + 4] == ":":
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
    
    while sp():
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
    global index, address
    address = ""
    if line[index] == "<":
        address += "<"
        index += 1
        if mailbox():
            if line[index] == ">":
                address += ">"
                return True
        else:
            raise ParamArgSytanxException()
    raise ParamArgSytanxException()

def mailbox():
    """Examines <local-part> "@" <domain>"""
    global index, address
    if local_part():
        if line[index] != "@":
            raise ParamArgSytanxException
        address += "@"
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
    global index, address
    if not char():
        raise ParamArgSytanxException()
    while char():
        address += line[index]
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
    global index, address
    if element():
        if line[index] == ".":
            address += "."
            index += 1
            return domain()
        return True
    return False

def element():
    """Examines <letter> | <name>"""
    global index
    if name():
        return True
    elif letter():
        return True
    raise ParamArgSytanxException()

def name():
    """Examines <letter> <let-dig-str>"""
    global index, address
    if letter():
        address += line[index]
        index += 1
        while let_dig_str():
            address += line[index]
            index += 1
        return True
    return False

def letter():
    """Examines for any one of the 52 alphabetic characters"""
    global index
    if line[index].isalpha():
        return True
    return False

def let_dig_str():
    """Examines <let-dig> | <let-dig-str>"""
    global index, address
    check = False
    while let_dig():
        address += line[index]
        index += 1
        let_dig()
    return False

def let_dig():
    """Examines <letter> | <digit>"""
    global index
    return letter() or digit()

def digit():
    """Examines any one of the ten digits 0 through 9"""
    global index
    return line[index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def crlf():
    """Examines for the newline character"""
    global index
    if index >= len(line) or line[index] != '\n':
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
    global index, address, command
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

state = "MAIL-FROM"
message = []
recipients = []
sender = ""
address = ""
command = False

class state(Enum):
    MAIL = "mail"
    RCPT = "rcpt"
    DATA = "data"

def state_checker():
    global current, message, command, recipients, sender, address, line
    if state.MAIL == current:
        # expecting a mail command
        try:
            # tesing mail command and continues to change state and pass if correct
            mail_from_cmd()
            sender = address
            address = ""
            current = state.RCPT
            print("250 OK")
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
        # failing to catch a ParameterException because it will be caught later down in the looping block
    elif state.RCPT == current:
        # testing RCPT TO command because the state is currently RCPT
        try:
            # test RCPT TO and if a successful message, passes, adds to recipients and is prepared to run again if necessary
            rcpt_to_cmd()
            recipients.append(address)
            address = ""
            print("250 OK")
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
                if len(recipients) > 0:
                    try:
                        # checks data command for passing
                        data_cmd()
                        current = state.DATA
                        print("354 Start mail input; end with <CRLF>.<CRLF>")
                    except ParamArgSytanxException as e:
                        # if a Param arg is caught with DATA then it is not properly formatted as a DATA command
                        raise ParamArgSytanxException()
                    except CommandSytanxException as e: 
                        # if a command syntax exception is caught on DATA then an error is thrown
                        raise CommandSytanxException()    
                else:
                    try: 
                        data_cmd()
                        raise BadSequenceException() 
                    except ParamArgSytanxException as e:
                        raise BadSequenceException()
                    except CommandSytanxException as e:
                        raise CommandSytanxException()     
        # not accounting for parameter exception as it will be caught in the original loop because it is not caught here      
    elif state.DATA == current:
        # only enters if there has been a successful data command retreieved after RCPT TO
        if line != ".\n":
            # add to message message
            message.append(line)
        else:
            # message has been terminated by a \n.\n
            # code to add to file
            folder = "forward"
            try:
                path = os.path.dirname(__file__)
                folder = os.path.join(path, folder)
                if not os.path.exists(folder):
                    os.mkdir(folder)
                # creates a file for each recipient
                
                for recipient in recipients:
                    file = recipient[1: -1] # gets the address of the recipient without brackets for file name
                    destination = os.path.join(folder, file) # creates file path
                    if os.path.exists(destination):
                        with open(destination, 'a') as email: # append if file exists
                            email.write('From: ' + sender + '\n')
                            for receiver in recipients:
                                email.write('To: ' + receiver + '\n') # includes all receivers
                            for line in message:
                                email.write(line)
                    else: # write to new file if not
                        with open(destination, 'w') as email: 
                            email.write('From: ' + sender + '\n')
                            for receiver in recipients:
                                email.write('To: ' + receiver + '\n') # includes all receivers
                            for line in message:
                                email.write(line)
                # reset for next message
                print("250 OK")
                recipients = []
                message = []
                current = state.MAIL
            # error catching for I/O issues
            except PermissionError() as e:
                print("Error: Permission to edit file denied")
                recipients = []
                message = []
                current = state.MAIL
            except FileNotFoundError() as e:
                print("Error: File with name has not been found.")  
                recipients = []
                message = []
                current = state.MAIL


current = state.MAIL
# after a fully successeful message need to make a file and save message there
for line in sys.stdin:
    try:
        # test each command
        index = 0
        print(line.strip('\n'))
        state_checker()
    except CommandSytanxException as e:
        print("500 Syntax error: command unrecognized")
        # reset data for MAIL FROM state after error
        recipients = []
        message = []
        current = state.MAIL 
    except BadSequenceException as e:
        print("503 Bad sequence of commands")
        # reset data for MAIL FROM state after error
        recipients = []
        message = []
        current = state.MAIL
    except ParamArgSytanxException as e:
        print("501 Syntax error in parameters or arguments")
        # reset data for MAIL FROM state after error
        recipients = []
        message = []
        current = state.MAIL

if current == state.DATA:
    print("501 Syntax error in parameters or arguments")
    