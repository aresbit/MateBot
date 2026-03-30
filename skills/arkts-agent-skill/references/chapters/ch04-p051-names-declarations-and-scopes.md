# Chapter 4: Names, Declarations and Scopes

Page range: 51-66

## Page 51

#### 3.17.2 Readonly Array Types

Readonly array type is immutable, i.e.:

• Length of a variable of a readonly array type cannot be changed;

• Elements of a reasonably array type cannot be modified after the initial assignment directly nor through a function or method call.

Otherwise, a compile-time error occurs.

let x: readonly number [] = [1, 2, 3]
x[0] = 42 // compile-time error as array itself is readonly

Readonly array type with elements of type T can have the following two syntax forms:

• readonly T[] and

• ReadonlyArray<T>.

Both forms specify identical (indistinguishable) types (see Type Identity).

Note. In arrays of arrays, all arrays are readonly.

### 3.18 Tuple Types

Tuple type is a reference type created as a fixed set of other types.

The syntax of tuple type is presented below:

tupleType:
  '[' (type (',' type)* ',?)?' ]'
;

The value of a tuple type is a group of values of types that comprise the tuple type. The number of values in the group equals the number of types in a tuple type declaration. The order of types in a tuple type declaration specifies the type of the corresponding value in the group.

It implies that each element of a tuple has its own type. The operator ‘[]’ (square brackets) is used to access the elements of a tuple in a manner similar to accessing the elements of an array.

An index expression must be of integer type. The index of the first tuple element is 0. Only constant expressions can be used as the index providing access to tuple elements:

let tuple: [number, number, string, boolean, Object] =
[6, 7, "abc", true, 42]
tuple[0] = 42
console.log(tuple[0], tuple[4]) // `42 42` be printed

A tuple does not have length property so the legal TypeScript code like below issues compile-time error in ArkTS:

## Page 52

let tuple : [number, string] = [1, ""]
for (let index = 0; index < tuple.length; index++) { // compile-time error
    // no 'length' property
    let element: Object = tuple[index]
    // do something with the element
}

Any tuple type is assignable (see Assignability) to class Object (see Type Object).

An empty tuple is a corner case. It is only added to support TypeScript compatibility:

let empty: [] = [] // empty tuple with no elements in it

#### 3.18.1 Readonly Tuple Types

If an tuple type has the prefix  $ \underline{\text{are}} $  $ \underline{\text{are}} $  $ \underline{\text{are}} $  $ \underline{\text{are}} $  $ \underline

let x: readonly [number, string] = [1, "abc"]
x[0] = 42 // compile-time error as tuple itself is readonly

### 3.19 Function Types

Function type can be used to express the expected signature of a function. A function type consists of the following:

• Optional type parameters;

• List of parameters (which can be empty);

• Optional return type.

The syntax of function type is as follows:

functionType:
    '(' ftParameterList? ')' ftReturnType
;
ftParameterList:
    ftParameter (',' ftParameter)* (',' ftRestParameter)?
    | ftRestParameter
;
ftParameter:
    identifier ('？')？ '：' type
;
ftRestParameter:

(continues on next page)

## Page 53

(continued from previous page)

'...' ftParameter
;
ftReturnType:
'=>' type
;

let binaryOp: (x: number, y: number) => number
function evaluate(f: (x: number, y: number) => number) { }

The rest parameter is described in Rest Parameter.

A type alias can set a name for a function type (see Type Alias Declaration):

type BinaryOp = (x: number, y: number) => number
let op: BinaryOp

If a function type has the ‘?’ mark for a parameter name, then this parameter and all parameters that follow (if any) are optional. Otherwise, a compile-time error occurs. The actual type of the parameter is then a union of the parameter type and type undefined. This parameter has no default value.

type FuncTypeWithOptionalParameters = (x?: number, y?: string) => void
let foo: FuncTypeWithOptionalParameters
    = ():void => {} // OK: as arguments are just ignored
foo = (p: number):void => {} // CTE as call with zero arguments is invalid
foo = (p?: number):void => {} // OK: as call with zero or one argument is valid
foo = (p1: number, p2?: string):void => {} // Compile-time error: as call with zero__
arguments is invalid
foo = (p1?: number, p2?: string):void => {} // OK

foo()
foo(undefined)
foo(undefined, undefined)
foo(42)
foo(42, undefined)
foo(42, "a string")

