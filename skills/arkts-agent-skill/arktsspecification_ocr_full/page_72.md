The modifier native indicates that the function is a native function (see Native Functions in Experimental Features). If a native function has a body, then a compile-time error occurs.

Functions with the modifier async are discussed in Async Functions.

#### 4.7.1 Signatures

A signature defines parameters and the return type (see Return Type) of a function, method, or constructor.

The syntax of signature is presented below:

signature:
    '( ' parameterList? ' )' returnType?
;

#### 4.7.2 Parameter List

A signature may contain a parameter list that specifies an identifier of each parameter name, and the type of each parameter. The type of each parameter must be defined explicitly. If the parameter list is omitted, then the function or the method has no parameters.

The syntax of parameter list is presented below:

parameterList:
    parameter (',' parameter)* (',' restParameter)? ','?
| restParameter ','?
;
parameter:
    annotationUsage? (requiredParameter | optionalParameter)
;
requiredParameter:
    identifier ':' type
;

If a parameter is required, then each function or method call must contain an argument corresponding to that parameter. The function below has required parameters:

function power(base: number, exponent: number): number {
    return Math.pow(base, exponent)
}
power(2, 3) // both arguments are required in the call

Several parameters can be optional, allowing to omit corresponding arguments in a call (see Optional Parameters).

A compile-time error occurs if an optional parameter precedes a required parameter.

The last parameter of a function or a method can be a single rest parameter (see Rest Parameter).
