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
