# Chapter 15: Semantic Rules

Page range: 237-266

## Page 237

(continued from previous page)

'from' importPath
;

An importPath cannot refer to the file the current module is stored in. Otherwise, a compile-time error occurs.

If re-exported declarations are not distinguishable (see Declarations) within the scope of the current module, then a compile-time error occurs.

The re-exporting practices are represented in the following examples:

export * from "path_to_the_module" // re-export all exported declarations
export * as qualifier from "path_to_the_module"
// re-export all exported declarations with qualification
export { d1, d2 as d3 } from "path_to_the_module"
// re-export particular declarations some under new name
export {default} from "path_to_the_module"
// re-export default declaration from the other module
export {default as name} from "path_to_the_module"
// re-export default declaration from the other module under 'name'

### 13.6 Top-Level Statements

A module can contain sequences of statements that logically comprise one sequence of statements.

The syntax of top-level statements is presented below:

topLevelStatements: statement*
;

A module can contain any number of top-level statements that logically merge into a single sequence in the textual order:

statements_1
/* top-declarations except constant and variable declarations */
statements_2

The sequence above is equal to the following:

/* top-declarations except constant and variable declarations */
statements_1; statements_2

This situation is represented by the example below:

// The actual text combination of the statements and declarations
console.log("Start of top-level statements")
type A = number | string
let a: A = 56
function foo() {
    console.log(a)

(continues on next page)

## Page 238

7 }
8 a = "a string"
9
10 // The logically ordered text - declarations then statements
11 type A = number | string
12 function foo () {
13     console.log (a)
14     }
15 console.log ("Start of top-level statements")
16 let a: A = 56
17 a = "a string"

• If a module is imported by some other module, then the semantics of top-level statements is to initialize the imported module. It means that all top-level statements are executed only once before a call to any other function, or before the access to any top-level variable of the module.

• If a module is used as a program, then top-level statements are used as a program entry point (see Program Entry Point). The set of top-level statements being empty implies that the program entry point is also empty and does nothing. If a module has the main function, then it is executed after the execution of the top-level statements.

// Source file A
{ // Block form
    console.log("A.top-level statements")
}

// Source file B
import * as A from "Source file A "
function main () {
    console.log("B.main")
}

The output is as follows:
A. Top-level statements,
B. Main.

// One source file
console.log("A.Top-level statements")
function main() {
    console.log("B.main")
}

A compile-time error occurs if top-level statements contain a return statement (Expression Statements).

The execution of top-level statements means that all statements, except type declarations, are executed one after another in the textual order of their appearance within the module until an error situation is thrown (see Errors), or last statement is executed.

## Page 239

### 13.7 Program Entry Point

Modules can act as programs (applications). Program execution starts from the execution of a program entry point which can be of the following two kinds:

• Top-level statements for modules (see Top-Level Statements); or

• Sole top-level statement (the first statement in the top-level statements acts as the entry point);

• Entry point function (see below).

- Both top-level statement and entry point function (same as above, plus the function called after the top-level statement execution is completed).

Entry point functions have the following features:

A module can have the following forms of entry point:

• Any exported top-level function can be used as an entry point. An entry point is selected by the compiler, the execution environment, or both;

• Sole entry point function (main or other as described below);

• Entry point function must either have no parameters, or have one parameter of type string[] that provides access to the arguments of a program command line;

• Entry point function return type is either void (see Type void) or int;

• Entry point function cannot have overloading;

• Entry point function is called main by default.

The example below represents different forms of valid and invalid entry points:

function main() {
    // Option 1: a return type is inferred from the body of main().
    // It will be 'int' if the body has 'return' with the integer expression
    // and 'void' if no return at all in the body
}

function main(): void {
    // Option 2: explicit :void - no return in the function body required
}

function main(): int {
    // Option 3: explicit :int - return is required
    return 0
}

function main(): string { // compile-time error: incorrect main signature
    return ""
}

function main(p: number) { // compile-time error: incorrect main signature
}

// Option 4: top-level statement is the entry point
console.log("Hello, world!")

// Option 5: top-level exported function

(continues on next page)

## Page 240

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>27</td><td style='text-align: center; word-wrap: break-word;'>export function entry() {}</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>28</td><td style='text-align: center; word-wrap: break-word;'>// Option 5: top-level exported function with command-line arguments</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>29</td><td style='text-align: center; word-wrap: break-word;'>export function entry(cmdLine: string[]) {}</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>30</td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

## Page 241

## AMBIENT DECLARATIONS

Ambient declaration specifies an entity that is declared elsewhere. Ambient declarations:

• Provide type information for entities included into a program from external sources.

• Introduce no new entities like regular declarations do.

• Cannot include executable code, and thus have no initializers.

Ambient functions, methods, and constructors have no bodies.

The syntax of ambient declaration is presented below:

ambientDeclaration:
  'declare'
  ( ambientConstantDeclaration
  | ambientFunctionDeclaration
  | overloadFunctionDeclaration
  | ambientClassDeclaration
  | ambientInterfaceDeclaration
  | ambientNamespaceDeclaration
  | ambientAnnotationDeclaration
  | ambientAccessorDeclaration
  | 'const'? enumDeclaration
  | typeAlias
)

An ambient enumeration type declaration can be prefixed by the keyword const for TypeScript compatibility. It has no influence on the declared type.

A compile-time error occurs if the modifier declare is used in a context that is already ambient:

declare namespace A{
    declare function foo(): void // compile-time error
}

A compile-time warning occurs if an ambient declaration is marked with export keyword as all ambient declarations are exported by default:

export declare namespace A{ // compile-time warning
    function foo(): void
}

## Page 242

### 14.1 Ambient Constant Declarations

The syntax of ambient constant declaration is presented below:

ambientConstantDeclaration:
    'const' ambientConstList；《
    ;

ambientConstList:
    ambientConst（'，' ambientConst）*
;

ambientConst:
    identifier（('：' type）|（'='）
→(IntegerLiteral|FloatLiteral|StringLiteral|MultilineStringLiteral)))
;

An initializer expression for an ambient constant must be a numeric or string literal. The meaning of the literal is to define the type of the ambient constant, while the actual value must be provided when a non-ambient declaration is available.

### 14.2 Ambient Function Declarations

The syntax of ambient function declaration is presented below:

ambientFunctionDeclaration: 'function' identifier typeParameters? signature;

A compile-time error occurs if explicit return type for an ambient function declaration is not specified.

declare function foo(x: number): void // ok
declare function bar(x: number) // compile-time error

Ambient functions cannot have parameters with default values but can have optional parameters.

Ambient function declarations cannot specify function bodies.

declare function foo(x?: string): void // ok
declare function bar(y: number = 1): void // compile-time error

Note. The modifier async cannot be used in an ambient context.

## Page 243

### 14.3 Ambient Overload Function Declarations

The syntax of ambient overload function declaration is identical to that of Function Overload Declarations. The semantics of such declarations is defined by the same rules.

// Top-level functions are overloaded
declare function foo1(p: string): void
declare function foo2(p: number): void
declare overload foo {foo1, foo2}

// Namespace functions are overloaded
declare namespace N {
    function foo1(p: string): void
    function foo2(p: number): void
    overload foo {foo1, foo2}
}

// All calls are valid
foo("a string")
foo(5)
N.foo("a string")
N.foo(5)

### 14.4 Ambient Class Declarations

The syntax of ambient class declaration is presented below:

ambientClassDeclaration:
  'class' | 'struct' identifier typeParameters?
  classExtendsClause? implementsClause?
  '{' ambientClassMember* '}'
;
ambientClassMember:
  ambientAccessModifier?
  ( ambientFieldDeclaration
  | ambientConstructorDeclaration
  | ambientMethodDeclaration
  | overloadMethodDeclaration
  | ambientClassAccessorDeclaration
  | ambientIndexerDeclaration
  | ambientCallSignatureDeclaration
  | ambient 词性
  )
  ;
ambientAccessModifier:
  'public' | 'protected'
;

## Page 244

Ambient field declarations have no initializers.

The syntax of ambient field declaration is presented below:

ambientFieldDeclaration:
    ambientFieldModifier* identifier : 'type
;
ambientFieldModifier:
    'static' | 'readonly'
;

Ambient constructor, method, and accessor declarations have no bodies.

Their syntax is presented below:

ambientConstructorDeclaration:
    'constructor' parameters
;
ambientMethodDeclaration:
    ambientMethodModifier* identifier signature
;
ambientMethodModifier:
    'static'
;
ambientClassAccessorDeclaration:
    ambientMethodModifier*
( 'get' identifier '(' ')' returnType
| 'set' identifier '(' parameter ')'
)
;

Ambient methods can be overloaded similarly to non-ambient methods with the same syntax and semantics (see Class Method Overload Declarations).

// Class methods are overloaded
declare class A {
    foo1(p: string): void
    foo2(p: number): void
    overload foo {foo1, foo2}
}

// All methods calls are valid
function demo (a: A) {
    a.foo("a string")
    a.foo(5)
}

## Page 245

#### 14.4.1 Ambient Indexer

Ambient indexer declarations specify the indexing of a class instance in an ambient context. The feature is provided for TypeScript compatibility:

The syntax of ambient indexer declaration is presented below:

ambientIndexerDeclaration:
    'readonly'? ['identifier': 'indexType'] 'returnType';
indexType: 'number';

The following restriction applies: Only one ambient indexer declaration is allowed in an ambient class declaration.

declare class C {
    [index: number]: number
}

Note. Ambient indexer declaration is supported in ambient contexts only. If written in ArkTS, ambient class implementation must conform to Indexable Types.

#### 14.4.2 Ambient Call Signature

Ambient call signature declarations are used to specify callable types in an ambient context. The feature is provided for TypeScript compatibility:

The syntax of ambient call signature declaration is presented below:

ambientCallSignatureDeclaration:
signature
;

declare class C {
    (someArg: number): boolean
}

Note. Ambient class signature declaration is supported in ambient contexts only. If written in ArkTS, ambient class implementation must conform to Callable Types with $_invoke Method.

#### 14.4.3 Ambient Iterable

Ambient秤able declaration indicates that a class instance is iterable in an ambient context. The feature is provided for TypeScript compatibility:

The syntax of ambient iterable declaration is presented below:

ambient 词性限定

'[Symbol.iterator]' '(' ')' returnType
;

## Page 246

The following restrictions apply:

• returnType must be a type that implements Interface defined in Standard Library.

• Only one ambient iterable declaration is allowed in an ambient class declaration.

declare class C {
    [Symbol.iterator](); CIterator
}

### 14.5 Ambient Interface Declarations

The syntax of ambient interface declaration is presented below:

Note. Ambient秤的 $ ^{1} $is supported in ambient contexts only. If written in ArkTS, ambient class implementation must conform to Iterable Types.

ambientInterfaceDeclaration:
    'interface' identifier typeParameters?
    interfaceExtendsClause?
    '{' ambientInterfaceMember* '}'
;
ambientInterfaceMember
    : interfaceProperty
    | ambientInterfaceMethodDeclaration
    | ambientIndexerDeclaration
    | ambientIterableDeclaration
;
ambientInterfaceMethodDeclaration:
    'default'? identifier signature
;

Ambient interface can contain additional members in the same manner as an ambient class (see Ambient Indexer, and Ambient Iterable).

If an interface method declaration is marked with the keyword default, then a non-ambient interface must contain the default implementation for the method as follows:

declare interface I1 {
    default foo (): void // method foo will have the default implementation
}
class C1 implements I1 {} // Class C1 is valid as foo() has the default implementation

interface I1 {
    // If such interface is used as I1 it will be runtime error as there is
    // no default implementation for foo()
    foo (): void
}

## Page 247

declare interface I2 {
    foo () : void // method foo has no default implementation
}
class C2 implements I2 {} // Class C2 is invalid as foo() has no implementation
class C3 implements I2 { foo() {} } // Class C3 is valid as foo() has implementation

### 14.6 Ambient Namespace Declarations

Namespaces are used to logically group multiple entities. ArkTS supports ambient namespaces for better TypeScript compatibility. TypeScript often uses ambient namespaces to specify the platform API or a third-party library API.

The syntax of ambient namespace declaration is presented below:

ambientNamespaceDeclaration:
    'namespace' identifier '{' ambientNamespaceElement* '}'
;
ambientNamespaceElement:
    ambientNamespaceElementDeclaration | exportDirective
;
ambientNamespaceElementDeclaration:
    'export'?
    ( ambientConstantDeclaration
    | ambientFunctionDeclaration
    | ambientClassDeclaration
    | ambientInterfaceDeclaration
    | ambientNamespaceDeclaration
    | ambientAccessorDeclaration
    | 'const'? enumDeclaration
    | typeAlias
)

An enumeration type declaration can be prefixed with the keyword const for TypeScript compatibility. The prefix has no influence on the declared type. Only exported entities can be accessed outside a namespace.

Namespaces can be nested:

declare namespace A {
    export namespace B {
        export function foo(): void;
    }
}

A namespace is not an object but merely a scope for entities that can be accessed by using qualified names only.

If an ambient namespace is imported from a module, then all ambient namespace declarations are accessible (see Accessible) across all declarations and top-level statements of the current module.

## Page 248

// File1.d.ets
export declare namespace A { // namespace itself must be exported
    function foo(): void
        type X = Array<number>
    }

    // File2.ets
    import {A} from 'File1.d.ets'

    A.foo() // Valid function call, as 'foo' is accessible for top-level statements
    function foo() {
        A.foo() // Valid function call, as 'foo' is accessible here as well
    }
    class C {
        method() {
            A.foo() // Valid function call, as 'foo' is accessible here too
            let x: A.X = [] // Type A.X can be used
        }
    }
}

A compile-time error occurs if an ambient namespace declaration contains an exportDirective that refers to a declaration which is not a part of the namespace.

export declare namespace A {
    export {foo} // compile-time error: no 'foo' in namespace 'A'
}
function foo() {}

#### 14.6.1 Implementing Ambient Namespace Declaration

If an ambient namespace is implemented in ArkTS, a namespace with the same name must be declared (see Namespace Declarations) as the top-level declaration of a module. All namespace names of a nested namespace (i.e. a namespace embedded into another namespace) must be the same as in ambient context.

## Page 249

## SEMANTIC RULES

This Chapter contains semantic rules to be used throughout this Specification document. The description of the rules is more or less informal. Some details are omitted to simplify the understanding.

### 15.1 Semantic Essentials

The section gives a brief introduction to the major semantic terms and their usage in several contexts.

#### 15.1.1 Type of Standalone Expression

Standalone expression (see Type of Expression) is an expression for which there is no target type in the context where the expression is used.

The type of a standalone expression is determined as follows:

• In case of Numeric Literals, the type is the default type of a literal:

- Type of Integer Literals is int or long;

– Type of Floating-Point Literals is double or float.

• In case of Constant Expressions, the type is inferred from operand types and operations.

• In case of an Array Literal, the type is inferred from the elements (see Array Type Inference from Types of Elements).

• Otherwise, a compile-time error occurs. Specifically, a compile-time error occurs if an object literal is used as a standalone expression.

The situation is represented in the example below:

function foo() {
    1     // type is 'int'
    1.0     // type is 'number'
    [1.0, 2.0]    // type is number[]
    [1, "aa"]    // type is (int | string)
}

## Page 250

#### 15.1.2 Specifics of Assignment-like Contexts

Assignment-like context (see Assignment-like Contexts) can be considered as an assignment x = expr, where x is a left-hand-side expression, and expr is a right-hand-side expression. E.g., there is an implicit assignment of expr to the formal parameter foo in the call foo(expr), and implicit assignments to elements or properties in Array Literal and Object Literal.

Assignment-like context is specific in that the type of a left-hand-side expression is known, but the type of a right-hand-side expression is not necessarily known in the context as follows:

• If the type of a right-hand-side expression is known from the expression itself, then the Assignability check is performed as in the example below:

