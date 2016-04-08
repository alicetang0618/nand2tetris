# Symbol Table module for Jack compiler
from Util import *

class SymbolTable:
    """ Symbol Table module """

    def __init__(self):
        '''
        Creates a new empty symbol table.
        '''
        self.class_table = {}
        self.subroutine_table = {}
        self.current_scope = self.class_table

    def start_subroutine(self):
        '''
        Starts a new subroutine scope.
        '''
        self.current_scope = self.subroutine_table

    def end_subroutine(self):
        '''
        Ends a subroutine scope and returns to the class scope.
        '''
        self.subroutine_table = {}
        self.current_scope = self.class_table

    def define(self, name, t, k):
        '''
        Defines a new identifier of a given name, type, and kind and assigns 
        it a running index.
        Input: name (string), t (string), k (STATIC, FIELD, ARG, or VAR)
        '''
        self.current_scope[name] = (t, k, self.var_count(k, self.current_scope))

    def var_count(self, kind, scope):
        '''
        Returns the number of variables of the given kind already defined in
        the given scope.
        Input: kind (STATIC, FIELD, ARG, or VAR)
        Output: int
        '''
        return len([name for name, val in scope.items() if val[KIND] == kind])

    def kind_of(self, name):
        '''
        Returns the kind of the named identifier. If the identifier is unknown 
        in both the current scope and other tables, returns NONE.
        Input: name (string)
        Output: (STATIC, FIELD, ARG, VAR, NONE)
        '''
        if name in self.current_scope:
            return self.current_scope[name][KIND]
        elif name in self.class_table:
            return self.class_table[name][KIND]
        return NONE

    def type_of(self, name):
        '''
        Returns the type of the named identifier.
        Input: name (string)
        Output: string
        '''
        if name in self.current_scope:
            return self.current_scope[name][TYPE]
        elif name in self.class_table:
            return self.class_table[name][TYPE]
        return NONE

    def index_of(self, name):
        '''
        Returns the index assigned to the named identifier.
        Input: name (string)
        Output: int
        '''
        if name in self.current_scope:
            return self.current_scope[name][INDEX]
        elif name in self.class_table:
            return self.class_table[name][INDEX]
        return NONE