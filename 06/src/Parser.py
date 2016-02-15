# Parser module for assembler
import re, sys
from util import clean_command

class Parser:
    """ Parser module """

    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

    def __init__(self, lines_in):
        self.lines = lines_in
        self.command = ""
        self.idx = -1

    def has_more_commands(self):
        '''
        Returns true if there are more commands in the input.
        '''
        return self.idx < len(self.lines) - 1

    def advance(self):
        ''' 
        Reads the next command from the input and makes it the 
        current command.
        '''
        assert(self.has_more_commands())
        self.idx += 1
        self.command = clean_command(self.lines[self.idx])
        if self.command == "" and self.has_more_commands():
            self.advance()

    def commandType(self):
        '''
        Returns the type of the current command.
        '''
        if self.command == "":
            return None
        if self.command[0] == '@':
            return Parser.A_COMMAND
        elif self.command[0] == '(':
            return Parser.L_COMMAND
        else:
            return Parser.C_COMMAND

    def symbol(self):
        '''
        Returns the symbol or decimal Xxx of the 
        current command @Xxx or (Xxx).
        '''
        assert(self.commandType() in [Parser.A_COMMAND, Parser.L_COMMAND])
        if self.commandType() == Parser.A_COMMAND:
            return self.command[1:]
        else:
            return self.command[1:-1]

    def dest(self):
        '''
        Returns the dest mnemonic in the current C-command.
        '''
        assert(self.commandType() == Parser.C_COMMAND)
        match = re.match(r'^(\w+)=.*$', self.command)
        if match:
            return match.group(1)
        else:
            return ""

    def comp(self):
        '''
        Returns the comp mnemonic in the current C-command.
        '''
        assert(self.commandType() == Parser.C_COMMAND)
        rv = re.sub(r'^\w*=', '', self.command)
        rv = re.sub(r';\w*$', '', rv)
        assert(rv != "")
        return rv

    def jump(self):
        '''
        Returns the jump mnemonic in the current C-command.
        '''
        assert(self.commandType() == Parser.C_COMMAND)
        match = re.match(r'^.*;(\w+)$', self.command)
        if match:
            return match.group(1)
        else:
            return ""
