# Constants and utility functions for Jack Compiler

ARG     = 'argument'
CONST   = 'constant'
LOCAL   = 'local'
THAT    = 'that'
POINTER = 'pointer'
TEMP    = 'temp'
NOT     = 'not'
ADD     = 'add'

TYPE    = 0
KIND    = 1
INDEX   = 2

KEYWORD      = 0
SYMBOL       = 1
IDENTIFIER   = 2
INT_CONST    = 3
STRING_CONST = 4

CLASS        = 'class'
METHOD       = 'method'
FUNCTION     = 'function'
CONSTRUCTOR  = 'constructor'
INT          = 'int'
BOOLEAN      = 'boolean'
CHAR         = 'char'
VOID         = 'void'
VAR          = 'var'
STATIC       = 'static'
FIELD        = 'field'
LET          = 'let'
DO           = 'do'
IF           = 'if'
ELSE         = 'else'
WHILE        = 'while'
RETURN       = 'return'
TRUE         = 'true'
FALSE        = 'false'
NULL         = 'null'
THIS         = 'this'
NONE         = ''

KEYWORDS = [CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN, CHAR, VOID, VAR,
            STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS]
SYMBOLS = '{}()[].,;+-*/&|<>=~'
OPS = {'+': 'add', '-': 'sub', '*': 'call Math.multiply 2', '/': 'call Math.divide 2', 
        '&': 'and', '|': 'or', '<': 'lt', '>': 'gt', '=': 'eq'}
UNARYOPS = {'-': 'neg', '~': 'not'}
SYMBOL_DICT = {FIELD: 'this', STATIC: STATIC, ARG: ARG, VAR: 'local'}

def remove_comments(s, start, end):
    '''
    Removes comments covered by the start and end symbols from a string s.
    Input: s (string), start (string), end (string)
    Output: string
    '''
    rv = ''
    end_idx = 0
    while s.find(start, end_idx) != -1:
        start_idx = s.find(start, end_idx)
        rv += s[end_idx:start_idx]
        end_idx = s.find(end, start_idx) + len(end)
    rv += s[end_idx:]
    return rv

def clean_string(s):
    '''
    Removes tabs, line returns and comments from a string, and normalizes white spaces.
    Input: s (string)
    Output: the cleaned string
    '''
    # remove comments
    rv = remove_comments(s, '/*', '*/')
    rv = remove_comments(rv, '//', '\n')
        
    # remove tabs and line returns
    rv = rv.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')

    return rv.strip()