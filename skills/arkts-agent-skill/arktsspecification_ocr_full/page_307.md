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