type IncorrectFuncTypeWithOptionalParameters = (x?: number, y: string) => void
// compile-time error: no mandatory parameter can follow an optional parameter

function bar (
    p1?: number,
    p2: number | undefined
) {
    p1 = p2 // OK
    p2 = p1 // OK
    // Types of p1 and p2 are identical
}

More details on function types assignability are provided in Subtyping for Function Types.

## Page 54

#### 3.19.1 Type Function

Type Function is a predefined type that is a direct superinterface of any function type.

A value of type Function cannot be called directly. A developer must use the unsafeCall method instead. This method checks the arguments of type Function, and calls the underlying function value if the number and types of the arguments are valid.

function foo(n: number) {}

let f: Function = foo

f(1) // compile-time error: cannot be called

f.unsafeCall(3.14) // correct call and execution
f.unsafeCall() // runtime error: wrong number of arguments

Another important property of type Function is name. It is a string that contains the name associated with the function object in the following way:

• If a function or a method is assigned to a function object, then the associated name is that of the function or of the method;

• If a lambda is assigned to a variable of Function type, then the associated name is that of the variable;

• Otherwise, the string is empty.

function print_name (f: Function) {
    console.log(f.name)
}

function foo() {}
print_name(foo) // output: "foo"

class A {
    static sm() {}
    m() {}
}

print_name(A.sm) // output: "sm"
print_name(new A().m) // output: "m"

let x: Function = (): void => {}
print_name(x) // output: "x"

let y = x
print_name(y) // output: "x"

print_name ((): void=>{}) // output: ""

The declarations of the unsafeCall method, name property, and all other methods and properties of type Function are included in the ArkTS Standard Library.

## Page 55

### 3.20 Union Types

Union type is a reference type created as a combination of other types.

The syntax of union type is as follows:

unionType:
    type ('|' type)*
;

A compile-time error occurs if the type in the right-hand side of a union type declaration leads to a circular reference.

Typical usage examples of union types are represented below:

The values of a union type are valid values of all types the union is created from.

type OperationResult = "Done" | "Not done"
function do_action(): OperationResult {
    if (someCondition) {
        return "Done"
    } else {
        return "Not done"
    }
}

class Cat {
    // ...
}

class Dog {
    // ...
}

class Frog {
    // ...
}

type Animal = Cat | Dog | Frog | number
// Cat, Dog, and Frog are some types (class type or interface type)

let animal: Animal = new Cat()
animal = new Frog()
animal = 42
// One may assign the variable of the union type with any valid value

enum StringEnum {One = "One", Two = "Two"}

type Union1 = string | StringEnum // OK, will be reduced during normalization

Values of particular types can be received from a union by using different mechanisms as follows:

class Cat { sleep () {}; meow () {} }
class Dog { sleep () {}; bark () {} }
class Frog { sleep () {}; leap () {} }

type Animal = Cat | Dog | Frog

let animal: Animal = new Cat()

(continues on next page)

## Page 56

if (animal.instanceof Frog) {
    // animal is of type Frog here, conversion can be used:
    let frog: Frog = animal as Frog
    frog.leap()
}
animal.sleep() // Any animal can sleep

(continued from previous page)

Predefined types are represented by the following example:

type Predefined = number | boolean
let p: Predefined = 7
if (p instanceof number) {
    // type of 'p' is number here
}

Literal types are represented by the following example:

type BMW_ModelCode = "325" | "530" | "735"
let car_code: BMW_ModelCode = "325"
if (car_code == "325") {
    car_code = "530"
} else if (car_code == "530") {
    car_code = "735"
} else {
    // pension :-)
}

Note. A compile-time error occurs if an expression of a union type is compared to a literal value or a constant that does not belong to the values of the union type:

type BMW_ModelCode = "325" | "530" | "735"
let car_code: BMW_ModelCode = "325"
if (car_code == "234") { ... }
/*
compile-time error as "234" does not belong to values of literal type BMW_ModelCode
*/
function model_code_test (code: string) {
    if (car_code == code) { ... }
    // This test is to be resolved during program execution
}

## Page 57

#### 3.20.1 Union Types Normalization

Union types normalization allows minimizing the number of types within a union type, while keeping type safety. Some types can also be replaced for more general types.

