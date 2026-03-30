# Chapter 8: Annotations

Page range: 305-312

## Page 305

#### 17.10.2 Native Methods

Native method is a method marked with the keyword native (see Method Declarations).

Native methods are the methods implemented in a platform-dependent code written in another programming language (e.g., C).

A compile-time error occurs if:

• Method declaration contains the keyword abstract along with the keyword native.

• Native method has a body (see Method Body) that is a block instead of a simple semicolon or empty body.

#### 17.10.3 Native Constructors

Native constructor is a constructor marked with the keyword native (see Constructor Declaration).

Native constructors are the constructors implemented in a platform-dependent code written in another programming language (e.g., C).

A compile-time error occurs if a native constructor has a non-empty body (see Constructor Body).

### 17.11 Classes Experimental

#### 17.11.1 Final Classes

A class can be declared final to prevent extension, i.e., a class declared final can have no subclasses. No method of a final class can be overridden.

If a class type F expression is declared final, then only a class F object can be its value.

A compile-time error occurs if the extends clause of a class declaration contains another class that is final.

#### 17.11.2 Final Methods

A method can be declared final to prevent it from being overridden (see Overriding Methods) in subclasses.

A compile-time error occurs if:

• The method declaration contains the keyword abstract or static along with the keyword final.

• A method declared final is overridden.

## Page 306

#### 17.11.3 Constructor Names

A Constructor Declaration allows a developer to set a name used to explicitly specify constructor to call in New Expressions:

class Temperature{
    // use specified scale:
    constructor Celsius(n: double) {/*body1*/}/
    constructor Fahrenheit(n: double) {/*body2*/}/
}

new Temperature.Celsius(0)
new Temperature.Fahrenheit(32)

If a constructor has a name, then using the constructor directly in a new expression implies using the constructor name explicitly:

class X{
    constructor ctor1(p: number) {/*body1*/}
    constructor ctor2(p: string) {/*body2*/}
}

new X(1) // compile-time error
new X("abs") // compile-time error
new X.ctor1(1) // OK
new X.ctor2("abs") // OK

A compile-time error occurs if a constructor name is used as a named reference (see Named Reference) in any expression.

class X{
    constructor foo() {}
}
const func = X.foo // Compile-time error

The feature is also important for Constructor Overload Declarations.

### 17.12 Default Interface Method Declarations

The syntax of interface default method is presented below:

interfaceDefaultMethodDeclaration:
    'private'? identifier signature block
;

A default method can be explicitly declared private in an interface body.

A block of code that represents the body of a default method in an interface provides a default implementation for any class if such a class does not override the method that implements the interface.

## Page 307

### 17.13 Adding Functionality to Existing Types

ArkTS supports adding functions and accessors to already defined types. The usage of functions so added looks the same as if they are methods and accessors of these types. The mechanism is called Functions with Receiver and Accessors with Receiver. This feature is often used to add new functionality to a class or an interface without having to inherit from the class or to implement the interface. However, it can be used not only for classes and interfaces but also for other types.

Moreover, Function Types with Receiver and Lambda Expressions with Receiver can be defined and used to make the code more flexible.

#### 17.13.1 Functions with Receiver

Function with receiver declaration is a top-level declaration (see Top-Level Declarations) that looks almost the same as Function Declarations, except that the first mandatory parameter uses keyword this as its name.

The syntax of function with receiver is presented below:

functionWithReceiverDeclaration:
    'function' identifier typeParameters? signatureWithReceiver block;

signatureWithReceiver:
    '(' receiverParameter (',' parameterList)? ')' returnType?
;

receiverParameter:
    annotationUsage? 'this' ':' type
;

Function with receiver can be called in the following two ways by making:

• Ordinary function call (see Function Call Expression) when the first argument is the receiver object;

• Method call (see Method Call Expression) when the receiver is an objectReference before the function name passed as the first argument of the call.

All other arguments are handled in an ordinary manner.

Note. Derived classes or interfaces can be used as receivers.

class C {}

function foo(this: C) {}
function bar(this: C, n: number): void {}

let c = new C()

// as a function call:

(continues on next page)

## Page 308

(continued from previous page)

foo(c)
bar(c, 1)

// as a method call:
c.foo()
c.bar(1)

interface D {
    function foo1(this: D) {
        function bar1(this: D, n: number): void {
            function demo (d: D) {
                // as a function call:
                foo1(d)
                bar1(d, 1)
                
                // as a method call:
                    d.foo1()
                    d.bar1(1)
            }
            class E implements D {
                const e = new E
            
            // derived class is used as a receiver for a method call:
                e.foo1()
                e.bar1(1)
            
            // the same as a function call:
                foo1(e)
                bar1(e, 1)
            }
        }
    }
}

The keyword this can be used inside a function with receiver. It corresponds to the first parameter. Otherwise, a compile-time error occurs. The type of parameter this is called the receiver type (see Receiver Type).

If the receiver type is a class or interface type, then private or protected members are not accessible (see Accessible) within the body of a function with receiver. Only public members can be accessed:

class A {
    foo() { ... this.bar() ... }
    // function bar() is accessible here
    protected member_1 ...
    private member_2 ...
}

function bar(this: A) { ...
    this.foo() // Method foo() is accessible as it is public
    this.member_1 // Compile-time error as member_1 is not accessible
    this.member_2 // Compile-time error as member_2 is not accessible
    ...
}

let a = new A()
a.foo() // Ordinary class method is called
a.bar() // Function with receiver is called

## Page 309

A compile-time error occurs if the name of a function with receiver is the same as the name of an accessible (see Accessible) instance method or field of the receiver type:

class A {
    foo () { ... }
}
function foo(this: A) { ... } // Compile-time error to prevent ambiguity below
(new A).foo()

