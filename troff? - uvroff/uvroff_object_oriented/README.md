## UVroff_object_oriented

### What is it?
In assignment 3 of SENG265, we were required to transfrom the uvroff program that was in imperative style (showed at the parent directory "troff? -uvroff") to **object-oriented** style

### implementation
"UVroff_class" is namely a class that does the same formatting functions, however with applying OO style, couple things changed. 

1. Consider interface. With class, we have interface. Class hides implementation detail of uvroff, interface expose how to use it. Here UVroff is the class written in uvroff_class.py, its constructor is __init__(). init function makes up the API that users of UVroff class need to know. Usually, a set of parameters will be specified for users to invoke UVroff class such that they can initialize a object.

2. programming with "self". what self is can be a confusing question when shift from imperative programming to object-oriented programming. "self" can be considered as a record of data, a record is a compound datatype that exists in every GPL and it is just designed to stores different types of data and together they are referred by one name. Each data item in the record is identified by **[record name].[data item name]**. The types of data referred here are regular datatypes, they can be int, char, array ... With object-oriented, "self" include functions as unique kind of datatype. It is weird as it sounds but a piece of code is also usually interpreted as string type in GPL. So ***What is the benefit of using "self"?*** With "self", we can declare a variable ***anywhere*** in the program and refer to it ***anywhere*** in the program, therefore, object-oriented programming has scope rules same as imperative programming, and additionally "self" behave like a global storage.

3. 

***GPL--general purpose language