Union type  $ T_1 \mid \ldots \mid T_N $, where  $ N > 1 $, can be formally reduced to type  $ U_1 \mid \ldots \mid U_M $, where  $ M \leq N $, or even to a non-union type  $ V $. In this latter case  $ V $ can be a predefined value type or a literal type.

The normalization process presumes that the following steps are performed one after another:

1. All nested union types are linearized.

2. All type aliases (if any and except recursive ones) are recursively replaced for non-alias types.

3. Identical types within a union type are replaced for a single type with account to the readonly type flag priority.

4. If at least one type in a union is Any, then all other types are removed.

5. If positioned among union types, type never is removed.

6. If one type in a union is string, then all string literal types (if any) are removed.

This procedure is performed recursively until none of the above steps can be performed again.

The normalization process results in a normalized union type. The process is represented by the examples below:

( T1 | T2) | (T3 | T4) // normalized as T1 | T2 | T3 | T4. Linearization
type A = A[] | string // No changes. Recursive type alias is kept
type B = number
type C = string
type D = B | C // normalized as number | string. Type aliases are unfolded
number | number // normalized as number. Identical types elimination
(number[]) | (readonly number[]) // normalized as readonly number[]. Readonly version_
→wins
"1" | string | number // normalized as string | number. Literal type value belongs to_
→another type values
class Base {}
class Derived extends Base {}
Base | Derived // normalized as Base | Derived (no change)

The ArkTS compiler applies normalization while processing union types and handling type inference for array literals (see Array Type Inference from Types of Elements).

#### 3.20.2 Access to Common Union Members

Where u is a variable of union type  $ T_1 \mid ... \mid T_N $, ArkTS supports access to a common member of u.m if the following conditions are fulfilled:

• Each  $ T_{i} $ is an interface or class type;

• Each  $ T_{i} $ has a non-static member with the name m; and

## Page 58

• For any  $ T_{i} $, m is one of the following:
– Method or accessor with an equal signature; or
– Same-type field.

Otherwise, a compile-time error occurs as follows:

class A {
    n = 1
    s = "aa"
    foo() {}
    goo(n: number) {}
    static foo () {}
}

class B {
    n = 2
    s = 3.14
    foo() {}
    goo() {}
    static foo () {}
}

let u: A | B = new A

let x = u.n // ok, common field
u.foo() // ok, common method

console.log(u.s) // compile-time error as field types differ
u.goo() // compile-time error as signatures differ

type AB = A | B
AB.foo() // compile-time error as foo() is a static method

A compile-time error occurs if in some  $ T_{i} $ the name m is overloaded (see Overloading):

class C {
    overload foo { foo1, foo2 }
    foo1(a: number): void {}
    foo2(a: string): void {}
}

class D {
    foo(a: number): void {}
    foo2(a: string): void {}
}

function test(x: C | D) {
    x.foo() // compile-time error, as 'foo' in C is the overload alias
    x.foo2("aa") // ok, as 'foo2' in both C and D is a method
}

## Page 59

#### 3.20.3 Keyof Types

Keyof type is a special form of a union type that is built by using the keyword keyof. The keyword keyof is applied to a class or an interface type (see Classes and Interfaces). The resultant new type is a union of names (as string literal types) of all accessible members (see Accessible) of the class or the interface type.

The syntax of keyof type is presented below:

keyofType:
'keyof' typeReference
;

A compile-time error occurs if typeReference is neither a class nor an interface type. The semantics of type keyof is represented by the example below:

class A {
    field: number
    method() {}
}
type KeysOfA = keyof A // "field" | "method"
let a_keys: KeysOfA = "field" // OK
a_keys = "any string different from field or method"
// Compile-time error: invalid value for the type KeysOfA

If a class or an interface is empty, then its type keyof is equivalent to type never:

class A {} // Empty class
type KeysOfA = keyof A // never

### 3.21 Nullish Types

ArkTS has nullish types that are in fact a specific form of union types (see Union Types).

T | null or T | undefined or T | undefined | null can be used as the type to specify a nullish version of type T.

All predefined types except Type Any, and all user-defined types are non-nullish types. Non-nullish types cannot have a null or undefined value at runtime.

A variable declared to have type T | null can hold the values of type T and its derived types, or the value null. Such a type is called a nullable type.

A variable declared to have type T | undefined can hold the values of type T and its derived types, or the value undefined.

