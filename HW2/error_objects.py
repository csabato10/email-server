# Chiara Sabato - csabato - 730466575
# Honor Pledge: I will neither give nor receive aid on this assessment.

# Catches issues in the command of the input
class CommandSytanxException(Exception):
    pass

# Catches errors in the parameter of the input
class ParamArgSytanxException(Exception):
    pass

# Catches a correct command but seen in the wrong order
class BadSequenceException(Exception):
    pass