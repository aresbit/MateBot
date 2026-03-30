# Chapter 5: Generics

Page range: 67-80

## Page 67

### 4.5 Type Declarations

An interface declaration (see Interfaces), a class declaration (see Classes), an enum declaration (see Enumerations), or a type alias (see Type Alias Declaration) are type declarations.

The syntax of type declaration is presented below:

typeDeclaration:
    classDeclaration
    | interfaceDeclaration
    | enumDeclaration
    | typeAlias
    ;

#### 4.5.1 Type Alias Declaration

Type aliases enable using meaningful and concise notations by providing the following:

• Names for anonymous types (array, function, and union types); or

• Alternative names for existing types.

Scopes of type aliases are module or namespace level scopes. Names of all type aliases must follow the uniqueness rules of Declarations in the current context.

The syntax of type alias is presented below:

typeAlias:
    'type' identifier typeParameters? '=' type
;

Meaningful names can be provided for anonymous types as follows:

type Matrix = number[][]
type Handler = (s: string, no: number) => string
type Predicate<T> = (x: T) => boolean
type NullableNumber = number | null

If the existing type name is too long, then a shorter new name can be introduced by using type alias (particularly for a generic type).

type Dictionary = Map<string, string>
type MapOfString<T> = Map<T, string>

A type alias acts as a new name only. It neither changes the original type meaning nor introduces a new type.

type Vector = number[]
function max(x: Vector): number {
    let m = x[0]
    for (let v of x)
        if (v > m) m = v
        return m

(continues on next page)

## Page 68

(continued from previous page)

7 }
8
9 let x: Vector = [2, 3, 1]
10 console.log(max(x)) // output: 3

Type aliases can be recursively referenced inside the right-hand side of a type alias declaration.

In a type alias defined as type A = something, A can be used recursively if it is one of the following:

• Array element type: type A = A]; or

• Type argument of a generic type: type A = C<A>.

type A = A[] // ok, used as element type

class C<T> { /*body*/ }
type B = C<B> // ok, used as a type argument

type D = string | Array<D> // ok

Any other use causes a compile-time error, because the compiler does not have enough information about the defined alias:

type E = E // compile-time error
type F = string | E // compile-time error

The same rules apply to a generic type alias defined as type A<T> = something:

type A<T> = Array<A<T>> // ok, A<T> is used as a type argument
type A<T> = string | Array<A<T>> // ok

type A<T> = A<T> // compile-time error

A compile-time error occurs if a generic type alias is used without a type argument:

type A<T> = Array<A> // compile-time error

Note. There is no restriction on using a type parameter T in the right side of a type alias declaration. The following code is valid:

type NodeValue<T> = T | Array<T> | Array<NodeValue<T>>;

### 4.6 Variable and Constant Declarations

A non-ambient variable declaration introduces a new variable which is in fact a named storage location. A declared variable must be assigned an initial value before the first usage. The initial value is assigned either as a part of the declaration or in various forms via initialization.

The syntax of variable declarations is presented below:

## Page 69

variableDeclarations:
    'let' variableDeclarationList
;
variableDeclarationList:
    variableDeclaration (',' variableDeclaration)*
;
variableDeclaration:
    identifier ':' type initializer?
| identifier initializer
;
initializer:
    '=' expression
;

When a variable is introduced by a variable declaration, type T of the variable is determined as follows:

• T is the type specified in a type annotation (if any) of the declaration.

– If the declaration also has an initializer, then the initializer expression type must be assignable to T (see Assignability with Initializer).

• If no type annotation is available, then T is inferred from the initializer expression (see Type Inference from Initializer).

An ambient variable declaration must have type but has no initializer. Otherwise, a compile-time error occurs.

let a: number // ok
let b = 1 // ok, type 'int' is inferred
let c: number = 6, d = 1, e = "hello" // ok

// ok, type of lambda and type of 'f' can be inferred
let f = (p: number) => b + p
let x // compile-time error -- either type or initializer

Every variable in a program must have an initial value before it can be used:

• If the initializer of a variable is specified explicitly, then its execution produces the initial value for this variable.

• Otherwise, the following situations are possible:

