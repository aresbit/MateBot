7 }
8 a = "a string"
9
10 // The logically ordered text - declarations then statements
11 type A = number | string
12 function foo () {
13     console.log (a)
14     }
15 console.log ("Start of top-level statements")
16 let a: A = 56
17 a = "a string"

• If a module is imported by some other module, then the semantics of top-level statements is to initialize the imported module. It means that all top-level statements are executed only once before a call to any other function, or before the access to any top-level variable of the module.

• If a module is used as a program, then top-level statements are used as a program entry point (see Program Entry Point). The set of top-level statements being empty implies that the program entry point is also empty and does nothing. If a module has the main function, then it is executed after the execution of the top-level statements.

// Source file A
{ // Block form
    console.log("A.top-level statements")
}

// Source file B
import * as A from "Source file A "
function main () {
    console.log("B.main")
}

The output is as follows:
A. Top-level statements,
B. Main.

// One source file
console.log("A.Top-level statements")
function main() {
    console.log("B.main")
}

A compile-time error occurs if top-level statements contain a return statement (Expression Statements).

The execution of top-level statements means that all statements, except type declarations, are executed one after another in the textual order of their appearance within the module until an error situation is thrown (see Errors), or last statement is executed.
