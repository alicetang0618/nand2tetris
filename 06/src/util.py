# Utility functions for the assembler project

def to_binary(n):
    '''
    Convert decimal to binary
    '''
    return bin(int(n))[2:]

def clean_command(line):
    '''
    Removes white spaces and comments from a string.
    '''
    line = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
    # If there is a "//" sequence in the line, slice the line to get rid of the comments.
    cmt_idx = line.find("//")
    if cmt_idx != -1:
        line = line[:cmt_idx]
    return line