# Chapter 17: Experimental Features

Page range: 271-304

## Page 271

p4: Object,
p5: Object,
p6: Object,
p7: Object
): void
}
interface Derived1 extends Base {
    kinds_of_return_type(): Base // Valid overriding
}
interface Derived2 extends Base {
    kinds_of_return_type(): (q: Derived) => Base // Valid overriding
}
interface Derived3 extends Base {
    kinds_of_return_type(): number // Valid overriding
}
interface Derived4 extends Base {
    kinds_of_return_type(): number | string // Valid overriding
}
interface Derived5 extends Base {
    kinds_of_return_type(): E1 // Valid overriding
}
interface Derived6 extends Base {
    kinds_of_return_type(): Base[] // Valid overriding
}
interface Derived7 extends Base {
    kinds_of_return_type(): [Base, Base] // Valid overriding
}

### 15.9 Overloading

Overloading is the language feature that allows to use the same name to call several functions, or methods, or constructors with different signatures.

The actual function, method, or constructor to be called is determined at compile time. Thus, overloading is compile-time polymorphism by name.

ArkTS supports the following two overloading mechanisms:

• Conventional overloading TBD; and

• Innovative managed overloading (see Overload Declarations).

Overload resolution is used to select one entity to call from a set of candidates if the name to call refers to an overload declaration (see Overload Resolution).

Both mechanisms of resolution use the first-match textual order to streamline the resolution process.

TBD: A compile-time warning is issued if the order of entities in an overload declaration implies that some overloaded entities can never be selected for a call.

## Page 272

function f1 (p: number) {}
function f2 (p: string) {}
function f3 (p: number|string) {}
overload foo {f1, f2, f3} // f3 will never be called as foo()

foo (5) // f1() is called
foo ("5") // f2() is called

#### 15.9.1 Overload Resolution

Overload declaration defines an ordered set of entities, and the first entity from this set that is accessible and has an appropriate signature is used to call at the call site. This approach is called managed overloading because the first-match algorithm provides full control for a developer to select a specific entity to call. This developer control over calls is represented in the following example:

function max2i(a: int, b: int): int
    return a > b ? a : b
}
function max2d(a: double, b: double): double {
    return a > b ? a : b
}
function maxN(...a: double[]): double {
    // returns max element in array 'a'
}
overload max {max2i, max2d, maxN}
let i = 1
let j = 2
let pi = 3.14

max(i, j) // max2i is used
max(i, pi) // max2d is used
max(i, pi, 4) // maxN is used
max(1) // maxN is used
max(false, true) // compile-time error, no appropriate signature

Overload resolution for an instance method overload (see Class Method Overload Declarations) always uses the type of the object reference known at compile time. It can be either the type used in a declaration, or a smart type (see Smart Types) as represented in the example below:

class A {
    foo1(x: A) { console.log("A.foo") }
    overload foo { foo1 }
}

class B extends A {
    foo2(x: B) { console.log("B.foo") }
    overload foo { foo2, foo1 }
}

(continues on next page)

## Page 273

function test(a: A) {
    a.foo(new B()) // 'fool' is called as overload from 'A' is used
}

test(new B()) // output: A.foo

let b = new B()
b.foo(b) // output: B.foo, as overload from 'B' is used

### 15.10 Type Erasure

Type erasure is the compilation technique which provides a special handling of certain language types, primarily Generics, when applied to the semantics of the following expressions:

• InstanceOf Expression;

• Cast Expression.

As a result, special types must be used for the execution of such expressions. Certain types in such expressions are handled as their corresponding effective types, while the effective type is defined as type mapping. The effective type of a specific type T is always a supertype of T. As a result, the relationship of an original type and an effective type can have the following two kinds:

• Effective type of T is identical to T, and type erasure has no effect. So, type T is retained.

• If effective type of T is not identical to T, then the type T is considered affected by type erasure, i.e., erased.

In addition, accessing a value of type T, particularly by Field Access Expression, Method Call Expression, or Function Call Expression, can cause ClassCastError thrown if type T and the target type are both affected by type erasure, and the value is produced by a Cast Expression.

class A<T> {
    field?: T

    test(value: Object) {
        return value instanceof T // CTE, T is erased
    }

    cast(value: Object) {
        return value as T // OK, but check is done during execution
    }
}

function castToA(p: Object) {
    p instanceof A<number> // CTE, A<number> is erased

    return p as A<number> // OK, but check is performed against type A, but not A<number>
}

Type mapping determines the effective types as follows:

## Page 274

• Type Parameter Constraint for Type Parameters.

• Instantiation of the same generic type (see Explicit Generic Instantiations) for generic types (see Generics), with its type arguments selected in accordance with Type Parameter Variance as outlined below:

– Covariant type parameters are instantiated with the constraint type;

– Contravariant type parameters are instantiated with the type never;

– Invariant type parameters are instantiated with no type argument, i.e., Array<T> is instantiated as Array<>.

• Union type constructed from the effective types of types T1 | T2 ... Tn within the original union type for Union Types in the form T1 | T2 ... Tn.

• Same for Array Types in the form T[] as for generic type Array<T>.

• Instantiation of FixedArray for FixedArray<T> instantiations, with the effective type of type argument T preserved.

• Instantiation of an internal generic function type with respect to the number of parameter types n for Function Types in the form (P1, P2 ..., Pn) => R. Parameter types P1, P2 ... Pn are instantiated with Any, and the return type R is instantiated with type never.

- Instantiation of an internal generic tuple type with respect to the number of element types n for Tuple Types in the form [T1, T2 ..., Tn].

• String for String Literal Types.

• Enumeration base type of the same const enum type for const enum types (see Enumerations).

• Otherwise, the original type is preserved.

### 15.11 Static Initialization

Static initialization is a routine performed once for each class (see Classes), namespace (see Namespace Declarations), or module (see Modules and Namespaces).

Static initialization execution involves the execution of the following:

• Initializers of variables or static fields;

• Top-level statements;

• Code inside a static block.

Static initialization is performed before the first execution of one of the following operations:

• Invocation of a static method or function of an entity scope;

• Access to a static field or variable of an entity scope;

• Instantiation of an entity that is an interface or class;

