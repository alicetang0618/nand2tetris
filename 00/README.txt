MPCS 52011 Project 0
Xiaorui Tang, xiaoruit, 449972


## Requirment
 - Python 2.x or 3.x


## To Compile
 - The code can be compiled automatically when you run the program.


## To run
 - Decompress the package, and then run the program at the command line: 
 	unzip xiaoruit-Project0.zip
 	cd xiaoruit-Project0/src
 	python strip_white_space.py [no-comments] <path_to_file>
   For example:
    python strip_white_space.py no-comments /tmp/testfile.in
    python strip_white_space.py /tmp/testfile.in

 - Please make sure the name of the input text file ends with ".in". If more than one 
   command line arguments end with ".in", the program will take the first one as the input file name.

 - The program will create an output file ending with ".out" in the same directory
   as the input file. For example, running the program on /tmp/testfile.in will create
   a file /tmp/testfile.out as the output.

 - Use the "no-comments" option if you want to remove all the comments starting with "//" 
   in the text file. Don't use this option if you only want to remove all the white spaces
   and blank lines.
   

## Limitations
 - The program works properly on text files. It does not handle some other document formats
   like doc/docx, pdf, or encoded text files.

 - The program does not take multiple text files as input files. It only takes one file at a
   time. If there are multiple command line arguments ending with ".in", the program takes the
   first one as the input file.

 - The program only removes comments beginning with the sequence "//" and ending at the line 
   return. It does not remove comments beginning with "#", or surronded by "'''", "/*" and "*/", etc.