function foo(x: string, y: string) {
    x = y // ok, assignability is checked
}

• Otherwise, an attempt is made to apply the type of the left-hand-side expression to the right-hand-side expression. A compile-time error occurs if the attempt fails as in the example below:

function foo(x: int, y: double[]) {
    x = 1 // ok, type of '1' is inferred from type of 'x'
    y = [1, 2] // ok, array literal is evaluated as [1.0, 2.0]
}

#### 15.1.3 Specifics of Variable Initialization Context

If the variable or a constant declaration (see Variable and Constant Declarations) has an explicit type annotation, then the same rules as for assignment-like contexts apply. Otherwise, there are two cases for let x = expr (see Type Inference from Initializer) as follows:

• The type of the right-hand-side expression is known from the expression itself, then this type becomes the type of the variable as in the example below:

function foo(x: int) {
    let y = x // type of 'y' is 'int'
}

• Otherwise, the type of expr is evaluated as type of a standalone expression as in the example below:

function foo() {
    let x = 1 // x is of type 'int' (default type of '1')
    let y = [1, 2] // x is of type 'number[]'
}

## Page 251

#### 15.1.4 Specifics of Numeric Operator Contexts

The postfix and prefix increment and decrement operators evaluate byte and short operands without widening. It is also true for an assignment operator (considering assignment as a binary operator).

For other numeric operators, the operands of unary and binary numeric expressions are widened to a larger numeric type. The minimum type is int. None of those operators evaluates values of types byte and short without widening. Details of specific operators are discussed in corresponding sections of the Specification.

#### 15.1.5 Specifics of String Operator Contexts

If one operand of the binary operator '+' is of type string, then the string conversion applies to another non-string operand to convert it to string (see String Concatenation and String Operator Contexts).

#### 15.1.6 Other Contexts

The only semantic rule for all other contexts, and specifically for Overriding, is to use Subtyping.

#### 15.1.7 Specifics of Type Parameters

If the type of a left-hand-side expression in assignment-like context is a type parameter, then it provides no additional information for type inference even where a type parameter constraint is set.

If the target type of an expression is a type parameter, then the type of the expression is inferred as the type of a standalone expression.

The semantics is represented in the example below:

class C<T extends number> {
    constructor (x: T) {}
}

new C(1) // compile-time error

The type of ‘1’ in the example above is inferred as int (default type of an integer literal). The expression is considered new C<int>(1) and causes a compile-time error because int is not a subtype of number (type parameter constraint).

Explicit type argument new C<number>(1) must be used to fix the code.

## Page 252

#### 15.1.8 Semantic Essentials Summary

Major semantic terms are listed below:

• Type of Expression;

• Assignment-like Contexts:

• Type Inference from Initializer;

• Numeric Operator Contexts;

• String Operator Contexts;

• Subtyping;

• Assignability;

• Overriding;

• Overloading;

• Type Inference.

### 15.2 Subtyping

Subtype relationship between types S and T, where S is a subtype of T (recorded as S<:T), means that any object of type S can be safely used in any context to replace an object of type T. The opposite relation (recorded as T:>S) is called supertype relationship. Each type is its own subtype and supertype (S<:S and S:>S).

By the definition of S<:T, type T belongs to the set of supertypes of type S. The set of supertypes includes all direct supertypes (discussed in subsections), and all their respective supertypes. More formally speaking, the set is obtained by reflexive and transitive closure over the direct supertype relation.

The terms subclass, subinterface, superclass, and superinterface are used in the following sections as synonyms for subtype and supertype when considering non-generic classes, generic classes, or interface types.

If a relationship of two types is not described in one of the following sections, then the types are not related to each other. Specifically, two Resizable Array Types and two Tuple Types are not related to each other, except where they are identical (see Type Identity).

class Base {}
class Derived extends Base {}

function not_a_subtype (
    ab: Array<Base>, ad: Array<Derived>,
    tb: [Base, Base], td: [Derived, Derived],
) {
    ab = ad // Compile-time error
    tb = td // Compile-time error
}

## Page 253

#### 15.2.1 Subtyping for Non-Generic Classes and Interfaces

S for non-generic classes and interfaces is a direct subclass or subinterface of T (or of Object type) when one of the following conditions is true:

• Class S is a direct subtype of class T (S<:T) if T is mentioned in the extends clause of S (see Class Extension Clause):

// Illustrating S<:T
class T {}
class S extends T {}
function foo(t: T) {}

// Using T
foo(new T)

// Using S (S<:T)
foo(new S)

• Class S is a direct subtype of class Object (S<:Object) if S has no Class Extension Clause:

// Illustrating S<:Object
class S {}
function foo(o: Object) {}

// Using Object
foo(new Object)

// Using S (S<:Object)
foo(new S)

• Class S is a direct subtype of interface T (S<:T) if T is mentioned in the implements clause of S (see Class Implementation Clause):

// Illustrating S<:T
// S is class, T is interface
interface T {}
class S implements T {}
function foo(t: T) {}
let s: S = new S

// Using T
let t: T = s
foo(t)

// Using S (S<:T)
foo(s)

• Interface S is a direct subtype of interface T (S<:T) if T is mentioned in the extends clause of S (see Superinterfaces and Subinterfaces):

// Illustrating S<:T
// S is interface, T is interface
interface T {}
interface S extends T {}

(continues on next page)

## Page 254

