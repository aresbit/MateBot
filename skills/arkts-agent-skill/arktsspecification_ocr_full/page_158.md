The string concatenation operator can be used to rewrite the above example as follows:

let a = 2
let b = 2
console.log("The result of " + a + " * " + b + " is " + a * b)

An embedded expression can contain nested multiline strings.

### 7.32 Lambda Expressions

Lambda expression fully defines an instance of a function type (see Function Types) by providing optional annotation usage (see Using Annotations), optional async mark (see Async Lambdas), mandatory lambda signature, and its body. The declaration of lambda expression is generally similar to that of a function declaration (see Function Declarations), except that a lambda expression has no function name specified, and can have types of parameters omitted.

The syntax of lambda expression is presented below:

lambdaExpression:
    annotationUsage? 'async'? lambdaSignature）=>lambdaBody
;
lambdaBody:
    expression | block
;
lambdaSignature:
    ('lambdaParameterList? ')' returnType?
| identifier
;
lambdaParameterList:
    lambdaParameter (',' lambdaParameter)* (',' restParameter)? ','?
| restParameter ','?
;
lambdaParameter:
    annotationUsage? (lambdaRequiredParameter | lambdaOptionalParameter)
;
lambdaRequiredParameter:
    identifier (':' type)?
;
lambdaOptionalParameter:
    identifier '?' (':' type)?
;
lambdaRestParameter:
    '...' lambdaRequiredParameter
