# Parser module for VM translator
from Util import *

class Parser:
    """ Parser module """

    def __init__(self, file_in):
        '''
        Constructor
        Input: file_in (string)
        '''
        f = open(file_in)
        self.lines = f.readlines()
        self.command = ""
        self.idx = -1

    def has_more_commands(self):
        '''
        Returns true if there are more commands in the input.
        Output: boolean
        '''
        return self.idx < len(self.lines) - 1

    def advance(self):
        ''' 
        Reads the next command from the input and makes it the current command.
        '''
        assert(self.has_more_commands())
        self.idx += 1
        self.command = clean_command(self.lines[self.idx])
        if self.command == "" and self.has_more_commands():
            self.advance()

    def command_type(self):
        '''
        Returns the type of the current command.
        Output: C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, 
        C_RETURN, or C_CALL
        '''
        words = self.command.split()
        if len(words) == 3:
            if words[0] == 'push':
                return C_PUSH
            elif words[0] == 'pop':
                return C_POP
        if len(words) == 1 and words[0] in ARITHMETIC_CODE_DICT.keys():
            return C_ARITHMETIC
        # If the line doesn't match the pattern of C_ARITHMETIC, 
        # C_PUSH or C_POP, return None as the command type.
        return None

    def arg1(self):
        '''
        Returns the first argument of the current command.
        Output: string
        '''
        assert(self.command_type() not in [C_RETURN, None])
        if self.command_type() == C_ARITHMETIC:
            return self.command
        else:
            return self.command.split()[1]

    def arg2(self):
        '''
        Returns the second argument of the current command.
        Output: string
        '''
        assert(self.command_type() in [C_PUSH, C_POP, C_FUNCTION, C_CALL])
        return self.command.split()[2]