• Static initialization of a direct subclass of an entity that is a class.

Note. None of the operations above invokes a static initialization recursively if the static initialization of the same entity is not complete.

Note. For namespaces, the code in a static block is executed only when namespace members are used in the program (an example is provided in Namespace Declarations).

## Page 275

If static initialization routine execution is terminated due to an exception thrown, then the initialization is not complete. Repeating an attempt to execute a static initialization produces an exception again.

Static initialization routine invocation of a concurrent execution (see Coroutines (Experimental)) involves synchronization of all coroutines that try to invoke it. The synchronization is to ensure that the initialization is performed only once, and the operations that require the static initialization to be performed are executed after the initialization completes.

If static initialization routines of two concurrently initialized classes are circularly dependent, then a deadlock can occur.

#### 15.11.1 Static Initialization Safety

A compile-time error occurs if a named reference refers to a not yet initialized entity, including one of the following:

• Variable (see Variable and Constant Declarations) of a module or namespace (see Namespace Declarations);

• Static field of a class (see Static and Instance Fields).

If detecting an access to a not yet initialized entity is not possible, then runtime evaluation is performed as follows:

• Default value is produced if the type of an entity has a default value;

• Otherwise, NullPointerError is thrown.

### 15.12 Dispatch

As a result of assignment (see Assignment) to a variable or call (see Method Call Expression or Function Call Expression), the actual runtime type of a parameter of class or interface can become different from the type explicitly specified or inferred at the point of declaration.

In this situation method calls are dispatched during program execution based on their actual type.

This mechanism is called dynamic dispatch. Dynamic dispatch is used in OOP languages to provide greater flexibility and the required level of abstraction. Unlike static dispatch where the particular method to be called is known at compile time, dynamic dispatch requires additional action during program code execution. Compilation tools can optimize dynamic to static dispatch.

### 15.13 Compatibility Features

Some features are added to ArkTS in order to support smooth TypeScript compatibility. Using these features while doing the ArkTS programming is not recommended in most cases.

## Page 276

#### 15.13.1 Extended Conditional Expressions

ArkTS provides extended semantics for conditional expressions to ensure better TypeScript alignment. It affects the semantics of the following:

• Ternary conditional expressions (see Ternary Conditional Expressions, Conditional-And Expression, Conditional-Or Expression, and Logical Complement);

• while and do statements (see while Statements and do Statements);

• for statements (see for Statements);

• if statements (see if Statements).

Note. The extended semantics is to be deprecated in one of the future versions of ArkTS.

The extended semantics approach is based on the concept of truthiness that extends the boolean logic to operands of non-boolean types.

Depending on the kind of a valid expression's type, the value of the valid expression can be handled as true or false as described in the table below:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Value Type Kind</td><td style='text-align: center; word-wrap: break-word;'>When false</td><td style='text-align: center; word-wrap: break-word;'>When true</td><td style='text-align: center; word-wrap: break-word;'>ArkTS Code Example to Check</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>string</td><td style='text-align: center; word-wrap: break-word;'>empty string</td><td style='text-align: center; word-wrap: break-word;'>non-empty string</td><td style='text-align: center; word-wrap: break-word;'>s.length == 0</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>boolean</td><td style='text-align: center; word-wrap: break-word;'>false</td><td style='text-align: center; word-wrap: break-word;'>true</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>enum</td><td style='text-align: center; word-wrap: break-word;'>enum constant handled as false</td><td style='text-align: center; word-wrap: break-word;'>enum constant handled as true</td><td style='text-align: center; word-wrap: break-word;'>x.valueOf()</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number (double/float)</td><td style='text-align: center; word-wrap: break-word;'>0 or NaN</td><td style='text-align: center; word-wrap: break-word;'>any other number</td><td style='text-align: center; word-wrap: break-word;'>n != 0 &amp;&amp; !isNaN(n)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>any integer type</td><td style='text-align: center; word-wrap: break-word;'>== 0</td><td style='text-align: center; word-wrap: break-word;'>!= 0</td><td style='text-align: center; word-wrap: break-word;'>i != 0</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bigint</td><td style='text-align: center; word-wrap: break-word;'>== 0n</td><td style='text-align: center; word-wrap: break-word;'>!= 0n</td><td style='text-align: center; word-wrap: break-word;'>i != 0n</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>null or undefined</td><td style='text-align: center; word-wrap: break-word;'>always</td><td style='text-align: center; word-wrap: break-word;'>never</td><td style='text-align: center; word-wrap: break-word;'>x != null or x != undefined</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Union types</td><td style='text-align: center; word-wrap: break-word;'>When value is false according to this column</td><td style='text-align: center; word-wrap: break-word;'>When value is true according to this column</td><td style='text-align: center; word-wrap: break-word;'>x != null or x != undefined for union types with nullish types</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Any other nonNullish type</td><td style='text-align: center; word-wrap: break-word;'>never</td><td style='text-align: center; word-wrap: break-word;'>always</td><td style='text-align: center; word-wrap: break-word;'>new SomeType != null</td></tr></table>

Extended semantics of Conditional-And Expression and Conditional-Or Expression affects the resultant type of expressions as follows:

- Type of conditional-and expression A && B equals the type of B if the result of A is handled as true. Otherwise, the expression type equals the type of A.

• Type of conditional-or expression A || B equals the type of B if the result of A is handled as false. Otherwise, the expression type equals the type of A.

The way this approach works in practice is represented in the example below. Any nonzero number is handled as true. The loop continues until it becomes zero that is handled as false:

for (let i = 10; i; i--) {
    console.log(i)
}
/* And the output will be 10
    9

(continues on next page)

## Page 277

(continued from previous page)


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>7</td><td style='text-align: center; word-wrap: break-word;'>8</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>8</td><td style='text-align: center; word-wrap: break-word;'>7</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>9</td><td style='text-align: center; word-wrap: break-word;'>6</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>10</td><td style='text-align: center; word-wrap: break-word;'>5</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>11</td><td style='text-align: center; word-wrap: break-word;'>4</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>12</td><td style='text-align: center; word-wrap: break-word;'>3</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>13</td><td style='text-align: center; word-wrap: break-word;'>2</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>14</td><td style='text-align: center; word-wrap: break-word;'>1</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>15</td><td style='text-align: center; word-wrap: break-word;'>*/</td></tr></table>