function foo(t: T) {}
    let t: T
    let s: S

    // Using T
    class A implements T {}
    t = new A
    foo(t)

    // Using S (S<: T)
    class B implements S {}
    s = new B
    foo(s)

• Interface S is a direct subtype of class Object (S<:Object) if S has no extends clause (see Superinterfaces and Subinterfaces).

// Illustrating subinterface of Object
interface S {}
function foo(o: Object) {}

// Using Object
foo(new Object)

// Using subinterface of Object
class A implements S {}
let s: S = new A;
foo(s)

#### 15.2.2 Subtyping for Generic Classes and Interfaces

A generic class or generic interface is declared as C <F₁, ..., Fₙ>, where n>0 is a direct subtype of another generic class or interface T, if one of the following conditions is true:

• T is a direct superclass of C <F₁, ..., Fᵢ> mentioned in the extends clause of C:

// T<U, V> is direct superclass of C<U,V>
// T<U, V>>: C<U, V>

class T<U, V> {
    foo(p: U|V): U|V { return p }
}

class C<U, V> extends T<U, V> {
    bar(u: U): U { return u }
}

// OK, exact match

(continues on next page)

## Page 255

let t: T<int, boolean> = new T<int, boolean>
    let c: C<int, boolean> = new C<int, boolean>

// OK, assigning to direct superclass
t = new C<int, boolean>

// CTE, cannot assign to subclass
c = new T<int, boolean>

• T is one of direct superinterfaces of C <F1, ..., Fn> (see Superinterfaces and Subinterfaces):

// Interface I<U, V> is direct superinterface
// of J<U, V>, X<U, V>

interface I<U, V> {
    foo(u: U): U;
    bar(v: V): V;
}

// J<U, V> <: I<U, V>
// since J extebdss I
interface J<U, V> extends I<U, V>
{
    foo(u: U): U
        bar(v: V): V
        foo1(p: U|V): U|V
    }

    // X<U, V> <: I<U, V>
    // since X implements I
    class X<U, V> implements I<U, V> {
        foo(u: U): U { return u }
        bar(v: V): V { return v }
    }

    // Y<U, V> <: J<U, V> (directly)
    // Also Y<U, V> <: I<U, V> (transitively)
    class Y<U, V> implements J<U, V> {
        foo(u: U): U { return u }
        bar(v: V): V { return v }
    }

    fool(p: U|V): U|V { return p }
}

let i: I<int, boolean>
    let j: J<int, boolean>
    let x = new X<int, boolean>
    let y = new Y<int, boolean>

    // OK, assigning to direct supertypes

(continues on next page)

## Page 256

(continued from previous page)

41 | i = x
42 | j = y
43 | // OK, assigning subinterface (J<:I)
44 | i = j
45 |
46 | // CTE, cannot assign superinterface (I>:J)
47 | j = i

• T is type Object (C<:Object) if C <F₁, ..., Fₙ> is either a generic class type with no direct superclasses, or a generic interface type with no direct superinterfaces:

// Object is direct superclass and for C<U,V>
// and direct superinrerface for I<U,V>

class C<U, V> {
    foo(u: U): U { return u }
    bar(v: V): V { return v }
}

interface I<U, V> {
    foo(u: U): U { return u }
    bar(v: V): V { return v }
}

let o: Object = new Object
    let c: C<int, boolean> = new C<int, boolean>
    let i: I<int, boolean>

    // example1 - C<U,V> <: Object
    function example1(o: Object) {}

    // OK, example(Object)
    example1(o)
    // OK, C<int, boolean> <: Object
    example1(c)

    // example2 - I<U,V> <: Object
    function example2(o: Object) {}
    class D<U, V> implements I<U, V> {}
    i = new D<int, boolean>

    // OK, example2(Object)
    example2(o)
    // OK, I<int, boolean> <: Object
    example2(i)

The direct supertype of a type parameter is the type specified as the constraint of that type parameter.

If type parameters of a generic class or an interface have a variance specified (see Type Parameter Variance), then the subtyping for instantiations of the class or interface is determined in accordance with the variance of the appropriate type parameter. For example, with generic class G<in T1, out T2> the G<S, T> <: G<U, V> when S>:U and T<:V

The following code illustrates this:

## Page 257

// Subtyping illustration for generic with parameter variance

// U1 <: U0
class U0 {}
class U1 extends U0 {}

// Generic with contravariant parameter
class E<in T> {}

let e0: E<U0> = new E<U1> // CTE, E<U0> is subtype of E<U1>
let e1: E<U1> = new E<U0> // OK, E<U1> is supertype for E<U0>

// Generic with covariant parameter
class F<out T> {}

let f0: F<U0> = new F<U1> // OK, F<U0> is supertype for F<U1>
let f1: F<U1> = new F<U0> // CTE, F<U1> is subtype of F<U0>

#### 15.2.3 Subtyping for Literal Types

Any string literal type (see String Literal Types) is subtype of type string. It affects overriding as shown in the example below:

class Base {
    foo(p: "1"): string { return "42" }
}
class Derived extends Base {
    override foo(p: string): "1" { return "1" }
}
// Type "1" <: string

let base: Base = new Derived
let result: string = base.foo("1")
/* Argument "1" (value) is compatible to type "1" and to type string in the overridden method
    Function result of type string accepts "1" (value) of literal type "1"
*/

Literal type null (see Literal Types) is a subtype and a supertype to itself. Similarly, literal type undefined is a subtype and a supertype to itself.

