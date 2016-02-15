# SymbolTable module for assembler

class SymbolTable:
    """ SymbolTable  module """

    def __init__(self):
        self._symbols = {
            'SP': 0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
            'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
            'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14,
            'R15':15, 'SCREEN':16384, 'KBD':24576}

    def addEntry(self, symbol, address):
        '''
        Adds a (symbol, address) pair to the symbol table.
        '''
        # If the symbol table already contains this symbol, append "--" + 
        # str(# occurrences of the symbol in the symbol_table dictionary)
        # to the original symbol and use it as a new symbol.
        if self.contains(symbol):
            symbol = symbol + "--" + self.numOccurrences(symbol)
        self._symbols[symbol] = address

    def contains(self, symbol):
        '''
        Returns true if the symbol is contained in the symbol table.
        '''
        return symbol in self._symbols

    def getAddress(self, symbol):
        '''
        Returns the associated address for the given symbol.
        '''
        return self._symbols[symbol]

    def numOccurrences(self, symbol):
        '''
        Returns the number of occurrences for a symbol in the symbol table.
        '''
        return str([key[:key.find('--')] if key.find('--') != -1 else key \
            for key in self.symbols.keys()].count(symbol))