– If the type of a variable is T, and T has a default value (see Default Values for Types), then the variable is initialized with the default value.

– If a variable has no default value, then its value must be set by the Simple Assignment Operator before any use of the variable.

Invalid initialization is represented in the example below:

let a = b // compile-time error: circular dependency
let b = a

## Page 70

#### 4.6.2 Constant Declarations

A constant declaration introduces a named variable with a mandatory explicit value. The value of a constant cannot be changed by an assignment expression (see Assignment). If the constant is an object or array, then object fields or array elements can be modified.

The syntax of constant declarations is presented below:

constantDeclarations:
    'const' constantDeclarationList
;

constantDeclarationList:
    constantDeclaration (',' constantDeclaration)*
;

constantDeclaration:
    identifier (':' type)? initializer
;

The type T of a constant declaration is determined as follows:

• If T is the type specified in a type annotation (if any) of the declaration, then the initializer expression must be assignable to T (see Assignability with Initializer).

• If no type annotation is available, then T is inferred from the initializer expression (see Type Inference from Initializer).

const a: number = 1 // ok
const b = 1 // ok, int type is inferred
const c: number = 1, d = 2, e = "hello" // ok
const x // compile-time error -- initializer is mandatory
const y: number // compile-time error -- initializer is mandatory

#### 4.6.3 Assignability with Initializer

If a variable or constant declaration contains type annotation T and initializer expression E, then the type of E must be assignable to T (see Assignability).

#### 4.6.4 Type Inference from Initializer

The type of a declaration that contains no explicit type annotation is inferred from the initializer expression as follows:

- In a variable declaration (not in a constant declaration, though), if the initializer expression is of a literal type, then the literal type is replaced for its supertype, if any (see Subtyping for Literal Types). If the initializer expression is of a union type that contains literal types, then each literal type is replaced for its supertype (see Subtyping for Literal Types), and then normalized (see Union Types Normalization).

• Otherwise, the type of a declaration is inferred from the initializer expression.

## Page 71

If the type of the initializer expression cannot be inferred, then a compile-time error occurs (see Object Literal):

let a = null // type of 'a' is null
let aa = undefined // type of 'aa' is undefined
let arr = [null, undefined] // type of 'arr' is (null | undefined)[]

let cond: boolean = /*some initialization*/

let b = cond ? 1 : 2 // type of 'b' is int
let c = cond ? 3 : 3.14 // type of 'c' is double
let d = cond ? "one" : "two" // type of 'd' is string
let e = cond ? 1 : "one" // type of 'e' is int | string

const bb = cond ? 1 : 2 // type of 'bb' is int
const cc = cond ? 3 : 3.14 // type of 'cc' is double
const dd = cond ? "one" : "two" // type of 'dd' is "one" | "two"
const ee = cond ? 1 : "one" // type of 'ee' is int | "one"

let f = {name: "aa"} // compile-time error: type unknown

declare let x1 = 1 // compile-time error: ambient variable cannot have initializer
declare const x2 = 1 // type of 'x2' is int
let x3 = 1 // type of 'x3' is int
const x4 = 1 // type of 'x4' is int

declare let s1 = "1" // compile-time error: ambient variable cannot have initializer
declare const s2 = "1" // type of 's2' is "1"
let s3 = "1" // type of 's3' is string
const s4 = "1" // type of 's4' is "1"

### 4.7 Function Declarations

Function declarations specify names, signatures, and bodies when introducing named functions. An optional function body is a block (see Block).

The syntax of function declarations is presented below:

functionDeclaration:
    modifiers? 'function' identifier
    typeParameters? signature block?
;

modifiers:
    'native' | 'async'
;

Functions must be declared on the top level (see Top-Level Statements).

If a function is declared generic (see Generics), then its type parameters must be specified.

## Page 72

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

## Page 73

If a parameter type is prefixed with `ready`, then there are additional restrictions on the parameter as described in `Readonly Parameters`.

#### 4.7.3 Readonly Parameters

If the parameter type is `readonly` array or `tuple` type, then no assignment and no function or method call can modify elements of this array or `tuple`. Otherwise, a compile-time error occurs:

function foo(array: readonly number[], tuple: readonly [number, string]) {
    let element = array[0] // OK, one can get array element
    array[0] = element // compile-time error, array is readonly

    element = tuple[0] // OK, one can get tuple element
    tuple[0] = element // compile-time error, tuple is readonly
}

Any assignment of readonly parameters and variables must follow the limitations stated in Type of Expression.

#### 4.7.4 Optional Parameters

Optional parameters can be of two forms as follows:

optionalParameter:
    identifier (':' type)?）=' expression
| identifier '?' ':' type
;

The first form contains an expression that specifies a default value. It is called a parameter with default value. The value of the parameter is set to the default value if the argument corresponding to that parameter is omitted in a function or method call:

function pair(x: number, y: number = 7)
{
    console.log(x, y)
}
pair(1, 2) // prints: 1 2
pair(1) // prints: 1 7

The second form is a short-cut notation and identifier '?' ':' type effectively means that identifier has type T | undefined with the default value undefined.

For example, the following two functions can be used in the same way:

function hello1(name: string | undefined = undefined) {}
function hello2(name?: string) {}

hello1() // 'name' has 'undefined' value

(continues on next page)

## Page 74

hello1("John") // 'name' has a string value
hello2() // 'name' has 'undefined' value
hello2("John") // 'name' has a string value

function foo1 (p?: number) {}
function foo2 (p: number | undefined = undefined) {}

foo1() // 'p' has 'undefined' value
foo1(5) // 'p' has a numeric value
foo2() // 'p' has 'undefined' value
foo2(5) // 'p' has a numeric value

#### 4.7.5 Rest Parameter

Rest parameters allow functions, methods, constructors, or lambdas to take arbitrary numbers of arguments. Rest parameters have the spread operator ‘...’ as a prefix before the parameter name.

The syntax of rest parameter is presented below:

restParameter:
    annotationUsage? '...' identifier ':' type
;

A compile-time error occurs if a rest parameter:

• Is not the last parameter in a parameter list;

• Has a type that is not an array type, a tuple type, nor a type parameter constrained by an array or a tuple type.

A call of entity with a rest parameter of array type T[] (or FixedArray<T>) can accept any number of arguments of types that are assignable (see Assignability) to T:

function sum(...numbers: number[]): number {
    let res = 0
    for (let n of numbers)
        res += n
    return res
}

sum() // returns 0
sum(1) // returns 1
sum(1, 2, 3) // returns 6

If an argument of array type T[] is to be passed to a call of entity with the rest parameter, then the spread expression (see Spread Expression) must be used with the spread operator ‘...’ as a prefix before the array argument:

function sum(...numbers: number[]): number {
    let res = 0
    for (let n of numbers)
        res += n

(continues on next page)

## Page 75

(continued from previous page)

return res
}

let x: number[] = [1, 2, 3]
sum(...x) // spread an array 'x'
// returns 6

A call of entity with a rest parameter of tuple type  $ [T_1, \ldots, T_n] $ can accept only n arguments of types that are assignable (see Assignability) to the corresponding  $ T_i $:

function sum(...numbers: [number, number, number]): number {
    return numbers[0] + numbers[1] + numbers[2]
}

sum() // compile-time error: wrong number of arguments, 0 instead of 3
sum(1) // compile-time error: wrong number of arguments, 1 instead of 3
sum(1, 2, "a") // compile-time error: wrong type of the 3rd argument
sum(1, 2, 3) // returns 6

It is legal though meaningless to declare a function with an optional parameter followed by a rest parameter of a tuple type. However, use of such function without explicitly set optional and rest parameters will cause compile-time error:

// optional tuple + rest tuple
function g(opt?: [number, string], ...tail: [number, string]) { // OK
    // ...
}

g() // CTE - no rest tuple
g([1, "str"]) // CTE - no rest tuple
g([1, "str"], 1, "str") // OK

If an argument of tuple type  $ [T_1, \ldots, T_n] $ is to be passed to a call of entity with the rest parameter, then a spread expression (see Spread Expression) must have the spread operator ‘...’ as a prefix before the tuple argument:

function sum(...numbers: [number, number, number]): number {
    return numbers[0] + numbers[1] + numbers[2]
}

let x: [number, number, number] = [1, 2, 3]
sum(...x) // spread tuple 'x'
// returns 6

If an argument of fixed-size array type FixedArray<T> is to be passed to a function or a method with the rest parameter, then the spread expression (see Spread Expression) must be used with the spread operator ‘…’ as a prefix before the fixed-size array argument:

function sum(...numbers: Array<number>): number {
    let res = 0
    for (let n of numbers)
        res += n
    return res
}

(continues on next page)

## Page 76

(continued from previous page)

let x: FixedArray<number> = [1, 2, 3]
sum(...x) // spread an fixed-size array 'x'
// returns 6

If constrained by an array or a tuple type, a type parameter can be used with generics as a rest parameter.

function sum<T extends Array<number>>(...numbers: T): number {
    let res = 0
    for (let n of numbers)
        res += n
    return res
}

Note. Any call to a function, method, constructor, or lambda with a rest parameter implies that a new array or tuple is created from the arguments provided.

function foo(...array_parameter: number[], ...tuple_parameter: [number, string]) {
    // array_parameter is a new array created from the arguments passed
    // tuple_parameter is a new tuple created from the arguments passed
    array_parameter[0] = 1234
    tuple_parameter[0] = 1234
    console.log(array_parameter[0], tuple_parameter[0]) // 1234 1234 is the output
}

const array_argument: number[] = [1,2,3,4]
const tuple_argument: [number, string] = [1,"234"]

console.log(array_argument[0], tuple_argument[0]) // 11 is the output

foo(...array_argument, ...tuple_argument)
    // array_argument is spread into a sequence of its elements
    // tuple_argument is spread into a sequence of its elements

console.log(array_argument[0], tuple_argument[0]) // 11 is the output

#### 4.7.6 Shadowing by Parameter

If the name of a parameter is identical to the name of a top-level variable accessible (see Accessible) within the body of a function or a method with that parameter, then the name of the parameter shadows the name of the top-level variable within the body of that function or method:

let x: number = 1
function foo (x: string) {
    // 'x' refers to the parameter and has type string
}
class SomeClass {
    method (x: boolean) {
        // 'x' refers to the method parameter and has type boolean
    }
}

## Page 77

(continued from previous page)

10

X++ // 'x' refers to the global variable

#### 4.7.7 Return Type

Function, method, or lambda return type defines the resultant type of the function, method, or lambda execution (see Function Call Expression, Method Call Expression, and Lambda Expressions). During the execution, the function, method, or lambda can produce a value of a type that is assignable to the return type (see Assignability).

The syntax of return type is presented below:

returnType:
    ':' (type | 'this')
;

If function or method return type is not void (see Type void), and the execution path of the function or method body has no return statement (see return Statements), then a compile-time error occurs.

A compile-time error occurs if lambda return type is not never (see Type never), and the execution path of a function, method, or lambda body has no return statement (see return Statements).

A special form of return type with the keyword this as type annotation can be used in class instance methods only (see Methods Returning this).

If function, method, or lambda return type is not specified, then it is inferred from its body (see Return Type Inference). If there is no body, then the function, method, or lambda return type is void (see Type void).

#### 4.7.8 Return Type Inference

A missing function, method, or lambda return type can be inferred from the function, method, or lambda body. A compile-time error occurs if return type is missing from a native function (see Native Functions).

The current version of ArkTS allows inferring return types at least under the following conditions:

• If there is no return statement, or if all return statements have no expressions, then the return type is void (see Type void).

• If there are k return statements (where k is 1 or more) with the same type expression R, then R is the return type.

• If there are k return statements (where k is 2 or more) with expressions of types  $ T_1 $,  $ \ldots $,  $ T_k $, then R is the union type (see Union Types) of these types ( $ T_1 \mid \ldots \mid T_k $), and its normalized version (see Union Types Normalization) is the return type. If at least one of return statements has no expression, then type undefined is added to the return type union.

• If a lambda body contains no return statement but at least one throw statement (see throw Statements), then the lambda return type is never (see Type never).

