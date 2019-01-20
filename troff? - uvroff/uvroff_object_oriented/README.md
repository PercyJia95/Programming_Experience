## UVroff_object_oriented

### What is it?
In assignment 3 of SENG265, we were required to transfrom the uvroff program that was in imperative style (showed at the parent directory "troff? -uvroff") to **object-oriented** style

### implementation
"UVroff_class" is namely a class that does the same formatting functions, however with applying OO style, couple things changed. 

1. Consider interface. With class, we have interface. Class hides implementation detail of uvroff, interface expose how to use it. Here UVroff is the class written in uvroff_class.py, its constructor is __init__(). init function makes up the API that users of UVroff class need to know. Usually, a set of parameters will be specified for users to invoke UVroff class such that they can initialize a object.

2. Programming with "self". what self is can be a confusing question when shift from imperative programming to object-oriented programming. "self" can be considered as a record of data, a record is a compound datatype that exists in every GPL and it is just designed to store different types of data and together they are also given one name. Each data item in the record is identified by **[record name].[data item name]**. The types of data referred here are regular datatypes, they can be int, char, array ... With object-oriented, "self" includes methods (called functions in imperative programming) as unique kind of datatype. It is weird as it sounds but a piece of code is also interpreted as strings in GPL. 
So **What is the benefit of using "self"?** With "self", we can declare a variable **anywhere** in the program and refer to it **anywhere** in the program, therefore, object-oriented programming has scope rules same as imperative programming, and additionally "self" behave like a global storage.

3. Take advantage of the exception handling. Exception are common in programming. Without handling such as in C language, the operating system simply kills the running program (so developer may be left with a confusing segmenation fualt error). Object-oriented levitates the elegance of error handling by declaring exception class, they are instantiated when exception is raised. With option to specify actions to take at error, program can continue even it crushes. 

***GPL--general purpose language
