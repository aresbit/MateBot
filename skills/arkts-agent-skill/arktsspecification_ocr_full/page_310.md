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