## Page 278

## Page 279

## CONCURRENCY

### 16.1 Introductory Note

Most modern hardware has multiple cores. To achieve maximum performance, the software must be capable of using more than one core in some scenarios (e.g., multimedia processing, data analysis, simulation, modelling, databases etc.).

Providing support to a number of asynchronous APIs at different levels is also crucial.

### 16.2 Concurrency Subsystem Overview

#### 16.2.1 Major Concurrency Features

ArkTS has APIs for asynchronous programming that enables tasks to be suspended and resumed later, and supports coroutines that can run in parallel (implicitly or explicitly). Since the ArkTS coroutines share memory, a developer must be aware about the possible associated issues, and use appropriate functionality to guarantee thread safety.

ArkTS enables both asynchronous programming and parallel-run coroutines, and provides machinery for trustworthy concurrent programs by providing the following:

1. Asynchronous features async / await / Promise;

2. Coroutines (experimental) in Standard Library;

3. Structured concurrency in Standard Library (TaskPool API);

4. Synchronization primitives and “thread”-safe containers in Standard Library.

## Page 280

### 16.3 Asynchronous API

#### 16.3.1 Async Functions

Async functions are coroutines (i.e., functions which can be suspended and resumed later) that can be called as regular functions. A compile-time error occurs if:

• Async function is called in a static initializer, including module scope;

• Async function has an abstract or a native modifier;

• Return type of an async function is other than Promise<T>.

Type Promise<T> is a library type discussed in detail in the ArkTS Concurrency Specification.

The returning values of both type Promise<T> and type T are allowed inside the async function body (see Return Type Inference).

Using return statement without an expression is allowed if the return type is  $ Promise<void> $. No-argument return statement can be added implicitly as the last statement of the function body if there is no explicit return statement in a function with the return  $ Promise<void> $.

Note. Using type Promise<void> is not recommended as this type is supported for the sake of backward TypeScript compatibility only.

#### 16.3.2 Async Lambdas

A lambda with the modifier async (see Lambda Expressions) is an implicit coroutine that can be called as a regular lambda.

Async lambdas follow the same rules as Async Functions.

#### 16.3.3 Async Methods

A class method with the modifier async (see Method Declarations) is an implicit coroutine that can be called as a regular method.

Async methods follow the same rules as Async Functions.

#### 16.3.4 await

The syntax of await expression is presented below:

awaitExpression:
    'await' expression
;

## Page 281

The expression is a subtype of Promise. If expression is  $ Promise<T> $, then type of awaitExpression is  $ Awaited<T> $.

await is used to wait for Promise

If Promise not resolved, then the current coroutine is suspended until it is resolved.

If Promise is rejected, then the reason of the rejection is thrown.

Using await outside of async functions is forbidden.

#### 16.3.5 Promise

The Promise object is introduced to support asynchronous API. It is the object that represents a proxy for the result of an asynchronous operation. The semantics of Promise is similar to the semantics of Promise in JavaScript/TypeScript if it is used in the context of a single coroutine.

Promise object represents the values returned by the call of an async function. Promise object can be used without any qualification as it is defined in the Standard Library.

The Promise lifetime is not limited to the lifetime of the root coroutine as it is created.

Promise is not in general designed to be used concurrently and simultaneously from multiple coroutines. However, it is safe to do the following:

• Pass Promise from one coroutine to another, and avoid using it again in the original coroutine.

• Pass Promise from one coroutine to another, use it in both coroutines, and call then only in one coroutine.

- Pass Promise from one coroutine to another, use it in both coroutines, and call them in both coroutines. The user is to provide custom synchronization to guarantee that there is not called simultaneously for this Promise.

The methods are used as follows:

• then takes two arguments. The first argument is the callback used if the promise is fulfilled. The second argument is used if it is rejected, and returns Promise<U>.

• If then is called from the same parent coroutine several times, then the order of then is the same if called in JavaScript/TypeScript. The callback is called on the coroutine when then called, and if Promise is passed from one coroutine to another and called then in both, then they are called in different coroutines (possibly concurrently). The developer must consider a possible data race, and take appropriate care.

Promise<U>::then<U, E = never>(onFulfilled: ((value: T) => U|PromiseLike<U>
    ←throws)|undefined, onRejected: ((error: Any) => E|PromiseLike<E> throws)|undefined):
    ←Promise<Awaited<U|E>>

• catch takes one argument (the callback called after promise is rejected) and returns Promise<Awaited<U|T>>

Promise<U>::catch<U = never>(onRejected?: (error: Any) => U|PromiseLike<U> throws):_
    →Promise<Awaited<T | U>>

• finally takes one argument (the callback called after promise is either fulfilled or rejected) and returns Promise<Awaited<T>>.

finally(onFinally?: () => void throws): Promise<Awaited<T>>

## Page 282

#### 16.3.6 Unhandled Rejected Promises

In case of an unhandled rejection of Promise, either the custom handler provided for Promise rejection is called, or the default Promise rejection handler is called upon the entire program completion.

### 16.4 Coroutines (Experimental)

A function or lambda can be a coroutine. ArkTS supports basic coroutines and structured coroutines. Basic coroutines are used to create and launch a coroutine. The result is then to be awaited. Details are provided in Standard Library.

## Page 283

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

## Page 284

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Type&#x27;s Set of Values</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>char (32-bits)</td><td style='text-align: center; word-wrap: break-word;'>Symbols with codes from U+0000 to U+10FFFF (maximum valid Unicode code point) inclusive</td></tr></table>

Predefined constructors, methods, and constants for char type are parts of the ArkTS Standard Library.

#### 17.1.1 Character Literals

Character literal represents the following:

• Value consisting of a single character; or

- Single escape sequence preceded by the characters single quote (U+0027) and ‘c’ (U+0063), and followed by a single quote U+0027).

The syntax of character literal is represented below:

CharLiteral:
    'c\' SingleQuoteCharacter '\\'
;

SingleQuoteCharacter:
~[\\\\r\n]
| '\\' EscapeSequence
;