## Page 258

#### 15.2.4 Subtyping for Union Types

A union type U participates in a subtyping relationship (see Subtyping) in the following cases:

1. Union type U (U₁ | ... | Uₙ) is a subtype of type T if each Uᵢ is a subtype of T.

let s1: "1" | "2" = "1"
let s2: string = s1 // ok

let a: string | number | boolean = "abc"
let b: string | number = 42
a = b // OK
b = a // compile-time error, boolean is absent is 'b'

class Base {}
class Derived1 extends Base {}
class Derived2 extends Base {}

let x: Base = ...
let y: Derived1 | Derived2 = ...

x = y // OK, both Derived1 and Derived2 are subtypes of Base
y = x // compile-time error

let x: Base | string = ...
let y: Derived1 | string ...
x = y // OK, Derived1 is subtype of Base
y = x // compile-time error

2. Type T is a subtype of union type U (U1 | ... | Un) if for some i T is a subtype of Ui.

let u: number | string = 1 // ok
u = "aa" // ok
u = 1.0 // ok, 1.0 is of type 'number' (double)
u = 1 // compile-time error, type 'int' is not a subtype of 'number'
u = true // compile-time error

Note. If union type normalization produces a single type, then this type is used instead of the initial set of union types. This concept is represented in the example below:

let u: "abc" | "cde" | string // type of 'u' is string

#### 15.2.5 Subtyping for Function Types

Function type F with parameters  $ FP_1 $,  $ \ldots $,  $ FP_m $ and return type FR is a subtype of function type S with parameters  $ SP_1 $,  $ \ldots $,  $ SP_n $ and return type SR if all of the following conditions are met:

• m ≤ n;

• Parameter type of  $ SP_i $ for each  $ i \leq m $ is a subtype of parameter type of  $ FP_i $ (contravariance), and  $ SP_i $ is: - Rest parameter if  $ FP_i $ is a rest parameter; - Optional parameter if  $ FP_i $ is an optional parameter.

• Type FR is a subtype of SR (covariance).

## Page 259

class Base {}
class Derived extends Base {}

function check(
    bb: (p: Base) => Base,
    bd: (p: Base) => Derived,
    db: (p: Derived) => Base,
    dd: (p: Derived) => Derived
) {
    bb = bd
    /* OK: identical parameter types, and covariant return type */
    bb = dd
    /* Compile-time error: parameter type are not contravariant */
    db = bd
    /* OK: contravariant parameter types, and covariant return type */

    let f: (p: Base, n: number) => Base = bb
    /* OK: subtype has less parameters */

    let g: () => Base = bb
    /* Compile-time error: less parameters than expected */
}

let foo: (x?: number, y?: string) => void = (): void => {} // OK: ``m <= n``
foo = (p?: number): void => {} // OK: ``m <= n``
foo = (p1?: number, p2?: string): void => {} // OK: Identical types
foo = (p: number): void => {}
    // Compile-time error: 1st parameter in type is optional but mandatory in lambda
    foo = (p1: number, p2?: string): void => {}
    // Compile-time error: 1st parameter in type is optional but mandatory in lambda

#### 15.2.6 Subtyping for Fixed-Size Array Types

Subtyping for fixed-size array types is based on subtyping of their element types. It is formally defined as follows:

FixedSize<B> <: FixedSize<A> if B <: A.

The situation is represented in the following example:

let x: FixedArray<number> = [1, 2, 3]
let y: FixedArray<Object> = x // ok, as number <: Object
x = y // compile-time error

Such subtyping allows array assignments that can lead to ArrayStoreError at runtime if a value of a type which is not a subtype of an element type of one array is put into that array by using the subtyping of another array element type. Type safety is ensured by runtime checks performed by the runtime system as represented in the example below:

class C {}
class D extends C {}

(continues on next page)

## Page 260

function foo (ca: FixedArray<C>) {
    ca[0] = new C() // ArrayStoreError if ca refers to FixedArray<D>
}

let da: FixedArray<D> = [new D()]

foo(da) // leads to runtime error in 'foo'

#### 15.2.7 Subtyping for Intersection Types

Intersection type I defined as  $ (I_1 \& \ldots \mid I_n) $ is a subtype of type T if  $ I_i $ is a subtype of T for some  $ i $.

Type T is a subtype of intersection type  $ (I_1 \& \ldots \mid I_n) $ if T is a subtype of each  $ I_i $.

#### 15.2.8 Subtyping for Difference Types

Difference type A - B is a subtype of T if A is a subtype of T.

Type T is a subtype of the difference type A - B if T is a subtype of A, and no value belongs both to T and B (i.e., T & B = never).

### 15.3 Type Identity

Identity relation between two types means that the types are indistinguishable. Identity relation is symmetric and transitive. Identity relation for types A and B is defined as follows:

• Array types A = T1[] and B = Array<T2> are identical if T1 and T2 are identical.

• Tuple types  $ A = [T_1, T_2, \ldots, T_n] $ and  $ B = [U_1, U_2, \ldots, U_m] $ are identical on condition that:

- n is equal to m, i.e., the types have the same number of elements;

– Every  $ T_i $ is identical to  $ U_i $ for any  $ i $ in 1 … n.

• Union types  $ A = T_1 \mid T_2 \mid \ldots \mid T_n $ and  $ B = U_1 \mid U_2 \mid \ldots \mid U_m $ are identical on condition that:

– n is equal to m, i.e., the types have the same number of elements;

-  $ U_i $ in U undergoes a permutation after which every  $ T_i $ is identical to  $ U_i $ for any  $ i $ in 1 ... n.

• Types A and B are identical if A is a subtype of B (A<:B), and B is at the same time a subtype of A (A:>B).

Note. Type Alias Declaration creates no new type but only a new name for the existing type. An alias is indistinguishable from its base type.

## Page 261

Note. If a generic class or an interface has a type parameter T while its method has its own type parameter T, then the two types are different and unrelated.

class A<T> {
    data: T
    constructor (p: T) { this.data = p } // OK, as here 'T' is a class type parameter
    method <T>(p: T) {
        this.data = p // compile-time error as 'T' of the class is different from 'T' of the_method
    }
}

### 15.4 Assignability

Type  $ T_{1} $ is assignable to type  $ T_{2} $ if:

•  $ T_{1} $ is type never;

 $ T_{1} $ is identical to  $ T_{2} $ (see Type Identity);

• T1 is a subtype of T2 (see Subtyping); or

• Implicit conversion (see Implicit Conversions) is present that allows converting a value of type T1 to type T2.

Assignability relationship is asymmetric, i.e., that T1 is assignable to T2 does not imply that T2 is assignable to type T1.

### 15.5 Invariance, Covariance and Contravariance

Variance is how subtyping between types relates to subtyping between derived types, including generic types (See Generics), member signatures of generic types (type of parameters, return type), and overriding entities (See Override-Compatible Signatures). Variance can be of three kinds:

• Covariance,

• Contravariance, and

• Invariance.

Covariance means it is possible to use a type which is more specific than originally specified.

Contravariance means it is possible to use a type which is more general than originally specified.

Invariance means it is only possible to use the original type, i.e., there is no subtyping for derived types.

Valid and invalid usages of variance are represented in the examples below. If class Base is defined as follows:

class Base {
    method_one(p: Base): Base {}
    method_two(p: Derived): Base {}
    method_three(p: Derived): Derived {}
}

## Page 262

—then the code below is valid:

class Derived extends Base {
    // invariance: parameter type and return type are unchanged
    override method_one(p: Base): Base {}

    // covariance for the return type: Derived is a subtype of Base
    override method_two(p: Derived): Derived {}

    // contravariance for parameter types: Base is a supertype for Derived
    override method_three(p: Base): Derived {}
}

On the contrary, the following code causes compile-time errors:

class Derived extends Base {

    // covariance for parameter types is prohibited
    override method_one(p: Derived): Base {}

    // contravariance for the return type is prohibited
    override method_tree(p: Derived): Base {}
}

### 15.6 Compatibility of Call Arguments

The following semantic checks must be performed to arguments from the left to the right when checking the validity of any function, method, constructor, or lambda call:

Step 1: All arguments in the form of spread expression (see Spread Expression) are to be linearized recursively to ensure that no spread expression is left at the call site.

Step 2: The following checks are performed on all arguments from left to right, starting from  $ \arg\_pos = 1 $ and  $ \arg\_pos = 1 $:

if parameter at position par_pos is of non-rest form, then

if  $ T_{\arg\_pos} <: T_{\text{par\_pos}} $, then increment  $ \arg\_pos $ and  $ \text{par\_pos} $ else a compile-time error occurs, exit Step 2

else // parameter is of rest form (see Rest Parameter)

if parameter is of rest_array_form, then

if T arg_pos <: T rest_array_type, then increment arg_pos else increment par_pos

else // parameter is of rest_tuple_form

for rest_tuple_pos in 1 .. rest_tuple_types.count do

if  $ T_{\text{arg\_pos}} <: T_{\text{rest\_tuple\_pos}} $, then increment  $ \text{arg\_pos} $ and  $ rest\_tuple\_pos $ else if  $ rest\_tuple\_pos < rest\_tuple\_types.count $, then increment  $ rest\_tuple\_pos $ else a compile-time error occurs, exit Step 2

end increment par_pos

## Page 263

end
end

Checks are represented in the examples below:

call [...1, "str", true], ...[ ...123] // Initial call form

call (1, "str", true, 123) // To be unfolded into the form with no spread expressions

function foo1 (p: Object) {}
    foo1 (1) // Type of '1' must be assignable to 'Object'
    // p becomes 1

function foo2 (...p: Object[]) {}
    foo2 (1, "111") // Types of '1' and "111" must be assignable to 'Object'
    // p becomes array [1, "111"]

function foo31 (...p: (number|string)[]) {}
    foo31 (...[1, "111"]) // Type of array literal [1, "111"] must be assignable to_
    (number|string)[]
    // p becomes array [1, "111"]

function foo32 (...p: [number, string]) {}
    foo32 (...[1, "111"]) // Types of '1' and "111" must be assignable to 'number' and 'string'
    'accordingly
    // p becomes tuple [1, "111"]

function foo4 (...p: number[]) {}
    foo4 (1, ...[2, 3]) //
    // p becomes array [1, 2, 3]

function foo5 (p1: number, ...p2: number[]) {}
    foo5 (...[1, 2, 3]) //
    // p1 becomes 1, p2 becomes array [2, 3]

### 15.7 Type Inference

