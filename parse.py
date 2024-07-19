"""Parsing Email Command - Chiara Sabato"""
# Honor Pledge: I will neither give nor receive aid on this assessment.

import sys

def mail_from_cmd():
    """Examines “MAIL” <SP> “FROM:” <reverse-path> <CRLF>"""
    global index, error_code
    error_code = "mail-from-cmd"
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
    return False

def whitespace():
    """Examines for whitespace"""
    global index, error_code
    if not sp():
        error_code = "whitespace"
        return False
    
    while sp():
        index += 1
    
    return True

def sp():
    """Examines for the space or tab character"""
    global index
    return line[index] == " " or line[index] == "\t" 

def nullspace():
    """Examines for nullspace"""
    global index
    if index >= len(line):
        return False
    if null():
        return True
    elif whitespace():
        return True
    else:
        return False
    
    
def null():
    """Examines for no character"""
    global index
    return line[index] == ""

def reverse_path():
    """Examines <path>"""
    return path()

def path():
    """Examines "<" <mailbox> ">" """
    global index, error_code
    if line[index] == "<":
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
        if line[index] != "@":
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
    while char():
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
        if line[index] == ".":
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
    if letter():
        index += 1
        while let_dig_str():
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
    global index
    check = False
    while let_dig():
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
    global index, error_code
    error_code = "CRLF"
    if index >= len(line):
        return False
    return line[index] == '\n'

def special():
    """Examines for > < ( ) [ ] \ . , ; : @ and three quotes"""
    global index
    if index + 2 < len(line):
        if line[index] + line[index + 1] + line[index + 2] == '"""':
            return True
    return line[index] in [">", "<", "(", ")", "[", "]", "\\", ".", ",", ";", ":", "@", '"""']

for line in sys.stdin:
    index = 0
    error_code = None
    result = mail_from_cmd()
    # process input line
    print(line.strip('\n'))
    if result:
        print("Sender ok")
    else:
        print(f"ERROR -- {error_code}")