The examples are presented below:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;a&#x27;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;\n&#x27;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;\x7F&#x27;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>4</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;\u0000&#x27;</td></tr></table>

<div style="text-align: center;">Character literals are of type char.</div>


#### 17.1.2 Character Equality Operators

Value equality is used for operands of type char.

If both operands represent the same Unicode code point, then the result of ‘==’ or ‘===’ is true. Otherwise, the result is false.

## Page 285

### 17.2 Fixed-Size Array Types

Fixed-size array type, written as FixedArray<T>, is the built-in type characterized by the following:

• Any instance of array type contains elements. The number of elements is known as array length, and can be accessed by using the length property.

• Array length is a non-negative integer number.

• Array length is set once at runtime and cannot be changed after that.

• Array element is accessed by its index. Index is an integer number starting from 0 to array length minus 1.

• Accessing an element by its index is a constant-time operation.

• If passed to a non-ArkTS environment, an array is represented as a contiguous memory location.

• Type of each array element is assignable to the element’s type specified in the array declaration (see Assignability).

Fixed-size arrays differ from resizable arrays as follows:

• Fixed-size array length is set once to achieve better performance;

• Fixed-size arrays have no methods defined;

• Fixed-size arrays have several constructors (see Fixed-Size Array Creation);

• Fixed-size arrays are not compatible with resizable arrays.

Incompatibility between a resizable array and a fixed-size array is represented by the example below:

function foo(a: FixedArray<number>, b: Array<number>) {
    a = b // compile-time error
    b = a // compile-time error
}

#### 17.2.1 Fixed-Size Array Creation

Fixed-size array can be created by using Array Literal or constructors defined for type FixedArray<T>, where T must be a concrete type. A compile time error occurs if T is a type parameter.

Using an array literal to create an array is represented in the example below:

let a : FixedArray<number> = [1, 2, 3]
/* create array with 3 elements of type number */
a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
let y = a[2] /* get the last element of array 'a' */
let count = a.length // get the number of array elements
y = a[3] // Will lead to runtime error - attempt to access non-existing array element

Several constructors can be called to create a FixedArray<T> instance as follows:

• constructor(len: int), if type T has either a default value (see Default Values for Types) or a constructor that can be called with no argument provided:

## Page 286

// type "number" has a default value:
let a = new FixedArray<number>(3) // creates array [0.0, 0.0, 0.0]

class C {
    constructor (n?: number) {}
}
let b = new FixedArray<C>(2) // creates array [new C(), new C()]

• constructor(len: int, elem: T) for any T. The constructor creates an array instance filled with a single value elem:

let a = new FixedArray<string>(3, "a") // creates array ["a", "a", "a"]

• constructor(len: int, elems: (inx: int) => T) for any T. The constructor creates an array instance where each i element is evaluated as a result of the elems call with argument i:

let a = new FixedArray<int>(3, (inx: int) => 3 - inx)
// creates array [3, 2, 1]

New Expressions cannot use generic parameters to create a Fixed-size array. Attempting to do so causes a compile-time error as in the following example:

function f<T>(): T {
    let ret = new FixedArray<T>(3) // compile-time error, generic parameter T
    return ret
}

### 17.3 Resizable Array Creation Expressions

Array creation expression creates new objects that are instances of resizable arrays (see Resizable Array Types). An array instance can be created alternatively by using Array Literal.

The syntax of array creation expression is presented below:

newArrayInstance:
    'new' arrayElementType dimensionExpression+ (arrayElement)?
;

arrayElementType:
    typeReference
| '(' type ')'
;

dimensionExpression:

(continues on next page)

## Page 287

(continued from previous page)

