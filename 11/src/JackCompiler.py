import JackTokenizer, CompilationEngine, sys, os, glob
from Util import *

class JackCompiler:
    ''' Jack Compiler module '''

    def __init__(self, file_in, file_out):
        '''
        Constructor
        Input: file_in (string)
        '''
        self.file_in = file_in
        self.file_out = file_out

    def parse(self):
        parser = CompilationEngine.CompilationEngine(self.file_in, self.file_out)
        while parser.get_terminal() == (KEYWORD, CLASS):
            parser.compile_class()
        parser.vm_writer.close()


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python JackCompiler.py <file.jack|directory>')
    arg = sys.argv[1]

    # If the argument ends with '.jack', use it as the single input file.
    if arg.endswith('.jack'):
        file_list = [arg]
    # Otherwise, consider the argument as a directory.
    else:
        if arg.endswith('/'):
            arg = arg[:-1]
        # Get a list of files ending with '.jack' from the directory.
        file_list = glob.glob(arg + '/*.jack')
        if len(file_list) == 0:
            print('''Error: No proper input file names found. Please \
use a file name ending with '.jack' or a directory containing '.jack' files.''')
            sys.exit()

    for file_in in file_list:
        file_out = file_in.replace('.jack', '.vm')
        jack_compiler = JackCompiler(file_in, file_out) 
        jack_compiler.parse()