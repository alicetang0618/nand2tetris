# Tokenizer module for Jack compiler
from Util import *

class JackTokenizer:
    """ Tokenizer module """

    def __init__(self, file_in):
    	'''
    	Opens the input file/stream and gets ready to tokenize it.
    	Input: file_in (string)
    	'''
    	f = open(file_in)
    	file_string = f.read()
    	f.close()
    	self.commands = clean_string(file_string)
    	self.current = ""
    	self.current_type = -1

    def has_more_tokens(self):
    	'''
    	Returns true if there are more tokens in the input.
    	Output: boolean
    	'''
    	return len(self.commands) > 0

    def advance(self):
    	'''
    	Gets the next token from the input and makes it the current token.
    	'''
    	assert(self.has_more_tokens())
    	if self.commands[0] == '"':
    		idx = self.commands[1:].find('"')
    		if idx == -1:
    			print("Syntax Error: Only one double quote was found.")
    			sys.exit()
    		self.current = self.commands[1:idx+1]
    		self.commands = self.commands[idx+2:].strip()
    		self.current_type = STRING_CONST
    	elif self.commands[0].isdigit():
    		idx = 1
    		while idx < len(self.commands):
    			if not self.commands[idx].isdigit():
    				break
    			idx += 1
    		self.current = self.commands[:idx]
    		self.commands = self.commands[idx:].strip()
    		self.current_type = INT_CONST
    	elif self.commands[0] in SYMBOLS:
    		self.current = self.commands[0]
    		self.commands = self.commands[1:].strip()
    		self.current_type = SYMBOL
    	else:
    		idx = 1
    		while idx < len(self.commands):
    			if self.commands[idx] in SYMBOLS + " ":
    				break
    			idx += 1
    		self.current = self.commands[:idx]
    		if idx == len(self.commands):
    			self.commands = ""
    		else: 
    			self.commands = self.commands[idx:].strip()
    		if self.current in KEYWORDS:
    			self.current_type = KEYWORD
    		else:
    			self.current_type = IDENTIFIER

    def token_type(self):
    	'''
    	Returns the type of the current token.
    	Output: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
    	'''
    	return self.current_type

    def key_word(self):
    	'''
    	Returns the keyword which is the current token.
    	Output: CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN, CHAR, VOID, 
    	VAR, STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE, NULL, THIS
    	'''
    	assert(self.current_type == KEYWORD)
    	return self.current

    def symbol(self):
    	'''
    	Returns the character which is the current token. 
    	Output: char
    	'''
    	assert(self.current_type == SYMBOL)
    	return self.current

    def identifier(self):
    	'''
    	Returns the identifier which is the current token. 
    	Output: string
    	'''
    	assert(self.current_type == IDENTIFIER)
    	return self.current

    def int_val(self):
    	'''
    	Returns the integer value of the current token.
    	Output: int
    	'''
    	assert(self.current_type == INT_CONST)
    	return self.current

    def string_val(self):
    	'''
    	Returns the string value of the current token, without the double quotes.
    	Output: string
    	'''
    	assert(self.current_type == STRING_CONST)
    	return self.current