[' expression '']
;
arrayElement:
(' expression '')
;

let x = new number[2][2] // create 2x2 matrix

Array creation expression creates an object that is a new array with the elements of the type specified by arrayElementType.

The type of each dimension expression must be assignable (see Assignability) to an int type. Otherwise, a compile-time error occurs.

A compile-time error occurs if any dimension expression is a constant expression that is evaluated to a negative integer value at compile time.

If the type of any dimension expression is number or other floating-point type, and its fractional part is other than '0', then errors occur as follows:

• Compile-time error, if the situation is identified during compilation; and

• Runtime error, if the situation is identified during program execution.

If arrayElement is provided, then the type of the expression can be as follows:

• Type of array element denoted by arrayElementType, or

• Lambda function with the return type equal to the type of array element denoted by arrayElementType and the parameters of type int, and the number of parameters equal to the number of array dimensions.

Otherwise, a compile-time error occurs.

let x = new number[-3] // compile-time error

let y = new number[3.141592653589] // compile-time error

foo (3.141592653589)
function foo (size: number) {
    let y = new number[size] // runtime error
}

A compile-time error occurs if arrayElementType refers to a class that does not contain an accessible (see Accessible) parameterless constructor, or constructor with all parameters of the second form of optional parameters (see Optional Parameters), or if type has no default value:

class C{
    constructor (n: number) {}
}
let x = new C[3] // compile-time error: no parameterless constructor

class A {
    constructor (p1?: number, p2?: string) {}
}
let y = new A[2] // OK, as all 3 elements of array will be filled with
// new A() objects

## Page 288

A compile-time error occurs if arrayElementType is a type parameter:

class A<T> {
    foo() {
        new T[2] // compile-time error: cannot create an array of type parameter_
    }
}

#### 17.3.1 Runtime Evaluation of Array Creation Expressions

The evaluation of an array creation expression at runtime is performed as follows:

1. The dimension expressions are evaluated. The evaluation is performed left-to-right. If any expression evaluation completes abruptly, then the expressions to the right of it are not evaluated.

2. The values of dimension expressions are checked. If the value of any dimension expression is less than zero, then NegativeArraySizeError is thrown.

3. Space for the new array is allocated. If the available space is not sufficient to allocate the array, then OutOfMemoryError is thrown, and the evaluation of the array creation expression completes abruptly.

4. When an array with one dimension is created, each element of that array is initialized to its default value if type default value is defined (Default Values for Types). If the default value for an element type is not defined, but the element type is a class type, then its parameterless constructor is used to create the value of each element.

5. When array with several dimensions is created, the array creation effectively executes a set of nested loops of depth n-1.

### 17.4 Enumerations Experimental

Several experimental features described below are available for enumerations.

#### 17.4.1 Enumeration Methods

Several static methods are available to handle each enumeration type as follows:

• Method static values() returns an array of enumeration constants in the order of declaration.

• Method static getValueOf(name: string) returns an enumeration constant with the given name, or throws an error if no constant with such name exists.

• Method static fromValue(value: T), where T is the base type of the enumeration, returns an enumeration constant with a given value, or throws an error if no constant has such a value.

## Page 289

enum Color { Red, Green, Blue = 5 }
let colors = Color.values()
    //colors[0] is the same as Color.Red

let red = Color.getValueOf("Red")

Color.fromValue(5) // ok, returns Color.Blue
Color.fromValue(6) // throws runtime error

Additional methods for instances of an enumeration type are as follows:

• Method valueOf() returns a numeric or string value of an enumeration constant depending on the type of the enumeration constant.

• Method getName() returns the name of an enumeration constant.

enum Color { Red, Green = 10, Blue }

let c: Color = Color.Green

console.log(c.valueOf()) // prints 10

console.log(c.getName()) // prints Green

Note. Methods c.toString() and c.valueOf().toString() return the same value.

### 17.5 Indexable Types

If a class or an interface declares one or two functions with names $_get and $_set, and signatures (index: Type1): Type2 and (index: Type1, value: Type2) respectively, then an indexing expression (see Indexing Expressions) can be applied to variables of such types:

class SomeClass {
    $_get (index: number): SomeClass { return this }
    $_set (index: number, value: SomeClass) { }
}
let x = new SomeClass
x = x[1] // This notation implies a call: x = x.$_get (1)
x[1] = x // This notation implies a call: x.$_set (1, x)

If only one function is present, then only the appropriate form of indexing expression (see Indexing Expressions) is available:

class ClassWithGet {
    $_get (index: number): ClassWithGet { return this }
}
let getClass = new ClassWithGet
getClass = getClass[0]
getClass[0] = getClass // Error - no $_set function available

class ClassWithSet {
    $_set (index: number, value: ClassWithSet) {}
}

(continues on next page)

## Page 290

(continued from previous page)

let setClass = new ClassWithSet
setClass = setClass[0] // Error - no $_get function available
setClass[0] = setClass

Type string can be used as a type of the index parameter:

class SomeClass {
    $_get (index: string): SomeClass { return this }
    $_set (index: string, value: SomeClass) {}
}
let x = new SomeClass
x = x["index string"]
// This notation implies a call: x = x.$_get ("index string")
x["index string"] = x
// This notation implies a call: x.$_set ("index string", x)

Functions $_get and $_set are ordinary functions with compiler-known signatures. The functions can be used like any other function. The functions can be abstract, or defined in an interface and implemented later. The functions can be overridden and provide a dynamic dispatch for the indexing expression evaluation (see Indexing Expressions). The functions can be used in generic classes and interfaces for better flexibility. A compile-time error occurs if these functions are marked as async.

interface ReadonlyIndexable<K, V> {
    $_get (index: K): V
}

interface Indexable<K, V> extends ReadonlyIndexable<K, V> {
    $_set (index: K, value: V)
}

class IndexableByNumber<V> implements Indexable<number, V> {
    private data: V[] = []
    $_get (index: number): V { return this.data [index] }
    $_set (index: number, value: V) { this.data[index] = value }
}

class IndexableByString<V> implements Indexable<string, V> {
    private data = new Map<string, V>
    $_get (index: string): V { return this.data [index] }
    $_set (index: string, value: V) { this.data[index] = value }
}

class BadClass extends IndexableByNumber<boolean> {
    override $_set (index: number, value: boolean) { index / 0 }
}

let x: IndexableByNumber<boolean> = new BadClass
x[42] = true // This will be dispatched at runtime to the overridden
// version of the $_set method
x.$_get (15) // $_get and $_set can be called as ordinary
// methods

## Page 291

### 17.6 Iterable Types

A class or an interface is iterable if it implements the interface Interactive defined in the Standard Library, and thus has an accessible parameterless method with the name $_iterator and a return type that is a subtype (see Subtyping) of type Iterator as defined in the Standard Library. It guarantees that an object returned by the $_iterator method is of the type which implements Iterator, and thus allows traversing an object of the iterable type.

A union of iterable types is also iterable. It means that instances of such types can be used in for-of statements (see for-of Statements).

An iterable class C is represented in the example below:

class C implements Interactive<string> {
    data: string[] = ['a', 'b', 'c']
    $_iterator() { // Return type is inferred from the method body
        return new CIterator(this)
    }
}

class CIterator implements Interface<string> {
    index = 0
    base: C
    constructor (base: C) {
        this.base = base
    }
    next(): Interface<string> {
        return {
            done: this.index >= this.base.data.length,
            value: this.index >= this.base.data.length ? undefined : this.base.data[this.index++]
        }
    }
    let c = new C()
    for (let x of c) {
        console.log(x)
    }
}

In the example above, class C method $_iterator returns CIterator<string> that implements Iterator<string>. If executed, this code prints out the following:

"a"
"b"
"c"

The method $_iterator is an ordinary method with a compiler-known signature. This method can be used like any other method. It can be abstract or defined in an interface to be implemented later. A compile-time error occurs if this method is marked as async.

Note. To support the code compatible with TypeScript, the name of the method $_iterator can be written as [Symbol.iterator]. In this case, the class iterable looks as follows:

## Page 292

class C {
    data: string[] = ['a', 'b', 'c');
    [Symbol.iterator]() {
        return new CIterator(this)
    }
}

The use of the name [Symbol.iterator] is considered deprecated. It can be removed in the future versions of the language.

### 17.7 Callable Types

A type is callable if the name of the type can be used in a call expression. A call expression that uses the name of a type is called a type call expression. Only class type can be callable. To make a type callable, a static method with the name $_invoke or $_instantiate must be defined or inherited:

class C {
    static $_invoke() { console.log("invoked") }
}
C() // prints: invoked
C.$_invoke() // also prints: invoked

In the above example, C() is a type call expression. It is the short form of the normal method call C.$_invoke(). Using an explicit call is always valid for the methods $_invoke and $_instantiate.

Note. Only a constructor—not the methods $_invoke or $_instantiate—is called in a new expression:

class C {
    static $_invoke() { console.log("invoked") }
    constructor() { console.log("constructed") }
}
let x = new C() // constructor is called

The methods $_invoke and $_instantiate are similar but have differences as discussed below.

A compile-time error occurs if a callable type contains both methods invoke and $_instantiate.

#### 17.7.1 Callable Types with $_invoke Method

The static method $_invoke can have an arbitrary signature. The method can be used in a type call expression in either case above. If the signature has parameters, then the call must contain corresponding arguments.

class Add {
    static $_invoke(a: number, b: number): number {
        return a + b
    }
}

(continues on next page)

## Page 293

(continued from previous page)

}
console.log(Add(2, 2)) // prints: 4

That a type contains the instance method $_invoke does not make the type callable.

#### 17.7.2 Callable Types with $_instantiate Method

The static method $_instantiate can have an arbitrary signature by itself. If it is to be used in a type call expression, then its first parameter must be a factory (i.e., it must be a parameterless function type returning some class type). The method can have or not have other parameters, and those parameters can be arbitrary.

In a type call expression, the argument corresponding to the factory parameter is passed implicitly:

class C {
    static $_instantiate(factory: () => C): C {
        return factory()
    }
}
let x = C() // factory is passed implicitly
// Explicit call of：‘_instantiate' requires explicit 'factory':
let y = C.$_instantiate(() => { return new C() })

If the method $_instantiate has additional parameters, then the call must contain corresponding arguments:

class C {
    name = ""
    static $_instantiate(factory: () => C, name: string): C {
        let x = factory()
        x.name = name
        return x
    }
}
let x = C("Bob") // factory is passed implicitly

A compile-time error occurs in a type call expression with type T, if:

• T has neither method $_invoke nor method $_instantiate; or

• T has the method $_instantiate but its first parameter is not a factory.

class C {
    static $_instantiate(factory: string): C {
        return factory()
    }
}
let x = C() // compile-time error, wrong $_instantiate' 1st parameter

That a type contains the instance method $_instantiate does not make the type callable.

## Page 294

#### 17.8.1 For-of Explicit Type Annotation

An explicit type annotation is allowed for a ForVariable (see for-of Statements):

// explicit type is used for a new variable,
let x: number[] = [1, 2, 3]
for (let n: number of x) {
    console.log(n)
}

Type of elements in a for-of expression must be assignable (see Assignability) to the type of the variable. Otherwise, a compile-time error occurs.

### 17.9 Overload Declarations

ArkTS supports both the conventional overloading and an innovative form of managed overloading that allows a developer to fully control the order of selecting a specific entity to call from several overloaded entities Overloading.

The actual entity to be called is determined at compile time. Thus, overloading is related to the compile-time polymorphism by name. The semantic details are discussed in Overloading.

An overload declaration is used in managed overloading to define a set and an order of the overloaded entities (functions, methods, or constructors).

An overload declaration can be used for:

• Functions (see Function Declarations), including functions in namespaces;

• Class or interface methods (see Method Declarations and Interface Method Declarations); and

• Ambient Declarations.

An overload declaration starts with the keyword overload and declares an overload alias for a set of explicitly listed entities as follows:

function max2(a: number, b: number): number {
    return a > b ? a : b
}
function maxN(...a: number[]): number {
    // return max element
}
// declare 'max' as an ordered set of functions max2 and maxN
overload max { max2, maxN }

## Page 295

(continued from previous page)

max(1, 2) // max2 is called
max(3, 2, 4) // maxN is called
max("a", "b") // compile-time error, no function to call

maxN(1, 2) // maxN is explicitly called

The semantics of an entity included into an overload set does not change. Such entities follow the ordinary accessibility rules, and can be used separately from an overload alias, e.g., called explicitly as follows:

maxN(1, 2) // maxN is explicitly called
max2(2, 3) // max2 is explicitly called

When calling an overload alias, entities from an overload set are checked in the listed order, and the first entity with an appropriate signature is called (see Overload Resolution for detail). A compile-time error occurs if no entity with an appropriate signature is available:

1  $ \begin{cases} \text{max}(1) & // \text{max}N \text{ is called} \\ \text{max}(1, 2) & // \text{max}2 \text{ is called, as is the first in order} \end{cases} $
2  $ \begin{cases} \text{max}(a", b") & // \text{compile-time error, no function to call} \end{cases} $

It means that exactly one entity is selected for a call at the call site. Otherwise, a compile-time error occurs.

An overloaded entity in an overload declaration can be generic (see Generics).

If during Overload Resolution type arguments are provided explicitly in a call of an overload alias (see Explicit Generic Instantiations), then consideration is given only to the entities that have an equal number of type parameters and type arguments.

If type arguments are not provided explicitly (see Implicit Generic Instantiations), then consideration is given to all entities as represented in the example below:

function foo1(s: string) {}
function foo2<T>(x: T) {}

overload foo { foo1, foo2 }

foo("aa") // foo1 is called
foo(1) // foo2 is called, implicit generic instantiation
foo<string>("aa") // foo2 is called

An entity can be listed in several overload declarations:

function max2i(a: int, b: int): int {
    return a > b ? a : b
}
function maxNi(...a: int[]): int {
    // return max element
}
function maxN(...a: number[]): number {
    // return max element
}

overload maxi { max2i, maxNi }
overload max { max2i, maxNi, maxN }

## Page 296

#### 17.9.1 Function Overload Declarations

Function overload declaration allows declaring an overload alias for a set of functions (see Function Declarations).

The syntax is presented below:

overloadFunctionDeclaration:
'overload' identifier '{' qualifiedName (',' qualifiedName)* ','? '}'
;

A compile-time error occurs, if a qualified name does not refer to an accessible function.

A compile-time error occurs, if an overload alias is exported but an overloaded function is not:

export function foo1(p: string) {}
function foo2(p: number) {}
export overload foo { foo1, foo2 } // compile-time error, 'foo2' is not exported
overload bar { foo1, foo2 } // ok, as 'bar' is not exported

All overloaded functions must be in the same module or namespace scope (see Scopes). Otherwise, a compile-time error occurs. The erroneous overload declarations are represented in the example below:

import {foo1} from "something"

function foo2() {}

overload foo {foo1, foo2} // compile-time error

namespace N {
    export function fooN() {}
    namespace M {
        export function fooM() {}
    }
    overload goo {M.fooM, fooN} // compile-time error
}

overload bar {foo2, N.fooN} // compile-time error

#### 17.9.2 Class Method Overload Declarations

Method overload declaration allows declaring an overload alias as a class member (see Class Members) for a set of static or instance methods (see Method Declarations). The syntax is presented below:

overloadMethodDeclaration:
  overloadMethodModifier*
  'overload' identifier '{' identifier (',' identifier)* ','? '}'
;

overloadMethodModifier: 'static' | 'async';

Using method overload declaration and calling an overload alias are represented in the example below:

## Page 297

class Processor {
    overload process { processNumber, processString }
    processNumber(n: number) {/*body*/}
    processString(s: string) {/*body*/}
}

let c = new C()
c.process(42) // calls processNumber
c.process("aa") // calls processString

Static overload alias is represented in the example below:

class C {
    static one(n: number) {/*body*/}
    static two(s: string) {/*body*/}
    static overload foo { one, two }
}

A compile-time error occurs if:

• Method modifier is used more than once in an method overload declaration;

• Overload alias is:

• Identifier in the overloaded method list does not refer to an accessible method (either declared or inherited) of the current class;

– Static but the overloaded method is not;

– Non-static but the overloaded method is not;

– Marked async but the overloaded method is not; or

– Not async but the overloaded method is.

Overload alias and overloaded methods can have different access modifiers. A compile-time error occurs if the overload alias is:

• public but at least one overloaded method is not public;

• protected but at least one overloaded method is private.

Valid and invalid overload declarations are represented in the example below:

class C {
    private foo1(x: number) {/*body*/}
    protected foo2(x: string) {/*body*/}
    public foo3(x: boolean) {/*body*/}
    foo4() {/*body*/} // implicitly public

    public overload foo { foo3, foo4 } // ok
    protected overload bar { foo2, foo3 } // ok
    private overload goo { foo1, foo2, foo3 } // ok

    public overload err1 {foo2, foo3} // compile-time error, foo2 is not public
    protected overload err2 {foo2, foo1} // compile-time error, foo1 is private
}

Some or all overloaded functions can be native as follows:

## Page 298

class C {
    native foo1(x: number)
    foo2(x: string) {/*body*/}
    overload foo { foo1, foo2 }
}

An overload alias is used like an ordinary class method except that it is replaced in a call at compile time for one of overloaded methods that use the type of object reference. The overload declaration in subtypes is represented in the example below:

In addition, overriding an overload declaration in a subclass can include new methods and change the order of all methods in the overload declaration.

If a superclass has an overload declaration, then this declaration can be overridden in a subclass. If a subclass does not override an overload declaration, then the declaration from the superclass is inherited.

If a subclass overrides an overload declaration, then this declaration must list all methods of the overload declaration in a superclass. Otherwise, a compile-time error occurs.

class Base {
    overload process { processNumber, processString }
    processNumber(n: number) {/*body*/}
    processString(s: string) {/*body*/}
}

class D1 extends Base {
    // method is overridden
    override processNumber(n: number) {/*body*/}
    // overload declaration is inherited
}

class D2 extends Base {
    // method is added:
    processInt(n: int) {/*body*/}
    // new order for overloaded methods is specified:
    overload process { processInt, processNumber, processString }
}

new D1().process(1) // calls processNumber from D1

new D2().process(1) // calls processInt from D2 (as it is listed earlier)
new D2().process(1.0) // calls processNumber from Base (first appropriate)

Methods with special names (see Indexable Types, Iterable Types, and Callable Types) can be overloaded like ordinary methods:

class C {
    getByNumber(n: number): string {...}
    getByString(s: string): string {...}
    overload $_get { getByNumber, getByString }
}

let c = new C()

(continues on next page)

## Page 299

(continued from previous page)

c[1] // getByNumber is used
c["abc"] // getByString is used

If a class implements some interfaces with overload declarations for the same alias, then a new overload declaration must include all overloaded methods. Otherwise, a compile-time error occurs.

interface I1 {
    overload foo {f1, f2}
    // f1 and f2 are declared in I1
}

interface I2 {
    overload foo {f3, f4}
    // f3 and f4 are declared in I2
}

class C implements I1, I2 {
    // compile-time error as no new overload is defined
}

class D implements I1, I2 {
    overload foo {f2, f3, f1, f4} // OK, as new overload is defined
}

class E implements I1, I2 {
    overload foo {f2, f4} // compile-time error as not all methods are used
}

const i1: I1 = new D

i1.foo(<arguments>) // call is valid if arguments fit first signature of {f1, f2} set

const i2: I2 = new D

i2.foo(<arguments>) // call is valid if arguments fit first signature of {f3, f4} set

const d: D = new D

d.foo(<arguments>) // call is valid if arguments fit first signature of {f2, f3, f1, f4}
→ set

#### 17.9.3 Interface Method Overload Declarations

Interface method overload declaration allows declaring an overload alias as an interface member (see Interface Members) for a set of interface methods (see Interface Method Declarations).

The syntax is presented below:

overloadInterfaceMethodDeclaration:
'overload' identifier '{' identifier (',' identifier)* ','? '}';

The use of a method overload declaration is represented in the example below:

interface I {
    foo(): void

(continues on next page)

## Page 300

(continued from previous page)

bar(n?: string): void
  overload goo { foo, bar }
}

function example(i: I) {
  i.goo()     // calls i.foo()
  i.goo("hello")  // calls i.bar("hello")
  i.bar()       // explicit call: i.bar(undefined)
}

An overload alias is used like an ordinary interface method, except that in a call it is replaced at compile time by one of overloaded methods by using the type of object reference.

A class that implements an interface with an overload alias usually implements all interface methods, except those having a default body (see Default Interface Method Declarations):

// Using interface overload declaration
class C implements I {
    foo(): void {/*body*/}
    bar(n?: string): void {/*body*/}
}

let c = new C()
c.goo() // calls c.foo()

An interface overload alias can be overridden in a class. In this case, the overload declaration in the class must contain all methods overloaded in the interface. Otherwise, a compile-time error occurs.

class D implements I {
    foo(): void {/*body*/}
    bar(n?: string): void {/*body*/}
    overload goo(bar, foo) // order is changes
}

let d = new D()
d.goo() // d.bar(undefined) is used, as it is the first appropriate method

An overload alias defined in a superinterface can be overridden in a subinterface. In this case, the overload declaration of the subinterface must contain all methods overloaded in superinterface. Otherwise, a compile-time error occurs.

The overload alias defined in superinterfaces must be overridden in a subinterface if several overload declarations for the same alias are inherited into the interface, otherwise a compile-time error occurs.

interface I1 {
    overload foo {f1, f2}
    // f1 and f2 are declared in I1
}

interface I2 {
    overload foo {f3, f4}
    // f3 and f4 are declared in I2
}

interface I3 extends I1, I2 {
    // compile-time error as no new overload for 'foo' is defined
}

(continues on next page)

## Page 301

(continued from previous page)

interface I4 extends I1, I2 {
    overload foo { f4, f1, f3, f2 } // OK, as new overload is defined
}
interface I5 extends I1, I2 {
    overload foo { f1, f3 } // compile-time error as not all methods are included
}

#### 17.9.4 Constructor Overload Declarations

Constructor overload declaration allows declaring an overload alias and setting an order of constructors for a call in a new expression.

The syntax is presented below:

overloadConstructorDeclaration:
'overload' 'constructor'、「'identifier (',' 'identifier)*', '?' '};

