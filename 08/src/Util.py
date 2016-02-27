# Constants and utility functions for VM translator class

C_ARITHMETIC = 0
C_PUSH       = 1
C_POP        = 2
C_LABEL      = 3
C_GOTO       = 4
C_IF         = 5
C_FUNCTION   = 6
C_RETURN     = 7
C_CALL       = 8

ARITHMETIC_CODE_DICT = {'add': "M=M+D\n", 'sub': "M=M-D\n", 'and': "M=M&D\n", 'or': "M=M|D\n",
             'eq': 'D;JNE\n', 'gt': 'D;JLE\n', 'lt': 'D;JGE\n', 'neg': "M=-M\n", 
             'not': "M=!M\n"}

SEGMENT_CODE_DICT = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
             'pointer': 3, 'temp': 5}

def clean_command(line):
    '''
    Removes tabs, line returns and comments from a string.
    Input: line (string)
    Output: the cleaned string
    '''
    line = line.replace("\t", "").replace("\n", "").replace("\r", "")
    # If there is a "//" sequence in the line, slice the line to get rid of the comments.
    cmt_idx = line.find("//")
    if cmt_idx != -1:
        line = line[:cmt_idx].strip()
    return line