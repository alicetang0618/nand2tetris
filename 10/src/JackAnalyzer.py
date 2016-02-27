import JackTokenizer, CompilationEngine, sys, os, glob
from Util import *

class JackAnalyzer:
    """ Jack Analyzer module """

    def __init__(self, file_in, file_out):
        '''
        Constructor
        Input: file_in (string)
        '''
        self.file_in = file_in
        self.file_out = open(file_out, "w")

    def tokenize(self):
        tokenizer = JackTokenizer.JackTokenizer(self.file_in)
        self.file_out.write("<tokens>\n")
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            token_type = tokenizer.token_type()
            if token_type == KEYWORD:
                self.file_out.write("<keyword> " + tokenizer.key_word() + " </keyword>\n")
            elif token_type == SYMBOL:
                self.file_out.write("<symbol> " + tokenizer.symbol() + " </symbol>\n")
            elif token_type == IDENTIFIER:
                self.file_out.write("<identifier> " + tokenizer.identifier() + " </identifier>\n")
            elif token_type == INT_CONST:
                self.file_out.write("<integerConstant> " + tokenizer.int_val() + " </integerConstant>\n")
            elif token_type == STRING_CONST:
                self.file_out.write("<stringConstant> " + tokenizer.string_val() + " </stringConstant>\n")
        self.file_out.write("</tokens>\n")
        self.file_out.close()

    def parse(self):
        parser = CompilationEngine.CompilationEngine(self.file_in, self.file_out)
        while parser.get_terminal() == "<keyword> class </keyword>\n":
            parser.compile_class()
        self.file_out.close()


if __name__ == "__main__":

    if len(sys.argv) not in [2, 3]:
        print("Usage: python JackAnalyzer.py <file.jack|directory> [print_tokens]")
    arg = sys.argv[1]
    print_tokens = (len(sys.argv) == 3 and sys.argv[2] == "print_tokens")

    # If the argument ends with ".jack", use it as the single input file.
    if arg.endswith(".jack"):
        file_list = [arg]
    # Otherwise, consider the argument as a directory.
    else:
        if arg.endswith("/"):
            arg = arg[:-1]
        # Get a list of files ending with ".vm" from the directory.
        file_list = glob.glob(arg + "/*.jack")
        if len(file_list) == 0:
            print("""Error: No proper input file names found. Please \
use a file name ending with '.jack' or a directory containing '.jack' files.""")
            sys.exit()

    for file_in in file_list:
        directory = file_in[:file_in.rfind("/")] + "/output/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_out = (directory + file_in[file_in.rfind("/")+1:]).replace(".jack", ".xml")
        if print_tokens:
            file_out = file_out.replace(".xml", "T.xml")
            jack_analyzer = JackAnalyzer(file_in, file_out) 
            jack_analyzer.tokenize()
        else:
            jack_analyzer = JackAnalyzer(file_in, file_out) 
            jack_analyzer.parse()