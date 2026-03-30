(continued from previous page)

console.log("not a Person")

printName(new Person("Bob")) // output: Bob
printName(1) // output: not a Person

### 7.17 Type0f Expression

The syntax of typeof expression is presented below:

typeOfExpression:
  'typeof' expression
;

Any type of expression is of type string.

If typeof expression refers to a name of an overloaded function or method, then a compile-time error occurs.

The evaluation of a type of expression starts with the expression evaluation. If this evaluation causes an error, then the type of expression evaluation terminates abruptly. Otherwise, the value of a type of expression is defined as follows:

1. The value of a TypeOf expression is known at compile time
