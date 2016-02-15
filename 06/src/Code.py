# Code module for assembler
from util import to_binary

class Code:
    """ Code module """

    def __init__(self):
        self._dest_list = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
        self._comp_dict = {
                '0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100',
                'A':'0110000', '!D':'0001101', '!A':'0110001', '-D':'0001111',
                '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110',
                'A-1':'0110010','D+A':'0000010','A+D':'0000010','D-A':'0010011',
                'A-D':'0000111','D&A':'0000000','A&D':'0000000','D|A':'0010101',
                'A|D':'0010101',
                'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111',
                'M-1':'1110010','D+M':'1000010','M+D':'1000010','D-M':'1010011',
                'M-D':'1000111','D&M':'1000000','M&D':'1000000','D|M':'1010101',
                'M|D':'1010101' }
        self._jump_list = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']


    def dest(self, mnemonic):
        '''
        Translate dest code into binary.
        '''
        assert(mnemonic in self._dest_list)
        return to_binary(self._dest_list.index(mnemonic)).zfill(3)

    def comp(self, mnemonic):
        '''
        Translate comp code into binary.
        '''
        assert(mnemonic in self._comp_dict)
        return self._comp_dict[mnemonic]

    def jump(self, mnemonic):
        '''
        Translate jump code into binary.
        '''
        assert(mnemonic in self._jump_list)
        return to_binary(self._jump_list.index(mnemonic)).zfill(3)