MPCS 52011 Project 10
Xiaorui Tang, xiaoruit, 449972


## Requirment
 - Python 2.x or 3.x


## To Compile
 - The code can be compiled automatically when you run the program.


## To run
 - Decompress the package, and then run the program at the command line: 
      unzip 10_xiaoruit.zip
      cd 10_xiaoruit/src
      python JackAnalyzer.py <path_to_file|directory> [print_tokens]
   For example:
      python JackAnalyzer.py ../test/ArrayTest/
      python JackAnalyzer.py ../test/ArrayTest/Main.jack
      python JackAnalyzer.py ../test/ArrayTest/ print_tokens

 - The program only accepts one or two command line arguments. For the first argument, if you use a single file as input, make sure the name of the input file ends with ".jack"; if you use a directory as input, make sure there is at least one file ending with ".vm" in the directory. 
   If there is a second argument and its value is "print_tokens", the program will output files containing only a list of tokens. 
   If the second argument is not specified by the user, the program will output files containing the complete XML output.

 - The program will create an "output" directory in the same directory as the input file or directory, if there isn't a directory named "output". For example, running the program on /tmp/testfile.jack will create a directory /tmp/output/. Running the program on /tmp/testfiles/ will create a directory /tmp/testfiles/output/.
   If "print_tokens" is not specified, the program will generate a list of ".xml" files in the "output" directory corresponding to each ".jack" file in the input directory.
   If "print_tokens" is specified, the program will generate a list of "T.xml" files corresponding to each ".jack" file in the input directory. For example, for test.jack, it will generate a file named testT.xml in the "output" directory.


## Limitation
 - It assumes that the input ".jack" files have the correct Jack syntax. The program cannot detect and report all the syntax errors.