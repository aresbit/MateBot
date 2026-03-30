## EXPERIMENTAL FEATURES

This Chapter introduces the ArkTS features that are considered parts of the language, but have no counterpart in TypeScript, and are therefore not recommended to those who seek a single source code for TypeScript and ArkTS.

Some features introduced in this Chapter are still under discussion. They can be removed from the final version of the ArkTS specification. Once a feature introduced in this Chapter is approved and/or implemented, the corresponding section is moved to the body of the specification as appropriate.

The array creation feature introduced in Resizable Array Creation Expressions enables users to dynamically create objects of array type by using runtime expressions that provide the array size. This addition is useful to other array-related features of the language, such as array literals. This feature can also be used to create arrays of arrays.

Overloading functions, methods, or constructors is a practical and convenient way to write program actions that are similar in logic but different in implementation. ArkTS uses Overload Declarations as an innovative form of managed overloading.

Section Native Functions and Methods introduces practically important and useful mechanisms for the inclusion of components written in other languages into a program written in ArkTS.

Sections Final Classes and Final Methods discuss the well-known feature that in many OOP languages provides a way to restrict class inheritance and method overriding. Making a class final prohibits defining classes derived from it, whereas making a method final prevents it from overriding in derived classes.

Section Adding Functionality to Existing Types discusses the way to add new functionality to an already defined type.

Section Enumeration Methods adds methods to declarations of the enumeration types. Such methods can help in some kinds of manipulations with enums.

The ArkTS language supports writing concurrent applications in the form of coroutines (see Coroutines (Experimental)) that allow executing functions concurrently.

There is a basic set of language constructs that support concurrency. A function to be launched asynchronously is marked by adding the modifier async to its declaration. In addition, any function or lambda expression can be launched as a separate thread explicitly by using the launch function from the standard library.

### 17.1 Type char

Values of char type are Unicode code points.