This feature can be used if there are more than one constructors declared in the class, and maximum one of them is anonymous (see Constructor Names).

Only a single constructor overload declaration is allowed in a class. Otherwise, a compile-time error occurs.

Overload alias for constructors is used the same way as anonymous constructor (see New Expressions).

The use of a constructor overload declaration is represented in the example below:

class BigFloat {
    constructor fromNumber(n: number) {/*body1*/}
    constructor fromString(s: string) {/*body2*/}

    overload constructor { fromNumber, fromString }
}

new BigFloat(1) // fromNumber is used
new BigFloat("3.14") // fromString is used

If a class has an anonymous constructor it is implicitly placed at first position in a list of overloaded constructors:

class C {
    constructor () { /*body*/ }
    constructor fromString(s?: string) { /*body*/ }

    overload constructor { fromString }
}

new C() // anonymous constructor is used
new C("abc") // fromString is used
new C.fromString("aa") // fromString is explicitly used

## Page 302

#### 17.9.5 Overload Alias Name Same As Function Name

A name of a top-level overload declaration can be the same as the name of an overloaded function. This situation is represented in the following example:

function foo(n: number): number {/*body1*/}
function fooString(s: number): string {/*body2*/}

overload foo {foo, fooString}

foo(1)    // overload alias is used to call 'foo'
foo("aa") // overload alias is used to call 'fooString'

