// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
	@SCREEN 
	D=A
	@i         // i refers to some memory location; used to store the index of current location
	M=D        // i=SCREEN

(START)
	@KBD
	D=M        // D=RAM[KBD]
	@WHITE
	D;JEQ      // if RAM[KBD]==0, namely no key is pressed, jump to WHITE
// if keyboard is pressed, turn the current screen location to black
	@i
	A=M        // put the value stored in i in the A register
	M=-1       // go to the address and set it to -1 (black)
// check whether we need to increase the index
	@KBD
	D=A
	@i
	D=D-M
	D=D-1      // D=KBD-i-1
	@START
	D;JEQ      // if i==KBD-1, don't increase the index, jump to START
// increase the index	
	@i
	M=M+1      // i=i+1
	@START
	0;JMP      // jump to START

(WHITE)
// if no key is pressed, turn the current screen location to white
	@i
	A=M        // put the value stored in i in the A register
	M=0        // go to the address and set it to 0 (white)
// check whether we need to decrease the index
	@SCREEN
	D=A
	@i
	D=M-D      // D=i-SCREEN
	@START
	D;JEQ      // if i==SCREEN, don't decrease the index, jump to START
// decrease the index
	@i
	M=M-1      // i=i-1
	@START
	0;JMP      // jump to START