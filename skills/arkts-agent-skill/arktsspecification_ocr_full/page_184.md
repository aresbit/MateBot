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