A variable declared to have type T | null | undefined can hold values of type T and its derived types, and the values undefined or null.

Nullish type is a reference type (see Union Types). A reference that is null or undefined is called a nullish value.

An operation that is safe with no regard to the presence or absence of nullish values (e.g., re-assigning one nullable value to another) can be used 'as is' for nullish types.

The following nullish-safe options exist for dealing with nullish type T:

## Page 60

• Using safe operations:

– Safe method call (see Method Call Expression for details);

– Safe field access expression (see Field Access Expression for details);

– Safe indexing expression (see Indexing Expressions for details);

– Safe function call (see Function Call Expression for details);

• Converting from T | null or T | undefined to T:

-  $  \text{on } T \mid \text{null or } T \mid \text{undefined to } T  $:
- Cast Expression;
- Ensure-not-nullish expression (see Ensure-Not-Nullish Expression for details);
Supplying a value to be used if a nullish value is present:
-coalescing expression (see Nullish-Coalescing Expression for details).

Note. Nullish types are not compatible with type Object:

function nullish (
    o: Object, nullish1: null, nullish2: undefined, nullish3: null | undefined
    nullish4: AnyClassOrInterfaceType | null | undefined
) {
    o = nullish1 /* compile-time error - type 'null' is not compatible with Object */
    o = nullish2 /* compile-time error - type 'undefined' is not compatible with Object */
    o = nullish3 /* compile-time error - type 'null|undefined' is not compatible with Object */
    o = nullish4 /* compile-time error - type 'AnyClassOrInterfaceType|null|undefined' is not compatible with Object */
}

### 3.22 Default Values for Types

Note. This ArkTS feature is experimental.

So-called default values are used by the following types for variables that require no explicit initialization (see Variable Declarations):

• Value Types:

• Type undefined and all its supertypes

All other types, including reference types, enumeration types, and type parameters have no default values.

Default values of value types are as follows:

## Page 61

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Data Type</td><td style='text-align: center; word-wrap: break-word;'>Default Value</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number</td><td style='text-align: center; word-wrap: break-word;'>0 as number</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte</td><td style='text-align: center; word-wrap: break-word;'>0 as byte</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>short</td><td style='text-align: center; word-wrap: break-word;'>0 as short</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>int</td><td style='text-align: center; word-wrap: break-word;'>0 as int</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>long</td><td style='text-align: center; word-wrap: break-word;'>0 as long</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>+0.0 as float</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>double</td><td style='text-align: center; word-wrap: break-word;'>+0.0 as double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>char</td><td style='text-align: center; word-wrap: break-word;'>u0000</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>boolean</td><td style='text-align: center; word-wrap: break-word;'>false</td></tr></table>

Value undefined is the default value of each type to which this value can be assigned.

class A {
    f1: string | undefined
    f2?: boolean
}
let a = new A()
console.log (a.f1, a.f2)
// Output: undefined, undefined

## Page 62

## Page 63

# NAMES, DECLARATIONS AND SCOPES

This chapter introduces the following three mutually-related notions:

• Names.

• Declarations, and

• Scopes.

Each entity in an ArkTS program—a variable, a constant, a class, a type, a function, a method, etc.—is introduced via a declaration. An entity declaration defines a name of the entity. The name is used to refer to the entity further in the program text. The declaration binds the entity name with the scope (see Scopes). The scope affects the accessibility of a new entity, and how it can be referred to by its qualified or simple (unqualified) name.

### 4.1 Names

A name is a sequence of one or more identifiers. A name allows referring to any declared entity. Names can have two syntactical forms:

• Simple name that consists of a single identifier;

• Qualified name that consists of a sequence of identifiers with the token ‘.’ as separator.

Both situations are covered by the below syntax rule:

qualifiedName:
    identifier ('.' identifier )*
;

In a qualified name N.x (where N is a simple name, and x is an identifier that can follow a sequence of identifiers separated with ‘.’ tokens), N can name the following:

• Name of a module (see Modules and Namespaces) that is introduced as a result of import * as N (see Bind All with Qualified Access) with x to name the exported entity;

• A class or interface type (see Classes, Interfaces) with x to name its static member;

• A class or interface type variable with x to name its instance member.

## Page 64

### 4.2 Declarations

A declaration introduces a named entity in an appropriate declaration scope (see Scopes), see

• Type Declarations;

• Variable and Constant Declarations;

• Function Declarations;

• Classes;

• Interfaces;

• Enumerations:

• Local Declarations;

• Top-Level Declarations;

• Overload Declarations;

• Annotations;

• Ambient Declarations.

Each declaration in the declaration scope must be distinguishable. Declarations are distinguishable if they have different names.

Distinguishable declarations are represented by the examples below:

const PI = 3.14
const pi = 3
function Pi() {}
type IP = number[]
class A {
    static method() {}
    method() {}
    field: number = PI
    static field: number = PI + pi
}

A compile-time error occurs if a declaration is not distinguishable:

// compile-time error: The constant and the function have the same name
const PI = 3.14
function PI() { return 3.14 }

// compile-time error: The type and the variable have the same name.
class Person {}
let Person: Person

// compile-time error: The field and the method have the same name.
class C {
    counter: number
    counter(): number {
        return this.counter
    }
}

(continues on next page)

## Page 65

/* compile-time error: Name of the declaration clashes with the predefined type or standard library entity name. */
let number: number = 1
let String = true
function Record () {}
interface Object {}
let Array = 42

/* compile-time error: ambient and non-ambient declarations refer to the same entity in a single module
*/
declare function foo()
function foo() {}

### 4.3 Scopes

Different entity declarations introduce new names in different scopes. Scope is the region of program text where an entity is declared, along with other regions it can be used in. The following entities are always referred to by their qualified names only:

• Class and interface members (both static and instance ones);

• Entities imported via qualified import; and

• Entities declared in namespaces (see Namespace Declarations).

Other entities are referred to by their simple (unqualified) names.

Entities within the scope are accessible (see Accessible).

The scope level of an entity depends on the context the entity is declared in:

- Module level scope is applicable to modules only. Constants and variables are accessible (see Accessible) from their respective points of declaration to the end of the module. Other entities are accessible through the entire scope level. If exported, a name can be accessed in other modules.

• Namespace level scope is applicable to namespaces only. Constants and variables are accessible (see Accessible) from their respective points of declaration to the end of the namespace including all embedded namespaces. Other entities are accessible through the entire namespace scope level including embedded namespaces. If exported, a name can be accessed outside the namespace with mandatory namespace name qualification.

• A name declared inside a class (class level scope) is accessible (see Accessible) in the class and sometimes, depending on the access modifier (see Access Modifiers), outside the class, or by means of a derived class.

Access to names inside the class is qualified with one of the following:

- Keywords this or super;

– Class instance expression for the names of instance entities; or

- Name of the class for static entities.

Outside access is qualified with one of the following:

## Page 66

- The expression the value stores;

– A reference to the class instance for the names of instance entities; or

- Name of the class for static entities.

ArkTS supports using the same identifier as names of a static entity and of an instance entity. The two names are distinguishable by the context, which is either a name of a class for static entities or an expression that denotes an instance.

• A name declared inside an interface (interface level scope) is accessible (see Accessible) inside and outside that interface (default public).

• The scope of a type parameter name in a class or interface declaration is that entire declaration, excluding static member declarations.

• The scope of a type parameter name in a function declaration is that entire declaration (function type parameter scope).

• The scope of a name declared inside the body of a function or a method declaration is the body of that declaration from the point of declaration and up to the end of the body (method or function scope). This scope is also applied to function or method parameter names.

• The scope of a name declared inside a block is the body of the block from the point of the name declaration and up to the end of the block (block scope).

function foo() {
    let x = y // compile-time error - y is not accessible yet
    let y = 1
}

Scopes of two names can overlap (e.g., when statements are nested). If scopes of two names overlap, then:

• The innermost declaration takes precedence; and

• Access to the outer name is not possible.

Class, interface, and enum members can only be accessed by applying the dot operator ‘.’ to an instance. Accessing them otherwise is not possible.

### 4.4 Accessible

Entity is considered accessible if it belongs to the current scope (see Scopes) and means that its name can be used for different purposes as follows:

• Type name is used to declare variables, constants, parameters, class fields, or interface properties;

• Function or method name is used to call the function or method;

• Variable name is used to read or change the value of the variable;

• Name of a module introduced as a result of import with Bind All with Qualified Access (see Bind All with Qualified Access) is used to deal with exported entities.
