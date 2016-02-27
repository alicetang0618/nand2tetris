MPCS 52011 Project 8
Xiaorui Tang, xiaoruit, 449972


## Requirment
 - Python 2.x or 3.x


## To Compile
 - The code can be compiled automatically when you run the program.


## To run
 - Decompress the package, and then run the program at the command line: 
      unzip 08_xiaoruit.zip
      cd 08_xiaoruit/src
      python VMTranslator.py <path_to_file>
   For example:
      python VMTranslator.py ../test/FunctionCalls/SimpleFunction/
      python VMTranslator.py ../test/FunctionCalls/SimpleFunction/SimpleFunction.vm

 - The program only accepts one command line argument. If you use a single file as input, make sure the name of the input file ends with ".vm". If you use a directory as input, make sure there is at least one file ending with ".vm" in the directory.

 - The program will create an output file ending with ".asm" in the same directory as the input file or directory. For example, running the program on /tmp/testfile.vm will create a file /tmp/testfile.asm as the output. Running the program on /tmp/testfiles/ will create a file /tmp/testfiles/testfiles.asm as the output.


## Limitation
 - It assumes that each program has a Sys.init function. If the test script does not have this function (like SimpleFunction, BasicLoop, FibonacciSeries in the "test" directory), please comment out the two lines in CodeWriter.write_init() to generate the correct asm codes:
	self.file_out.write("@256\nD=A\n@SP\nM=D\n")
	self.write_call("Sys.init", 0)