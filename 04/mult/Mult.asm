// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
	@R2
	M=0    // RAM[2]=0
	@R1
	D=M    // D=RAM[1]
	@i     // i refers to some memory location
	M=D    // i=RAM[1]
// the following 4 lines are not necessary, but can improve efficiency when R0==0
	@R0
	D=M    // D=RAM[0]
	@END
	D;JEQ  // if RAM[0]==0, jump to END
(LOOP)
	@i
	D=M    // D=i
	@END
	D;JEQ  // if i==0, jump to END
	@R0
	D=M    // D=RAM[0]
	@R2
	M=M+D  // RAM[2]=RAM[2]+RAM[0]
	@i
	M=M-1  // i=i-1
	@LOOP
	0;JMP  // jump to LOOP
(END)
	@END
	0;JMP  // infinite loop