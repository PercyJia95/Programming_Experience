# Error_handling

1. #### NegativeOptionArgumentError

    Error test case: e_in01.txt

    .LW, .LS, .LM do not take negative arguments

    ```
    ---error input
    >.LW -1
    >one
    ---program exits with message
    <At 1 of the text file, .LW or .LS or .LM has negative argument
    <
    ---code
    The code checks lw, ls, lm for positive argument. when encounter negative arguement, it raise NegativeOptionArgumentError. The code later tries to catch it along with all other kinds of exceptions, with a try-catch block.
    ```

2. #### ValueError (occour at non-integer arguments for .LW, .LS, .LM)

    Error test case: e_in02.txt, e_in04.txt

    Within all four options, only .FT accept non-integer argument, so if non-integer argument is provided, the option-parser of my code would raise error and post-option-parser part of my code will catch the exception.

    ```
    ---error input
    >.LS a-1
    >one
    ---program exits gracefully with message
    <At line 1 of the text file, .LW or .LS option has invalid argument
    <
    ---code
    implemented with a try-catch block wrapped around option-parser,
    then catch built-in error, ValueError
    ```

3. #### FTOptionError ( occour at argument for .FT has non on/off argument )

    Error test case: e_in03.txt

    ```
    ---error input
    >.FT
    >one
    ---programm exits with message
    <At 1 of the text file, .FT has invalid argument
    ---code
    if words[1] == 'on':
    	self.ft = 1
    elif words[1] == 'off':
    	self.ft = 0
    else:
    	raise FTOptionError("At line {} of the text file, .FT option  has invalid 		argument".format(self.nth_line))
    ```

4. #### File not found error

    error_input_file: None

    ```python
    elif self.filename is not None:
    try:
    	self.f = open(self.filename)
    except FileNotFoundError as e:
    	print(e, file=sys.stderr)
    	sys.exit(-1)
    ```
    If there is file not found with given input such as ./tests/e_in0a.txt, should output

    ```
    [Errno 2] No such file or directory: './tests/e_in0a.txt'
    ```

5. #### Errorous arguments to object of UVroff class

    error_input_file: test_exception.py

    **example error input:**

    ```python
    f = UVroff(filename, filename)
    ```

    While two initialization arguments are not None, (note: at least one of them should be None and not both are None), uvroff raises ArgumentError exception

    ```
    condition_1 = (arg_1 is None and arg_2 is None)
    condition_2 = (arg_1 is not None and arg_2 is not None)
    	if condition_1 or condition_2:
        	raise ArgumentError("Two arguments were both None or both non-None, expect one and only one None argument")
       	elif self.filename == "stdin":
       	...
    ```
