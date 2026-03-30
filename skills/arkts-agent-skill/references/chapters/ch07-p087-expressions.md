# Chapter 7: Expressions

Page range: 87-196

## Page 87

(continued from previous page)

function foo <T extends SuperType> (p: Awaited<T>) {}
function bar <T extends SubType> (p: Awaited<T>) {
    foo (p) // is a valid call as Awaited<T extends SubType> <: Awaited<T extends_SuperType>
}

#### 5.3.2 NonNullable Utility Type

Type NonNullable<T> constructs a type by excluding null and undefined types. If type T contains neither null nor undefined, then NonNullable<T> leaves T intact. The use of type NonNullable<T> is represented in the example below:

type X = Object | null | undefined
type Y = NonNullable<X> // type of 'Y' is Object

class A <T> {
    field: NonNullable<T> // This is a non-nullable version of the type parameter
    constructor (field: NonNullable<T>) {
        this.field = field
    }
}

const a = new A<Object|null> (new Object)
a.field // type of field is Object

#### 5.3.3 Partial Utility Type

Type Partial<T> constructs a type with all properties of T set to optional. T must be a class or an interface type. Otherwise, a compile-time error occurs. No method (not even any getter or setter) of T is a part of the Partial<T> type. The use is represented in the example below:

interface Issue {
    title: string
    description: string
}

function process(issue: Partial<Issue>) {
    if (issue.title != undefined) {
        /* process title */
    }
}

process({title: "aa"}) // description is undefined

## Page 88

In the example above, type Partial<Issue> is transformed to a distinct but analogous type as follows:

interface /*some name*/ {
    title?: string
    description?: string
}

Type T is not assignable to Partial<T> (see Assignability), and variables of Partial<T> are to be initialized with valid object literals.

Note. If class T has a user-defined getter, setter, or both, then none of those is called when object literal is used with Partial<T> variables. Object literal has its own built-in getters and setters to modify its variables. It is represented in the example below:

interface I {
    property: number
}

class A implements I {
    _property: number
    set property(property: number) {
        console.log("Setter called")
        this._property = property
    }
    get property(): number {
        console.log("Getter called");
        return this._property
    }
}

function foo (partial: Partial<A>) {
    partial.property = 42 // setter to be called
    console.log(partial.property) // getter to be called
}

foo ({property: 1}) // No getter or setter from class A is called
// 42 is printed as object literal has its own setter and getter

#### 5.3.4 Required Utility Type

Type Required<T> is opposite to Partial<T>, and constructs a type with all properties of T set to required (i.e., not optional). T must be a class or an interface type, otherwise a compile-time error occurs. No method (not even any getter or setter) of T is part of the Required<T> type. Its usage is represented in the example below:

interface Issue {
    title?: string
    description?: string
}
let c: Required<Issue> = { // CTE: 'description' should be defined

(continues on next page)

## Page 89

(continued from previous page)

title: "aa"
}

In the example above, type Required<Issue> is transformed to a distinct but analogous type as follows:

interface /*some name*/ {
    title: string
    description: string
}

Type T is not assignable (see Assignability) to Required<T>, and variables of Required<T> are to be initialized with valid object literals.

#### 5.3.5 Readonly Utility Type

Type `Readonly<T>` constructs a type with all properties of T set to `readonly`. It means that the properties of the constructed value cannot be reassigned. T must be a class or an interface type, otherwise a compile-time error occurs. No method (not even any `getter` or `setter`) of T is part of the `Readonly<T>` type. Its usage is represented in the example below:

interface Issue {
    title: string
}

const myIssue: Readonly<Issue> = {
    title: "One"
};

myIssue.title = "Two" // compile-time error: readonly property

Type T is assignable (see Assignability) to Readonly<T>, and allows assignments as a consequence:

class A {
    f1: string = ""
    f2: number = 1
    f3: boolean = true
}
let x = new A
let y: Readonly<A> = x // OK

#### 5.3.6 Record Utility Type

Type Record<K, V> constructs a container that maps keys (of type K) to values of type V.

Type K is restricted to numeric types (see Numeric Types), type string, string literal types and union types constructed from these types.

## Page 90

A compile-time error occurs if any other type, or literal of any other type is used in place of this type.

Its usage is represented in the example below:

type R1 = Record<number, Object> // ok
type R2 = Record<boolean, Object> // compile-time error
type R3 = Record<"salary" | "bonus", Object> // ok
type R4 = Record<"salary" | boolean, Object> // compile-time error
type R5 = Record<"salary" | number, Object> // ok
type R6 = Record<string | number, Object> // ok

Type V has no restrictions.

A special form of object literals is supported for instances of type Record (see Object Literal of Record Type).

Access to Record<K, V> values is performed by an indexing expression like r[index], where r is an instance of type Record, and index is the expression of type K (see Record Indexing Expression for detail).

Variables of type Record<K, V> can be initialized by a valid object literal of Record type (see Object Literal of Record Type) where the literal is valid if the type of key expression is compatible with key type K, and the type of value expression is compatible with the value type V.

type Keys = 'key1' | 'key2' | 'key3'

let x: Record<Keys, number> = {
    'key1': 1,
    'key2': 2,
    'key3': 4,
}

console.log(x['key2']) // prints 2
x['key2'] = 8

console.log(x['key2']) // prints 8

In the example above, K is a union of literal types and thus the result of an indexing expression is of type V. In this case it is number.

#### 5.3.7 Utility Type Private Fields

Utility types are built on top of other types. Private fields of the initial type stay in the utility type but they are not accessible (see Accessible) and cannot be accessed in any way. It is represented in the example below:

function foo(): string { // Potentially some side effect
    return "private field value"
}

class A {
    public_field = 444
    private private_field = foo()
}

function bar (part_a: Readonly<A>) {
    console.log(part_a)
}

(continues on next page)

## Page 91

