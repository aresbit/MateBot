(continued from previous page)

| relationalExpression
| equalityExpression
| bitwiseAndLogicalExpression
| conditionalAndExpression
| conditionalOrExpression
;

The syntax below introduces several productions to be used by other expression syntax rules:

objectReference:
    typeReference
| 'super'
| primaryExpression
;

objectReference refers to one of the following three options:

• Class that is to handle static members;

- super that is to access constructors declared in the superclass, or the overridden method version of the superclass;

- primaryExpression that is to refer to a variable after evaluation, unless the manner of the evaluation is altered by the chaining operator '?.' (see Chaining Operator).

If the form of primaryExpression is thisExpression, then the pattern "this?." is handled as a compile-time error.

If the form of primaryExpression is super, then the pattern "super?." is handled as a compile-time error.

The syntax of arguments is presented below:

arguments:
    '( ' argumentSequence? ')'
;
argumentSequence:
    restArgument
    | expression (',' expression)* (',' restArgument)? ','?
;
restArgument:
    '...'? expression
;

The arguments grammar rule refers to the list of call arguments. Only the last argument can have the form of a spread expression (see Spread Expression).

### 7.1 Evaluation of Expressions

The result of a program expression evaluation denotes the following:

• Variable (the term variable is used here in the general, non-terminological sense to denote a modifiable lvalue in the left-hand side of an assignment); or
