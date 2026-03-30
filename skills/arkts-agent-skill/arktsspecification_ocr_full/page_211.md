• All methods inherited from superinterfaces refer to the same implementation, and this default implementation is the current interface method; or

• One method m in some superinterface overrides all other methods from other superinterfaces.

Otherwise, a compile-time error occurs.

interface I1 { foo () {} }
interface I2 { foo () {} }
interface II1 extends I1, I2 {
    foo () {} // foo() from II1 overrides both foo() from I1 and foo() from I2
}
interface II2 extends I1, I2 {
    // Compile-time error as foo() from I1 and foo() from I2 have different_
    →implementations
}
interface I3 extends I1 {}
interface I4 extends I1 {}
interface II3 extends I3, I4 {
    // OK, as foo() from I3 and foo() from I4 refer to the same implementation
}
class Base {}
class Derived extends Base {}
interface II1 {
    foo (p: Base) {}
}
interface II2 {
    foo (p: Derived) {}
}
interface II3 extends II1, II2 {}
    // foo() from II1 overrides foo() from II2

### 10.3 Interface Members

An interface declaration can contain interface members, i.e., its properties (see Interface Properties) and methods (see Interface Method Declarations).

The syntax of interface member is presented below:

interfaceMember
    : annotationUsage?
    ( interfaceProperty
    | interfaceMethodDeclaration
    | overloadInterfaceMethodDeclaration
)

The scope of declaration of a member m that the interface type I declares or inherits is specified in Scopes.
