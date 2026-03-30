# Chapter 10: Implementation Details

Page range: 315-318

## Page 315

improve readability.

### 17.14 Trailing Lambdas

The trailing lambda is a special form of notation for function or method call when the last parameter of a function or a method is of function type, and the argument is passed as a lambda using the Block notation. The trailing lambda syntactically looks as follows:

class A {
    foo (f: ()=>void) { ... }
}

let a = new A()
a.foo() { console.log ("method lambda argument is activated") }
// method foo receives last argument as the trailing lambda

The syntax of trailing lambda is presented below:

trailingLambdaCall:
    (objectReference '' identifier typeArguments?)
    | expression ('?.' | typeArguments)?
)
arguments block
;

Currently, no parameter can be specified for the trailing lambda, except a receiver parameter (see Lambda Expressions with Receiver). Otherwise, a compile-time error occurs.

A block immediately after a call is always handled as trailing lambda. A compile-time error occurs if the last parameter of the called entity is not of a function type.

The semicolon ‘;’ separator can be used between a call and a block to indicate that the block does not define a trailing lambda. When calling an entity with the last optional parameter (see Optional Parameters), it means that the call must use the default value of the parameter.

function foo (f := >void) { ... }

foo() { console.log("trailing lambda") }
// 'foo' receives last argument as the trailing lambda

function bar(f?: () => void) { ... }

bar() { console.log("trailing lambda") }
// function 'bar' receives last argument as the trailing lambda,
bar(); { console.log("that is the block code") }
// function 'bar' is called with parameter 'f' set to 'undefined'

function goo(n: number) { ... }

goo() { console.log("aa") } // compile-time error as goo() requires an argument
goo(); { console.log("aa") } // compile-time error as goo() requires an argument

## Page 316

If there are optional parameters in front of an optional function type parameter, then calling such a function or method can skip optional arguments and keep the trailing lambda only. This implies that the value of all skipped arguments is undefined.

function foo (p1?: number, p2?: string, f?: ()=>string) {
    console.log (p1, p2, f?.)
}

foo()    // undefined undefined undefined
foo() { return "lambda" }    // undefined undefined lambda
foo(1) { return "lambda" }    // 1 undefined lambda
foo(1, "a") { return "lambda" } // 1 a lambda

## Page 317

## ANNOTATIONS

Annotation is a special language element that changes the semantics of the declaration to which it is applied by adding metadata.

Declaring and using an annotation is represented in the example below:

// Annotation declaration:
@interface ClassAuthor {
    authorName: string
}

// Annotation use:
@ClassAuthor({authorName: "Bob"}
class MyClass {/*body*/}

The annotation ClassAuthor in the example above adds metadata to the class declaration.

An annotation must be placed immediately before the declaration to which it is applied. An annotation can include arguments as in the example above.

For an annotation to be used, the name of the annotation must be prefixed with the character ‘@’ (e.g., @MyAnno). No white space and line separator is allowed between the character ‘@’ and the name:

ClassAuthor({authorName: "Bob"}) // compile-time error, no '@'
@ ClassAuthor({authorName: "Bob"}) // compile-time error, space is forbidden

A compile-time error occurs if the annotation name is not accessible (see Accessible) at the place of use. An annotation declaration can be exported and used in other modules.

Multiple annotations can be applied to a single declaration:

@MyAnno()
@ClassAuthor({authorName: "John Smith”）
class MyClass {/*body*/}

### 18.1 Declaring Annotations

Declaring an annotation is similar to declaring an interface where the keyword interface is prefixed with the character '@'.

## Page 318

The syntax of annotation declaration is presented below:

annotationDeclaration:
  '@interface ' identifier '{' annotationField* '}'
;
annotationField:
  identifier ':' type const Initializer?
;
const Initializer:
  =' constantExpression
;

As any other declared entity, an annotation can be exported by using the keyword export.

Type in the annotation field is restricted (see Types of Annotation Fields).

The default value of an annotation field can be specified by using `initializer` as `constant` expression. A compile-time error occurs if the value of this expression cannot be evaluated at compile time.

Annotation must be defined at the top level. Otherwise, a compile-time error occurs.

Annotation cannot be extended as inheritance is not supported.

The name of an annotation cannot coincide with the name of another entity:

@interface Position {/*properties*/}

class Position {/*body*/} // compile-time error: duplicate identifier

An annotation declaration defines no type, and no type alias can be applied to the annotation or used as an interface:

@interface Position {}
type Pos = Position // compile-time error

class A implements Position {} // compile-time error

#### 18.1.1 Types of Annotation Fields

The choice of types for annotation fields is limited to the following:

• Numeric Types:

• Type boolean (see Type boolean);

• Type string;

• Enumeration types (see Enumerations);

• Array of the above types (e.g., string[]), including arrays of arrays (e.g., string[][]).

A compile-time error occurs if any other type is used as the type of an annotation field.