Using an overload alias causes no ambiguity for it is considered at the call site only, i.e., an overload alias is not considered in the following situations:

• List of the overloaded entities (see Function Overload Declarations);

• Function Reference.

function foo(n: number): number {/*body1*/}
function fooString(s: number): string {/*body2*/}
overload foo {foo, fooString}

let func1 = foo // function 'foo' is used, not overload alias

If the name of an overload alias is the same as the name of a function that is not listed as an overloaded function, then a compile-time error occurs as follows:

function foo(n: number) {/*body1*/}
function fooString(s: number) {/*body2*/}
function fooBoolean(b: boolean) {/*body3*/}

overload foo { // compile-time error
    fooBoolean, fooString
}

#### 17.9.6 Overload Alias Name Same As Method Name

A name of a class or interface overload declaration can be the same as the name of an overloaded method. As one example, a method defined in a superclass can be used as one of overloaded methods in a same-name subclass overload declaration. This important case is represented by the following example:

class C {
    foo(n: number): number {/*body*/}
}
class D implements C {
    fooString(s: number): string {/*body*/}
}

(continues on next page)

## Page 303

6
7
8
9
0
10
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
967
968
969
970
971
972
973
974
975
976
977
978
979
980
981
982
983
984
985
986
987
988
989
990
991
992
993
994
995
996
997
998
999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
10

