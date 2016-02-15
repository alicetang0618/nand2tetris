import Parser, CodeWriter, sys, glob
from Util import *

class VMTranslator:
    """ VM translater module """

    def __init__(self, file_list, file_out):
        '''
        Constructor
        Input: file_list (list of strings), file_out (string)
        '''
        self.files_in = file_list
        self.file_out = file_out

    def translate_all(self):
        '''
        Translates all the .vm files in file_list to assembly language 
        and save the output to file_out.
        '''
        code_writer = CodeWriter.CodeWriter(self.file_out)
        for file_in in self.files_in:
            self.translate(file_in, code_writer)
        code_writer.close()

    def translate(self, file_in, code_writer):
        '''
        Translate a single .vm file. Called in self.translate_all().
        Input: file_in (string), code_writer (CodeWriter object)
        '''
        parser = Parser.Parser(file_in)
        code_writer.set_file_name(file_in)
        while parser.has_more_commands():
            parser.advance()
            arg1 = parser.arg1()
            # For project 07, only consider C_ARITHMETIC, C_PUSH and C_POP.
            if parser.command_type() == C_ARITHMETIC:
                code_writer.write_arithmetic(arg1)
            elif parser.command_type() in [C_PUSH, C_POP]:
                arg2 = parser.arg2()
                code_writer.write_push_pop(parser.command_type(), arg1, arg2)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python VMTranslator.py <file.vm|directory>")
    arg = sys.argv[1]

    # If the argument ends with ".vm", use it as the single input file.
    if arg.endswith(".vm"):
        file_list = [arg]
        file_out = arg.replace('.vm', '.asm')
    # Otherwise, consider the argument as a directory.
    else:
        if arg.endswith("/"):
            arg = arg[:-1]
        # Get a list of files ending with ".vm" from the directory.
        file_list = glob.glob(arg + "/*.vm")
        if len(file_list) == 0:
            print("""Error: No proper input file names found. Please use a file name ending with '.vm' or a directory containing '.vm' files.""")
            sys.exit()
        file_out = arg + ".asm"
    
    vm_translator = VMTranslator(file_list, file_out)
    vm_translator.translate_all()