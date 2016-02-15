import sys

if __name__ == "__main__":

	file_in = ""
	no_comments = False

	for arg in sys.argv[1:]:
		# Only takes file names ending with ".in" as valid input file names.
		if arg.endswith(".in"):
			# If the command line arguments contain multiple file names ending with ".in",
			# use the first one as the input file.
			if len(file_in) == 0:
				file_in = arg
			else:
				print("Warning: You put in more than one name ending with '.in'. Only the first file is going to be processed.")
		elif arg == "no-comments":
			no_comments = True

	# If no valid file name entered by the user, print an error and exit the program.
	if len(file_in) == 0:
		print("Error: No proper input file name found. Please use a file name ending with '.in'.")
		sys.exit()

	# If the input file cannot be found, print an error and exit the program.
	try:
		fi = open(file_in)
	except:
		print("Error: The input file is not found. Please verify that the path is valid.")
		sys.exit()

	# Read the lines in the input file 
	content_in = fi.readlines()
	fi.close()

	# Open an empty output file
	fo = open(file_in[:-3] + ".out", "w")
	start_line = False

	for line in content_in:
		# Get rid of spaces and tabs
		line_out = line.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
		if no_comments:
			# If there is a "//" sequence in the line, slice the line to get rid of the comments.
			cmt_idx = line_out.find("//")
			if cmt_idx != -1:
				line_out = line_out[:cmt_idx]
		# Get rid of the empty lines
		if len(line_out) > 0:
			if start_line:
				line_out = "\n" + line_out
			else:
				start_line = True
			# Write the line to the output file
			fo.write(line_out)
	
	# Close the output file and exit the program
	fo.close()
	sys.exit()