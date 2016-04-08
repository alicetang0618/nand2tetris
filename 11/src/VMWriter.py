# VM Writer module for Jack compiler

class VMWriter:
    """ VM Writer module """

    def __init__(self, file_out):
    	'''
    	Creates a new file and prepares it for writing.
    	Input: out_file (string)
    	'''
    	self.file_out = open(file_out, "w")

    def write_push(self, seg, idx):
    	'''
    	Writes a VM push command.
    	Input: seg (string), idx (int)
    	'''
    	self.file_out.write("push %s %d\n" % (seg, idx))

    def write_pop(self, seg, idx):
    	'''
    	Writes a VM pop command.
    	Input: seg (string), idx (int)
    	'''
    	self.file_out.write("pop %s %d\n" % (seg, idx))

    def write_arithmetic(self, command):
    	'''
    	Writes a VM arithmetic command.
    	Input: command
    	'''
    	self.file_out.write(command + "\n")

    def write_label(self, label):
    	'''
    	Writes a VM label command.
    	Input: label (string)
    	'''
    	self.file_out.write("label %s\n" % label)

    def write_goto(self, label):
    	'''
    	Writes a VM goto command.
    	Input: label (string)
    	'''
    	self.file_out.write("goto %s\n" % label)

    def write_if(self, label):
    	'''
    	Writes a VM if-goto command.
    	Input: label (string)
    	'''
    	self.file_out.write("if-goto %s\n" % label)

    def write_call(self, name, n_args):
    	'''
    	Writes a VM call command.
    	Input: name (string), n_args (int)
    	'''
    	self.file_out.write("call %s %d\n" % (name, n_args))

    def write_function(self, name, n_locals):
    	'''
    	Writes a VM function command.
    	Input: name (string), n_locals (int)
    	'''
    	self.file_out.write("function %s %d\n" % (name, n_locals))

    def write_return(self):
    	'''
    	Writes a VM return command.
    	'''
    	self.file_out.write("return\n")

    def close(self):
    	'''
    	Closes the output file.
    	'''
    	self.file_out.close()