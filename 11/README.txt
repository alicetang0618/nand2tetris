MPCS 52011 Project 11
Xiaorui Tang, xiaoruit, 449972


## Requirment
 - Python 2.x or 3.x


## To Compile
 - The code can be compiled automatically when you run the program.


## To run
 - Decompress the package, and then run the program at the command line: 
      unzip 11_xiaoruit.zip
      cd 11_xiaoruit/src
      python JackCompiler.py <path_to_file|directory>
   For example:
      python JackCompiler.py ../test/Pong/
      python JackCompiler.py ../test/Seven/Main.jack

 - The program only accepts one command line argument. If you use a single file as input, make sure the name of the input file ends with ".jack"; if you use a directory as input, make sure there is at least one file ending with ".jack" in the directory.

 - The program will create output files ending with ".vm" in the same directory as the input files or directory. Each output ".vm" file corresponds to an input ".jack" file. For example, running the program on /tmp/testfile.jack will create a file /tmp/testfile.vm as the output. Running the program on /tmp/testfiles/ will create a set of ".vm" files in /tmp/testfiles/ as the output.

## Limitation
 - It assumes that the input ".jack" files have the correct Jack syntax. The program cannot detect and report all the syntax errors.