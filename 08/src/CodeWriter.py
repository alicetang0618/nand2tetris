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
        # Keep track of the function that has the current control.
        self.current_function = ""

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
                self.file_out.write("D=M-D\n@" + self.label_prefix() + "FALSE" + str(self.symbol_idx) 
                    + "\n" + ARITHMETIC_CODE_DICT[command]+ "@SP\nA=M-1\nM=-1\n@" + self.label_prefix() + "END" 
                    + str(self.symbol_idx) + "\n0;JMP\n(" + self.label_prefix() + "FALSE" + str(self.symbol_idx)
                    + ")\n@SP\nA=M-1\nM=0\n(" + self.label_prefix() + "END" + str(self.symbol_idx) + ")\n")
                # Everytime after using the symbols, increase the symbol index by 1
                self.symbol_idx += 1
        else:
        # That is, if command in ['neg', 'not'] 
            self.file_out.write("@SP\nA=M-1\n" + ARITHMETIC_CODE_DICT[command])

    def write_push_pop(self, command, segment, index):
        '''
        Writes the assembly code that is the translation of the given push 
        or pop command.
        Input: command (C_PUSH, C_POP), segment (string), index (string)
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

    def label_prefix(self):
        prefix = ""
        if len(self.current_function) > 0:
            prefix = self.current_function + "$" 
        return prefix

    def write_init(self):
        '''
        Writes assembly code that effects the VM initialization.
        '''
        self.file_out.write("@256\nD=A\n@SP\nM=D\n")
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        '''
        Writes assembly code that effects the label command.
        Input: label (string)
        '''
        self.file_out.write("(" + self.label_prefix() + label + ")\n" )

    def write_goto(self, label):
        '''
        Writes assembly code that effects the goto command.
        Input: label (string)
        '''
        self.file_out.write("@" + self.label_prefix() + label + "\n0;JMP\n")

    def write_if(self, label):
        '''
        Writes assembly code that effects the if-goto command.
        Input: label (string)
        '''
        self.file_out.write("@SP\nAM=M-1\nD=M\n@" + self.label_prefix() + label + "\nD;JNE\n")

    def write_call(self, function_name, num_args):
        '''
        Writes assembly code that effects the call command.
        Input: function_name (string), num_args (int)
        '''
        address = "return-address" + str(self.symbol_idx)
        self.symbol_idx += 1
        self.file_out.write("@" + address + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        for seg in ['LCL', 'ARG', 'THIS', 'THAT']:
            self.file_out.write("@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" % seg)
        # LCL = SP
        # ARG = SP-num_args-5
        self.file_out.write("@SP\nD=M\n@LCL\nM=D\n@" + str(int(num_args) + 5)
            + "\nD=D-A\n@ARG\nM=D\n@" + function_name + "\n0;JMP\n(" + address + ")\n")

    def write_return(self):
        '''
        Writes assembly code that effects the return command.
        '''
        # FRAME = LCL
        # RET = *(FRAME-5)
        # *ARG = pop()
        # SP = ARG+1
        # THAT = *(FRAME-1)
        # THIS = *(FRAME-2)
        # ARG = *(FRAME-3)
        # LCL = *(FRAME-4)
        # goto RET
        self.file_out.write("@LCL\nD=M\n@FRAME\nM=D\n@5\nA=D-A\nD=M\n@RET\nM=D\n\
@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\nD=A+1\n@SP\nM=D\n@FRAME\nAM=M-1\nD=M\n\
@THAT\nM=D\n@FRAME\nAM=M-1\nD=M\n@THIS\nM=D\n@FRAME\nAM=M-1\nD=M\n@ARG\nM=D\n\
@FRAME\nA=M-1\nD=M\n@LCL\nM=D\n@RET\nA=M\n0;JMP\n")

    def write_function(self, function_name, num_locals):
        '''
        Writes assembly code that effects the function command.
        Input: function_name (string), num_locals (string)
        '''
        self.file_out.write("(" + function_name + ")\n")
        self.current_function = function_name
        for i in range(int(num_locals)):
            self.write_push_pop(C_PUSH, "constant", "0")

    def write_comment(self, s):
        '''
        Helper function used for debugging.
        '''
        self.file_out.write("// " + s + "\n")

    def close(self):
        '''
        Closes the output file.
        '''
        self.file_out.close()