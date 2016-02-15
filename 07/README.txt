MPCS 52011 Project 7
Xiaorui Tang, xiaoruit, 449972


## Requirment
 - Python 2.x or 3.x


## To Compile
 - The code can be compiled automatically when you run the program.


## To run
 - Decompress the package, and then run the program at the command line: 
      unzip 07_xiaoruit.zip
      cd 07_xiaoruit/src
      python VMTranslator.py <path_to_file>
   For example:
      python VMTranslator.py ../test/MemoryAccess/StaticTest/
      python VMTranslator.py ../test/MemoryAccess/StaticTest/StaticTest.vm

 - The program only accepts one command line argument. If you use a single file as input, make sure the name of the input file ends with ".vm". If you use a directory as input, make sure there is at least one file ending with ".vm" in the directory.

 - The program will create an output file ending with ".asm" in the same directory as the input file or directory. For example, running the program on /tmp/testfile.vm will create a file /tmp/testfile.asm as the output. Running the program on /tmp/testfiles/ will create a file /tmp/testfiles.asm as the output.
   

## Limitation
 - The program only can only deal with stack arithmetic and memory access commands of the VM language. If the input files contain other types of commands in VM language, the program will leave out those lines.