ArkTS supports strong typing but allows not to burden a programmer with the task of specifying type annotations everywhere. A smart compiler can infer types of some entities and expressions from the surrounding context. This technique called type inference allows keeping type safety and program code readability, doing less typing, and focusing on business logic. Type inference is applied by the compiler in the following contexts:

• Type Inference for Numeric Literals;

• Variable and constant declarations (see Type Inference from Initializer);

• Implicit generic instantiations (see Implicit Generic Instantiations);

• Function, method or lambda return type (see Return Type Inference);

## Page 264

• Lambda expression parameter type (see Lambda Signature);

• Array literal type inference (see Array Literal Type Inference from Context, and Array Type Inference from Types of Elements);

• Object literal type inference (see Object Literal);

• Smart types (see Smart Types).

#### 15.7.1 Type Inference for Numeric Literals

The type of expression of a numeric type for Constant Expressions is first evaluated from the expression as follows:

• Type of an integer literal is the default type of the literal: int or long (see Integer Literals);

• Type of a floating-point literal is the default type of the literal: double or float (see Floating-Point Literals);

• Type of a named constant is specified in the constant declaration;

• Result type of an operator is evaluated according to the rules of the operator;

• Type of a Cast Expression is specified in the expression target type.

The evaluated numeric result type can be inferred to a numeric target type from the context on condition that:

1. Last executed operator in the expression is not a cast operator as;

2. Target type is a numeric type larger than the evaluated result type; or

3. The evaluated result type is an integer type, the target type is a smaller integer type with the value of the expression fitting into its range; or

4. The target type is float, the evaluated result type is double and the value of the expression fits into the range of type float.

A compile-time error occurs if the context is a union type, and the evaluated value can be treated as value of several of union component types.

Valid and invalid narrowing is represented in the examples below:

let b: byte = 127 // ok, int -> byte narrowing
b = 64 + 63 // ok, int -> byte narrowing
b = 128 // compile-time-error, value is out of range
b = 1.0 // compile-time-error, floating-point value cannot be narrowed
b = 1 as short // // compile-time-error, cast expression fixes 'short' type

let s: short = 32768 // compile-time-error, value is out of range

let u: byte | int = 1 // compile-time error, ambiguity

## Page 265

#### 15.7.2 Smart Types

Data entities like local variables (see Variable and Constant Declarations) and parameters (see Parameter List), if not captured in a lambda body and modified by the lambda code, are subjected to smart typing.

Every data entity has a static type, which is specified explicitly or inferred at the point of declaration. This type defines the set of operations that can be applied to the entity (namely, what methods can be called, and what other entities can be accessed if the entity acts as a receiver of the operation):

let a = new Object
a.toString() // entity 'a' has method toString()

If an entity is class type (see Classes), interface type (see Interfaces), or union type (see Union Types), then the compiler can narrow (smart cast) a static type to a more precise type (smart type), and allow operations that are specific to the type so narrowed:

function boo() {
    let a: number | string = 42
    a++ /* Smart type of 'a' is number and number-specific operations are type-safe */
}

class Base {}
class Derived extends Base { method () {} }
function goo() {
    let b: Base = new Derived
    b.method () /* Smart type of 'b' is Derived and Derived-specific operations can be applied in type-safe way */
}

Other examples are explicit calls to instanceof (see InstanceOf Expression) or checks against null (see Equality Expressions) as parts of if statements (see if Statements) or ternary conditional expressions (see Ternary Conditional Expressions):

function foo (b: Base, d: Derived|null) {
    if (b.instanceof Derived) {
        b.method()
    }
    if (d != null) {
        d.method()
    }
}

In like cases, a smart compiler requires no additional checks or casts (see Cast Expression) to deduce a smart type of an entity.

Overloading (see Overload Declarations) can cause tricky situations when a smart type results in calling an entity that suits the smart type rather than a declared type of an argument (see Overload Resolution):

class Base {b = 1}
class Derived extends Base{d = 2}

function fooBase (p: Base) {}
function fooDerived (p: Derived) {}

(continues on next page)

## Page 266

(continued from previous page)

7 overload foo { fooDerived, fooBase }

8 function too() {
    let a: Base = new Base
    foo (a) // fooBase will be called
    let b: Base = new Derived
    foo (b) // as smart type of 'b' is Derived, fooDerived will be called
}

Particular cases supported by the compiler are determined by the compiler implementation.

### 15.8 Overriding

Method overriding is the language feature closely connected with inheritance. It allows a subclass or a subinterface to offer a specific implementation of a method already defined in its supertype optionally with modified signature.

The actual method to be called is determined at runtime based on object type. Thus, overriding is related to runtime polymorphism.

ArkTS uses the override-compatibility rule to check the correctness of overriding. The overriding is correct if method signature in a subtype (subclass or subinterface) is override-compatible with the method defined in a supertype (see Override-Compatible Signatures).

An implementation is forced to Make a Bridge Method for Overriding Method in some cases of method overriding.

#### 15.8.1 Overriding in Classes

Note. Only accessible (see Accessible) methods are subjected to overriding. The same rule applies to accessors in case of overriding.

An overriding member can keep or extend an access modifier (see Access Modifiers) of a member that is inherited or implemented. Otherwise, a compile-time error occurs.

A compile-time error occurs if an attempt is made to do the following:

• Override a private method of a superclass; or

- Declare a method with the same name as that of a private method with default implementation from any super-interface.

class Base {
    public public_member() {}
    protected protected_member() {}
    private private_member() {}
}

interface Interface {
