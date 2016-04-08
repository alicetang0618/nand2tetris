# Compilation Engine module for Jack compiler
import JackTokenizer, SymbolTable
from Util import *

class CompilationEngine:
    """ Compilation Engine module """

    def __init__(self, file_in, file_out):
        '''
        Creates a new compilation engine with the given input and output. 
        Input: file_in (string), file_out (_io.TextIOWrapper)
        '''
        self.file_out = file_out
        self.tokenizer = JackTokenizer.JackTokenizer(file_in)
        self.indent = 0
        self.symbol_table = SymbolTable.SymbolTable()


    def write(self, s):
        '''
        Writes a string with the current indentation level.
        Input: s (string)
        '''
        self.file_out.write("  "*self.indent + s)


    def get_terminal(self):
        '''
        Gets the next token from the tokenizer.
        Output: string
        '''
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            token_type = self.tokenizer.token_type()
            if token_type == KEYWORD:
                return ("<keyword> " + self.tokenizer.key_word() + " </keyword>\n")
            elif token_type == SYMBOL:
                return ("<symbol> " + self.tokenizer.symbol() + " </symbol>\n")
            elif token_type == IDENTIFIER:
                return ("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
            elif token_type == INT_CONST:
                return ("<integerConstant> " + self.tokenizer.int_val() + " </integerConstant>\n")
            elif token_type == STRING_CONST:
                return ("<stringConstant> " + self.tokenizer.string_val() + " </stringConstant>\n")
        return None


    def compile_class(self):
        '''
        Compiles a complete class.
        '''
        self.write("<class>\n")
        self.indent += 1
        self.write("<keyword> class </keyword>\n")
        self.write(self.get_terminal())
        self.write("<<<<id> category: class>\n")
        self.write(self.get_terminal())
        next_token = self.get_terminal()
        # class variable declarations
        while next_token in ["<keyword> static </keyword>\n", "<keyword> field </keyword>\n"]:
            self.compile_class_var_dec(next_token)
            next_token = self.get_terminal()
        # subroutines
        while next_token in ["<keyword> constructor </keyword>\n", "<keyword> function </keyword>\n", "<keyword> method </keyword>\n"]:
            self.compile_subroutine(next_token)
            next_token = self.get_terminal()
        self.write(next_token)
        self.indent -= 1
        self.write("</class>\n")


    def compile_class_var_dec(self, start_token):
        '''
        Compiles a static declaration or a field declaration.
        Input: start_token (string)
        '''
        self.write("<classVarDec>\n")
        self.indent += 1
        self.write(start_token)
        type_token = self.get_terminal()
        self.write(type_token)
        if type_token.startswith("<identifier>"):
            self.write("<<<<id> category: class>\n")
            type_token = type_token[13:-15]
        else:
            type_token = type_token[10:-12]
        next_token = self.get_terminal()
        while next_token != "<symbol> ; </symbol>\n":
            self.write(next_token)
            if next_token.startswith("<identifier>"):
                self.symbol_table.define(next_token[13:-15], type_token, start_token[10:-12])
                self.write("<<<<id> category: %s, used: %d, running: %d>\n" % \
                    (self.symbol_table.kind_of(next_token[13:-15]), 1, self.symbol_table.index_of(next_token[13:-15])))
            next_token = self.get_terminal()
        self.write(next_token)
        self.indent -= 1
        self.write("</classVarDec>\n")


    def compile_subroutine(self, start_token):
        '''
        Compiles a complete method, function, or constructor.
        Input: start_token (string)
        '''
        self.symbol_table.start_subroutine()
        self.write("<subroutineDec>\n")
        self.indent += 1
        # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('
        self.write(start_token)
        next_token = self.get_terminal()
        self.write(next_token)
        if next_token.startswith("<identifier>"):
            self.write("<<<<id> category: class>\n")
        self.write(self.get_terminal())
        self.write("<<<<id> category: subroutine>\n")
        self.write(self.get_terminal())
        # parameterList ')'
        self.compile_parameter_list()
        self.write("<symbol> ) </symbol>\n")
        # subroutineBody
        self.write("<subroutineBody>\n")
        self.indent += 1
        self.write(self.get_terminal())
        next_token = self.get_terminal()
        while next_token == "<keyword> var </keyword>\n":
            self.compile_var_dec(next_token)
            next_token = self.get_terminal()
        self.compile_statements(next_token)
        self.write("<symbol> } </symbol>\n")
        self.indent -= 1
        self.write("</subroutineBody>\n")
        self.indent -= 1
        self.write("</subroutineDec>\n")
        self.symbol_table.end_subroutine()


    def compile_parameter_list(self):
        '''
        Compiles a (possibly empty) parameter list, not including the enclosing "()".
        '''
        self.write("<parameterList>\n")
        self.indent += 1
        next_token = self.get_terminal()
        while next_token != "<symbol> ) </symbol>\n":
            if next_token == "<symbol> , </symbol>\n":
                self.write(next_token)
            else:
                type_token = next_token
                var_token = self.get_terminal()
                self.write(type_token)
                if type_token.startswith("<identifier>"):
                    self.write("<<<<id> category: class>\n")
                    type_token = type_token[13:-15]
                else:
                    type_token = type_token[10:-12]
                self.write(var_token)
                self.symbol_table.define(var_token[13:-15], type_token, "argument")
                self.write("<<<<id> category: %s, used: %d, running: %d>\n" % \
                    (self.symbol_table.kind_of(var_token[13:-15]), 1, self.symbol_table.index_of(var_token[13:-15])))
            next_token = self.get_terminal()
        self.indent -= 1
        self.write("</parameterList>\n")


    def compile_var_dec(self, start_token):
        '''
        Compiles a var declaration.
        Input: start_token (string)
        '''
        self.write("<varDec>\n")
        self.indent += 1
        self.write(start_token)
        type_token = self.get_terminal()
        self.write(type_token)
        if type_token.startswith("<identifier>"):
            self.write("<<<<id> category: class>\n")
            type_token = type_token[13:-15]
        else:
            type_token = type_token[10:-12]
        next_token = self.get_terminal()
        while next_token != "<symbol> ; </symbol>\n":
            self.write(next_token)
            if next_token.startswith("<identifier>"):
                self.symbol_table.define(next_token[13:-15], type_token, "var")
                self.write("<<<<id> category: %s, used: %d, running: %d>\n" % \
                    (self.symbol_table.kind_of(next_token[13:-15]), 1, self.symbol_table.index_of(next_token[13:-15])))
            next_token = self.get_terminal()
        self.write(next_token)
        self.indent -= 1
        self.write("</varDec>\n")


    def compile_statements(self, start_token):
        '''
        Compiles a sequence of statements, not including the enclosing "{}".
        Input: start_token (string)
        '''
        self.write("<statements>\n")
        self.indent += 1
        next_token = start_token
        while next_token != "<symbol> } </symbol>\n":
            if next_token == "<keyword> if </keyword>\n":
                next_token = self.compile_if(next_token)
                if next_token == -1:
                    next_token = self.get_terminal() 
            else:
                if next_token == "<keyword> let </keyword>\n":
                    self.compile_let(next_token)
                elif next_token == "<keyword> while </keyword>\n":
                    self.compile_while(next_token)
                elif next_token == "<keyword> do </keyword>\n":
                    self.compile_do(next_token)
                elif next_token == "<keyword> return </keyword>\n":
                    self.compile_return(next_token)
                next_token = self.get_terminal() 
        self.indent -= 1
        self.write("</statements>\n")


    def compile_do(self, start_token):
        '''
        Compiles a do statement.
        Input: start_token (string)
        '''
        self.write("<doStatement>\n")
        self.indent += 1
        self.write(start_token)
        self.write(self.get_terminal())
        next_token = self.get_terminal()
        if next_token == "<symbol> . </symbol>\n":
            if start_token[13:-14] in self.symbol_table.class_table or \
            start_token[13:-14] in self.symbol_table.subroutine_table:
                self.write("<<<<id> category: variable>\n")
            else:
                self.write("<<<<id> category: class>\n")
            self.write(next_token)
            self.write(self.get_terminal())
            self.write("<<<<id> category: subroutine>\n")
            next_token = self.get_terminal()
        else:
            self.write("<<<<id> category: subroutine>\n")
        self.write(next_token)
        next_token = self.compile_expression_list()
        self.write(next_token)
        self.write(self.get_terminal())
        self.indent -= 1
        self.write("</doStatement>\n")


    def compile_let(self, start_token):
        '''
        Compiles a let statement.
        Input: start_token (string)
        '''
        self.write("<letStatement>\n")
        self.indent += 1
        self.write(start_token)
        var_token = self.get_terminal()
        self.write(var_token)
        self.write("<<<<id> category: %s, used: %d, running: %d>\n" % \
            (self.symbol_table.kind_of(var_token[13:-15]), \
            1, self.symbol_table.index_of(var_token[13:-15])))
        next_token = self.get_terminal()
        while next_token != "<symbol> ; </symbol>\n":
            self.write(next_token)
            if next_token[9] == "[":
                next_token = self.compile_expression(self.get_terminal())
            elif next_token[9] == "=":
                next_token = self.compile_expression(self.get_terminal())
            else:
                next_token = self.get_terminal()
        self.write(next_token)
        self.indent -= 1
        self.write("</letStatement>\n")


    def compile_while(self, start_token):
        '''
        Compiles a while statement.
        Input: start_token (string)
        '''
        self.write("<whileStatement>\n")
        self.indent += 1
        self.write(start_token)
        self.write(self.get_terminal())
        next_token = self.compile_expression(self.get_terminal())
        self.write(next_token)
        self.write(self.get_terminal())
        self.compile_statements(self.get_terminal())
        self.write("<symbol> } </symbol>\n")
        self.indent -= 1
        self.write("</whileStatement>\n")


    def compile_return(self, start_token):
        '''
        Compiles a return statement.
        Input: start_token (string)
        '''
        self.write("<returnStatement>\n")
        self.indent += 1
        self.write(start_token)
        next_token = self.get_terminal()
        if next_token != "<symbol> ; </symbol>\n":
            next_token = self.compile_expression(next_token)
        self.write(next_token)
        self.indent -= 1
        self.write("</returnStatement>\n")


    def compile_if(self, start_token):
        '''
        Compiles an if statement, possibly with a trailing else clause.
        Input: start_token (string)
        Ouput: next_token (string) / -1
        '''
        self.write("<ifStatement>\n")
        self.indent += 1
        self.write(start_token)
        self.write(self.get_terminal())
        next_token = self.compile_expression(self.get_terminal())
        self.write(next_token)
        self.write(self.get_terminal())
        self.compile_statements(self.get_terminal())
        self.write("<symbol> } </symbol>\n")
        # consider the possiblity of having "else" clause
        next_token = self.get_terminal()
        if next_token != "<keyword> else </keyword>\n":
            self.indent -= 1
            self.write("</ifStatement>\n")
            return next_token
        else:
            self.write(next_token)
            self.write(self.get_terminal())
            self.compile_statements(self.get_terminal())
            self.write("<symbol> } </symbol>\n")
            self.indent -= 1
            self.write("</ifStatement>\n")
            return -1


    def compile_expression(self, start_token):
        '''
        Compiles an expression.
        Input: start_token (string)
        Output: next_token (string)
        '''
        self.write("<expression>\n")
        self.indent += 1
        next_token = self.compile_term(start_token)
        while next_token[9] in OPS:
            self.write(next_token)
            next_token = self.compile_term(self.get_terminal())
        self.indent -= 1
        self.write("</expression>\n")
        return next_token


    def compile_term(self, start_token):
        '''
        Compiles a term.
        Input: start_token (string)
        Output: next_token (string)
        '''
        self.write("<term>\n")
        self.indent += 1
        written = False

        # '(' expression ')'
        if start_token == "<symbol> ( </symbol>\n":
            self.write(start_token)
            next_token = self.compile_expression(self.get_terminal())
            self.write(next_token)
            next_token = self.get_terminal()
        # unaryOp term
        elif start_token[9] in "-~":
            self.write(start_token)
            next_token = self.compile_term(self.get_terminal())
        # Other cases
        else:
            self.write(start_token)
            next_token = self.get_terminal()
            if start_token.startswith("<identifier>"):
                if start_token[13:-15] in self.symbol_table.class_table or \
                start_token[13:-15] in self.symbol_table.subroutine_table:
                    self.write("<<<<id> category: %s, used: 1, running: %d>\n" % \
                        (self.symbol_table.kind_of(start_token[13:-15]), self.symbol_table.index_of(start_token[13:-15])))
                else:
                    if next_token[9] == ".":
                        self.write("<<<<id> category: class>\n")
                    else:
                        self.write("<<<<id> category: subroutine>\n")
                if next_token[9] == ".":
                    self.write(next_token)
                    self.write(self.get_terminal())
                    self.write("<<<<id> category: subroutine>\n")
                    next_token = self.get_terminal()
            while next_token[9] not in OPS + ",)];":
                self.write(next_token)
                if next_token[9] in "[(":
                    # varName '[' expression ']'
                    if next_token[9] == "[":
                        next_token = self.compile_expression(self.get_terminal())
                    # subroutine calls
                    else:
                        next_token = self.compile_expression_list()
                    self.write(next_token)
                    written = True
                # other cases
                else:
                    next_token = self.get_terminal()

        # If the next token is already written to the file, get the next one.
        if written:
            next_token = self.get_terminal()
        self.indent -= 1
        self.write("</term>\n")
        return next_token


    def compile_expression_list(self):
        '''
        Compiles a (possibly empty) comma-separated list of expressions.
        Input: start_token (string)
        Output: next_token (string)
        '''
        self.write("<expressionList>\n")
        self.indent += 1
        next_token = self.get_terminal()
        while next_token != "<symbol> ) </symbol>\n":
            next_token = self.compile_expression(next_token)
            if next_token == "<symbol> , </symbol>\n":
                self.write(next_token)
                next_token = self.get_terminal()
        self.indent -= 1
        self.write("</expressionList>\n")
        return next_token
        