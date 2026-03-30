#### 9.7.5 Overriding Methods

The override modifier indicates that an instance method in a superclass is overridden by the corresponding instance method from a subclass (see Overriding).

The usage of the modifier override is optional but strongly recommended as it makes the overriding explicit.

A compile-time error occurs if:

• Method marked with the modifier override overrides no method from a superclass.

• Method declaration contains modifier static along with the modifier override.

If the signature of an overridden method contains parameters with default values (see Optional Parameters), then the overriding method must always use the same default parameter values for the overridden method. Otherwise, a compile-time error occurs.

More details on overriding are provided in Overriding in Classes and Overriding and Overloading in Interfaces.

#### 9.7.6 Native Methods

Native methods are discussed in Native Methods.

#### 9.7.7 Method Body

Method body is a block of code that implements a method. A semicolon or an empty body (i.e., no body at all) indicates the absence of implementation.

An abstract or native method must have an empty body.

In particular, a compile-time error occurs if:

• The body of an abstract or native method declaration is a block.

• The method declaration is neither abstract nor native, but its body is either empty

The rules that apply to return statements in a method body are discussed in return Statements.

A compile-time error occurs if a method is declared to have a return type, but its body can complete normally (see Normal and Abrupt Statement Execution).

#### 9.7.8 Methods Returning this

A return type of an instance method can be this. It means that the return type is the class type to which the method belongs. It is the only place where the keyword this can be used as type annotation (see Signatures and Return Type).

The only result that is allowed to be returned from such a method is this:
