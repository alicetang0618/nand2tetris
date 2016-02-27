MPCS 52011 Project 9
Xiaorui Tang, xiaoruit, 449972

Program: DrawBoard

## To Compile
 - Decompress the package:
 	  unzip 09_xiaoruit.zip
 - Use JackCompiler.sh to create a set of ".vm" files:
      bash JackCompiler.sh [path_to_directory/]09_xiaoruit/DrawBoard/


## To run
 - Load the whole program directory into the VMEmulator and start the program.


## Goal
 - There will be a black square and a black circle on the screen. The black circle works like a pen, and the black square works like an eraser.
 - Use the eraser (black square) to erase the moving trace created by the pen (black circle). In other words, the black circle is what you are going to erase, and the black square is your eraser.


## How to play
 - You are going to move the eraser (square) to erase the moving trace of the pen (circle).
 - You can move the black square around the screen and change its size during the movement.
 - Everytime when the black square moves, the black circle moves in the same direction accordingly, causing the black area to expand. The black circle always moves half as quickly as the black square.
 - If the eraser moves past the black area, the part of black circles intersected with the moving trace of the eraser will be erased.
 - Once the square and circle start to move, they would not stop moving until they reach the boundary of the screen.
 - You can only increase the size of your eraser if it currently does not touch the right or bottom boundary of the screen.


## Use the keyboard
 - In the beginning, you can specify the initial size and position of your eraser. Use your keyboard to input numbers and hit "return" key to submit. The circle and square will appear after you input all the parameters. 
 	 - Restrictions on the parameters:
 	 	0 < x < 510 - size
 	 	0 < y < 254 - size
 	 	size > 0

 - After the function "DrawBoard.run" is pushed onto the Call Stack, you can control the keyboard to move the square and the circle:
	 - The arrow keys are used to move the square.
	 - The 'z' & 'x' keys are used to decrement and increment the size.
	 - The 'q' key is used to quit the game.