• If a function, a method, or a lambda is async (see Asynchronous API), a return type is inferred by applying the above rules, and the return type T is not Promise, then the return type is assumed to be Promise<T>.

## Page 78

Future compiler implementations are to infer the return type in more cases. Type inference is represented in the example below:

// Explicit return type
function foo(): string { return "foo" }

// Implicit return type inferred as string
function goo() { return "goo" }

class Base {}
class Derived1 extends Base {}
class Derived2 extends Base {}

function bar (condition: boolean) {
    if (condition)
        return new Derived1()
    else
        return new Derived2()
}

// Return type of bar will be Derived1/Derived2 union type
function boo (condition: boolean) {
    if (condition) return 1
}

// That is a compile-time error as there is an execution path with no return

If the compiler fails to recognize a particular type inference case, then a corresponding compile-time error occurs.

## Page 79

## GENERICS

Class, interface, type alias, method, and function are program entities that can be parameterized in ArkTS by one or several types. An entity so parameterized introduces a generic declaration (called a generic for brevity).

Types used as generic parameters in a generic are called type parameters (see Type Parameters).

A generic must be instantiated in order to be used. Generic instantiation is the action that transforms a generic into a real program entity (non-generic class, interface, union, array, method, or function), or into another generic instantiation. Instantiation (see Generic Instantiations) can be performed either explicitly or implicitly.

ArkTS has special types that look similar to generics syntax-wise, and allow creating new types during compilation (see Utility Types).

### 5.1 Type Parameters

Type parameter is declared in the type parameter section. It can be used as an ordinary type inside a generic.

Syntax-wise, a type parameter is an unqualified identifier with a proper scope (see Scopes for the scope of type parameters). Each type parameter can have a constraint (see Type Parameter Constraint). A type parameter can have a default type (see Type Parameter Default), and can specify its in- or out- variance (see Type Parameter Variance).

The syntax of type parameter is presented below:

typeParameters:
    '<' typeParameterList '>'
;

typeParameterList:
    typeParameter (',' typeParameter)*
;

typeParameter:
    ('in' | 'out')? identifier constraint? typeParameterDefault?
;

constraint:
    'extends' type
;

(continues on next page)

## Page 80

(continued from previous page)

typeParameterDefault:
    '=' typeReference ('[]')?
;

A generic class, interface, type alias, method, or function defines a set of parameterized classes, interfaces, unions, arrays, methods, or functions respectively (see Generic Instantiations). A single type argument can define only one set for each possible parameterization of the type parameter section.

#### 5.1.1 Type Parameter Constraint

If possible instantiations need to be constrained, then an individual constraint can be set for each type parameter after the keyword extends. A constraint can have the form of any type.

If no constraint is specified, then the constraint is Type Any, i.e., the lacking explicit constraint effectively means extends Any. As a consequence, the type parameter is not compatible with Type Object, and has neither methods nor fields available for use.

If type parameter T has type constraint S, then the actual type of the generic instantiation must be a subtype of S (see Subtyping). If the constraint S is a non-nullish type (see Nullish Types), then T is also non-nullish.

class Base {}
class Derived extends Base { }
class SomeType { }

class G<T extends Base> { }

let x = new G<Base> // OK
let y = new G<Derived> // OK
let z = new G<SomeType> // Compile-time : SomeType is not compatible with Base

class H<T extends Base|SomeType> {}
let h1 = new H<Base> // OK
let h2 = new H<Derived> // OK
let h3 = new H<SomeType> // OK
let h4 = new H<Object> // Compile-time : Object is not compatible with Base/SomeType

class Exotic<T extends "aa"| "bb"> {}
let e1 = new Exotic<"aa"> // OK
let e2 = new Exotic<"cc"> // Compile-time : "cc" is not compatible with "aa"| "bb"

class A {
    f1: number = 0
    f2: string = ""
    f3: boolean = false
}
class B <T extends keyof A> {}
let b1 = new B<'f1'> // OK
let b2 = new B<'f0'> // Compile-time error as 'f0' does not fit the constraint
let b3 = new B<keyof A> // OK