A compile-time error occurs if an attempt is made to call a function with receiver from a derived class variable:

class B extends A {
    const b = new B
    b.foo()  // Compile-time error
    foo (b)  // OK
}

Function with receiver cannot have the same name as a global function. Otherwise, a compile-time error occurs.

function foo(this: A) { ... }
function foo() { ... } // Compile-time error

Function with receiver can be generic as in the following example:

function foo<T>(this: B<T>, p: T) {
    console.log(p)
}

function demo(p1: B<SomeClass>, p2: B<BaseClass>) {
    p1.foo(new SomeClass())
        // Type inference should determine the instantiating type
    p2.foo<BaseClass>(new DerivedClass())
        // Explicit instantiation
}

Functions with receiver are dispatched statically. What function is being called is known at compile time based on the receiver type specified in the declaration. A function with receiver can be applied to the receiver of any derived class until it is overridden within the derived class:

class Base { ... }
class Derived extends Base { ... }

function foo(this: Base) { console.log("Base.foo is called") }

let b: Base = new Base()

b.foo() // `Base.foo is called` to be printed
b = new Derived()

b.foo() // `Base.foo is called` to be printed

A function with receiver can be defined in a module other than the one that defines the receiver type. This is represented in the following examples:

// file a.ets
class A {
    foo() { ... }
}

(continues on next page)

## Page 310

{
    "file ext.ets"
    import {A} from "a.ets" // name 'A' is imported
    function bar(this: A) {
        this.foo() // Method foo() is called
    }
}

#### 17.13.2 Receiver Type

Receiver type is the type of the receiver parameter in a function, function type, and lambda with receiver. A receiver type may be an interface type, a class type, an array type, or a type parameter. Otherwise, a compile-time error occurs.

The use of array type as receiver type is presented in the example below:

function addElements(this: number[], ...s: number[]) {
    ...
}

let x: number[] = [1, 2]
x.addElements(3, 4)

#### 17.13.3 Accessors with Receiver

Note. Accessor declarations at the top level or in namespaces are of the following two kinds:

• Accessors with Receiver (as described in this subsection) that can be used much like fields of a class; and

Accessor with receiver declaration is either a top-level declaration (see Top-Level Declarations), or a declaration inside a namespace (see Namespace Declarations) that can be used as class (see Class Accessor Declarations) or interface accessor (see Interface Properties) for a specified receiver type:

The syntax of accessor with receiver is presented below:

accessorWithReceiverDeclaration:
    'get' identifier '(' receiverParameter ')' returnType block
| 'set' identifier '(' receiverParameter ',' parameter ')' block
;

The keyword this can be used inside a function with receiver. It corresponds to the first parameter. Otherwise, a compile-time error occurs. The type of parameter this is called the receiver type (see Receiver Type).

If the receiver type is a class type or an interface type, then private or protected members are not accessible (see Accessible) within the body of a function with receiver. Only public members can be accessed:

A get-accessor (getter) must have the keyword this as the only getter parameter (receiverParameter) and an explicit return type.

## Page 311

A set-accessor (setter) must have a keyword this as a first setter parameter (receiver parameter), one other parameter, and no return type.

The keyword this has the same meaning and can be used in the same manner as described in Functions with Receiver:

- The keyword this can be used inside an accessor with receiver. It corresponds to the first parameter. Otherwise, a compile-time error occurs.

• The type of parameter this is called the receiver type (see Receiver Type).

• If the receiver type is a class or interface type, then private or protected members are not accessible (see Accessible) within the body of a function with receiver. Only public members can be accessed.

Note. If the accessor with receiver is an entity of a namespace, then the same rules apply to it when exporting and using qualified names as the rules that apply to other namespace entities (see Namespace Declarations).

The use of getters and setters looks the same as the use of fields:

名

A compile-time error occurs if an accessor is used in the form of a function or a method call.

#### 17.13.4 Function Types with Receiver

Function type with receiver specifies the signature of a function or lambda with receiver. It is almost the same as function type (see Function Types), except that the first parameter is mandatory, and the keyword this is used as its name:

The syntax of function type with receiver is presented below:

functionTypeWithReceiver:
    '(' receiverParameter (',' ftParameterList)? ')' ftReturnType
;

The type of a receiver parameter is called the receiver type (see Receiver Type).

## Page 312

class A {...}

type FA = (this: A) => boolean
type FN = (this: number[], max: number) => number

Function type with receiver can be generic as in the following example:

class B<T> {...}

type FB<T> = (this: B<T>, x: T): void
type FBS = (this: B<string>, x: string): void

The usual rule of function type compatibility (see Subtyping for Function Types) is applied to function type with receiver, and parameter names are ignored.

class A {...}

type F1 = (this: A) => boolean
type F2 = (a: A) => boolean

function foo(this: A): boolean {}
function goo(a: A): boolean {}

let f1: F1 = foo // ok
f1 = goo // ok

let f2: F2 = goo // ok
f2 = foo // ok
f1 = f2 // ok

The sole difference is that only an entity of function type with receiver can be used in Method Call Expression. The declarations from the previous example are reused in the example below:

let a = new A()
a.f1() // ok, function type with receiver
f1(a) // ok

a.f2() // compile-time error
f2(a) // ok

#### 17.13.5 Lambda Expressions with Receiver

Lambda expression with receiver defines an instance of a function type with receiver (see Function Types with Receiver). It looks almost the same as an ordinary lambda expression (see Lambda Expressions), except that the first parameter is mandatory, and the keyword this is used as its name:

The syntax of lambda expression with receiver is presented below:

lambdaExpressionWithReceiver:
    annotationUsage?

(continues on next page)