(continued from previous page)


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>12</td><td style='text-align: center; word-wrap: break-word;'>}</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>13</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>14</td><td style='text-align: center; word-wrap: break-word;'>bar (\{public_field: 777\} // OK, object literal has no field `private_field`</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>15</td><td style='text-align: center; word-wrap: break-word;'>bar (\{public_field: 777, private_field: &quot;&quot;\} // compile-time error, incorrect field name</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>16</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>17</td><td style='text-align: center; word-wrap: break-word;'>bar (new A) // OK, object of type `Readonly&lt;A&gt;` has field `private_field`</td></tr></table>

## Page 92

## Page 93

## CONTEXTS AND CONVERSIONS

This Chapter defines expression contexts and conversions that can be applied to expressions in different contexts. Contexts can be of the following kinds:

• Assignment-like Contexts:

• String Operator Contexts with string concatenation (operator ‘+’);

• Numeric Operator Contexts with all numeric operators ('+', '-', etc.).

### 6.1 Assignment-like Contexts

Assignment-like contexts include the following:

• Declaration contexts that allow setting an initial value to a variable (see Variable Declarations), a constant (see Constant Declarations), or a field (see Field Declarations) with an explicit type annotation;

• Assignment contexts that allow assigning (see Assignment) an expression value to a variable;

• Call contexts that allow assigning an argument value to a corresponding formal parameter of a function, method, constructor or lambda call (see Function Call Expression, Method Call Expression, Explicit Constructor Call, and New Expressions);

• Return contexts (see return Statements) the allow specifying a resultant value of a function, method or lambda call;

• Composite literal contexts that allow setting an expression value to an array element (see Array Literal Type Inference from Context), a class, or an interface field (see Object Literal);

The examples are presented below:

// declaration contexts:
let x: number = 1
const str: string = "done"
class C {
    f: string = "aa"
}

// assignment contexts:
x = str.length
new C().f = "bb"

## Page 94

function foo<T1, T2> (p1: T1, p2: T2) {
    let t1: T1 = p1
    let t2: T2 = p2
}

// call contexts:
function foo(s: string) {}
foo("hello")

// composite literal contexts:
let a: number[] = [str.length, 11]

In all these cases, the expression type must be assignable to the target type (see Assignability). Assignability allows using of one of Implicit Conversions. If there is no applicable conversion, then a compile-time error occurs.

### 6.2 String Operator Contexts

String context applies only to a non-string operand of the binary operator ‘+’ if the other operand is string.

String conversion for a non-string operand is evaluated as follows:

• An operand of an integer type (see Integer Types and Operations) is converted to type string with a value that represents the operand in the decimal form.

• An operand of a floating-point type (see Floating-Point Types and Operations) is converted to type string with a value that represents the operand in the decimal form without the loss of information.

• An operand of type boolean is converted to type string with the values true or false.

• An operand of enumeration type (see Enumerations) is converted to type string with the value of the corresponding enumeration constant if values of enumeration are of type string.

• The operand of a nullish type that has a nullish value is converted as follows:

- Operand null is converted to string null.

- Operand undefined is converted to string undefined.

• An operand of a reference type or an enum type with non-string values is converted by applying the method call toString().

If there is no applicable conversion, then a compile-time error occurs.

The target type in this context is always string:

1 console.log(" " + null) // prints "null"
2 console.log("value is " + 123) // prints "value is 123"
3 console.log("BigInt is " + 123n) // prints "BigInt is 123"
4 console.log(15 + " steps") // prints "15 steps"
5 let x: string | null = null
6 console.log("string is " + x) // prints "string is null"

## Page 95

### 6.3 Numeric Operator Contexts

Numeric contexts apply to the operands of an arithmetic operator. Numeric contexts use numeric types conversions (see Widening Numeric Conversions), and ensure that each argument expression can be converted to target type T while the arithmetic operation for the values of type T is being defined.

An operand of enumeration type (see Enumerations) can be used in a numeric context if enumeration base type is a numeric type. The type of this operand is assumed to be the same as the enumeration base type.

Numeric contexts take the following forms:

• Unary Expressions;

• Multiplicative Expressions;

• Additive Expressions;

• Shift Expressions;

• Relational Expressions;

• Equality Expressions;

• Bitwise and Logical Expressions;

• Conditional-And Expression;

• Conditional-Or Expression.

#### 6.3.1 Numeric Conversions for Relational and Equality Operands

Relational and equality operators (see Relational Expressions and Equality Expressions) allow the following:

• Implicit conversion, where operands are of numeric types but have different sizes (see Widening Numeric Conversions), with their specific details stated in Specifics of Numeric Operator Contexts; and

• Conversion of operands with BigInt() function, where one operand type is bigint and the other is numeric. The situation for the relational operator ‘<’ is represented in the example below:

1 let a: int = 1
2 let b: long = 0
3 let c: bigint = -1n
4
5 if (b<a) { // `a`` converted to `long` prior to comparison
6     ;
7 }
8
9 if (c<b) { // `b` converted to `bigint` prior to comparison
10     ;
11 }

## Page 96

### 6.4 Implicit Conversions

This section describes all implicit conversions that are allowed. Each conversion is allowed in a particular context (e.g., if an expression that initializes a local variable is subject to Assignment-like Contexts, then the rules of this context define what specific conversion is implicitly chosen for the expression).

#### 6.4.1 Widening Numeric Conversions

Widening numeric conversions convert the following:

• Values of a smaller numeric type to a larger type (see Numeric Types);

• Values of enumeration type (if enumeration constants of this type are of a numeric type) to the same or a larger numeric type.


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>From</td><td style='text-align: center; word-wrap: break-word;'>To</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte</td><td style='text-align: center; word-wrap: break-word;'>short, int, long, float, double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>short</td><td style='text-align: center; word-wrap: break-word;'>int, long, float, double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>int</td><td style='text-align: center; word-wrap: break-word;'>long, float, or double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>long</td><td style='text-align: center; word-wrap: break-word;'>float or double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>enumeration with numeric constants</td><td style='text-align: center; word-wrap: break-word;'>larger numeric type</td></tr></table>

The above conversions cause no loss of information about the overall magnitude of a numeric value. Some least significant bits of the value can be lost only in conversions from an integer type to a floating-point type if the IEEE 754 round-to-nearest mode is used correctly. The resultant floating-point value is properly rounded to the integer value.

Widening numeric conversions never cause runtime errors.

#### 6.4.2 Enumeration to Constants Type Conversions

The following conversions never cause a runtime error:

• Value of enumeration type without explicit base type is converted to the corresponding integer type (see Enumerations).

enum IntegerEnum { a, b, c}

let int_enum: IntegerEnum = IntegerEnum.a

let int_value: int = int_enum // int_value will get the value of 0

let number_value: number = int_enum

/* number_value will get the value of 0 as a result of conversion sequence: enumeration -> int -> number */

A value of enumeration type with string constants is converted to type string. This conversion never causes a runtime error.

## Page 97

enum StringEnum { a = "a", b = "b", c = "c"}
let string_enum: StringEnum = StringEnum.a
let a_string: string = string_enum // a_string will get the value of "a"

A value of enumeration type with an explicitly declared type of constants is converted to the declared type. This conversion never causes a runtime error.

enum DoubleEnum: double {a = 1.0, b = 2.0, c = 3.141592653589}
let dbl_enum: DoubleEnum = DoubleEnum.a
let dbl_value: double = dbl_enum // dbl_value will get the value of 1.0

### 6.5 Numeric Casting Conversions

A numeric casting conversion occurs if the target type and the expression type are both numeric. The context for a numeric casting conversion is where conversion methods are used as defined in the standard library (see Standard Library).

The explicit use of methods for numeric cast conversions is represented in the following example:

function process_int(an_int: int) { /* ... */ }

let pi = 3.14
process_int(pi.toInt())

A numeric casting conversion never causes a runtime error.

Numeric casting conversion of an operand of type double to target type float is performed in compliance with the IEEE 754 rounding rules. This conversion can lose precision or range, resulting in the following:

• Float zero from a nonzero double; and

• Float infinity from a finite double.

Double NaN is converted to float NaN.

Double infinity is converted to the same-signed floating-point infinity.

A numeric conversion of a floating-point type operand to target types long or int is performed by the following rules:

• If the operand is NaN, then the result is 0 (zero).

• If the operand is positive infinity, or if the operand is too large for the target type, then the result is the largest representable value of the target type.

• If the operand is negative infinity, or if the operand is too small for the target type, then the result is the smallest representable value of the target type.

• Otherwise, the result is the value that rounds toward zero by using IEEE 754 round-toward-zero mode.

A numeric casting conversion of a floating-point type operand to types byte or short is performed in two steps as follows:

• The casting conversion to int is performed first (see above);

• Then, the int operand is cast to the target type.

## Page 98

A numeric casting conversion from an integer type to a smaller integer type I discards all bits except the N lowest ones, where N is the number of bits used to represent type I. This conversion can lose the information on the magnitude of the numeric value. The sign of the resulting value can differ from that of the original value.

## Page 99

## EXPRESSIONS

This Chapter describes the meanings of expressions and the rules for the evaluation of expressions, except the expressions related to coroutines (see Coroutines (Experimental)) and expressions described as experimental (see Lambda Expressions with Receiver).

The syntax of expression is presented below:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>expression:</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>primaryExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>instanceOfExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>castExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>typeOfExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>nullishCoalescingExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>spreadExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>unaryExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>binaryExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>assignmentExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ternaryConditionalExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>stringInterpolation</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>lambdaExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>lambdaExpressionWithReceiver</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>awaitExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>primaryExpression:</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>literal</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>namedReference</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>arrayLiteral</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>objectLiteral</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>recordLiteral</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>thisExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>parenthesizedExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>methodCallExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>fieldAccessExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>indexingExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>functionCallExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>newExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ensureNotNullishExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>binaryExpression:</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>multiplicativeExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>additiveExpression</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>shiftExpression</td></tr></table>

(continues on next page)

## Page 100

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

## Page 101

• Value (results found elsewhere).

A variable or a value are equally considered the value of the expression if such a value is required for further evaluation.

The type of an expression is determined at compile time (see Type of Expression).

Expressions can contain assignments, increment operators, decrement operators, method calls, and function calls. The evaluation of an expression can produce side effects as a result.

Constant expressions (see Constant Expressions) are the expressions with values that can be determined at compile time.

#### 7.1.1 Type of Expression

Every expression in the ArkTS programming language has a type. The type of an expression is determined at compile time.

In most contexts, an expression must be compatible with the type expected in a context. This type is called target type. If no target type is available in a context, then the expression is called a standalone expression:

let a = expr // no target type is available

function foo() {
    expr // no target type is available
}

Otherwise, the expression is non-standalone:

let a: number = expr // target type of 'expr' is number

function foo(s: string) {}
foo(expr) // target type of 'expr' is string

In some cases, the type of an expression cannot be inferred (see Type Inference) from the expression itself (see Object Literal as an example). If such an expression is used as a standalone expression, then a compile-time error occurs:

class P { x: number, y: number }

let x = { x: 10, y: 10 } // standalone object literal - compile time error
let y: P = { x: 10, y: 10 } // OK, type of object literal is inferred

The evaluation of an expression type requires completing the following steps:

1. Collect information for type inference (type annotation, generic constraints, etc);

2. Perform Type Inference;

3. If the expression type is not yet inferred at a previous step, and the expression is a literal in the general sense, including Array Literal, then an attempt is made to evaluate the type from the expression itself.

A compile-time error occurs if none of these steps produces an appropriate expression type.

If the expression type is  $ \underline{\text{readonly}} $, then the target type must also be  $ \underline{\text{readonly}} $. Otherwise, a compile-time error occurs:

## Page 102

let readonly_array: readonly number[] = [1, 2, 3]

foo1(readonly_array) // OK

foo2(readonly_array) // compile-time error

function foo1 (p: readonly number[]) {}

function foo2 (p: number[]) {}

let writable_array: number [] = [1, 2, 3]

foo1 (读写able_array) // OK, as always safe

#### 7.1.2 Normal and Abrupt Completion of Expression Evaluation

Each expression in a normal mode of evaluation requires certain computational steps. Normal modes of evaluation for each kind of expression are described in the following sections.

An expression evaluation completes normally if all computational steps are performed without throwing an error.

On the contrary, an expression evaluation completes abruptly if an error is thrown in the process. The information on the cause of an abrupt completion is provided in the value attached to the error object.

Runtime errors can occur as a result of expression or operator evaluation as follows:

• If the value of an array index expression is negative, or greater than, or equal to the length of the array, then an array indexing expression (see Array Indexing Expression) throws RangeError.

• If the type of a value being assigned to a fixed-size array element is not a subtype of an array element type, then an Assignment throws ArrayStoreError.

• If a Cast Expression conversion cannot be performed at runtime, then it throws ClassCastError.

• If a right-hand expression has the zero value, then the integer division or integer remainder (see Division and Remainder) operator throws ArithmeticError.

An error during the evaluation of an expression can be caused by a possible hard-to-predict and hard-to-handle linkage and virtual machine error.

Abrupt completion of the evaluation of a subexpression results in the following:

• Immediate abrupt completion of an expression that contains the subexpression (if the evaluation of the contained subexpression is required for the evaluation of the entire expression); and

• Cancellation of all subsequent steps of the normal mode of evaluation.

The terms complete normally and complete abruptly can also denote normal and abrupt completion of the execution of a statement (see Normal and Abrupt Statement Execution). A statement can complete abruptly for many reasons in addition to an error being thrown.

## Page 103

#### 7.1.3 Order of Expression Evaluation

The operands of an operator are evaluated from left to right in accordance with the following rules:

• The order of evaluation depends on the assignment operator (see Assignment).

• Any right-hand expression is evaluated only after the left-hand expression of a binary operator is fully evaluated.

• Any part of the operation can be executed only after every operand of an operator (except conditional operators '&&', '||', and '?:') is fully evaluated.

The execution of a binary operator that is an integer division ‘/’ (see Division), or integer remainder ‘%’ (see Remainder) can throw ArithmeticError only after the evaluations of both operands complete normally.

• The ArkTS programming language follows the order of evaluation as indicated explicitly by parentheses, and implicitly by the precedence of operators. This rule particularly applies for infinity and NaN values of floating-point calculations. ArkTS considers integer addition and multiplication as provably associative. However, floating-point calculations must not be naively reordered because they are unlikely to be computationally associative (even though they appear mathematically associative).

#### 7.1.4 Operator Precedence

The table below summarizes the entire information on the precedence and associativity of operators. Each section on a particular operator also contains detailed information.


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Operator</td><td style='text-align: center; word-wrap: break-word;'>Precedence</td><td style='text-align: center; word-wrap: break-word;'>Associativity</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>grouping</td><td style='text-align: center; word-wrap: break-word;'>()</td><td style='text-align: center; word-wrap: break-word;'>n/a</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>member access and chaining</td><td style='text-align: center; word-wrap: break-word;'>.?</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>access and call</td><td style='text-align: center; word-wrap: break-word;'>[] . () new</td><td style='text-align: center; word-wrap: break-word;'>n/a</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>postfix increment and decrement</td><td style='text-align: center; word-wrap: break-word;'>++ --</td><td style='text-align: center; word-wrap: break-word;'>n/a</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>prefix increment and decrement, unary</td><td style='text-align: center; word-wrap: break-word;'>++ -- + - ! ~ typeof await</td><td style='text-align: center; word-wrap: break-word;'>n/a</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>operators, typeof, await</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>exponentiation</td><td style='text-align: center; word-wrap: break-word;'>**</td><td style='text-align: center; word-wrap: break-word;'>right-to-left</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>multiplicative</td><td style='text-align: center; word-wrap: break-word;'>*/ %</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>additive</td><td style='text-align: center; word-wrap: break-word;'>+-</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>cast</td><td style='text-align: center; word-wrap: break-word;'>as</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>shift</td><td style='text-align: center; word-wrap: break-word;'>&lt;&lt; &gt;&gt; &gt;&gt;</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>relational</td><td style='text-align: center; word-wrap: break-word;'>&lt; &gt; &lt;= &gt;= instanceof</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>equality</td><td style='text-align: center; word-wrap: break-word;'>== !=</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bitwise AND</td><td style='text-align: center; word-wrap: break-word;'>&amp;</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bitwise exclusive OR</td><td style='text-align: center; word-wrap: break-word;'>^</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bitwise inclusive OR</td><td style='text-align: center; word-wrap: break-word;'>|</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>logical AND</td><td style='text-align: center; word-wrap: break-word;'>&amp;&amp;</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>logical OR</td><td style='text-align: center; word-wrap: break-word;'>||</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>null-coalescing</td><td style='text-align: center; word-wrap: break-word;'>??</td><td style='text-align: center; word-wrap: break-word;'>left-to-right</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>ternary</td><td style='text-align: center; word-wrap: break-word;'>condition?whenTrue:whenFalse</td><td style='text-align: center; word-wrap: break-word;'>right-to-left</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>assignment</td><td style='text-align: center; word-wrap: break-word;'>= += -= %= *= /= &amp;= ^= |= &lt;&lt;= &gt;== &gt;==</td><td style='text-align: center; word-wrap: break-word;'>right-to-left</td></tr></table>

## Page 104

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

## Page 105

• Local variable or parameter of the surrounding function or method.

If not a simple name, qualifiedName refers to the following:

• Entity imported from a module.

• Entity exported from a namespace, or

• Member of some class or interface, or

• Special syntax form of Record Indexing Expression.

If typeArguments are provided, then qualifiedName is a valid instantiation of the generic method or function. Otherwise, a compile-time error occurs.

A compile-time error also occurs if a name referred by qualifiedName is one of the following:

• Undefined or inaccessible;

• Named constructor (see Constructor Names).

Type of a named reference is the type of an expression.

If a named reference refers to a function name, it is called Function Reference. If a named reference refers to a method name, it is called Method Reference.

#### 7.3.1 Function Reference

A function reference refers to a declared or imported function. Type of a function reference is derived from the function signature:

function foo(n: number): string { return n.toString() }
let func = foo // type of func is '(n: number) => string'
let x = func(1) // foo() called via reference

A function reference can refer to a generic function but only if Explicit Generic Instantiations is present, otherwise a compile-time error occurs:

function gen<T> (x: T) {}

let a = gen<string> // ok
let b = gen // compile-tin

function gen<T>
 $ \text{ants} $

A compile-time error occurs if an overload alias is used in a named reference:

function foo1(n: number) {}
function foo2(s: string) {}
overload foo { foo1, foo2 }

foo(1) // OK, overload call
let x = foo // Error: ref to overload
let y = foo2 // ok, ref to foo2

## Page 106

#### 7.3.2 Method Reference

A method reference refers to a static or instance method of a class or an interface. Type of a method reference is derived from the method signature:

class C {
    static foo(n: number) {}
    bar (s: string): boolean { return true }
}

// Method reference to a static method
const m1 = C.foo  // type of 'm1' is (n: number) => void

// Method reference to an instance method
const m2 = new C().bar  // type of 'm1' is (s: string) => boolean

If method reference refers to an instance method, that the named reference is bounded with the used instance of that class or interface.

class C {
    field = 123
    method(): number { return this.field }
}

let c1 = new C
let c2 = new C
let m1 = c1.method // 'c1' is bounded
let m2 = c2.method // 'c2' is bounded
c1.field = 42
console.log(m1(), m2()) // Outputs: 42 123

A method reference can refer to a generic method only if a generic instantiation is explicitly present (see Explicit Generic Instantiations). Otherwise, a compile-time error occurs:

class C {
    gen<T> (x: T) {}
}

let a = new C().gen<string> // ok
let b = new C().gen // compile-time error: no explicit type arguments

A compile-time error occurs if a method overload alias is used in a named reference:

class C {
    foo1(n: number) {}
    foo2(s: string) {}
    overload foo { foo1, foo2 }
}

let f = new C().foo // compile-time error

## Page 107

### 7.4 Array Literal

Array literal is an expression that can be used to create an array or tuple in some cases, and to provide some initial values.

The syntax of array literal is presented below:

arrayLiteral:
    [' expressionSequence? '']
;
expressionSequence:
    expression (',' expression)* ','?
;

An array literal is a comma-separated list of initializer expressions enclosed in square brackets ‘[’ and ‘]’. A trailing comma after the last expression in an array literal is ignored:

let x = [1, 2, 3] // ok
let y = [1, 2, 3, ] // ok, trailing comma is ignored

The number of initializer expressions enclosed in square brackets of the array initializer determines the length of the array to be constructed.

If memory is allocated as required for an array literal, then an array of the specified length is created, and all elements of the array are initialized to the values specified by initializer expressions.

On the contrary, the evaluation of an array literal expression completes abruptly if:

• Not enough memory is available for a new array, and OutOfMemoryError is thrown; or

• Some initialization expression completes abruptly.

Initializer expressions are executed from left to right. The  $ n' $th expression specifies the value of the  $ n-1' $th element of the array.

Array literals can be nested (i.e., the initializer expression that specifies an array element can be an array literal if that element is of array type).

Type of an array literal expression is inferred by the following rules:

• If a context is available, then type is inferred from the context. If successful, then type of an array literal is the inferred type T[], Array<T>, or tuple.

• Otherwise, type is inferred from the types of array literal elements.

More details of both cases are presented below.

#### 7.4.1 Array Literal Type Inference from Context

Type of an array literal can be inferred from the context, including explicit type annotation of a variable declaration, left-hand part type of an assignment, call parameter type, or type of a cast expression:

let a: number[] = [1, 2, 3] // ok, variable type is used
a = [4, 5] // ok, variable type is used

(continues on next page)

## Page 108

function min(x: number[]): number {
    let m = x[0]
    for (let v of x)
        if (v < m)
            m = v
    return m
}

min([1., 3.14, 0.99]); // ok, parameter type is used

// Array of array initialization
type Matrix = number[][]
let m: Matrix = [[1, 2], [3, 4], [5, 6]]

class aClass {
    let b1: Array <aClass> = [new aClass, new aClass]
    let b2: Array <number> = [1, 2, 3]
    let b3: FixedArray<number> = [1, 2]

    /* Type of literal is inferred from the context
     taken from b1, b2 and b3 declarations */
}

Possible kinds of context are represented in the following example:

let array: number[] = [1, 2, 3] // assignment context
function foo (array: number[]) {}
foo ([1, 2, 3]) // call context
let b = [1, 2, 3] as number[] // casting conversion

All valid conversions are applied to the initializer expression, i.e., each initializer expression type must be assignable (see Assignability) to the array element type. Otherwise, a compile-time error occurs.

let value: number = 2
let list: Object[] = [1, value, "hello", new Error()] // ok

If the type used in the context is a tuple type (see Tuple Types), and types of all literal expressions are compatible with tuple type elements at respective positions, then an array literal is of tuple type.

let tuple: [number, string] = [1, "hello"] // ok
let incorrect: [number, string] = ["hello", 1] // compile-time error

If the type used in the context is a union type (see Union Types), then it is necessary to try inferring the type of the array literal from its elements (see Array Type Inference from Types of Elements). If successful, then the type so inferred must be compatible with one of the types that form the union type. Otherwise, a compile-time error occurs:

let union_of_arrays_int: int[] | string[] = [1, 2] // OK, literal is int[]
    // Compatible with union
let union_of_arrays: number[] | string[] = [1, 2] // Error, literal is int[]
    // incompatible with union
let incorrect_union_of_arrays: number[] | string[] = [1, 2, "string"]
/* Error: (number|string)[] (type of the literal) is not compatible with number[] | string[] (type of the variable)
*/

## Page 109

If the type used in the context is a fixed-size array type (see Fixed-Size Array Types), and each initializer expression type is compatible with the array element type, then an array literal is of fixed-size array type.

let array: FixedArray<number> = [1, 2]

If the type used in the context is a readonly array, then an array literal is of readonly array type.

#### 7.4.2 Array Type Inference from Types of Elements

Where no context is set, and thus the type of an array literal cannot be inferred from the context (see Type of Expression), the type of array literal [  $  \text{expr}_1, \ldots, \text{expr}_N  $] is inferred from the initialization expression instead by using the following algorithm:

1. If array literal  $ (N == O) $ includes no element, then the type of the array literal cannot be inferred, and a compile-time error occurs.

2. If at least one element of an expression type cannot be determined, then the type of the array literal cannot be inferred, and a compile-time error occurs.

3. If each initialization expression is of a numeric type (see Numeric Types), then the array literal type is number[].

4. If all initialization expressions are of the same type T, then the array literal type is T[]

5. Otherwise, the array literal type is constructed as the union type T:sub:1 | ... |  $ T_N $, where  $ T_i $ is the type of  $ expr_i $, and then:

• If  $ T_{i} $ is a literal type, then it is replaced for its supertype;

• If  $ T_{i} $ is a union type comprised of literal types, then each constituent literal type is replaced for its supertype.

• Union Types Normalization is applied to the resultant union type after the above replacements.

type A = number
let u : "A" | "B" = "A"

let a = []
let b = ["a"]
let c = [1, 2, 3]
let d = ["a" + "b", 1, 3.14]
let e = [u]
let f = [() : void => {} , new A()] // compile-time error, type cannot be inferred
// type is string[]
// type is number[]
// type is (string | number)[]
// type is string[]
// type is (() => void | A)[]

### 7.5 Object Literal

Object literal is an expression that can be used to create a class instance with methods and fields with initial values. In some cases it is more convenient to use an object literal in place of a class instance creation expression (see New Expressions).

The syntax of object literal is presented below:

## Page 110

objectLiteral:
    {'objectLiteralMembers?'}'
;
objectLiteralMembers:
    objectLiteralMember(',' objectLiteralMember)*','?
;
objectLiteralMember:
    objectLiteralField
;
objectLiteralField:
    identifier ':' expression
;

An object literal field consists of an identifier and an expression as follows:

class Person {
    name: string = ""
    age: number = 0
}

let b: Person = {name: "Bob", age: 25}

let : Person = {name: "Alice", age: 18, } //ok, trailing comma is ignored

let c: Person | number = {name: "Mary", age: 17} // literal will be of type Person

An object literal method is a complete declaration of a public method. Examples of object literals with methods are provided in Object Literal of Interface Type.

Type of an object literal expression is always some class C that is inferred from the context. A type inferred from the context can be either a class (see Object Literal of Class Type), or an anonymous class created for the inferred interface type (see Object Literal of Interface Type).

A compile-time error occurs if:

• Type of an object literal cannot be inferred from the context (see Type of Expression for an example);

• Inferred type is not a class or interface type, or is an abstract class type (see Abstract Classes);

• Inferred type is not an interface type, and an object literal contains methods;

• Context is a union type, and an object literal can be treated as the value of several union component types.

let p = {name: "Bob", age: 25}
    // compile-time error, type cannot be inferred

class A { field = 1 }
class B { field = 2 }

let q: A | B = {field: 6}
    // compile-time error, type cannot be inferred as the literal
    // fits both A and B

## Page 111

#### 7.5.1 Object Literal of Class Type

If class type C is inferred from the context, then type of an object literal is C:

class Person {
    name: string = ""
    age: number = 0
}

function foo(p: Person) { /*some code*/ }
// ...
let p: Person = {name: "Bob", age: 25} /* ok, variable type is used */
foo({name: "Alice", age: 18}) // ok, parameter type is used

An identifier in each name-value pair must name a field of class C, or a field of any superclass of class C.

A compile-time error occurs if the identifier does not name an accessible member field (see Accessible) in type C:

class Friend {
    name: string = ""
    private nick: string = ""
    age: number
    sex?: "male"|"female"
}

// compile-time error, nick is private:
let f: Friend = {name: "Alexander", age: 55, nick: "Alex"}

A compile-time error occurs if type of an expression in a name-value pair is not assignable (see Assignability) to the field type:

let f: Friend = {name: 123} /* compile-time error - type of right hand-side is not assignable to the type of the left hand-side */

If some class fields have default values (see Default Values for Types) or explicit initializers (see Variable and Constant Declarations), then such fields can be skipped in the object literal.

let f: Friend = {} /* OK, as name, nick, age, and sex have either default value or explicit initializer */

If an object literal is to use class C, then class C must have a parameterless constructor (explicit or default) that is accessible (see Accessible) in the class-composite context.

A compile-time error occurs if:

• C contains no parameterless constructor; or

• No constructor is accessible (see Accessible).

These situations are presented in the examples below:

class C {
    constructor (x: number) {}
}

// ...
let c: C = {} /* compile-time error - no parameterless
    constructor */

## Page 112

class C {
    private constructor () {}
}

// ...
let c: C = {} /* compile-time error - constructor is not accessible */

If a class has accessors (see Class Accessor Declarations) for a property, and its setter is provided, then this property can be used as a part of an object literal. Otherwise, a compile-time error occurs:

class OK {
    set attr (attr: number) {}
}
const a: OK = {attr: 42} // OK, as the setter be called

class Err {
    get attr (): number { return 42 }
}
const b: Err = {attr: 42} // compile-time error - no setter for 'attr'

#### 7.5.2 Object Literal of Interface Type

If an interface type I is inferred from the context, then type of an object literal is an anonymous class implicitly created for interface I:

interface Person {
    name: string
    age: number
}
let b: Person = {name: "Bob", age: 25}

In the example above, type of b is an anonymous class that contains the same fields as the interface I properties.

Any properties that are optional can be skipped in an object literal. The values of such optional properties are set to undefined as follows:

interface Person {
    name: string
    age: number
    sex?: "male"|"female"
}
let b: Person = {name: "Bob", age: 25}
    // 'sex' field will have 'undefined' value

Properties that are non-optional cannot be skipped in an object literal, despite some property types having default values (see Default Values for Types). If a non-optional property (e.g., age in the example above) is skipped, then a compile-time error occurs.

A compile-time error occurs if an object literal of interface type introduces a new method:

## Page 113

interface I {}
const i: I = { foo(): void {} } // compile-time error

If an interface has accessors (see Interface Properties) for some property, and the property is used in an object literal, then a compile-time error occurs:

interface I1 {
    set attr (attr: number)
}
const a: I1 = {attr: 42} /* compile-time error - 'attr' cannot be used in object literal */
interface I2 {
    get attr(): number
}
const b: I2 = {attr: 42} /* compile-time error - 'attr' cannot be used in object literal */

#### 7.5.3 Object Literal of Record Type

Generic type Record<Key, Value>(see Record Utility Type) is used to map properties of a type (type Key) to another type (type Value). A special form of object literal is used to initialize the value of such type:

The syntax of record literal is presented below:

recordLiteral:
    {'keyValueSequence?'}
;
keyValueSequence:
    keyValue(','keyValue)*','?
;
keyValue:
    expression:'expression';

The first expression in keyValue denotes a key and must be of type Key. The second expression denotes a value and must be of type Value:

let map: Record<string, number> = {
    "John": 25,
    "Mary": 21,
}

console.log(map["John"]) // prints 25

interface PersonInfo {
    age: number

(continues on next page)

## Page 114

(continued from previous page)

salary: number
}
let map: Record<string, PersonInfo> = {
    "John": { age: 25, salary: 10},
    "Mary": { age: 21, salary: 20}
}

If a key is a union of literal types, then all variants must be listed in the object literal. Otherwise, a compile-time error occurs:

let map: Record<"aa" | "bb", number> = {
    "aa": 1,
} // compile-time error: "bb" key is missing

#### 7.5.4 Object Literal Evaluation

The evaluation of an object literal of type C (where C is either a named class type or an anonymous class type created for the interface) is to be performed by the following steps:

• A parameterless constructor is executed to produce an instance x of class C. The execution of the object literal completes abruptly if so does the execution of the constructor.

- Name-value pairs of the object literal are then executed from left to right in the textual order they occur in the source code. The execution of a name-value pair includes the following:

- Evaluation of the expression; and

– Assignment of the value of expression to the corresponding field of x as its initial value. This rule also applies to reading fields.

The execution of an object literal completes abruptly if so does the execution of a name-value pair.

An object literal completes normally with the value of a newly initialized class instance if so do all name-value pairs.

### 7.6 Spread Expression

Spread expression can be used only within an array literal (see Array Literal) or argument passing. The expression must be of array type (see Array Types) or tuple type (see tuple Types). Otherwise, a compile-time error occurs.

The syntax of spread expression is presented below:

spreadExpression:
    ...' expression
;

A spread expression for arrays or tuples can be evaluated as follows:

• By the compiler at compile time if expression is constant (see Constant Expressions);

## Page 115

• At runtime otherwise.

An array or tuple object referred by the expression is broken by the evaluation into a sequence of values. This sequence is used where a spread expression is used. It can be an assignment, a call of a function, method, or constructor. A sequence of types of these values is the type of the spread expression.

A spread expression for arrays is represented in the example below:

let array1 = [1, 2, 3]
let array2 = [4, 5]
let array3 = [...array1, ...array2] // spread array1 and array2 elements
    // while building new array literal at compile time
console.log(array3) // prints [1, 2, 3, 4, 5]

function foo (...array: number[]) {
    console.log(array)
}

foo (...array2) // spread array2 elements into arguments of the foo() call

function run_time_spread_application1 (a1: number[], a2: number[]) {
    console.log([...a1, 42, ...a2])
    // array literal will be built at runtime
}

run_time_spread_application1 (array1, array2) // prints [1, 2, 3, 42, 4, 5]

A spread expression for tuples is represented in the example below:

let tuple1: [number, string, boolean] = [1, "2", true]
let tuple2: [number, string] = [4, "5"]
// spread tuple1 and tuple2 elements
let tuple3: [number, string, boolean, number, string] = [...tuple1, ...tuple2]
// while building new tuple object at compile time
console.log(tuple3) // prints [1, 2, true, 4, 5]

function bar (...tuple: [number, string]) {
    console.log(tuple)
}
bar (...tuple2) // spread tuple2 elements into arguments of the foo() call

function run_time_spread_application2 (a1: [number, string, boolean], a2: [number, _, string]) {
    console.log([...a1, 42, ...a2])
    // such array literal will be built at runtime
}
run_time_spread_application2 (tuple1, tuple2) // prints [1, 2, true, 42, 4, "5"]

Note. If an argument is spread at the call site, then an appropriate parameter must be of the rest kind (see Rest Parameter). A compile-time error occurs if an argument is spread into a sequence of ordinary non-optional parameters as follows:

function foo1 (n1: number, n2: number) // non-rest parameters
{ ... }
let an_array = [1, 2]
foo1 (...an_array) // compile-time error

(continues on next page)

## Page 116

function foo2 (n1: number, n2: string) // non-rest parameters
{ ... }
let a_tuple: [number, string] = [1, "2"]
foo2 (...a_tuple) // compile-time error

### 7.7 Parenthesized Expression

The syntax of parenthesized expression is presented below:

parenthesizedExpression:
    '(' expression ')'
;

Type and value of a parenthesized expression are the same as those of the contained expression.

### 7.8 this Expression

The syntax of this expression is presented below:

thisExpression:
'this'
;

The keyword this can be used as an expression in the body of an instance method of a class (see Method Body) or an interface (see Default Interface Method Declarations). A corresponding class or interface type is the type of this expression. If a method is declared in an object literal (see Object Literal), then the type of the object literal is the type of this.

The keyword  $ \underline{\text{this}} $ can be used in a lambda expression only if it is allowed in the context in which the lambda expression occurs. The type of this is the type of a class or an interface in which it is declared, but not the type of the surrounding object literal type, if any.

The keyword this in a direct call expression this( arguments ) can only be used in an explicit constructor call statement (see Explicit Constructor Call).

The keyword this can also be used in the body of a function with receiver (see Functions with Receiver). The type of this expression is the declared type of the parameter this in a function.

A compile-time error occurs if the keyword this appears elsewhere.

The keyword this used as a primary expression denotes a value that is a reference to the following:

• Object for which the instance method is called; or

• Object being constructed.

The parameter this in a lambda body and in the surrounding context denote the same value.

## Page 117

The class of the actual object referred to at runtime can be T if T is a class type, or a subclass of T (see Subtyping).

The semantics of this in different contexts is represented in the example below:

interface anInterface {
    method() {
        this // type of 'this' is anInterface
    }
}

class aClass implements anInterface {
    method() {
        this // type of 'this' is aClass
    }
    field = (): void => {
        this // type of 'this' is aClass
    }
}

class AnotherClass {
    anotherMethod() {
        const obj: aClass = { // Object literal
            method() {
                this // type of 'this' is aClass
            },
            field: (): void => {
                this // type of 'this' is AnotherClass
            }
        }
    }
}

### 7.9 Field Access Expression

Field access expression can access a field of an object to which an object reference refers. The object reference can have different forms as described in detail in Accessing Current Object Fields and in Accessing SuperClass Properties.

The syntax of field access expression is presented below:

fieldAccessExpression:
    objectReference ('.' | '?.') identifier
;

A field access expression that contains ‘?.’ (see Chaining Operator) is called safe field access because it handles nullish object references safely.

If object reference evaluation completes abruptly, then so does the entire field access expression.

An object reference used to access a field must be a non-nullish reference type T. Otherwise, a compile-time error occurs.

A field access expression is valid if the identifier refers to an accessible member field (see Accessible) in type T. A compile-time error occurs otherwise.

## Page 118

Type of a field access expression is the type of a member field.

#### 7.9.1 Accessing Current Object Fields

The result of a field access expression is computed at runtime as described below.

a. Static field access (objectReference is evaluated in the form typeReference)

The evaluation of typeReference is performed. The result of a field access expression of a static field in a class is as follows:

• variable if the field is not readonly. The resultant value can be changed later.

• value if the field is readonly, except where field access occurs in a initializer block (see Static Initialization).

b. Instance field access (objectReference is evaluated in the form primaryExpression)

The evaluation of primaryExpression is performed. The result of field access expression of an instance field in a class or interface is as follows:

• variable if the field is not readonly. The resultant value can be changed later.

• value if the field is readonly, except where field access occurs in a constructor (see Constructor Declaration).

Only the primaryExpression type (not class type of an actual object referred at runtime) is used to determine the field to be accessed.

#### 7.9.2 Accessing SuperClass Properties

The form super.identifier is valid when accessing the superclass property via accessor (see Class Accessor Declarations). A compile-time error occurs if identifier in 'super.identifier' denotes a field.

class Base {
    get property(): number { return 1 }
    set property(p: number) {}
    field = 1234
}
class Derived extends Base {
    get property(): number { return super.property } // OK
    set property(p: number) { super.property = 42 } // OK
    foo () {
        super.field = 42 // compile-time error
        console.log (super.field) // compile-time error
    }
}

## Page 119

### 7.10 Method Call Expression

A method call expression calls a static or instance method of a class or an interface. Dynamic dispatch (see Dispatch) is used during program execution to perform a call in case of an instance method.

The syntax of method call expression is presented below:

methodCallExpression:
    objectReference('.' | '?.') identifier typeArguments? arguments block?
;

The syntax form that has a block associated with the method call is a special form called trailing lambda call (see Trailing Lambdas for details).

A method call with ‘? . ’ (see Chaining Operator) is called a safe method call because it handles nullish values safely.

There are several steps that determine and check the method to be called at compile time (see Step 1: Selection of Type to Use, Step 2: Selection of Method, and Step 3: Checking Method Modifiers).

#### 7.10.1 Step 1: Selection of Type to Use

The object reference is used to determine the type in which to search for the method. Three forms of object reference are possible:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Form of Object Reference</td><td style='text-align: center; word-wrap: break-word;'>Type to Use</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>typeReference</td><td style='text-align: center; word-wrap: break-word;'>Type denoted by typeReference.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>expression of type  $ T $</td><td style='text-align: center; word-wrap: break-word;'>T if  $ T $ is a class, interface, or union;  $ T $&#x27;s constraint (Type Parameter Constraint) if  $ T $ is a type parameter. A compile-time error occurs otherwise.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>super</td><td style='text-align: center; word-wrap: break-word;'>The superclass of the class that contains the method call.</td></tr></table>

#### 7.10.2 Step 2: Selection of Method

After the type to use is known, the method to call must be determined. If a method name in the call refers an overload declaration (see Overload Declarations), then Overload Resolution is used to select the method to call. A compile-time error occurs if no method is available to call.

#### 7.10.3 Step 3: Checking Method Modifiers

In this step, the single method to call is known, and the following set of semantic checks must be performed:

• If the method call has the form typeReference.identifier, then typeReference refers to a class, and the method must be declared static. Otherwise, a compile-time error occurs.

## Page 120

• If the method call has the form expression.identifier, then the method must not be declared static. Otherwise, a compile-time error occurs.

• If the method call has the form super.identifier, then the method must not be declared abstract or static. Otherwise, a compile-time error occurs.

A compile-time error occurs if a method has at least one parameter or return type of the type FixedArray parameterized with a type parameter and method call expression leads to instantiation of the type FixedArray with the predefined value type (see Value Types).

#### 7.10.4 Type of Method Call Expression

Type of a method call expression is the return type of the method.

class A {
    static method() { console.log("Static method() is called") }
    method() { console.log("Instance method() is called") }
}

let x = A.method() // compile-time error as void cannot be used as type annotation
A.method() // OK
let y = new A().method() // compile-time error as void cannot be used as type annotation
new A().method() // OK

### 7.11 Function Call Expression

Function call expression is used to call a function (see Function Declarations), a variable of a function type (Function Types), or a lambda expression (see Lambda Expressions).

The syntax of function call expression is presented below:

functionCallExpression:
    expression ('?.' | typeArguments)? arguments block?
;

A special syntactic form that contains a block associated with the function call is called trailing lambda call (see Trailing Lambdas for details).

A compile-time error occurs if the expression type is one of the following:

• Different than the function type;

• Nullish type without ‘?.’ (see Chaining Operator).

If the operator ‘? .’ (see Chaining Operator) is present, and the expression evaluates to a nullish value, then:

• Arguments are not evaluated;

• Call is not performed; and

## Page 121

• Result of functionCallExpression is not produced as a consequence.

The function call is safe because it handles nullish values properly.

If the form of expression in the call is qualifiedName, and qualifiedName refers an overload declaration (Overload Declarations), then Overload Resolution is used to select the function to call.

A compile-time error occurs if no function is available to call.

A compile-time error occurs if a function has at least one parameter or return type of the type FixedArray parameterized with a type parameter and function call expression leads to instantiation of the type FixedArray with the predefined value type (see Value Types).

Semantic check for call is performed in accordance with Compatibility of Call Arguments.

Various forms of function calls are represented in the example below:

function foo() { console.log("Function foo() is called") }
foo() // function call uses function name to call it

call (foo) // top-level function passed
call ((): void => { console.log("Lambda is called") }) // lambda is passed
call (A.method) // static method
call ((new A).method) // instance method is passed

class A {
    static method() { console.log("Static method() is called") }
    method() { console.log("Instance method() is called") }
}

function call (callee: () => void) {
    callee() // function call uses parameter name to call any functional object passed_
    →as an argument
}

(((): void => { console.log("Lambda is called") })) // function call uses lambda_
→expression to call it

let x = foo() // compile-time error as void cannot be used as type annotation

Type of a function call expression is the return type of the function.

### 7.12 Indexing Expressions

Indexing expressions are used to access elements of arrays (see Array Types), strings (see Type string), and Record instances (see Record Utility Type). Indexing expressions can also be applied to instances of indexable types (see Indexable Types).

The syntax of indexing expression is presented below:

indexingExpression:
    expression ('?.')? [' expression '']
;

## Page 122

Any indexing expression has two subexpressions as follows:

• Object reference expression before the left bracket; and

• Index expression inside the brackets.

If the operator '?.' (see Chaining Operator) is present in an indexing expression, then:

• It an object reference expression is not of a nullish type, then the chaining operator has no effect.

• Otherwise, object reference expression must be checked to nullish value. If the value is undefined or null, then the evaluation of the entire surrounding primary expression stops. The result of the entire primary expression is then undefined.

If no ‘?.’ is present in an indexing expression, then object reference expression must be of array type or Record type. Otherwise, a compile-time error occurs.

#### 7.12.1 Array Indexing Expression

Index expression for array indexing must be one of integer types, namely byte, short, or int. Otherwise, a compile-time error occurs.

The conversion of byte and short types (see Widening Numeric Conversions) is performed on an index expression to ensure that the resultant type is int. Otherwise, a compile-time error occurs.

Other numeric types (long, float, and double/number) must be converted explicitly by applying the methods defined in the classes of the Standard Library.

const a = ["Alice", "Bob", "Carol"]
function demo (l: long, f: float, d: double, n: number) {
    console.log(
        a[l.toInt()], a[f.toInt()],
        a[d.toInt()], a[n.toInt()]
    ) // OK to access array using index expression conversion methods
}

If the chaining operator ‘? .’ (see Chaining Operator) is present, and after its application the type of object reference expression is an array type, then it makes a valid array reference expression, and the type of the array indexing expression is T.

The result of an array indexing expression is a variable of type T (i.e., an element of the array selected by the value of that index expression).

It is essential that, if type T is a reference type, then the fields of array elements can be modified by changing the resultant variable fields:

let names: string[] = ["Alice", "Bob", "Carol"]
console.log(names[1]) // prints Bob
names[1] = "Martin"
console.log(names[1]) // prints Martin

console.log(names["1"]) // compile-time error as index of non-numeric type

class RefType {
    field: number = 42

## Page 123

}
const objects: RefType[] = [new RefType(), new RefType()]
const obj = objects[1]
obj.field = 777 // change the field in the array element
console.log(objects[0].field) // prints 42
console.log(objects[1].field) // prints 777

let an_array = [1, 2, 3]
let element = an_array[3.5] // compile-time error as index is not integer
function foo (index: number) {
    let element = an_array[index] // compile-time error as index is not integer
}

An array indexing expression evaluated at runtime behaves as follows:

• Object reference expression is evaluated first.

• If the evaluation completes abruptly, then so does the indexing expression, and the index expression is not evaluated.

• If the evaluation completes normally, then the index expression is evaluated. The resultant value of the object reference expression refers to an array.

• If the index expression value of an array is less than zero, greater than or equal to that array's length, then RangeError is thrown.

• Otherwise, the result of the array access is a type T variable within the array selected by the value of the index expression.

function setElement(names: string[], i: int, name: string) {
    names[i] = name // runtime error, if 'i' is out of bounds
}

#### 7.12.2 String Indexing Expression

Index expression for string indexing must be of one of integer types, namely byte, short, or int. The same rules apply as in Array Indexing Expression.

If the index expression value of a string is less than zero, greater than or equal to that string's length, then RangeError is thrown.

console.log("abc"[1]]) // prints: b
console.log("abc"[3]]) // runtime exception

The result of a string indexing expression is a value of string type.

Note. String value is immutable, and is not allowed to change a value of a string element by indexing.

let x = "abc"
x[1] = "d" // compile-time error, string value is immutable

## Page 124

#### 7.12.3 Record Indexing Expression

Indexing expression for a type Record<Key, Value> (see Record Utility Type) allows getting or setting a value of type Value at an index specified by the expression of type Key.

The following two cases are to be considered separately:

2. Other cases.

1. Type Key is a union that contains literal types only;

Case 1. If type Key is a union that contains literal types only, then an index expression can only be one of the literals listed in the type. The result of the indexing expression is of type Value.

type Keys = 'key1' | 'key2' | 'key3'

let x: Record<Keys, number> = {
    'key1': 1,
    'key2': 2,
    'key3': 4,
}

let y = x['key2'] // y value is 2

A compile-time error occurs if an index expression is not a valid literal:

console.log(x['key4']) // compile-time error
x['another key'] = 5 // compile-time error

The compiler guarantees that an object of Record<Key, Value> for this type Key contains values for all Key keys.

Case 2. An index expression has no restriction. The result of an indexing expression is of type Value | undefined.

let x: Record<number, string> = {
    1: "hello",
    2: "buy",
}

function foo(n: number): string | undefined {
    return x[n]
}

function bar(n: number): string {
    let s = x[n]
    if (s == undefined) { return "no" }
    return s!
}

foo(3) // prints "undefined"
bar(3) // prints "no"

let y = x[3]

Type of y in the code above is string | undefined. The value of y is undefined.

An indexing expression evaluated at runtime behaves as follows:

## Page 125

• Object reference expression is evaluated first.

• If the evaluation completes abruptly, then so does the indexing expression, and the index expression is not evaluated.

• If the evaluation completes normally, then the index expression is evaluated. The resultant value of the object reference expression refers to a record instance.

• If the record instance contains a key defined by the index expression, then the result is the value mapped to the key.

• Otherwise, the result is the literal undefined.

### 7.13 Chaining Operator

The chaining operator ‘?.’ is used to effectively access values of nullish types. It can be used in the following contexts:

• Field Access Expression.

• Method Call Expression.

• Function Call Expression.

• Indexing Expressions.

If the value of the expression to the left of ‘?.’ is undefined or null, then the evaluation of the entire surrounding primary expression stops. The result of the entire primary expression is then undefined. Thus the type of the entire primary expression is the union undefined | non-nullish type of the entire primary expression:

class Person {
    name: string
    spouse?: Person = undefined
    constructor(name: string) {
        this.name = name
    }
}

let bob = new Person("Bob")
console.log(bob.spouse?.name) // prints "undefined"
// type of bob.spouse?.name is undefined|string

bob.spouse = new Person("Alice")
console.log(bob.spouse?.name) // prints "Alice"
// type of bob.spouse?.name is undefined|string

If an expression is not of a nullish type, then the chaining operator has no effect.

A compile-time error occurs if a chaining operator is placed in the context where a variable is expected, e.g., in the left-hand-side expression of an assignment (see Assignment) or expression (see Postfix Increment, Postfix Decrement, Prefix Increment or Prefix Decrement).

## Page 126

### 7.14 New Expressions

There are two syntactical forms of the new expression:

newExpression:
    newClassInstance
| newArrayInstance
;

Type of a new expression is either class or array.

A new class instance expression creates a new object that is an instance of the specified class and it is described in full details below.

The creation of array instances is an experimental feature discussed in Resizable Array Creation Expressions.

The syntax of new class instance expression is presented below:

newClassInstance:
    'new' typeArguments? typeReference arguments?
;

Class instance creation expression specifies a class to be instantiated. It optionally lists all actual arguments for the constructor.

class A {
    constructor(p: number) {}
}

new A(5) // create an instance and call constructor
const a = new A(6) /* create an instance, call constructor and store
                    created and initialized instance in 'a' */

Class instance creation expression can throw an error (see Error Handling, Constructor Declaration).

When a class instance creation expression refers to classes FixedArray, Array, or derived classes of Array instantiated with an array element type of some class type then it turns out to be a special form of array creation expression. And in case when such array creation expression defines a number of elements of the created array it leads to a compile-time error if the type of an array element:

• refers to a class that contains neither an accessible (see Accessible) parameterless constructor nor a constructor with all parameters of the second form of optional parameters (see Optional Parameters); or

• has no default value.

The same restriction applies to ref:Resizable Array Creation Expressions.

class A<T> {
    foo() {
        const a1 = new Array<T> (5) // Array with 5 elements of type T cannot be created
        const a1 = new FixedArray<T> (5) // Array with 5 elements of type T cannot be created
    }
}

The execution of a class instance creation expression is performed as follows:

• New instance of class is created;

## Page 127

• Constructor of class is called to fully initialize the created instance.

The validity of the constructor call is similar to the validity of the method call as discussed in Step 2: Selection of Method, except the cases discussed in Constructor Body.

A compile-time error occurs if typeReference is a type parameter.

Note. If a class instance creation expression with no argument is used as object reference in a method call expression, then empty parentheses ‘()’ are to be used.

class A { method() {} }

new A.method() // compile-time error
new A().meth
(new

### 7.15 Instance0f Expression

The syntax of instanceof expression is presented below:

instanceOfExpression:
    expression 'instanceof' type
;

Any instance of expression in the form expr instanceof T is of type boolean.

The result of an instance of expression is true if the actual type of evaluated expr is a subtype of T (see Subtyping). Otherwise, the result is false.

A compile-time error occurs if type T is not retained by Type Erasure.

Generic type (see Generics) in the form of type name (see Type References) can be used as T operand of an instance of expression. In this case, the check is performed against the type name, and type parameters are ignored. Instantiated generic types (see Explicit Generic Instantiations) cannot be used because the T operand of an instance of must be retained by Type Erasure.

class C<T> {
    foo() {
        console.log(this.instanceof C) // true
        console.log(this.instanceof C<T>) // compile-time error
    }
}

let c = new C<number>
c.foo()

The type of an instance of expression is used for smart cast (see Smart Types) if applicable.

## Page 128

### 7.16 Cast Expression

The syntax of cast expression is as follows:

castExpression: expression 'as' type ;

Cast expression in the form expr as target applies the cast operator as to expr by issuing the value of a specified target type. Thus, the type of a cast expression is always the target type.

class X {}

let x1 : X = new X()
let ob : Object = x1 as Object // Object is the target type
let x2 : X = ob as X // X is the target type

A compile-time error occurs if the target type is type never:

1 as never // compile-time error

A compile-time error occurs if target type is not preserved by Type Erasure.

Two specific cases of a cast expression are described in the sections below:

- Type Inference in Cast Expression if expr is a numeric literal (see Numeric Literals), an Array Literal, or an Object Literal;

• Runtime Checking in Cast Expression otherwise.

If none of conditions stated in these sections are satisfied, then a compile-time error occurs.

#### 7.16.1 Type Inference in Cast Expression

The following combinations of expr and target are considered for the expr as target expression:

• expr is a numeric literal, see Type Inference for Numeric Literals for detail;

- expr is an Array Literal, and target is an array type or a tuple type (see Array Literal Type Inference from Context for detail);

- expr is an Object Literal, and target is class type, interface type, or Record Utility Type (see the subsections of Object Literal for detail).

This kind of a cast expression results in inferring the target type for expr. A compile-time error can occur when processing a cast expression (see corresponding sections for detail), but this expression never causes a runtime error by itself. However, the evaluation of array literal elements or object literal properties can cause a runtime error.

Casting for numeric literals is represented in the example below:

let x = 1 as byte // ok
let y = 128 as byte // compile-time error

Casting for array literals is represented in the example below:

## Page 129

let a = [1, 2] as double[] // ok, [1.0, 2.0]
let b = [1, 2] as double // compile-time error, wrong target type
let c = [1, "cc"] as double[] // compile-time error, wrong element type
let d = [1, "cc"] as [double, string] // ok, cast to the tuple type
let e = [1.0, "cc"] as [int, string] // compile-time error, wrong element type

Note. Assignability check is applied to the elements of an array literal.

Examples with object literals are provided in Object Literal.

#### 7.16.2 Runtime Checking in Cast Expression

If none of the previous kinds of cast expression can be applied, then expr as target checks if the type of expr is a subtype of target (see Subtyping).

If the actual type of expr is a subtype of target (see Subtyping), then the result of an as expression is the result of the evaluated expr. Otherwise, ClassCastError is thrown.

If target type is not preserved by Type Erasure, then the check is performed against an effective type of the target type. As the effective type is less specific than target in the case described, the usage of the resulting value can cause type violation, and ClassCastError is thrown as a consequence (see Type Erasure for detail).

Semantically, a cast expression of this kind is coupled tightly with InstanceOf Expression as follows:

• If the result of x instanceof T is true, then x as T never causes a runtime error;

• If x instanceof T causes a compile-time error as a result of Type Erasure, then x as T also causes a compile-time error.

• If otherwise the result of x instanceof T is false, then x as T causes ClassCastError thrown at runtime.

This situation is represented in the following example:

function foo (x: Object) {
    x as string
}

foo("aa") // OK
foo(1) // runtime error is thrown in foo by 'as' operator application

InstanceOf Expression can be used to prevent runtime errors. Moreover, the InstanceOf Expression makes cast conversion unnecessary in many cases as smart cast is applied (see Smart Types):

class Person {
    name: string
    constructor (name: string) { this.name = name }
}

function printName(x: Object) {
    if (x.instanceof Person) {
        // no need to cast, type of 'x' is 'Person' here
        console.log(x.name)
    } else {

(continues on next page)

## Page 130

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

## Page 131

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Expression Type</td><td style='text-align: center; word-wrap: break-word;'>TypeOf Result</td><td style='text-align: center; word-wrap: break-word;'>Code Example</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>string</td><td style='text-align: center; word-wrap: break-word;'>“string”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>let s: string = ...
typeof s</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>boolean</td><td style='text-align: center; word-wrap: break-word;'>“boolean”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>let b: boolean = ...
typeof b</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bigint</td><td style='text-align: center; word-wrap: break-word;'>“bigint”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>let b: bigint = ...
typeof b</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>any class or interface</td><td style='text-align: center; word-wrap: break-word;'>“object”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>let a: Object = ...
typeof a</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>any function type</td><td style='text-align: center; word-wrap: break-word;'>“function”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>let f: () =&gt; void = ...
typeof f</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>undefined</td><td style='text-align: center; word-wrap: break-word;'>“undefined”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>typeof undefined</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>null</td><td style='text-align: center; word-wrap: break-word;'>“object”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>typeof null</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>T|null, when T is a class (but not Object - see next table), interface or array</td><td style='text-align: center; word-wrap: break-word;'>“object”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>class C {}
let x: C | null = ...
typeof x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>enumeration type</td><td style='text-align: center; word-wrap: break-word;'>name of enumeration base type</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>enum C {R, G, B}
let c: C = ...
typeof c // &quot;int&quot;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number, double</td><td style='text-align: center; word-wrap: break-word;'>“number”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>let n: number = ...
typeof n</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Other numeric types:
byte, short, int, long, float</td><td style='text-align: center; word-wrap: break-word;'>“byte”, “short”, “int”, “long” or “float”, depending on type of expression</td><td style='text-align: center; word-wrap: break-word;'>let x: byte = ...
typeof x // &quot;byte&quot;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>char</td><td style='text-align: center; word-wrap: break-word;'>“char”</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>let x: char = ...
typeof x</td></tr></table>

2. The value of a TypeOf expression is determined at runtime

The result is the name of an actual type used at runtime for the following expression types:

## Page 132

Expression Type
Code Example

Object
function f(o: Object) {
    typeof o
}

union type
function f(p: A | B) {
    typeof p
}

type parameter
class A<T|null|undefined> {
    f: T
    m() {
        typeof this.f
    }
    constructor(p: T) {
        this.f = p
    }
}

### 7.18 Ensure-Not-Nullish Expression

Ensure-not-nullish expression is a postfix expression with the operator '!'. An ensure-not-nullish expression in the expression e! checks whether e of a nullish type (see Nullish Types) evaluates to a nullish value.

The syntax of ensure-not-nullish expression is presented below:

ensureNotNullishExpression: expression '!'

If the expression e is not of a nullish type, then the operator '!' has no effect.

If the result of the evaluation of e is not equal to null or undefined, then the result of e! is the outcome of the evaluation of e.

If the result of the evaluation of e is equal to null or undefined, then NullPointerError is thrown.

Type of ensure-not-nullish expression is the non-nullish variant of type of e.

## Page 133

### 7.19 Nullish-Coalescing Expression

Nullish-coalescing expression is a binary expression that uses the operator ‘??’.

The syntax of nullish-coalescing expression is presented below:

nullishCoalescingExpression: expression '??' expression ;

A nullish-coalescing expression checks whether the evaluation of the left-hand-side expression equals the nullish value:

• If so, then the right-hand-side expression evaluation is the result of a nullish-coalescing expression.

• If not so, then the result of the left-hand-side expression evaluation is the result of a nullish-coalescing expression, and the right-hand-side expression is not evaluated (the operator ‘??’ is thus lazy).

The type of a nullish-coalescing expression is a normalized union type (see Union Types) formed from the following:

• Non-nullish variant of the type of the left-hand-side expression; and

• Type of the right-hand-side expression.

The semantics of a nullish-coalescing expression is represented in the following example:

let x = lhs_expression ?? rhs_expression

let x$ = lhs_expression

if (x$ == null) {x = rhs_expression} else x = x$!

// Type of x is NonNullishType(LHS_expression) | Type(rhs_expression)

A compile-time error occurs if the nullish-coalescing operator is mixed with conditional-and or conditional-or operators without parentheses.

### 7.20 Unary Expressions

The syntax of unary expression is presented below:

unaryExpression:
  expression '++'
  | expression '--'
  | '++' expression
  | '--' expression
  | '+' expression
  | '-' expression
  | '~' expression
  | '!' expression
;

All expressions with unary operators (except postfix increment and postfix decrement operators) group right-to-left for ‘~+x’ to have the same meaning as ‘~(+)’.

## Page 134

The type of unaryExpression is not necessarily the same as the type of the expression provided. Further in the text, the type of unaryExpression is stated explicitly for each unary operator.

#### 7.20.1 Postfix Increment

Postfix increment expression is an expression followed by the increment operator '++'.

The expression must be left-hand-side expression (see Left-Hand-Side Expressions), so it denotes a variable.

A compile-time error occurs if type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a postfix increment expression is the type of the variable. The result of a postfix increment expression is a value, not a variable.

If the evaluation of the operand expression completes normally at runtime, then:

• The value 1 is added to the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the postfix increment expression completes abruptly, and no incrementation occurs.

The value of the postfix increment expression is the value of the variable before a new value is stored.

#### 7.20.2 Postfix Decrement

Postfix decrement expression is an expression followed by the decrement operator ‘--’. The expression must be left-hand-side expression (see Left-Hand-Side Expressions).

A compile-time error occurs if type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a postfix decrement expression is the type of the variable. The result of a postfix decrement expression is a value, not a variable.

If evaluation of the operand expression completes at runtime, then:

• The value 1 is subtracted from the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the postfix decrement expression completes abruptly, and no decrementation occurs.

The value of the postfix decrement expression is the value of the variable before a new value is stored.

## Page 135

#### 7.20.3 Prefix Increment

Prefix increment expression is an expression preceded by the operator ‘++’. The expression must be left-hand-side expression (see Left-Hand-Side Expressions).

A compile-time error occurs if the type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a prefix increment expression is the type of the variable. The result of a prefix increment expression is a value, not a variable.

If evaluation of the operand expression completes normally at runtime, then:

• The value 1 is added to the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the prefix increment expression completes abruptly, and no incrementation occurs.

The value of the prefix increment expression is the value of the variable after a new value is stored.

#### 7.20.4 Prefix Decrement

Prefix decrement expression is an expression preceded by the operator ‘--’. The expression must be left-hand-side expression (see Left-Hand-Side Expressions).

A compile-time error occurs if type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a prefix decrement expression is the type of the variable. The result of a prefix decrement expression is a value, not a variable.

If evaluation of the operand expression completes normally at runtime, then:

• The value 1 is subtracted from the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the prefix decrement expression completes abruptly, and no decrementation occurs. The value of the prefix decrement expression remains the value of the variable after a new value is stored.

#### 7.20.5 Unary Plus

Unary plus expression is an expression preceded by the operator ‘+’. Type of the operand expression with the unary operator ‘+’ must be convertible (see Implicit Conversions) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

A numeric types conversion is performed on the operand to ensure that the resultant type is that of the unary plus expression. The result of a unary plus expression is always a value, not a variable (even if the result of the operand expression is a variable).

## Page 136

Numeric widening occurs on the expression before a unary plus operator is applied. The type of the unary plus is determined as follows:

• Type of result is int for byte, short, and int;

• Type of result is the same as that of the initial expression for long, float, and double.

#### 7.20.6 Unary Minus

Unary minus expression is an expression preceded by the operator '-'. Type of the operand expression with the unary operator '-' must be convertible (see Widening Numeric Conversions) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

Numeric widening occurs on the expression before a unary minus operator is applied. The type of the unary minus is determined as follows:

• Type of result is int for byte, short, and int;

• Type of result is the same as that of the initial expression for long, float, and double.

The result of a unary minus expression is a value, not a variable (even if the result of the operand expression is a variable).

The unary negation operation is always performed on, and the result is drawn from the same value set as the promoted operand value.

Further value set conversions are then performed on the same result.

The value of a unary minus expression at runtime is the arithmetic negation of the promoted value of the operand.

The negation of integer values is the same as subtraction from zero. The ArkTS programming language uses two's-complement representation for integers. The range of two's-complement value is not symmetric. The same maximum negative number results from the negation of the maximum negative int or long. In that case, an overflow occurs but throws no error. For any integer value x, -x is equal to  $ (\sim x)+1 $.

The negation of floating-point values is not the same as subtraction from zero (if x is +0.0, then 0.0-x is +0.0, however -x is -0.0).

A unary minus merely inverts the sign of a floating-point number. Special cases to consider are as follows:

• Operand NaN results in NaN (NaN has no sign).

• Operand infinity results in the infinity of the opposite sign.

• Operand zero results in zero of the opposite sign.

#### 7.20.7 Bitwise Complement

Bitwise complement operator ‘~’ is applied to an operand of a numeric type or type bigint.

If the type of the operand is double or float, then it is truncated first to long or int, respectively. If the type of the operand is byte or short, then the operand is widened to int. If the type of the operand is bigint, then no conversion is required. Type of result is determined as follows:

• int for byte, short, int, and float.

## Page 137

• long for long and double.

The result of a unary bitwise complement expression is a value, not a variable (even if the result of the operand expression is a variable).

The value of a unary bitwise complement expression at runtime is the bitwise complement of the value of the operand. In all cases,  $ \sim x $ equals  $ (-x)-1 $.

#### 7.20.8 Logical Complement

Logical complement expression is an expression preceded by the operator '!'. Type of the operand expression with the unary '!' operator must be boolean or type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

The unary logical complement expression type is boolean.

The value of a unary logical complement expression is true if the (possibly converted) operand value is false, and false if the operand value (possibly converted) is true.

### 7.21 Multiplicative Expressions

Multiplicative expressions use multiplicative operators ‘*’, ‘/’, and ‘%’.

The syntax of multiplicative expression is presented below:

multiplicativeExpression:
    expression '*' expression
    | expression '/' expression
    | expression '%' expression
    | expression '**' expression
;

Multiplicative operators group left-to-right.

Type of each operand in a multiplicative operator must be convertible (see Numeric Operator Contexts) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

A numeric types conversion (see Widening Numeric Conversions) is performed on both operands to ensure that the resultant type is the type of the multiplicative expression.

The resultant type of an expression is inferred by the largest type after promoting byte and short operands to int:

• double if any operand is double;

• float if any operand is float, and no operand is double;

• long if any operand is long, and no operand is double or float;

• int if all operands are of type byte, short, or int.

This situation is represented in the following example:

## Page 138

// Code below prints true 4 times
let byte1: byte = 1
let byte2: byte = 1
let long1: long = 1
let float1: float = 1
let double1: double = 1

let res_byte = byte1 * byte2 // int
console.log(res_byte instanceof int)

let res_long = byte1 * long1 // long
console.log(res_long instanceof long)

let res_float = byte1 * float1 // float
console.log(res_float instanceof float)

let res_double = byte1 * double1 // double
console.log(res_double instanceof double)

The result of a unary bitwise complement expression is a value, not a variable (even if the operand expression is a variable).

#### 7.21.1 Multiplication

The binary operator ‘*’ performs multiplication, and returns the product of its operands.

Multiplication is a commutative operation if operand expressions have no side effects.

Integer multiplication is associative when all operands are of the same type.

Floating-point multiplication is not associative.

Type of a multiplication expression is the ‘largest’ (see Numeric Types) type of its operands.

If overflow occurs during integer multiplication, then:

• The result is the low-order bits of the mathematical product as represented in some sufficiently large two's-complement format.

• The sign of the result can be other than the sign of the mathematical product of the two operand values.

A floating-point multiplication result is determined in compliance with the IEEE 754 arithmetic:

• The result is NaN if:

- Either operand is NaN;

– Infinity is multiplied by zero.

• If the result is not NaN, then the sign of the result is as follows:

– Positive, where both operands have the same sign; and

– Negative, where the operands have different signs.

• If infinity is multiplied by a finite value, then the multiplication results in a signed infinity (the sign is determined by the rule above).

## Page 139

• If neither NaN nor infinity is involved, then the exact mathematical product is computed.

The product is rounded to the nearest value in the chosen value set by using the IEEE 754 round-to-nearest mode. The ArkTS programming language requires gradual underflow support as defined by IEEE 754 (see Floating-Point Types and Operations).

If the magnitude of the product is too large to represent, then the operation overflows, and the result is an appropriately signed infinity.

The evaluation of a multiplication operator ‘*’ never throws an error despite possible overflow, underflow, or loss of information.

#### 7.21.2 Division

The binary operatorத் /’ performs division and returns the quotient of its left-hand-side and right-hand-side expressions (dividend and divisor respectively).

Integer division rounds toward 0, i.e., the quotient of integer operands n and d, after a numeric types conversion on both (see Widening Numeric Conversions for details), is the integer value q with the largest possible magnitude that satisfies  $ |d \cdot q| \leq |n| $.

Note. The integer value q is:

• Positive, where  $ |n| \geq |d| $, and  $ n $ and  $ d $ have the same sign; but

• Negative, where  $ |n| \geq |d| $, and  $ n $ and  $ d $ have opposite signs.

The only one special case that does not comply with this rule is where integer overflow occurs. The result equals the dividend if the dividend is a negative integer of the largest possible magnitude for its type, while the divisor is -1. No error is thrown in this case despite the overflow.

However, if the divisor value of integer division is detected to be 0 during compilation, then a compile-time error occurs. Otherwise, an ArithmeticError is thrown during execution.

The result of a floating-point division is determined in compliance with the IEEE 754 arithmetic:

• The result is NaN if:

- Either operand is NaN;

– Both operands are infinity; or

- Both operands are zero.

• If the result is not NaN, then the sign of the result is:

– Positive, where both operands have the same sign; or

– Negative, where the operands have different signs.

• Division produces a signed infinity (the sign is determined by the rule above) if:

– Infinity is divided by a finite value; and

– A nonzero finite value is divided by zero.

• Division produces a signed zero (the sign is determined by the rule above) if:

– A finite value is divided by infinity; and

- Zero is divided by any other finite value.

## Page 140

• If neither NaN nor infinity is involved, then the exact mathematical quotient is computed.

If the magnitude of the product is too large to represent, then the operation overflows, and the result is an appropriately signed infinity.

The quotient is rounded to the nearest value in the chosen value set by using the IEEE 754 round-to-nearest mode. The ArkTS programming language requires gradual underflow support as defined by IEEE 754 (see Floating-Point Types and Operations).

The evaluation of a floating-point division operatorத் /' never throws an error despite possible overflow, underflow, division by zero, or loss of information.

The type of the division expression is the ‘largest’ numeric type (see Numeric Types) of its operands.

#### 7.21.3 Remainder

The binary operator ‘%’ yields the remainder of its operands (dividend as the left-hand-side, and divisor as the right-hand-side operand) from an implied division.

The remainder operator in ArkTS accepts floating-point operands (unlike in C and C++).

The remainder operation on integer operands produces a result value, i.e.,  $ (a/b) * b + (a\%b) $ equals a. Numeric type conversion on remainder operation is discussed in Widening Numeric Conversions.

This equality holds even in the special case where the dividend is a negative integer of the largest possible magnitude of its type, and the divisor is -1 (the remainder is then 0). According to this rule, the result of the remainder operation can only be one of the following:

• Negative if the dividend is negative; or

• Positive if the dividend is positive.

The magnitude of the result is always less than that of the divisor.

If the divisor value of integer remainder operator is detected to be 0 during compilation, then a compile-time error occurs. Otherwise, an ArithmeticError is thrown during execution.

The result of a floating-point remainder operation as computed by the operator %' is different than that produced by the remainder operation defined by IEEE 754. The IEEE 754 remainder operation computes the remainder from a rounding division (not a truncating division), and its behavior is different from that of the usual integer remainder operator. On the contrary, ArkTS presumes that the operator %' behaves on floating-point operations in the same manner as the integer remainder operator (comparable to the C library function fmod). The standard library (see Standard Library) routine Math.IEEEremainder can compute the IEEE 754 remainder operation.

The result of a floating-point remainder operation is determined in compliance with the IEEE 754 arithmetic:

• The result is NaN if:

– Either operand is NaN;

– The dividend is infinity;

– The divisor is zero; or

– The dividend is infinity, and the divisor is zero.

• If the result is not NaN, then the sign of the result is the same as the sign of the dividend.

• The result equals the dividend if:

– The dividend is finite, and the divisor is infinity; or

## Page 141

– If the dividend is zero, and the divisor is finite.

• If infinity, zero, or NaN are not involved, then the floating-point remainder  $ r $ from the division of the dividend  $ n $ by the divisor  $ d $ is determined by the mathematical relation  $ r = n - (d \cdot q) $, where  $ q $ is an integer that is only:

– Negative if n/d is negative, or

– Positive if n/d is positive.

• The magnitude of q is the largest possible without exceeding the magnitude of the true mathematical quotient of n and d.

The evaluation of the floating-point remainder operator ‘%’ never throws an error, even if the right-hand operand is zero. Overflow, underflow, or loss of precision cannot occur.

The type of the remainder expression is the 'largest' numeric type (see Numeric Types) of its operands.

#### 7.21.4 Exponentiation

The binary operator ‘**’ yields the result of raising the first operand (base) to the power of the second operand (exponent). The operation returns NaN in the following cases:

• Exponent is NaN;

• Base is NaN, and exponent is not 0;

• Base is  $ \pm1 $, and exponent is  $ \pm\text{Infinity} $; or

• Base is less than 0, and exponent is not an integer.

The binary operator ‘**’ is equivalent to Math.pow(), except it also accepts bigint types as operands.

### 7.22 Additive Expressions

Additive expressions use additive operators '+' and '-'.

The syntax of additive expression is presented below:

additiveExpression:
    expression '+' expression
| expression '-' expression
;

Additive operators group left-to-right.

If either operand of the operator is ‘+’ of type string, then the operation is a string concatenation (see String Concatenation). In all other cases, type of each operand of the operator ‘+’ must be convertible (see Widening Numeric Conversions) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

Type of each operand of the binary operator '-' must be convertible (see Widening Numeric Conversions) to a numeric type (see Numeric Types) in all cases. Otherwise, a compile-time error occurs.

Type of Additive expression is determined as follows:

## Page 142

• string if any operand is of type string;

• Type inferred after widening operands of numeric types by the rules explained in the example in Multiplicative Expressions.

#### 7.22.1 String Concatenation

If one operand of an expression is of type string, then the string conversion (see String Operator Contexts) is performed on the other operand at runtime to produce a string.

String concatenation produces a reference to a string object that is a concatenation of two operand strings. The left-hand-side operand characters precede the right-hand-side operand characters in a newly created string.

If the expression is not a constant expression (see Constant Expressions), then a new string object is created (see New Expressions).

#### 7.22.2 Additive Operators for Numeric Types

A numeric types conversion (see Widening Numeric Conversions) performed on a pair of operands ensures that both operands are of a numeric type. If the conversion fails, then a compile-time error occurs.

The binary operator ‘+’ performs addition and produces the sum of such operands.

The binary operator ‘-’ performs subtraction and produces the difference of two numeric operands.

Type of an additive expression performed on numeric operands is the largest type (see Numeric Types) to which operands of that expression are converted (see Multiplicative Expressions for an example).

If the promoted type is int or long, then integer arithmetic is performed. If the promoted type is float or double, then floating-point arithmetic is performed.

If operand expressions have no side effects, then addition is a commutative operation.

If all operands are of the same type, then integer addition is associative.

Floating-point addition is not associative.

If overflow occurs on an integer addition, then:

• Result is the low-order bits of the mathematical sum as represented in a sufficiently large two's-complement format.

• Sign of the result is opposite to that of the mathematical sum of the operands' values.

The result of a floating-point addition is determined in compliance with the IEEE 754 arithmetic as follows:

• The result is NaN if:

– Either operand is NaN; or

– The operands are two infinities of the opposite signs.

• The sum of two infinities of the same sign is the infinity of that sign.

• The sum of infinity and a finite value equals the infinite operand.

## Page 143

• The sum of two zeros of opposite sign is positive zero.

• The sum of two zeros of the same sign is zero of that sign.

• The sum of zero and a nonzero finite value is equal to the nonzero operand.

• The sum of two nonzero finite values of the same magnitude and opposite sign is positive zero.

• If infinity, zero, or  $ \mathrm{NaN} $ are not involved, and the operands have the same sign or different magnitudes, then the exact sum is computed mathematically.

If the magnitude of the sum is too large to represent, then the operation overflows. The result is an appropriately signed infinity.

Otherwise, the sum is rounded to the nearest value within the chosen value set by using the IEEE 754 round-to-nearest mode. The ArkTS programming language requires gradual underflow support as defined by IEEE 754 (see Floating-Point Types and Operations).

When applied to two numeric type operands (see Numeric Types), the binary operator '-' performs subtraction, and returns the difference of such operands (minuend as left-hand-side, and subtrahend as the right-hand-side operand).

The result of a-b is always the same as that of  $ a+(-b) $ in both integer and floating-point subtraction.

The subtraction from zero for integer values is the same as negation. However, the subtraction from zero for floating-point operands and negation is not the same (if x is +0.0, then 0.0-x is +0.0; however -x is -0.0).

The evaluation of a numeric additive operator never throws an error despite possible overflow, underflow, or loss of information.

### 7.23 Shift Expressions

Shift expressions use shift operators ‘<<’ (left shift), ‘>>’ (signed right shift), and ‘>>>’ (unsigned right shift). The value to be shifted is the left-hand-side operand in a shift operator, and the right-hand-side operand specifies the shift distance.

The syntax of shift expression is presented below:

shiftExpression:
    expression '<<' expression
    | expression '>>' expression
    | expression '>>>' expression
;

Shift operators group left-to-right.

Both operands of a shift expression must be of numeric types or type bigint.

If the type of one or both operands is double or float, then the operand or operands are truncated first to long or int, respectively. If the type of the left-hand-side operand is byte or short, then the operand is converted to int. If both operands are of type bigint, then no conversion is required. A compile-time error occurs if one operand is type bigint, and the other one is a numeric type. Also, a compile-time error occurs if ‘>>>’ (unsigned right shift) is applied to operands of type bigint.

The result of a shift expression is of the type to which its first operand converted.

## Page 144

If the left-hand-side operand is of the promoted type int, then only five lowest-order bits of the right-hand-side operand specify the shift distance (as if using a bitwise logical AND operator ‘&’ with the mask value 0x1f or 0b111111 on the right-hand-side operand). Thus, it is always within the inclusive range of 0 through 31.

If the left-hand-side operand is of the promoted type long, then only six lowest-order bits of the right-hand-side operand specify the shift distance (as if using a bitwise logical AND operator ‘&’ with the mask value 0x3f or 0b111111 the right-hand-side operand). Thus, it is always within the inclusive range of 0 through 63.

Shift operations are performed on the two's-complement integer representation of the value of the left-hand-side operand at runtime.

The value of  $ n \ll s $ is  $ n $ left-shifted by  $ s $ bit positions. It is equivalent to multiplication by two to the power  $ s $ even in case of an overflow.

The value of  $ n \gg s $ is  $ n $ right-shifted by  $ s $ bit positions with sign-extension. The resultant value is  $ floor(n/2s) $. If  $ n $ is non-negative, then it is equivalent to truncating integer division (as computed by the integer division operator by 2 to the power  $ s $).

The value of  $ n \gg \gg $ is n right-shifted by s bit positions with zero-extension, where:

• If n is positive, then the result is the same as that of  $ n \gg s $.

• If $n$ is negative, and type of the left-hand-side operand is int, then the result is equal to that of the expression ($n \gg s$) + (2 \ll \sim s)$.

• If $n$ is negative, and type of the left-hand-side operand is long, then the result is equal to that of the expression $(n>>s)+((2\ as\ long)\ <<\sim s)$.

### 7.24 Relational Expressions

Relational expressions use relational operators ‘<’, ‘>’, ‘<=’, and ‘>=’.

The syntax of relational expression is presented below:

relationalExpression:
    expression <' expression
    | expression '>' expression
    | expression <=' expression
    | expression >=' expression
;

Relational operators group left-to-right.

A relational expression is always of type boolean.

The four kinds of relational expressions are described below. The kind of a relational expression depends on types of operands. It is a compile-time error if at least one type of operands is different from types described below.

## Page 145

#### 7.24.1 Numeric Relational Operators

Type of each operand in a numeric relational operator must be convertible to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

Depending on the converted type of operands, a comparison is performed as follows:

• Signed integer comparison, if the converted operand type is int or long.

• Floating-point comparison, if the converted operand type is float or double.

he comparison of floating-point values drawn from any value set must be accurate.

A floating-point comparison must be performed in accordance with the IEEE 754 standard specification as follows:

• The result of a floating-point comparison is false if either operand is NaN.

• All values other than NaN must be ordered with the following:

– Negative infinity less than all finite values; and

– Positive infinity greater than all finite values.

• Positive zero equals negative zero.

Based on the above presumption, the following rules apply to integer, floating-point, or bigint operands other than NaN:

• The value produced by the operator ‘<’ is true if the value of the left-hand-side operand is less than that of the right-hand-side operand. Otherwise, the value is false.

• The value produced by the operator ‘<=’ is true if the value of the left-hand-side operand is less than or equal to that of the right-hand-side operand. Otherwise, the value is false.

• The value produced by the operator ‘>’ is true if the value of the left-hand-side operand is greater than that of the right-hand-side operand. Otherwise, the value is false.

• The value produced by the operator ‘>=’ is true if the value of the left-hand-side operand is greater than or equal to that of the right-hand-side operand. Otherwise, the value is false.

#### 7.24.2 String Relational Operators

Results of all string comparisons are defined as follows:

• Operator ‘<’ delivers true if the string value of the left-hand-side operand is lexicographically less than the string value of the right-hand-side operand, or false otherwise.

• Operator ‘<=’ delivers true if the string value of the left-hand-side operand is lexicographically less than or equal to the string value of the right-hand-side operand, or false otherwise.

• Operator ‘>’ delivers true if the string value of the left-hand-side operand is lexicographically greater than the string value of the right-hand-side operand, or false otherwise.

• Operator ‘>=’ delivers true if the string value of the left-hand-side operand is lexicographically greater than or equal to the string value of the right-hand operand, or false otherwise.

## Page 146

#### 7.24.3 Boolean Relational Operators

Results of all boolean comparisons are defined as follows:

• Operator ‘<’ delivers true if the left-hand-side operand is false, and the right-hand-side operand is true, or false otherwise.

• Operator ‘<=’ delivers:

- true when both operands are true, or the left-hand-side operand is false for any right-hand value;

– false when the left-hand-side operand is true, and the right-hand-side operand is false.

• Operator ‘>’ delivers true if the left-hand-side operand is true, and the right-hand-side operand is false, or false otherwise.

• Operator ‘>=’ delivers:

– true when both operands are false, or the left-hand-side operand is true for any right-hand-side value;

- false when the left-hand-side operand is false, and the right-hand-side operand is true.

#### 7.24.4 Enumeration Relational Operators

If both operands are of the same enumeration type (see Enumerations), then Numeric Relational Operators or String Relational Operators are used depending on the kind of enumeration constant value (Enumeration Integer Values or Enumeration String Values). Otherwise, a compile-time error occurs.

### 7.25 Equality Expressions

Equality expressions use equality operators ‘==’, ‘===’, ‘!=’, and ‘!==’.

The syntax of equality expression is presented below:

equalityExpression:
    expression ('==' | '===' | '!=' | '!=') expression
;

Equality operators group left-to-right. Equality operators are commutative if operand expressions cause no side effects.

Similarly to relational operators, equality operators return true or false. Equality operators have lower precedence than relational operators, for example,  $ a < b == c < d $ is true when both  $ a < b $ and  $ c < d $ are true.

Any equality expression is of type boolean.

The result produced by a != b and !(a == b) is the same in all cases. The result produced by a !== b and !(a === b) is the same.

The result of the operators ‘==’ and ‘===’ is the same in all cases except when comparing the values null and undefined (see Extended Equality with null or undefined).

A comparison that uses the operators ‘==’ and ‘===’ is evaluated to true when

• Operands of Type boolean have the same value;

## Page 147

• Operands of Type string or string literal type (see String Literal Types) have the same contents;

• Operands after a numeric conversion are of Type bigint (see Numeric Conversions for Relational and Equality Operands) and have the same value;

• Operands after a numeric conversion (see Widening Numeric Conversions, Numeric Conversions for Relational and Equality Operands) are of Numeric Types of the same value except NaN (see Numeric Equality Operators for detail);

• Operands of Type char have the same value (both operands represent the same Unicode code point);

• Operands of the same enumeration type (see Enumerations) have the same numeric values or the same string contents, depending on the type of enumeration constant values;

• Function references that refer to the same functional object (see Function Type Equality Operators for detail).

In all other cases, if types A and B do not overlap (and therefore an expression always evaluated to false at compile time), then:

• if each of A and B is either a predefined type or a union of predefined types, a compile-time-error is issued..

• in all other cases, a compile-time warning is issued.

Note. There are two main reasons why compiler do not use always a compile-time error:

• Compatibility with TypeScript code base

• The inferred smart type (see Smart Types) could lead in some cases to triggering the error even in the case when it is impossible at runtime (see an example below):

class B {
    f(): B|undefined { return undefined }
}
class D extends B {
    f(): D { return this }
}
function f(c: B) {
    if (c.instanceof D) {
        // smart type causes compile-time warning
        c.f() == undefined
    }
}

An evaluation of equality expressions always uses the actual types of operands as in the example below:

function equ(a: Object, b: Object): boolean {
    return a == b
}

equ(1, 1) // true, values are compared
equ(1, 2) // false, value are compared

equ("aa", "aa") // true, string contexts are compared
equ(1, "aa") // false, not compatible types

(continues on next page)

## Page 148

interface I1 {}
interface I2 {}

function equ1 (i1: I1, i2: I2) {
    return i1 == i2 // to be resolved during program execution
}

class A implements I1, I2 {}

const a = new A

equ1 (a, a) // true, the same values

An equality with values of two union types is represented in the example below:

function f1(x: number | string, y: boolean | null): boolean {
    return x == y // compile-time error, always evaluates to false
}

function f2(x: number | string, y: boolean | "abc"): boolean {
    // ok, can be evaluated as true
    return x == y
}

#### 7.25.1 Numeric Equality Operators

Type of each operand in a numeric equality operator must be convertible to a numeric type (see Numeric Types) as described in Numeric Conversions for Relational and Equality Operands. Otherwise, a compile-time error occurs.

A widening conversion can occur (see Widening Numeric Conversions) if type of one operand is smaller than type of the other operand (see Numeric Types).

If the converted type of the operands is int or long, then an integer equality test is performed.

If the converted type is float or double, then a floating-point equality test is performed.

The floating-point equality test must be performed in accordance with the following IEEE 754 standard rules:

• The result of ‘==’ or ‘===’ is false but the result of ‘!=’ is true if either operand is NaN.

The test x != x or x !== x is true only if x is NaN.

• Positive zero equals negative zero.

• Equality operators consider two distinct floating-point values unequal in any other situation.

For example, if one value represents positive infinity, and the other represents negative infinity, then each compares equal to itself and unequal to all other values.

Based on the above presumptions, the following rules apply to integer operands or floating-point operands other than NaN:

• If the value of the left-hand-side operand is equal to that of the right-hand-side operand, then the operator ‘==’ or ‘===’ produces the value true. Otherwise, the result is false.

• If the value of the left-hand-side operand is not equal to that of the right-hand-side operand, then the operator '!=' or '!==' produces the value true. Otherwise, the result is false.

## Page 149

1 5 == 5 // true
2 5 != 5 // false
3
4 5 === 5 // true
5
6 5 == new Number(5) // true
7 5 === new Number(5) // true
8
9 5 == 5.0 // true

#### 7.25.2 Function Type Equality Operators

If both operands refer to the same function object, then the comparison returns true. When comparing method references, not only the same method must be used, but also its bounded instances must be equal.

function foo() {}
function bar() {}
function goo(p: number) {}

foo == foo // true, same function object
foo == bar // false, different function objects
foo == goo // false, different function objects

class A {
    method() {}
    static method() {}
    foo () {}
}
const a = new A
a.method == a.method // true, same function object
A.method == A.method // true, same function object

const aa = new A
a.method == aa.method /* false, different function objects
    as 'a' and 'aa' are different bounded objects */
a.method == a.foo // false, different function objects

#### 7.25.3 Extended Equality with null or undefined

ArkTS provides extended semantics for equalities with null and undefined to ensure better alignment with TypeScript.

If one operand in an equality expression is null, and other is undefined, then the operator '!=' returns true, and the operator '!==' returns false:

## Page 150

function foo(x: Object | null, y: Object | null | undefined) {
    console.log(x == y, x === y)
}

foo(null, undefined) // output: true, false
foo(null, null) // output: true, true

Comparison the values null and undefined directly is also allowed:

console.log(null == undefined) // output: true
console.log(null === undefined) // output: false

### 7.26 Bitwise and Logical Expressions

The bitwise operators and logical operators are as follows:

• AND operator ‘&’;

• Exclusive OR operator ‘^’; and

• Inclusive OR operator '|'.

The syntax of bitwise and logical expression is presented below:

bitwiseAndLogicalExpression:
    expression '&' expression
    | expression '^' expression
    | expression '|' expression
;

These operators have different precedence. The operator '&' has the highest, while '|' has the lowest precedence.

Operators group left-to-right. Each operator is commutative if the operand expressions have no side effects, and associative.

The bitwise and logical operators can compare two operands of a numeric type, or two operands of the boolean type. Otherwise, a compile-time error occurs.

#### 7.26.1 Integer Bitwise Operators

Integer bitwise operators are ‘&’, ‘^’, and ‘|’ applied to operands of numeric types or type bigint.

If the type of one or both operands is double or float, then the operand or operands are truncated first to the appropriate integer type. If the type of any operand is byte or short, then the operand is converted to int. If operands are of different integer types, then the operand of a smaller type is converted to a larger type (see Numeric Types) by using Widening Numeric Conversions. If both operands are of type bigint, then no conversion is required. A compile-time error occurs if one operand of type bigint, and the other operand is of a numeric type.

The resultant type of the bitwise operator is the type of its operands.

## Page 151

The resultant value of ‘&’ is the bitwise AND of the operand values.

The resultant value of ‘^’ is the bitwise exclusive OR of the operand values.

The resultant value of ‘|’ is the bitwise inclusive OR of the operand values.

#### 7.26.2 Boolean Logical Operators

Boolean logical operators are ‘&’, ‘^’, and ‘|’ applied to operands of type boolean.

If both operand values are true, then the resultant value of ‘&’ is true. Otherwise, the result is false. If the operand values are different, then the resultant value of ‘^’ is true. Otherwise, the result is false. If both operand values are false, then the resultant value of ‘|’ is false. Otherwise, the result is true. Thus, boolean logical expression is of the boolean type.

### 7.27 Conditional-And Expression

The conditional-and operator ‘&&’ is similar to ‘&’ (see Bitwise and Logical Expressions) but evaluates its right-hand-side operand only if the value of the left-hand-side operand is true.

The computation results of ‘&&’ and ‘&’ on boolean operands are the same. The right-hand-side operand of ‘&&’ is not necessarily evaluated.

The syntax of conditional-and expression is presented below:

conditionalAndExpression:
expression '&&' expression
;

A conditional-and operator groups left-to-right.

A conditional-and operator is fully associative as regards both the result value and side effects (i.e., the evaluations of the expressions ((a) && (b)) && (c) and (a) && ((b) && (c)) produce the same result, and the same side effects occur in the same order for any a, b, and c).

A conditional-and expression is always of type boolean except the extended semantics (see Extended Conditional Expressions). A conditional-and expression with extended semantics can be of the first expression type.

Each operand of the conditional-and operator must be of type boolean, or of a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

The left-hand-side operand expression is first evaluated at runtime.

If the resultant value is false, then the value of the conditional-and expression is false. The evaluation of the right-hand-side operand expression is omitted.

If the value of the left-hand-side operand is true, then the right-hand-side expression is evaluated. The resultant value is the value of the conditional-and expression.

## Page 152

### 7.28 Conditional-Or Expression

The conditional-or operator ‘||’ is similar to ‘|’ (see Integer Bitwise Operators) but evaluates its right-hand-side operand only if the value of its left-hand-side operand is false.

The syntax of conditional-or expression is presented below:

conditionalOrExpression:
expression '||' expression
;

A conditional-or operator groups left-to-right.

A conditional-or operator is fully associative as regards both the result value and side effects (i.e., the evaluations of the expressions ((a) || (b)) || (c) and (a) || ((b) || (c)) produce the same result, and the same side effects occur in the same order for any a, b, and c).

A conditional-or expression is always of type boolean except the extended semantics (see Extended Conditional Expressions). A conditional-or expression with extended semantics can be of the first expression type.

Each operand of the conditional-or operator must be of type boolean or type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

The left-hand-side operand expression is first evaluated at runtime.

If the resultant value is true, then the value of the conditional-or expression is true, and the evaluation of the right-hand-side operand expression is omitted.

If the resultant value is false, then the right-hand-side expression is evaluated. The resultant value is the value of the conditional-or expression.

The computation results of ‘||’ and ‘|’ on boolean operands are the same, but the right-hand-side operand in ‘||’ cannot be evaluated.

### 7.29 Assignment

All assignment operators group right-to-left (i.e., a = b = c means a = (b = c). The value of c is thus assigned to b, and then the value of b to a).

The syntax of assignment expression is presented below:

assignmentExpression:
lhsExpression assignmentOperator rhsExpression
;
assignmentOperator
: '='
| '+=' | '-=' | '*=' | '=' | '%=' | '**=' | '=/='
| '<<=' | '>>>=' | '>>>='
| '&=' | '|=' | '^='

(continues on next page)

## Page 153

lhsExpression:
  expression
;
rhsExpression:
  expression
;

The first operand in an assignment operator represented by lhsExpression must be left-hand-side expression (see Left-Hand-Side Expressions). This first operand denotes a variable.

Type of the variable is the type of the assignment expression.

The result of the assignment expression at runtime is not a variable itself but the value of a variable after the assignment.

#### 7.29.1 Simple Assignment Operator

The form of a simple assignment expression is lhsExpression = rhsExpression.

A compile-time error occurs in the following situations:

• Type of rhsExpression is not assignable (see Assignability) to the type of the variable; or

• Type of lhsExpression is one of the following:

– readonly array (see Readonly Parameters), while the converted type of rhsExpression is a non-readonly array;

– readonly tuple (see Readonly Parameters), while the converted type of rhsExpression is a non-readonly tuple.

Otherwise, the assignment expression is evaluated at runtime in one of the following ways:

1. If lhsExpression is a field access expression e.f (see Field Access Expression), possibly enclosed in parentheses, then:

1. lhsExpression e is evaluated: if the evaluation of e completes abruptly, then so does the assignment expression.

2. rhsExpression is evaluated: if the evaluation completes abruptly, then so does the assignment expression.

3. If that evaluation completes normally, then the value of  $ rhsExpression $ is converted to the type of the field. In that case, the result of the conversion is assigned to the field.

2. If the lhsExpression is an array reference expression (see Array Indexing Expression), possibly enclosed in parentheses, then:

1. Array reference subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression and the index subexpression are not evaluated, and no assignment occurs.

2. If the evaluation completes normally, then the index subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

## Page 154

3. If the evaluation completes normally, then  $ rhsExpression $ is evaluated. If this evaluation completes abruptly, then so does the assignment expression, and no assignment occurs.

4. If the evaluation completes normally, but the value of the index subexpression is less than zero, or greater than, or equal to the length of the array, then RangeError is thrown, and no assignment occurs.

5. If lhsExpression denotes indexing of fixed-size array, and the type of rhsExpression is not a subtype of array element type, then ArrayStoreError is thrown, and no assignment occurs.

6. Otherwise, the value of the index subexpression is used to select an element of the array referred to by the value of the array reference subexpression and the value of rhsExpression is converted to the type of the array element. In that case, the result of the conversion is assigned to the array element.

3. If lhsExpression is a record access expression (see Record Indexing Expression), possibly enclosed in parentheses, then:

1. Object reference subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression and the index subexpression are not evaluated, and no assignment occurs.

2. If the evaluation completes normally, the index subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

3. If the evaluation completes normally, rhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

4. Otherwise, the value of the index subexpression is used as the key, and the value of rhsExpression converted to the type of the record value is used as the value. In that case, the assignment results in storing the key-value pair in the record instance.

If none of the above is true, then the following three steps are performed:

1. lhsExpression is evaluated to produce a variable. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

2. If the evaluation completes normally, then  $ rhsExpression $ is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

3. If that evaluation completes normally, then the value of  $ rhsExpression $ is converted to the type of the left-hand-side variable. In that case, the result of the conversion is assigned to the variable.

#### 7.29.2 Compound Assignment Operators

A compound assignment expression in the form:

lhsExpression op= rhsExpression

is equivalent to

lhsExpression = ((lhsExpression) op (rhsExpression)) as T

where T is type of lhsExpression, except that lhsExpression is evaluated only once.

While the nullish-coalescing assignment (??=) only evaluates the right operand, and assigns to the left operand if the left operand is null or undefined.

An assignment expression can be evaluated at runtime in one of the following ways:

1. If lhsExpression is not an indexing expression:

## Page 155

• lhsExpression is evaluated to produce a variable. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

• If the evaluation completes normally, then the value of lhsExpression is saved, and rhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, then the saved value of the left-hand-side variable, and the value of rhsExpression are used to perform the binary operation as indicated by the compound assignment operator. If the operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, then the result of the binary operation converts to the type of the left-hand-side variable. The result of such conversion is stored into the variable.

2. If lhsExpression is an array reference expression (see Array Indexing Expression), then:

• Array reference subexpression of lhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, the index subexpression, and rhsExpression are not evaluated, and no assignment occurs.

• If the evaluation completes normally, then the index subexpression of lhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

• If the evaluation completes normally, the value of the array reference subexpression refers to an array, and the value of the index subexpression is less than zero, greater than, or equal to the length of the array, then RangeError is thrown. In that case, no assignment occurs.

• If the evaluation completes normally, then the value of the index subexpression is used to select an array element referred to by the value of the array reference subexpression. The value of this element is saved, and then  $ rhsExpression $ is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, consideration must be given to the saved value of the array element selected in the previous step. While this element is a variable of type S, and T is type of lhsExpression of the assignment operator determined at compile time:

– If T is a predefined value type, then S is the same as T.

The saved value of the array element, and the value of rhsExpression are used to perform the binary operation of the compound assignment operator.

If this operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

If this evaluation completes normally, then the result of the binary operation converts to the type of the selected array element. The result of the conversion is stored into the array element.

– If T is a reference type, then it must be string.

S must also be a string because the class string is the final class. The saved value of the array element, and the value of rhsExpression are used to perform the binary operation (string concatenation) of the compound assignment operator ‘+=’. If this operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

– If the evaluation completes normally, then the string result of the binary operation is stored into the array element.

3. If lhsExpression is a record access expression (see Record Indexing Expression):

## Page 156

- The object reference subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, the index subexpression and rhsExpression are not evaluated, and no assignment occurs.

• If this evaluation completes normally, then the index subexpression of lhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

• If this evaluation completes normally, the value of the object reference subexpression and the value of index subexpression are saved, then  $ rhsExpression $ is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If this evaluation completes normally, the saved values of the object reference subexpression and index subexpression (as the key) are used to get the value that is mapped to the key (see Record Indexing Expression), then this value and the value of rhsExpression are used to perform the binary operation as indicated by the compound assignment operator. If the operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, then the result of the binary operation is stored as the key-value pair in the record instance (as in Simple Assignment Operator).

#### 7.29.3 Left-Hand-Side Expressions

Left-hand-side expression is an expression that is one of the following:

• Named variable;

• Field or setter resultant from a field access (see Field Access Expression); or

• Array or record element access (see Indexing Expressions).

A compile-time error occurs in the following situations:

• Expression contains the chaining operator ‘?.’ (see Chaining Operator);

• Result of expression is not a variable.

### 7.30 Ternary Conditional Expressions

The ternary conditional expression ‘condition?whenTrue:whenFalse’ uses the boolean value of the first expression (condition) to decide which of other two expressions to evaluate:

ternaryConditionalExpression:
    expression '?' expression ':' expression
;

The ternary conditional operator groups right-to-left (i.e., the meaning of a?b : c?d : e?f : g and a?b : (c?d : (e?f : g)) is the same).

The ternary conditional operator 'condition?whenTrue:whenFalse' consists of three operand expressions with the separators '?' between the first and the second expression, and '?' between the second and the third expression.

## Page 157

A compile-time error occurs if the first expression is not of type boolean, or a type mentioned in Extended Conditional Expressions.

Type of the ternary conditional expression is determined as the union of types of the second and the third expressions further normalized in accordance with the process discussed in Union Types Normalization. If the second and the third expressions are of the same type, then this is the type of the conditional expression.

The following steps are performed as the evaluation of a ternary conditional expression occurs at runtime:

1. The first operand (condition) of a ternary conditional expression is evaluated first.

2. If the value of the first operand is true, then the second operand expression (whenTrue) is evaluated. Otherwise, the third operand expression (whenFalse) is evaluated. The result of successful evaluation is the result of the ternary conditional expression.

The examples below represent different scenarios with standalone expressions:

class A {}
class B extends A {}

condition ? new A() : new B() // A | B => A

condition ? 5 : 6 // int

condition ? "5" : 6 // "5" | int

### 7.31 String Interpolation Expressions

'String interpolation expression' is a multiline string literal, i.e., a string literal delimited with backticks (see Multiline String Literal for detail) that contains at least one embedded expression.

The syntax of string interpolation expression is presented below:

stringInterpolation:
    ''' (BacktickCharacter | embeddedExpression)* ' '
;
embeddedExpression:
    '${' expression ' }'
;

An ‘embedded expression’ is an expression specified inside curly braces preceded by the dollar sign ‘$’. A string interpolation expression is of type string (see Type string).

When evaluating a string interpolation expression, the result of each embedded expression substitutes that embedded expression. An embedded expression must be of type string. Otherwise, the implicit conversion to string takes place in the same way as with the string concatenation operator (see String Concatenation):

let a = 2
let b = 2
console.log('The result of ${a} * ${b} is ${a * b}')
// prints: The result of 2 * 2 is 4

## Page 158

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

## Page 159

The usage of annotations is discussed in Using Annotations.

The examples of usage are presented below:

(x: number): number => { return Math.sin(x) } // block as lambda body
(x: number) => Math.sin(x) // expression as lambda body
e => e // shortest form of lambda

A lambda expression evaluation creates an instance of a function type (see Function Types) as described in detail in Runtime Evaluation of Lambda Expressions.

#### 7.32.1 Lambda Signature

Similarly to function declarations (see Function Declarations), a lambda signature is composed of formal parameters and optional return types. Unlike function declarations, type annotations of formal parameters can be omitted.

function foo<T> (a: (p1: T, ...p2: T[]) => T) {}
// All calls to foo pass valid lambda expressions in different forms
foo (e => e)
foo ((e1, e2) => e1)
foo ((e1, e2: Object) => e1)
foo ((e1: Object, e2) => e1)
foo ((e1: Object, e2, e3) => e1)
foo ((e1: Object, ...e2) => e1)

foo ((e1: Object, e2: Object) => e1)

function bar<T> (a: (...p: T[]) => T) {}
// Type can be omitted for the rest parameter
bar ((...e) => e)

function goo<T> (a: (p?: T) => T) {}
// Type can be omitted for the optional parameter
goo ((e?) => e)

The specification of scope is discussed in Scopes, and shadowing details of formal parameter declarations in Shadowing by Parameter.

A compile-time error occurs if:

• Lambda expression declares two formal parameters with the same name.

• Formal parameter contains no type provided, and type cannot be derived by Type Inference.

## Page 160

#### 7.32.2 Lambda Body

Lambda body can be a single expression or a block (see Block). Similarly to the body of a method or a function, a lambda body describes the code to be executed when a lambda expression call occurs (see Function Call Expression).

The meanings of names, and of the keywords this and super (along with the accessibility of the referred declarations) are the same as in the surrounding context. However, lambda parameters introduce new names.

If any local variable or formal parameter of the surrounding context is used but not declared in a lambda body, then the local variable or formal parameter is captured by the lambda.

If an instance member of the surrounding type is used in the lambda body defined in a method, then this is captured by the lambda.

A compile-time error occurs if a local variable is used in a lambda body but is neither declared in nor assigned before it.

If a lambda body is a single expression, then it is handled as follows:

• If the expression is a call expression with return type void, then the body is equivalent to the block: { expression }.

• Otherwise, the body is equivalent to the block: { return expression }.

If lambda signature return type is not void (see Type void) or never (see Type never), and the execution path of the lambda body has no return statement (see return Statements) or no single expression as a body, then a compile-time error occurs.

#### 7.32.3 Lambda Expression Type

Lambda expression type is a function type (see Function Types) that has the following:

• Lambda parameters (if any) as parameters of the function type; and

• Lambda return type as the return type of the function type.

Note. Lambda return type can be inferred from the lambda body and thus the return type can be dropped off.

const lambda = () => { return 123 } // Type of the lambda is () => int

const int_var: int = lambda()

#### 7.32.4 Runtime Evaluation of Lambda Expressions

The evaluation of a lambda expression itself never causes the execution of the lambda body. If completing normally at runtime, the evaluation of a lambda expression produces a new instance of a function type (see Function Types) that corresponds to the lambda signature. In that case, it is similar to the evaluation of a class instance creation expression (see New Expressions).

If the available space is not sufficient for a new instance to be created, then the evaluation of the lambda expression completes abruptly, and OutOfMemoryError is thrown.

Every time a lambda expression is evaluated, the outer variables referred to by the lambda expression are captured as follows:

## Page 161

function foo() {
    let y: int = 1
    let x = () => { return y + 1 } // 'y' is *captured*.
    console.log(x()) // Output: 2
}

The captured variable is not a copy of the original variable. If the value of the variable captured by the lambda changes, then the original variable is implied to change:

function foo() {
    let y: int = 1
    let x = () => { y++ } // 'y' is *captured*.
    console.log(y) // Output: 1
    x()
    console.log(y) // Output: 2
}

Capturing within the function scope is highlighted by the following example:

function capturingFunction() { // Function scope
    let v: number = 0 // A captured variable
    return (p: number) => {
        console.log("Previous value: ", v, " new value: ", p)
        v = p
    }
}

const func1 = capturingFunction()
const func2 = capturingFunction()
// Note: func1 and func2 are two different function type instances
func1(11) // Previous value: 0 new value: 11
func2(22) // Previous value: 0 new value: 22
func1(33) // Previous value: 11 new value: 33
func2(44) // Previous value: 22 new value: 44
/* Note:
    func1 calls work with their own version of variable 'v'
    func2 calls work with their own version of variable 'v'
*/

Capturing within the loop scope is highlighted by the following example:

const l = () => {}
const storage = [1, 1, 1, 1, 1] // fill array with some lambdas

for (let index = 0; index < 5; index++) {
    storage [index] = () => { console.log("Index ", index) }
    // Every lambda captures loop index variable
}
for (let index = 0; index < 5; index++) {
    storage[index]() // Captured indices printed
}

## Page 162

### 7.33 Constant Expressions

Constant expressions are expressions with values that can be evaluated at compile time.

The syntax of constant expression is presented below:

constantExpression: expression
;

A constant expression is an expression of a value type (see Value Types), or of type string that completes normally while being composed only of the following:

• Literals of a predefined value types, and literals of type string (see Literals);

• Enumeration type constants;

• Unary operators ‘+’, ‘-’, ‘~’, and ‘!’, but not ‘++’ or ‘--’ (see Unary Plus, Unary Minus, Prefix Increment, and Prefix Decrement);

• Casting conversions to numeric types (see Cast Expression);

• Multiplicative operators ‘*’, ‘/’, and ‘%’ (see Multiplicative Expressions);

• Additive operators ‘+’ and ‘-’ (see Additive Expressions);

• Shift operators ‘<<’, ‘>>’, and ‘>>>’ (see Shift Expressions);

• Relational operators ‘<', ‘<=', ‘>', and ‘>=' (see Relational Expressions);

• Equality operators ‘==’ and ‘!=’ (see Equality Expressions);

• Bitwise and logical operators ‘&', ‘^', and ‘|’ (see Bitwise and Logical Expressions);

• Conditional-and operator ‘&&’ (see Conditional-And Expression), and conditional-or operator ‘||’ (see Conditional-Or Expression);

• Ternary conditional operator 'condition?whenTrue:whenFalse' (see Ternary Conditional Expressions);

• Parenthesized expressions (see Parenthesized Expression) that contain constant expressions;

• Simple names or qualified names that refer to constants (see Constant Declarations) with constant expressions as initializers, declared in the same module.

The examples of constant expressions are presented below:

const a = 2

// Constant expressions:
1 + 2
a + 1
"aa" + "bb"
(a < 0) || (a > 5)

Note. The following expressions are not constant expressions:

## Page 163

let x = 2

// non-constant expressions:
x + 1
0x7f as short

## Page 164

## Page 165

## STATEMENTS

Statements are designed to control execution.

The syntax of statements is presented below:

statement:
    expressionStatement
    | block
    | localDeclaration
    | ifStatement
    | loopStatement
    | breakStatement
    | continueStatement
    | returnStatement
    | switchStatement
    | throwStatement
    | tryStatement
;

### 8.1 Normal and Abrupt Statement Execution

The actions that every statement performs in a normal mode of execution are specific for the particular kind of statement. Normal modes of evaluation for each kind of statement are described in the following sections.

A statement execution is considered to complete normally if the desired action is performed without an error being thrown. On the contrary, a statement execution is considered to complete abruptly if it causes an error thrown.

### 8.2 Expression Statements

Any expression can be used as a statement.

The syntax of expression statement is presented below:

## Page 166

expressionStatement:
  expression
;

The execution of a statement leads to the execution of the expression. The result of such execution is discarded.

### 8.3 Block

A sequence of statements (see Statements) enclosed in balanced braces forms a block.

The syntax of block statement is presented below:

block:
 '{' statement* '}'
;

The execution of a block means that all block statements, except type declarations, are executed one after another in the textual order of their appearance within the block while an error is thrown (see Errors), or until a return occurs (see return Statements).

If a block is the body of a functionDeclaration (see Function Declarations) or a classMethodDeclaration (see Method Declarations) declared implicitly or explicitly with return type void (see Type void), then the block can contain no return statement at all. Such a block is equivalent to one that ends in a return statement, and is executed accordingly.

### 8.4 Local Declarations

Local declarations define new mutable or immutable variables within the enclosing context.

Let and const declarations have the initialization part that presumes execution, and actually act as statements.

The syntax of local declaration is presented below:

localDeclaration:
    annotationUsage?
    ( variableDeclaration
    | constantDeclaration
)
;

## Page 167

The visibility of a local declaration name is determined by the surrounding function or method, and by the block scope rules (see Scopes). In order to avoid ambiguous interpretation, appropriate sections of this Specification are dedicated to a detailed discussion of the following entities:

• if Statements,

• for Statements,

• for-of Statements.

The usage of annotations is discussed in Using Annotations.

### 8.5 if Statements

An if statement allows executing alternative statements (if provided) under certain conditions.

The syntax of if statement is presented below:

ifStatement:
    'if '(' expression ')' thenStatement
    ('else' elseStatement)?
;
thenStatement:
statement
;
elseStatement:
statement
;

Type of expression must be boolean, or a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

If an expression is successfully evaluated as true, then a thenStatement is executed. Otherwise, an elseStatement is executed (if provided).

Any else corresponds to the nearest preceding if of an if statement:

if (Cond1)
    if (Cond2) statement1
    else statement2 // Executes only if: Cond1 && !Cond2

A Block can be used to combine the else part with the initial if as follows:

if (Cond1) {
    if (Cond2) statement1
}
else statement2 // Executes if: !Cond1

If thenStatement or elseStatement is any kind of a statement but not a block (see Block), then no block scope (see Scopes) is created for such a statement.

## Page 168

function foo(Cond1: boolean) {
    if (Cond1) let x: number = 1
    x = 2 // OK

    if (Cond1) {
        let x: number = 10; // OK, then-block scope
        let y: number = x;
    }
    else {
        let x: number = 20 // OK, no conflict, else-block scope
        y = x; // CTE, no y in scope
    }

    console.log(x) // OK, prints 2
    console.log(y) // CTE, y unknown
}

### 8.6 Loop Statements

ArkTS has four kinds of loops. A loop of each kind can be optionally labelled with an identifier. The identifier can be used only by the break Statements and continue Statements contained in the loop body.

The syntax of loop statements is presented below:

loopStatement:
    (identifier '：')?
    whileStatement
        | doStatement
        | forStatement
        | forOfStatement
    ;

A compile-time error occurs if the label identifier is not used within loopStatement, or is used in lambda expressions (see Lambda Expressions) within a loop body.

label: for (i = 1; i < 10; i++) {
    const f1 = () => {
        while (true) {
            continue label // Compile-time error
        }
    }
    const f2 = () => {
        do
            break label // Compile-time error
        while (true)
    }
}

## Page 169

### 8.7 while Statements and do Statements

A while statement and a do statement evaluate an expression and execute the statement repeatedly till the expression value is true. The key difference is that a whileStatement starts from evaluating and checking the expression value, and a doStatement starts from executing the statement.

The syntax of while and do statements is presented below:

whileStatement:
    'while' ('expression') statement
;
doStatement
    : 'do' statement 'while' ('expression')
;

Type of expression must be boolean, or a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

### 8.8 for Statements

The syntax of for statements is presented below:

forStatement:
    'for ' (' forInit? '; ' forContinue? '; ' forUpdate? ')' statement
;
forInit:
    expressionSequence
| variableDeclarations
;
forContinue:
    expression
;
forUpdate:
    expressionSequence
;

Type of forContinue expression must be boolean, or a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

// existing variable is used as a loop index variable
let i: number
for (i = 1; i < 10; i++) {

(continues on next page)

## Page 170

console.log(i)

// new variable is declared as a loop index variable with its type
// explicitly specified
for (let i: number = 1; i < 10; i++) {
    console.log(i)
}

// new variable is declared as loop index variable with its type
// inferred from its initialization part of the declaration
for (let i = 1; i < 10; i++) {
    console.log(i)
}

A variable declared in the forInit-part has the loop scope. It can be used in a forContinue expression, a forUpdate expression, a single-body statement, or in a body block if enclosed in parentheses:

// forInit declaration and no body block
let k: number = 0
for (let i: number = 1; i < 10; i++)
    k += i
console.log(k)
// i = k // CTE when uncommented
let i: number = k // OK

### 8.9 for-of Statements

A for-of loop iterates elements of array or string, or an instance of iterable class or interface (see Iterable Types).

The syntax of for-of statements is presented below:

forOfStatement:
    'for' ('forVariable 'of' expression ')' statement
;

forVariable:
    identifier | ('let' | 'const') identifier (':' type)?
;

A compile-time error occurs if the type of an expression is not array, string, or an iterable type.

The execution of a for-of loop starts from the evaluation of expression. If the evaluation is successful, then the resultant expression is used for loop iterations (execution of the statement). On each iteration, forVariable is set to successive elements of the array, string, or the result of class iterator advancement.

If forVariable has the modifiers let or const, then a new variable is declared in the loop scope. The new variable is accessible only inside the loop body. Otherwise, the variable is as declared above. The modifier const prohibits assignments into forVariable, while let allows modifications.

## Page 171

The type of forVariable declared inside the loop is inferred to be that of the iterated elements, namely:

• T, if Array<T> or FixedArray<T> instance is iterated;

• string, if string value is iterated;

• Type argument of the iterator, if an instance of the iterable type is iterated.

If forVariable is declared outside the loop, then the type of an iterated element must be assignable (see Assignability) to the type of the variable. Otherwise, a compile-time error occurs.

// existing variable 's'
let s : string
for (s of "a string object") {
    console.log(s)
}

// new variable 's', its type is inferred from expression after 'of'
for (let s of "a string object") {
    console.log(s)
}

// new variable 'element', its type is inferred from expression after 'of'.
// as 'const' it cannot be assigned with a new value in the loop body
for (const element of [1, 2, 3]) {
    console.log(element)
    element = 66 // Compile-time error as 'element' is 'const'
}

Explicit type annotation of forVariable is allowed as an experimental feature (see For-of Explicit Type Annotation).

### 8.10 break Statements

A break statement transfers control out of the enclosing loopStatement or switchStatement. If a break statement is used outside a loopStatement or a switchStatement, then a compile-time error occurs.

The syntax of break statement is presented below:

breakStatement:
'break' identifier?
;

A break statement with the label identifier transfers control out of the enclosing statement with the same label identifier. If there is no enclosing loop statement with the same label identifier (within the body of the surrounding function or method), then a compile-time error occurs.

A statement without a label transfers control out of the innermost enclosing switch, while, do, for, or for-of statement. If breakStatement is placed outside loopStatement or switchStatement, then a compile-time error occurs.

Examples of break statements with and without a label are presented below:

## Page 172

// Single iteration
while (true) {
    console.log("iteration") // get printed exactly once
    break;
}

let a: number = 0
outer:
do {
    for (a = 0; a < 10; a++) {
        if (a == 1) break outer
            console.log("inner") // get printed only once
        }
        console.log(a) // Never reached
    } while (true) // condition never used

### 8.11 continue Statements

A continue statement stops the execution of the current loop iteration, and transfers control to the next iteration. Appropriate checks of loop exit conditions depend on the kind of the loop.

The syntax of continue statement is presented below:

continueStatement:
    'continue' identifier?
;

A continue statement with no label transfers control to the next iteration of the enclosing loop statement. If there is no enclosing loop statement within the body of the surrounding function or method, then a compile-time error occurs.

A continue statement with the label identifier transfers control to the next iteration of the enclosing loop statement with the same label identifier. If there is no enclosing loop statement with the same label identifier (within the body of the surrounding function or method), then a compile-time error occurs.

Examples of continue statements with and without a label are presented below:

// continue    // would cause CTE if uncommented

// continue without label
// will print 0, 1, 2, 4 (3 skipped)
for (let a: number = 0; a < 5; a++) {
    if (a == 3) continue
        console.log("a = " + a)
}

let a: number
outer:
    do {
        for (a = 0; a < 10; a++) {
            if (a > 1) continue outer

(continues on next page)

## Page 173

console.log("inner") // get printed only twice

console.log("Outer") // Never reached

} while (false)

### 8.12 return Statements

A return statement can have or not have an expression.

The syntax of return statement is presented below:

returnStatement:
    'return' expression?
;

A return statement with expression can only occur inside a function, a method, or a lambda body with non-void return type.

A return statement (with no expression) can occur inside one of the following:

• Initializer block;

• Constructor body;

• Function, method, or lambda body with return type void (see Type void);

A compile-time error occurs if a return statement is found in:

• Top-level statements (see Top-Level Statements);

• Functions or methods with return type void (see Type void) that have an expression;

• Functions or methods with a non-void return type that have no expression.

The execution of a returnStatement leads to the termination of the surrounding function, method, or initializer. If an expression is provided, the resultant value is the evaluated expression.

In case of constructors, initializer blocks, and top-level statements, the control is transferred out of the scope of the construction, but no result is required. Other statements of the surrounding function, method body, initializer block, or top-level statement are not executed.

### 8.13 switch Statements

A switch statement transfers control to a statement or a block by using the result of successful evaluation of the value of a switch expression.

The syntax of switch statement is presented below:

## Page 174

switchStatement:
    (identifier ':()? 'switch' ('expression ')' switchBlock
    ;
switchBlock
    : '{' caseClause* defaultClause? caseClause* '}'
    ;
caseClause
    : 'case' expression ':' statement*
    ;
defaultClause
    : 'default' ':' statement*
    ;

The switch expression type must be of type char, byte, short, int, long, string, or enum.

If available, an optional identifier allows the break statement to transfer control out of a nested switch or loop statement (see break Statements).

A compile-time error occurs if not all of the following is true:

• Every case expression type is assignable (see Assignability) to the type of the switch statement expression.

• In a switch statement expression of type enum, every case expression associated with the switch statement is of type enum.

• No two case constant expressions (see Constant Expressions) have identical values.

• No case expression is null.

let arg = prompt("Enter a value?");
switch (arg) {
    case '0':
        case '1':
            console.log('One or zero')
            break
        case '2':
            console.log('Two')
            break
    default:
        console.log('An unknown value')
}

The execution of a switch statement starts from the evaluation of the switch expression.

The value of the switch expression is compared repeatedly to the value of case expressions starting from the top till the first match. The match means that particular case expression value equals the value of the switch expression in terms of the operator ‘==’. However, if the expression value is of type string, then the equality for strings determines the equality.

So, in case of match execution is transferred to the set of statements of the caseClause where match occurred. If this set of statements executes break statement then the whole switch statement terminates. If no break statement was executed then execution continues through all remaining caseClause*s as well as *defaultClause at last if it is present. If no match occurred and defaultClause is present then it is executed.

## Page 175

### 8.14 throw Statements

A throw statement causes an error object to be created and raised (see Error Handling). It immediately transfers control, and can exit multiple statements, constructors, functions, and method calls until a try statement (see try Statements) is found that catches the value thrown. If no try statement is found, then UncaughtExceptionError is thrown.

The syntax of throw statement is presented below:

throwStatement:
    'throw' expression
;

The expression type must be assignable (see Assignability) to type Error. Otherwise, a compile-time error occurs.

This implies that the object thrown is never null.

Errors can be thrown at any place in the code.

### 8.15 try Statements

A try statement runs block of code, and provides optional catch clause to handle errors (see Error Handling) which may occur during block of code execution.

The syntax of try statement is presented below:

tryStatement:
    'try' block catchClause? finallyClause?
;
catchClause:
    'catch' ('identifier ')' block
;
finallyClause:
    'finally' block
;

A try statement must contain either a finally clause, or a catch clause. Otherwise, a compile-time error occurs.

If the try block completes normally, then no action is taken, and no catch clause block is executed.

If an error is thrown in the try block directly or indirectly, then the control is transferred to the catch clause.

## Page 176

#### 8.15.1 catch Clause

A catch clause consists of two parts:

• A catch identifier that provides access to an object associated with the error thrown; and

• A block of code that handles the error.

The type of catch identifier inside the block is Error (see Error Handling).

class ZeroDivisor extends Error {}

function divide(a: number, b: number): number {
    if (b == 0)
        throw new ZeroDivisor()
    return a / b
}

function process(a: number, b: number): number {
    try {
        let res = divide(a, b)
        // further processing ...
        return res
    }
    catch (e) {
        return e instanceof ZeroDivisor? -1 : 0
    }
}

A catch clause handles all errors at runtime. It returns '-1' for the ZeroDivisor, and '0' for all other errors.

#### 8.15.2 finally Clause

A finally clause defines the set of actions in the form of a block to be executed without regard to whether a try-catch completes normally or abruptly.

The syntax of finally clause is presented below:

finallyClause:
'finally' block
;

A finally block is executed without regard to how (by reaching return or try-catch end or raising new error) the program control is transferred out. The finally block is particularly useful to ensure proper resource management.

Any required actions (e.g., flush buffers and close file descriptors) can be performed while leaving the try-catch:

class SomeResource {
    // some API
    // ...
    close() {}
}

(continues on next page)

## Page 177

function ProcessFile(name: string) {
    let r = new SomeResource()
    try {
        // some processing
    }
    finally {
        // finally clause will be executed after try-catch is
        executed normally or abruptly
        r.close()
    }
}

#### 8.15.3 try Statement Execution

1. A try block and the entire try statement complete normally if no catch block is executed. The execution of a try block completes abruptly if an error is thrown inside the try block.

2. The the execution of a try block completes abruptly if error x is thrown inside the try block. If the catch clause is present, and the execution of the body of the catch clause completes normally, then the entire try statement completes normally. Otherwise, the try statement completes abruptly.

3. If no catch clause is in place, then the error is propagated to the surrounding and caller scopes until reaching the scope with the catch clause to handle the error. If there is no such scope, then the whole coroutine stack (see Coroutines (Experimental)) is discarded. Subsequent steps are then defined by the execution environment.

4. If finally clause is in place, and its execution completes abruptly, then the try statement also completes abruptly.

## Page 178

## Page 179

## CLASSES

Class declarations introduce new reference types and describe the manner of their implementation.

A class body contains declarations and initializer blocks.

Declarations can introduce class members (see Class Members) or class constructors (see Constructor Declaration).

The body of the declaration of a member comprises the scope of a declaration (see Scopes).

Class members include:

• Fields.

• Methods, and

Class members can be declared or inherited.

• Accessors.

Every member is associated with the class declaration it is declared in.

Field, method, accessor and constructor declarations can have the following access modifiers (see Access Modifiers):

• Public.

• Protected.

• Private.

Every class defines two class-level scopes (see Scopes): one for instance members, and the other for static members. It means that two members of a class can have the same name if one is static while the other is not.

### 9.1 Class Declarations

Every class declaration defines a class type, i.e., a new named reference type.

The class name is specified by an identifier inside a class declaration.

If typeParameters are defined in a class declaration, then that class is a generic class (see Generics).

The syntax of class declaration is presented below:

classDeclaration:

    classModifier? 'class' identifier typeParameters?

    classExtendsClause? implementsClause?

(continues on next page)

## Page 180

(continued from previous page)

classMembers
;

classModifier:
'abstract' | 'final'
;

Classes with the final modifier are an experimental feature discussed in Final Classes.

The scope of a class declaration is specified in Scopes.

An example of a class is presented below:

class Point {
    public x: number
    public y: number
    public constructor(x : number, y : number) {
        this.x = x
        this.y = y
    }
    public distanceBetween(other: Point): number {
        return Math.sqrt(
            (this.x - other.x) * (this.x - other.x) +
            (this.y - other.y) * (this.y - other.y)
        )
    }
    static origin = new Point(0, 0)
}

#### 9.1.1 Abstract Classes

A class with the modifier abstract is known as abstract class. An abstract class is a class that cannot be instantiated, i.e., no objects of this type can be created. It serves as a blueprint for other classes by defining common fields and methods that subclasses must implement. Abstract classes can contain both abstract and concrete methods.

A compile-time error occurs if an attempt is made to create an instance of an abstract class:

abstract class X {
    field: number
    constructor (p: number) { this.field = p }
}
let x = new X(42)
// Compile-time error: Cannot create an instance of an abstract class.

Subclasses of an abstract class can be abstract or non-abstract. A non-abstract subclass of an abstract superclass can be instantiated. As a result, a constructor for the abstract class, and field initializers for non-static fields of that class are executed:

abstract class Base {
    field: number

(continues on next page)

## Page 181

constructor (p: number) { this.field = p }
}

class Derived extends Base {
    constructor (p: number) { super(p) }
}

A method with the modifier abstract is considered an abstract method (see Abstract Methods). Abstract methods have no bodies, i.e., they can be declared but not implemented.

Only abstract classes can have abstract methods. A compile-time error occurs if a non-abstract class has an abstract method:

class Y {
    abstract method (p: string)
    /* Compile-time error: Abstract methods can only
        be within an abstract class. */
}

A compile-time error occurs if an abstract method declaration contains the modifiers final or override.

abstract class Y {
    final abstract method (p: string)
    // Compile-time error: Abstract methods cannot be final
}

### 9.2 Class Extension Clause

All classes except class Object can contain the extends clause that specifies the base class, or the direct superclass of the current class. In this situation, the current class is a derived class, or a direct subclass. Any class, except class Object that has no extends clause, is assumed to have the extends Object clause.

The syntax of class extension clause is presented below:

classExtendsClause:
    'extends' typeReference
;

A compile-time error occurs if:

• typeReference refers directly to, or is an alias of any non-class type, e.g., of interface, enumeration, union, function, or utility type.

• Class type named by typeReference is not accessible (see Accessible).

• An extends clause appears in the declaration of the class Object.

• The extends graph has a cycle.

Class extension implies that a class inherits all members of the direct superclass.

Note. Private members are inherited from superclasses, but are not accessible (see Accessible) within subclasses:

## Page 182

class Base {
    /* All methods are accessible in the class where they were declared */
    public publicMethod () {
        this.protectedMethod()
        this.privateMethod()
    }
    protected protectedMethod () {
        this.publicMethod()
        this.privateMethod()
    }
    private privateMethod () {
        this.publicMethod();
        this.protectedMethod()
    }
}
class Derived extends Base {
    foo () {
        this.publicMethod() // OK
        this.protectedMethod() // OK
        this.privateMethod() // compile-time error:
            // the private method is inaccessible
    }
}

The transitive closure of a direct subclass relationship is the subclass relationship. Class A can be a subclass of class C if:

• Class A is the direct subclass of C; or

• Class A is a subclass of some class B, which is in turn a subclass of C (i.e., the definition applies recursively).

Class C is a superclass of class A if A is its subclass.

### 9.3 Class Implementation Clause

A class can implement one or more interfaces. Interfaces to be implemented by a class are listed in the implements clause. Interfaces listed in this clause are direct superinterfaces of the class.

The syntax of class implementation clause is presented below:

implementsClause:
    'implements' interfaceTypeList
;
interfaceTypeList:
    typeReference (',' typeReference)*
;

A compile-time error occurs if typeReference fails to name an accessible interface type (see Accessible).

## Page 183

// File1
interface I { } // Not exported

// File2
import {I} from "File1"
class C implements I {}

// Compile-time error I is not accessible

If some interface is repeated as a direct superinterface in a single implements clause (even if that interface is named differently), then all repetitions are ignored.

For the class declaration C <F₁, ..., Fₙ>(n ≥ 0, C ≠ Object):

- Direct superinterfaces of class type C <F₁, ..., Fₙ> are the types specified in the implements clause of the declaration of C (if there is an implements clause).

For the generic class declaration C <F₁, ..., Fₙ> (n > 0):

• Direct superinterfaces of the parameterized class type C < T₁, ..., Tₙ> are all types I < U₁θ, ..., Uₖθ> if:

-  $ T_i $ ( $ 1 \leq i \leq n $) is a type;

– I <U₁, …, Uₖ> is the direct superinterface of C <F₁, …, Fₙ>; and

− θ is the substitution  $ [F_1 := T_1, \ldots, F_n := T_n] $.

Interface type I is a superinterface of class type C if I is one of the following:

• Direct superinterface of C;

- Superinterface of J which is in turn a direct superinterface of C (see Superinterfaces and Subinterfaces that defines superinterface of an interface); or

• Superinterface of the direct superclass of C.

A class implements all its superinterfaces.

A compile-time error occurs if a class implements two interface types that represent different instantiations of the same generic interface (see Generics).

If a class is not declared abstract, then:

• Any abstract method of each direct superinterface is implemented (see Inheritance) by a declaration in that class.

• The declaration of an existing method is inherited from a direct superclass, or a direct superinterface.

A compile-time error occurs if a class field has the same name as a method from one of superinterfaces implemented by the class, except when one is static and the other is not.

#### 9.3.1 Implementing Interface Methods

If superinterfaces have more than one default implementation (see Default Interface Method Declarations) for some method m, then:

• The class that implements these interfaces has method that overrides m (see Override-Compatible Signatures); or

• There is a single interface method with default implementation that overrides all other methods; or

## Page 184

• All interface methods refer to the same implementation, and this default implementation is the current class method.

Otherwise, a compile-time error occurs.

interface I1 { foo () {} }
interface I2 { foo () {} }
class C1 implements I1, I2 {
    foo () {} // foo() from C1 overrides both foo() from I1 and foo() from I2
}

class C2 implements I1, I2 {
    // Compile-time error as foo() from I1 and foo() from I2 have different_
    →implementations
}

interface I3 extends I1 {
    interface I4 extends I1 {
        class C3 implements I3, I4 {
            // OK, as foo() from I3 and foo() from I4 refer to the same implementation
        }
    }

    interface I5 extends I1 { foo() {} } // override method from I1
    class C4 implements I1, I5 {
        // Compile-time error as foo() from I1 and foo() from I5 have different_
    →implementations
}

class Base {
    class Derived extends Base {
        interface IBase {
            foo(p: Base) {}
        }
        interface IDerived {
            foo(p: Derived) {}
        }
        class C implements IBase, IDerived {} // foo() from IBase overrides foo() from IDerived
        new C().foo(new Base) // foo() from IBase is called
    }
}

A single method declaration in a class is allowed to implement methods of one or more superinterfaces.

#### 9.3.2 Implementing Required Interface Properties

A class must implement all required properties from all superinterfaces (see Interface Properties) that can be defined in a form of a field or as a getter, a setter, or both. In any case implementation may be provided in a form of field or accessors.

The following table summarizes all valid variants of implementation, and a compile-time error occurs for any other combinations:

## Page 185

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Form of Interface Property</td><td style='text-align: center; word-wrap: break-word;'>Implementation in a Class</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>readonly field</td><td style='text-align: center; word-wrap: break-word;'>readonly field, field, getter, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>getter only</td><td style='text-align: center; word-wrap: break-word;'>readonly field, field, getter, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>field</td><td style='text-align: center; word-wrap: break-word;'>field, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>getter and setter</td><td style='text-align: center; word-wrap: break-word;'>field, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>setter only</td><td style='text-align: center; word-wrap: break-word;'>field, setter, or setter and getter</td></tr></table>

Providing implementation for the property in the form of a field is not necessary:

interface Style {
    get color(): string
        set color(s: string)
    }

    class StyleClassOne implements Style {
        color: string = ""
    }

    class StyleClassTwo implements Style {
        private color_: string = ""

        get color(): string {
            return this.color_
        }

        set color(s: string) {
            this.color_ = s
        }
    }
}

If a property is implemented as a field, then any required accessors and a private hidden field are defined implicitly. Entities for StyleClassOne are implicitly defined as follows:

class StyleClassOne implements Style {
    private $$_color: string = "" // the exact name of the field is implementation_
    →specific
    get color(): string { return this.$$_color }
    set color(s: string) { this.$$_color = s }
}

If a property is defined in a form that requires a setter, then the implementation of the property in the form of a readonly field causes a compile-time error:

interface Style {
    set color(s: string)
        可可
        可可
    }

    class StyleClassTwo implements Style {
        readonly color: string = "" // compile-time error
        readonly writable: number = 0 // compile-time error
    }
}

(continues on next page)

## Page 186

(continued from previous page)

function write_into_read_only (s: Style) {
    s.color = "Black"
    s.可可
    s.可可
}
write_into_read_only (new StyleClassTwo)

If a property is defined in the  $ \underline{\text{readonly}} $ form, then the implementation of the property can either keep the  $ \underline{\text{readonly}} $ form or extend it to a  $ \underline{\text{writable}} $ form as follows:

interface Style {
    get color(): string
    readonly readable: number
}

class StyleClassThree implements Style {
    get color(): string { return "Black" }
    set color(s: string) {} // OK!
    readable: number = 0 // OK!
}

function how_to_write (s: Style) {
    s.color = "Black" // compile-time error
    s.readable = 42 // compile-time error
    if (s.instanceof StyleClassThree) {
        let s1 = s as StyleClassThree
        s1.color = "Black" // OK!
        s1.readable = 42 // OK!
    }
}

how_to_write (new StyleClassThree)

#### 9.3.3 Implementing Optional Interface Properties

A class can implement Optional Interface Properties) from superinterfaces or use implicitly defined accessors from an interface.

The use of accessors implicitly defined in the interface is represented in the example below:

interface I {
    n?: number
}
class C implements I {}

let c = new C()
console.log(c.n) // Output: undefined
c.n = 1 // runtime error is thrown

## Page 187

The implementation of an optional interface property as a field is represented in the example below:

interface I {
    num?: number
}
class C implements I {
    num?: number = 42
}

For the example above, the private hidden field and the required accessors are defined implicitly for the class C overriding accessors from the interface:

class C implements I {
    private $$_num: number = 42 // the exact name of the field is implementation specific
    get num(): number | undefined { return this.$_num }
    set num(n: number | undefined) { this.$_num = n }
}

If a property is implemented by accessors (see Class Accessor Declarations), then it is acceptable to implement only one accessor for an optional field, and use default implementation for another accessor as represented in the following example:

interface I {
    num?: number
}

class C1 implements I { // OK, both default implementations
    }

    class C2 implements I { // OK, default implementation used for get set num(n: number | undefined) { this.$_num = n }
    }

    class C3 implements I { // OK, both explicit implementations get num(): number | undefined { return this.$_num }
    set num(n: number | undefined) { this.$_num = n }
}

A compile-time error occurs, if an optional property in an interface is implemented as non-optional field:

interface I {
    num?: number
}

class C implements I {
    num: number = 42 // compile-time error, must be optional
}

## Page 188

### 9.4 Class Members

A class can contain declarations of the following members:

• Fields.

• Methods.

• Accessors.

• Constructors.

• Method overloads (see Class Method Overload Declarations),

• Constructor overloads (see Constructor Overload Declarations), and

• Single static block for initialization (see Static Initialization).

The syntax is presented below:

classMembers:
    '{}
        classMember* staticBlock? classMember*
    '}'
;

classMember:
    annotationUsage?
    accessModifier?
    ( constructorDeclaration
        | overloadConstructorDeclaration
        | classFieldDeclaration
        | classMethodDeclaration
        | overloadMethodDeclaration
    | classAccessorDeclaration
)
;
staticBlock: 'static' Block;

Declarations can be inherited or immediately declared in a class. Any declaration within a class has a class scope. The class scope is fully defined in Scopes.

Members can be static or non-static as follows:

• Static members that are not part of class instances, and can be accessed by using a qualified name notation (see Names) anywhere the class name is accessible (see Accessible); and

• Non-static, or instance members that belong to any instance of the class.

Names of all static and non-static entities in a class declaration scope (see Scopes) must be unique, i.e., fields, methods, and overloads with the same static or non-static status cannot have the same name.

The use of annotations is discussed in Using Annotations.

Class members are as follows:

## Page 189

• Members inherited from their direct superclass (see Inheritance), except class Object that cannot have a direct superclass.

• Members declared in a direct superinterface (see Superinterfaces and Subinterfaces).

• Members declared in the class body (see Class Members).

Class members declared private are not accessible (see Accessible) to all subclasses of the current class.

Class members declared protected or public are inherited by all subclasses of the class and accessible (see Accessible) for all subclasses.

Constructors and static block are not members, and are not inherited.

Members can be as follows:

• Class fields (see Field Declarations),

• Methods (see Method Declarations), and

• Accessors (see Class Accessor Declarations).

A method is defined by the following:

1. Type parameter, i.e., the declaration of any type parameter of the method member.

2. Argument type, i.e., the list of types of arguments applicable to the method member.

3. Return type, i.e., the return type of the method member.

### 9.5 Access Modifiers

Access modifiers define how a class member or a constructor can be accessed. Accessibility in ArkTS can be of the following kinds:

• Private.

• Protected.

• Public.

The desired accessibility of class members and constructors can be explicitly specified by the corresponding access modifiers.

The syntax of class members or constructors modifiers is presented below:

accessModifier: 'private' | 'protected' | 'public'

If no explicit modifier is provided, then a class member or a constructor is implicitly considered public by default.

## Page 190

#### 9.5.1 Private Access Modifier

The modifier private indicates that a class member or a constructor is accessible (see Accessible) within its declaring class, i.e., a private member or constructor m declared in some class C can be accessed only within the class body of C:

class C {
    private count: number
    getCount(): number {
        return this.count // ok
    }
}

function increment(c: C) {
    c.count++ // compile-time error - 'count' is private
}

#### 9.5.2 Protected Access Modifier

The modifier protected indicates that a class member or a constructor is accessible (see Accessible) only within its declaring class and the classes derived from that declaring class. A protected member M declared in some class C can be accessed only within the class body of C or of a class derived from C:

class C {
    protected count: number
        getCount(): number {
            return this.count // ok
        }
}

class D extends C {
    increment() {
        this.count++ // ok, D is derived from C
    }
}

function increment(c: C) {
    c.count++ // compile-time error - 'count' is not accessible
}

#### 9.5.3 Public Access Modifier

The modifier public indicates that a class member or a constructor can be accessed everywhere, provided that the member or the constructor belongs to a type that is also accessible (see Accessible).

## Page 191

### 9.6 Field Declarations

Field declarations represent data members in class instances or static data members (see Static and Instance Fields). Class instance field declarations are its own fields in contrast to the inherited ones. Syntactically, a field declaration is similar to a variable declaration.

classFieldDeclaration:
    fieldModifier*
    identifier
    ('??': 'type initializer?
    | '?? initializer
    | '!! ':' type
)
;
fieldModifier:
    'static' | 'readonly' | 'override'
;

A field with an identifier marked with ‘?’ is called optional field (see Optional Fields). A field with an identifier marked with ‘!’ is called field with late initialization (see Fields with Late Initialization).

A compile-time error occurs if:

• Some field modifier is used more than once in a field declaration.

• Name of a field declared in the body of a class declaration is also used for a method of this class with the same static or non-static status.

• Name of a field declared in the body of a class declaration is also used for another field in the same declaration with the same static or non-static status.

Any static field can be accessed only with the qualification of a superclass name (see Field Access Expression).

A class can inherit more than one field or property with the same name from its superinterfaces, or from both its superclass (see Inheritance) and superinterfaces (see Interface Inheritance. However, an attempt to refer to such a field or property by its simple name within the class body causes a compile-time error.

The same field or property declaration can be inherited from an interface in more than one way. In that case, the field or property is considered to be inherited only once.

#### 9.6.1 Static and Instance Fields

There are two categories of class fields as follows:

• Static fields

Static fields are declared with the modifier static. A static field is not part of a class instance. There is one copy of a static field irrespective of how many instances of the class (even if zero) are eventually created.

Static fields are always accessed by using a qualified name notation wherever the class name is accessible (see Accessible).

• Instance, or non-static fields

## Page 192

Instance fields belong to each instance of the class. An instance field is created for, and associated with a newly-created instance of a class, or of its superclass. An instance field is accessible (see Accessible) via the instance name.

#### 9.6.2 Readonly (Constant) Fields

A field with the modifier `readonly` is a `readonly` field. Changing the value of a `readonly` field after `initialization` is not allowed. Both static and non-static fields can be declared `readonly` fields.

#### 9.6.3 Optional Fields

Optional field f?: T = expr effectively means that the type of f`is `T | undefined. If an initializer is absent in a field declaration, then the default value undefined (see Default Values for Types) is used as the initial value of the field.

For example, the following two fields are actually defined the same way:

class C {
    f?: string
    g: string | undefined = undefined
}

#### 9.6.4 Field Initialization

All fields except Fields with Late Initialization are initialized by using the default value (see Default Values for Types) or a field initializer (see below). Otherwise, the field can be initialized in one of the following:

• Initializer block of a static field (see Static Initialization), or

• Class constructor of a non-static field (see Constructor Declaration).

Field initializer is an expression that is evaluated at compile time or runtime. The result of successful evaluation is assigned into the field. The semantics of field initializers is therefore similar to that of assignments (see Assignment). Each initializer expression evaluation and the subsequent assignment are only performed once.

Readonly fields initialization never uses default values (see Default Values for Types).

The initializer of a non-static field declaration is evaluated at runtime. The assignment is performed each time an instance of the class is created.

The instance field initializer expression cannot use the following directly in any form:

• super; or

• this.

## Page 193

If the initializer expression contains one of the above patterns, then a compile-time error occurs.

If allowed in the code, the above restrictions can break the consistency of class instances as shown in the following examples:

class C {
    a = this     // Compile-time error

    f1 = this.foo()  // Compile-time error as 'this' method is invoked

    f2 = "a string field"

    foo(): string {
        // Type safety requires fields to be initialized before access
        console.log(this.f1, this.f2)
        return this.f2
    }

    class B {}
    function foo(f: () => B) { return f() }
    class A {
        field1 = foo(() => this.field2)  // Compile-time error as this is used in the_
        → initializer code
        field2 = new B
    }
}

#### 9.6.5 Fields with Late Initialization

Field with late initialization must be an instance field. If it is defined as static, then a compile-time error occurs.

Field with late initialization cannot be of a nullish type (see Nullish Types). Otherwise, a compile-time error occurs.

As all other fields, a field with late initialization must be initialized before it is used for the first time. However, this field can be initialized later and not within a class declaration. Initialization of this field can be performed in a constructor (see Constructor Declaration), although it is not mandatory.

Field with late initialization cannot have field initializers or be an optional field (see Optional Fields). Field with late initialization must be initialized explicitly, even though its type has a default value.

The fact of initialization of field with late initialization is checked when the field value is read. The check is normally performed at runtime. If the compiler identifies an error situation, then the error is reported at compile time:

class C {
    f!: string
}

let x = new C()
x.f = "aa"
console.log(x.f) // ok

(continues on next page)

## Page 194

(continued from previous page)

let y = new C()
console.log(y.f) // runtime or compile-time error

Note. Access to a field with late initialization in most cases is less performant than access to other fields.

TypeScript uses the term definite assignment assertion for the notion similar to late initialization. However, ArkTS uses stricter rules.

#### 9.6.6 Overriding Fields

When extending a class or implementing interfaces, a field declared in a superclass or a superinterface can be overridden by a field with the same name, and the same static or non-static modifier status. Using the keyword override is not required. The new declaration acts as redeclaration.

A compile-time error occurs if:

• Field marked with the modifier override does not override a field from a superclass.

• Field declaration contains the modifier static along with the modifier override.

• Types of the overriding field and of the overridden field are different.

class C {
    field: number = 1
}

class D extends C {
    field: string = "aa" // compile-time error: type is not the same
    override no_field = 1224 // compile-time error: no overridden field in the base_
    →class
        static override field: string = "aa" // compile-time error: static cannot override
}

Initializers of overridden fields are preserved for execution, and the initialization is normally performed in the context of superclass constructors.

class C {
    field: number = this.init()
    private init() {
        console.log("Field initialization in C")
        return 123
    }
}

class D extends C {
    override field: number = 123 // field can be explicitly marked as overridden
}

class Derived extends D {
    field = this.init_in_derived()
    private init_in_derived() {
        console.log("Field initialization in Derived")
        return 42
    }
}

(continues on next page)

## Page 195

(continued from previous page)

{
    }
}

new Derived()

/* Output:
    Field initialization in C
    Field initialization in Derived
*/

A compile-time error occurs if a field is not declared as `ready` in a `superclass`, while an `overriding` field is marked as `ready`:

class C {
    field = 1
}
class D extends C {
    readonly field = 2 // compile-time error, wrong overriding
}

A compile-time error occurs if a field overrides getter or setter in a superclass:

class C {
    get num(): number { return 42 }
    set num(x: number) {}
}
class D extends C {
    num: number = 2 // compile-time error, wrong overriding
}

The same compile-time error occurs in more complex case, where a field simultaneously overrides a field from a superclass and implements a property from a superinterface:

class C {
    num: number = 1
}
interface I {
    num: number
}
class D extends C implements I {
    num: number = 2 // compile-time error, conflict in overriding
}

The overriding conflict occurs as num in D, and must be both:

• Field to override a field inherited from the superclass C; and

• Two accessors (see Class Accessor Declarations) to implement a property from the superinterface ‘I’ (see Implementing Required Interface Properties).

Overriding a field by an accessor also causes a compile-time error as follows:

class C {
    num: number = 1
}
class D extends C {

(continues on next page)

## Page 196

get num(): number { return 42 } // compile-time error, wrong overriding
set num(x: number) {} // compile-time error, wrong overriding
}

### 9.7 Method Declarations

Methods declare executable code that can be called.

The syntax of class method declarations is presented below:

classMethodDeclaration:
    methodModifier* identifier typeParameters? signature block?
;

methodModifier:
    'abstract'
| 'static'
| 'final'
| 'override'
| 'native'
| 'async'
;

The identifier in a class method declaration defines the method name that can be used to refer to a method (see Method Call Expression).

Methods with the final modifier is an experimental feature discussed in detail in Final Methods.

A compile-time error occurs if:

• Method modifier appears more than once in a method declaration;

• Body of a class declaration declares a method but the name of that method is already used for a field in the same declaration.

A non-static method declared in a class can do the following:

• Implement a method inherited from a superinterface or superinterfaces (see Implementing Interface Methods);

• Override a method inherited from a superclass (see Overriding in Classes);

• Act as method declaration of a new method.

A static method declared in a class can do the following:

• Shadow a static method inherited from a superclass (see Static Methods);

• Act as method declaration of a new static method.