If names of a method and of an overload alias are the same, then the method can be overridden as usual:

class C {
    foo(n: number): number {/*body*/}
}

class D implements C {
    foo(n: number): number {/*body*/} // method is overridden
    fooString(s: number): string {/*body*/}

    overload foo { foo, fooString }
}

This feature is also valid in interfaces, or in an interface and a class that implements the interface:

interface I {
    foo(n: number): number {/*body*/}
}

interface ] extends I {
    fooString(s: number): string
    overload foo { foo, fooString }
}

class K implements I {
    foo(n: number): number {/*body*/}
    fooString(s: number): string {/*body*/}

    overload foo { foo, fooString }
}

Using an overload alias causes no ambiguity for it is considered at the call site only. An overload alias is not considered in the following situations:

• Overriding;

• List of the overloaded entities (see Class Method Overload Declarations and Interface Method Overload Declarations);

• Method Reference.

## Page 304

class C {
    foo(n: number): number {/*body*/}
}

class D implements C {
    fooString(s: number): string {/*body*/}
    overload foo { foo, fooString }
}

let d = new D()
let c: C = d

let func1 = c.foo // method 'foo' is used
let func2 = d.foo // method 'foo' is used, not overload alias

A compile-time error occurs if the name of an overload alias is the same as the name of a method (with the same static or non-static modifier) that is not listed as an overloaded method as follows:

class C {
    foo(n: number) {/*body*/}
    fooString(s: number) {/*body*/}
    fooBoolean(b: boolean) {/*body*/}

    overload foo { // compile-time error
        fooBoolean, fooString
    }
}

### 17.10 Native Functions and Methods

#### 17.10.1 Native Functions

Native function is a function marked with the keyword native (see Function Declarations).

Native function implemented in a platform-dependent code is typically written in another programming language (e.g., C). A compile-time error occurs if a native function has a body.
