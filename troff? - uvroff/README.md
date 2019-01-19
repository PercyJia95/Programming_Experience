"uvroff" is a program that we were assigned to develop in SENG265, a course introduces basis, tools, programming languages used in software engineering. 

### What is uvroff
"uvroff" is named after "troff". It is a basic troff, which does document processing in Unix, specifically it is a program to be input with a .txt file and parameters that specify the margin, spacing, line width. "uvroff" output the correct formatted text file. Within lines of input text file, user can also inserts delimiters that switches formatting function on or off.

### Implementation
You might have started guessing if uvroff implementation is scanning top to bottom of the input and compose an output. Yes, it scans input and meanwhile compose the output. uvroff basically works like read the input text line by line and prints a formatted line to output. It might cache some leftovers and stick it to the next line of input to compose a next line of output.
