#### 7.1.5 Evaluation of Arguments

An evaluation of arguments always progresses from left to right up to the first error, or through the end of the expression; i.e., any argument expression is evaluated after the evaluation of each argument expression to its left completes normally (including comma-separated argument expressions that appear within parentheses in method calls, constructor calls, class instance creation expressions, or function call expressions).

If the left-hand argument expression completes abruptly, then no part of the right-hand argument expression is evaluated.

#### 7.1.6 Evaluation of Other Expressions

These general rules cannot cover the order of evaluation of certain expressions when they from time to time cause exceptional conditions. The order of evaluation of the following expressions requires specific explanation:

• Class instance creation expressions (see New Expressions);

• Resizable Array Creation Expressions:

• Indexing Expressions;

• Method call expressions (see Method Call Expression);

• Assignments involving indexing (see Assignment);

• Lambda Expressions.

### 7.2 Literal

Literals (see Literals) denote fixed and unchanging values. Type of a literal is the type of an expression.

### 7.3 Named Reference

An expression can have the form of a named reference as described by the syntax rule as follows:

namedReference:
    qualifiedName typeArguments?
;

Type of a named reference expression is the type of the entity to which a named reference refers.

QualifiedName (see Names) is an expression that consists of dot-separated names. If qualifiedName consists of a single identifier, then it is called a simple name.

Simple name refers to the following:

• Entity declared in the current module;
