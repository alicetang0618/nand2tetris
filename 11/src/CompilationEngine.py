# Compilation Engine module for Jack compiler
import JackTokenizer, SymbolTable, VMWriter, sys
from Util import *

class CompilationEngine:
    ''' Compilation Engine module '''

    def __init__(self, file_in, file_out):
        '''
        Creates a new compilation engine with the given input and output. 
        Input: file_in (string), file_out (string)
        '''
        self.tokenizer = JackTokenizer.JackTokenizer(file_in)
        self.symbol_table = SymbolTable.SymbolTable()
        self.vm_writer = VMWriter.VMWriter(file_out)
        self.class_name = ''
        self.idx = 0


    def get_terminal(self):
        '''
        Gets the next token from the tokenizer.
        Output: tuple
        '''
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            token_type = self.tokenizer.token_type()
            if token_type == KEYWORD:
                return (KEYWORD, self.tokenizer.key_word())
            elif token_type == SYMBOL:
                return (SYMBOL, self.tokenizer.symbol())
            elif token_type == IDENTIFIER:
                return (IDENTIFIER, self.tokenizer.identifier())
            elif token_type == INT_CONST:
                return (INT_CONST, self.tokenizer.int_val())
            elif token_type == STRING_CONST:
                return (STRING_CONST, self.tokenizer.string_val())
        return None


    def compile_class(self):
        '''
        Compiles a complete class.
        '''
        self.class_name = self.get_terminal()[1]
        self.get_terminal()
        next_token = self.get_terminal()
        # class variable declarations
        while next_token in [(KEYWORD, STATIC), (KEYWORD, FIELD)]:
            self.compile_class_var_dec(next_token)
            next_token = self.get_terminal()
        # subroutines
        while next_token in [(KEYWORD, CONSTRUCTOR), (KEYWORD, FUNCTION), (KEYWORD, METHOD)]:
            self.compile_subroutine(self.class_name, next_token)
            next_token = self.get_terminal()
        if next_token == (SYMBOL, '}'):
            # Re-initialize class_name and symbol_table for the next class
            self.class_name = ''
            self.symbol_table = SymbolTable.SymbolTable()
            return
        else:
            print('Syntax Error: Class not defined correctly.')
            sys.exit()


    def compile_class_var_dec(self, start_token):
        '''
        Compiles a static declaration or a field declaration.
        Input: start_token (tuple)
        '''
        type_token = self.get_terminal()
        next_token = self.get_terminal()
        while next_token != (SYMBOL, ';'):
            if next_token[0] == IDENTIFIER:
                self.symbol_table.define(next_token[1], type_token[1], start_token[1])
            next_token = self.get_terminal()


    def compile_subroutine(self, class_name, start_token):
        '''
        Compiles a complete method, function, or constructor.
        Input: class_name (string), start_token (tuple)
        '''
        self.symbol_table.start_subroutine()
        type_token = self.get_terminal()
        name = self.get_terminal()
        self.get_terminal()
        if start_token == (KEYWORD, METHOD):
            self.symbol_table.define(THIS, type_token[1], ARG)
        self.compile_parameter_list()
        self.get_terminal()
        next_token = self.get_terminal()
        while next_token == (KEYWORD, VAR):
            self.compile_var_dec()
            next_token = self.get_terminal()
        self.vm_writer.write_function('%s.%s' % (class_name, name[1]), \
            self.symbol_table.var_count(VAR, self.symbol_table.current_scope))
        if start_token[1] == CONSTRUCTOR:
            self.vm_writer.write_push(CONST, \
                self.symbol_table.var_count(FIELD, self.symbol_table.class_table))
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop(POINTER, 0)
        elif start_token[1] == METHOD:
            self.vm_writer.write_push(ARG, 0)
            self.vm_writer.write_pop(POINTER, 0)
        self.compile_statements(next_token)
        self.symbol_table.end_subroutine()
        

    def compile_parameter_list(self):
        '''
        Compiles a (possibly empty) parameter list, not including the enclosing '()'.
        '''
        next_token = self.get_terminal()
        while next_token != (SYMBOL, ')'):
            if next_token != (SYMBOL, ','):
                type_token = next_token
                var_token = self.get_terminal()
                self.symbol_table.define(var_token[1], type_token[1], ARG)
            next_token = self.get_terminal()


    def compile_var_dec(self):
        '''
        Compiles a var declaration.
        '''
        type_token = self.get_terminal()
        next_token = self.get_terminal()
        while next_token != (SYMBOL, ';'):
            if next_token[0] == IDENTIFIER:
                self.symbol_table.define(next_token[1], type_token[1], VAR)
            next_token = self.get_terminal()


    def compile_statements(self, start_token):
        '''
        Compiles a sequence of statements, not including the enclosing '{}'.
        Input: start_token (tuple)
        '''
        next_token = start_token
        while next_token != (SYMBOL, '}'):
            if next_token == (KEYWORD, IF):
                next_token = self.compile_if()
                if next_token == -1:
                    next_token = self.get_terminal() 
            else:
                if next_token == (KEYWORD, LET):
                    self.compile_let()
                elif next_token == (KEYWORD, WHILE):
                    self.compile_while()
                elif next_token == (KEYWORD, DO):
                    self.compile_do()
                elif next_token == (KEYWORD, RETURN):
                    self.compile_return()
                next_token = self.get_terminal()


    def compile_do(self):
        '''
        Compiles a do statement.
        '''
        self.compile_term(self.get_terminal())
        self.vm_writer.write_pop(TEMP, 0)


    def compile_let(self):
        '''
        Compiles a let statement.
        '''
        dest_token = self.get_terminal()       
        next_token = self.get_terminal()
        # varName '[' expression ']'
        if next_token[1] == '[':
            next_token = self.compile_expression(self.get_terminal())
            self.get_terminal()
            self.vm_writer.write_push(SYMBOL_DICT[self.symbol_table.kind_of(dest_token[1])],
                self.symbol_table.index_of(dest_token[1]))
            self.vm_writer.write_arithmetic(ADD)
            self.vm_writer.write_pop(TEMP, 0)
            self.compile_expression(self.get_terminal())
            self.vm_writer.write_push(TEMP, 0)
            self.vm_writer.write_pop(POINTER, 1)
            self.vm_writer.write_pop(THAT, 0)
        # No expression
        else:
            self.compile_expression(self.get_terminal())
            self.vm_writer.write_pop(SYMBOL_DICT[self.symbol_table.kind_of(dest_token[1])],
                self.symbol_table.index_of(dest_token[1]))


    def compile_while(self):
        '''
        Compiles a while statement.
        '''
        l1 = 'WHILE_START%d' % self.idx
        l2 = 'WHILE_END%d' % self.idx
        self.idx += 1
        self.vm_writer.write_label(l1)
        self.get_terminal()
        self.compile_expression(self.get_terminal())
        self.vm_writer.write_arithmetic(NOT)
        self.vm_writer.write_if(l2)
        self.get_terminal()
        self.compile_statements(self.get_terminal())
        self.vm_writer.write_goto(l1)
        self.vm_writer.write_label(l2)


    def compile_return(self):
        '''
        Compiles a return statement.
        '''
        next_token = self.get_terminal()
        if next_token != (SYMBOL, ';'):
            self.compile_expression(next_token)
        else:
            self.vm_writer.write_push(CONST, 0)
        self.vm_writer.write_return()


    def compile_if(self):
        '''
        Compiles an if statement, possibly with a trailing else clause.
        Ouput: next_token (tuple) / -1
        '''
        l1 = 'IF_FALSE%d' % self.idx
        l2 = 'IF_END%d' % self.idx
        self.idx += 1
        self.get_terminal()
        self.compile_expression(self.get_terminal())
        self.vm_writer.write_arithmetic(NOT)
        self.vm_writer.write_if(l1)
        self.get_terminal()
        self.compile_statements(self.get_terminal())
        self.vm_writer.write_goto(l2)
        self.vm_writer.write_label(l1)
        # consider the possiblity of having 'else' clause
        next_token = self.get_terminal()
        if next_token != (KEYWORD, ELSE):
            self.vm_writer.write_label(l2)
            return next_token
        else:
            self.get_terminal()
            self.compile_statements(self.get_terminal())
            self.vm_writer.write_label(l2)
            return -1


    def compile_expression(self, start_token):
        '''
        Compiles an expression.
        Input: start_token (tuple)
        Output: next_token (tuple)
        '''
        next_token = self.compile_term(start_token)
        while next_token[1] in OPS:
            op = next_token[1]
            next_token = self.compile_term(self.get_terminal())
            self.vm_writer.write_arithmetic(OPS[op])
        return next_token


    def compile_term(self, start_token):
        '''
        Compiles a term.
        Input: start_token (tuple)
        Output: next_token (tuple)
        '''
        written = False
        # '(' expression ')'
        if start_token == (SYMBOL, '('):
            self.compile_expression(self.get_terminal())
            next_token = self.get_terminal()
        # unaryOp term
        elif start_token[1] in '-~':
            next_token = self.compile_term(self.get_terminal())
            self.vm_writer.write_arithmetic(UNARYOPS[start_token[1]])
        # Other cases
        else:
            next_token = self.get_terminal()
            # Integer constant
            if start_token[0] == INT_CONST:
                self.vm_writer.write_push(CONST, int(start_token[1]))
            # String constant
            elif start_token[0] == STRING_CONST:
                self.vm_writer.write_push(CONST, len(start_token[1]))
                self.vm_writer.write_call('String.new', 1)
                for char in start_token[1]:
                    self.vm_writer.write_push(CONST, ord(char))
                    self.vm_writer.write_call('String.appendChar', 2)
            # Keyword constant
            elif start_token[0] == KEYWORD:
                if start_token[1] == THIS:
                    self.vm_writer.write_push(POINTER, 0)
                elif start_token[1] in [FALSE, NULL]:
                    self.vm_writer.write_push(CONST, 0)
                elif start_token[1] == TRUE:
                    self.vm_writer.write_push(CONST, 0)
                    self.vm_writer.write_arithmetic(NOT)
            # varName
            elif next_token[1] not in '[(.':
                self.vm_writer.write_push(SYMBOL_DICT[self.symbol_table.kind_of(start_token[1])],
                    self.symbol_table.index_of(start_token[1]))
            else:
                # varName [ expression ]
                if next_token[1] == '[':
                    self.compile_expression(self.get_terminal())
                    self.vm_writer.write_push(SYMBOL_DICT[self.symbol_table.kind_of(start_token[1])],
                        self.symbol_table.index_of(start_token[1]))
                    self.vm_writer.write_arithmetic(ADD)
                    self.vm_writer.write_pop(POINTER, 1)
                    self.vm_writer.write_push(THAT, 0)
                # subroutineName '(' expressionList ')'
                elif next_token[1] == '(':
                    self.vm_writer.write_push(POINTER, 0)
                    cnt = self.compile_expression_list()
                    self.vm_writer.write_call('%s.%s' % (self.class_name, start_token[1]), cnt + 1)
                # ( className | varName) '.' subroutineName '(' expressionList ')'
                else:
                    cnt = 0
                    if self.symbol_table.kind_of(start_token[1]) in [FIELD, STATIC, VAR]:
                        self.vm_writer.write_push(SYMBOL_DICT[self.symbol_table.kind_of(start_token[1])],
                            self.symbol_table.index_of(start_token[1]))
                        cnt = 1
                    subroutine_name = self.get_terminal()
                    self.get_terminal()
                    cnt += self.compile_expression_list()
                    class_name = self.symbol_table.type_of(start_token[1])
                    if class_name == NONE:
                        class_name = start_token[1]
                    self.vm_writer.write_call('%s.%s' % (class_name, subroutine_name[1]), cnt)
                next_token = self.get_terminal()
        return next_token


    def compile_expression_list(self):
        '''
        Compiles a (possibly empty) comma-separated list of expressions.
        Output: cnt (int)
        '''
        cnt = 0
        next_token = self.get_terminal()
        while next_token != (SYMBOL, ')'):
            next_token = self.compile_expression(next_token)
            cnt += 1
            if next_token == (SYMBOL, ','):
                next_token = self.get_terminal()
        return cnt
        