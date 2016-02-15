# Code Writer module for VM translator
from Util import *

class CodeWriter:
    """ Code Writer module """

    def __init__(self, file_out):
        '''
        Constructor
        Input: file_out (string)
        '''
        self.file_out = open(file_out, "w")
        self.vm_file = ""
        # Append a unique symbol_idx to each symbol, like (FALSE) and (END), 
        # to avoid duplicated symbols.
        self.symbol_idx = 0

    def set_file_name(self, file_name):
        '''
        Informs the code writer that the translation of a new VM file is started.
        Input: file_name (string)
        '''
        self.vm_file = file_name[file_name.rfind("/")+1:].replace(".vm", "")

    def write_arithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given arithmetic command.
        Input: command (string)
        '''
        assert(command in ARITHMETIC_CODE_DICT.keys())
        if command not in ['neg', 'not']:
            self.file_out.write("@SP\nAM=M-1\nD=M\nA=A-1\n")
            if command in ['add', 'sub', 'and', 'or']:
                self.file_out.write(ARITHMETIC_CODE_DICT[command])
            else:
            # That is, if command in ['eq', 'gt', 'lt']
                self.file_out.write("D=M-D\n@FALSE" + str(self.symbol_idx) 
                    + "\n" + ARITHMETIC_CODE_DICT[command]+ "@SP\nA=M-1\nM=-1\n@END" 
                    + str(self.symbol_idx) + "\n0;JMP\n(FALSE" + str(self.symbol_idx)
                    + ")\n@SP\nA=M-1\nM=0\n(END" + str(self.symbol_idx) + ")\n")
                # Everytime after using the symbols, increase the symbol index by 1
                self.symbol_idx += 1
        else:
        # That is, if command in ['neg', 'not'] 
            self.file_out.write("@SP\nA=M-1\n" + ARITHMETIC_CODE_DICT[command])

    def write_push_pop(self, command, segment, index):
        '''
        Writes the assembly code that is the translation of the given push 
        or pop command.
        Input: command (C_PUSH, C_POP), segment (string), index (string/int)
        '''
        assert(command in [C_PUSH, C_POP])
        if command == C_PUSH:
            if segment == 'constant':
                self.file_out.write("@" + index + "\nD=A\n")
            elif segment == 'static':
                self.file_out.write("@" + self.vm_file + "." + index + "\nD=M\n")
            elif segment in ['pointer', 'temp']:
                self.file_out.write("@" + str(SEGMENT_CODE_DICT[segment]+int(index)) + "\nD=M\n")
            else: 
            # That is, segment in ['local', 'argument', 'this', 'that']
                self.file_out.write("@" + SEGMENT_CODE_DICT[segment] + "\nD=M\n@" 
                    + index + "\nA=D+A\nD=M\n")
            # After putting the value into D, push it on to stack from D.
            self.file_out.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        else:
            if segment == 'static':
                self.file_out.write("@" + self.vm_file + "." + index + "\nD=A\n")
            elif segment in ['pointer', 'temp']:
                self.file_out.write("@" + str(SEGMENT_CODE_DICT[segment]+int(index)) + "\nD=A\n")
            else:
            # That is, segment in ['local', 'argument', 'this', 'that']
                self.file_out.write("@" + SEGMENT_CODE_DICT[segment] + "\nD=M\n@" + index + "\nD=D+A\n")
            # After putting the dest address into D, store the address in
            # a temporary location, pop the value from the stack to D, and store
            # the value into the address.
            self.file_out.write("@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def close(self):
        '''
        Closes the output file.
        '''
        self.file_out.close()