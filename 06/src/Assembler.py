import Parser, Code, SymbolTable, sys
from util import to_binary

class Assembler:
    """ Assembler module """

    def __init__(self, lines_in, file_out):
        self.lines_in = lines_in
        self.file_out = file_out
        self.symbol_table = SymbolTable.SymbolTable()
        # The first available address in symbol table is 16
        self.symbol_address = 16

    def parse_l_commands(self):
        '''
        First pass: build the symbol table with ROM addresses.
        '''
        parser = Parser.Parser(self.lines_in)
        idx = 0
        while parser.has_more_commands():
            parser.advance()
            if parser.commandType() == parser.L_COMMAND:
                self.symbol_table.addEntry(parser.symbol(), idx)
            elif parser.commandType() in [parser.A_COMMAND, parser.C_COMMAND]:
                idx += 1

    def parse_ac_commands(self):
        '''
        Second pass: generate binary codes for A/C instructions.
        '''
        parser = Parser.Parser(self.lines_in)
        translator = Code.Code()
        start_line = True
        while parser.has_more_commands():
            parser.advance()
            if parser.commandType() in [parser.A_COMMAND, parser.C_COMMAND]:
                # For A instructions:
                if parser.commandType() == parser.A_COMMAND:
                    line = self.translate_a(parser)
                # For C instructions:
                else:
                    line = "111" + translator.comp(parser.comp()) \
                    + translator.dest(parser.dest()) + translator.jump(parser.jump())
                # Write the binary code to the output file
                if not start_line:
                    self.file_out.write("\n" + line)
                else:
                    self.file_out.write(line)
                    start_line = False

    def translate_a(self, parser):
        '''
        Generate binary codes for A instructions.
        '''
        assert(parser.commandType() == parser.A_COMMAND)
        smb = parser.symbol()
        if not smb.isdigit():
            if not self.symbol_table.contains(smb):
                self.symbol_table.addEntry(smb, self.symbol_address)
                self.symbol_address += 1
            smb = self.symbol_table.getAddress(smb)
        return "0" + to_binary(smb).zfill(15)

    def assemble(self):
        ''' Put it all together '''
        self.parse_l_commands()
        self.parse_ac_commands()


if __name__ == "__main__":

    file_in = ""

    for arg in sys.argv[1:]:
        # Only takes file names ending with ".asm" as valid input file names.
        if arg.endswith(".asm"):
            # If the command line arguments contain multiple file names ending with ".asm",
            # use the first one as the input file.
            if len(file_in) == 0:
                file_in = arg
            else:
                print("Warning: You put in more than one name ending with '.asm'. Only the first file is going to be processed.")

    if len(file_in) == 0:
        print("Error: No proper input file name found. Please use a file name ending with '.asm'.")
        sys.exit()

    # If the input file cannot be found, print an error and exit the program.
    try:
        fi = open(file_in)
    except:
        print("Error: The input file is not found. Please verify that the path is valid.")
        sys.exit()

    lines_in = fi.readlines()
    fi.close()
    file_out = open(file_in.replace('.asm', '.hack'), 'w')

    assembler = Assembler(lines_in, file_out)
    assembler.assemble()
    file_out.close()