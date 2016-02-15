MPCS 52011 Project 6
Xiaorui Tang, xiaoruit, 449972


## Requirment
 - Python 2.x or 3.x


## To Compile
 - The code can be compiled automatically when you run the program.


## To run
 - Decompress the package, and then run the program at the command line: 
      unzip project06_xiaoruit.zip
      cd project06_xiaoruit/src
      python Assembler.py <path_to_file>
   For example:
      python Assembler.py ../test/add/Add.asm

 - Please make sure the name of the input text file ends with ".asm". If more than one command line arguments end with ".asm", the program will take the first one as the input file name.

 - The program will create an output file ending with ".hack" in the same directory as the input file. For example, running the program on /tmp/testfile.asm will create a file /tmp/testfile.hack as the output.
   

## Limitation
 - The program does not take multiple asm files as input files. It only takes one file at a time. If there are multiple command line arguments ending with ".asm", the program takes the first one as the input file.