public_member()    // All members are public in interfaces
private private_member() {} // Except private methods with default implementation
}

class Derived extends Base implements Interface {
    public override public_member() {}
    // Public member can be overridden and/or implemented by the public one
    public override protected_member() {}
    // Protected member can be overridden by the protected or public one
    override private_member() {}
    // A compile-time error occurs if an attempt is made to override private member
    // or implement the private methods with default implementation
}

The table below represents semantic rules that apply in various contexts:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Context</td><td style='text-align: center; word-wrap: break-word;'>Semantic Check</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>An instance method is defined in a subclass with the same name as the instance method in a superclass.</td><td style='text-align: center; word-wrap: break-word;'>If signatures are override-compatible (see Override-Compatible Signatures), then overriding is used. Otherwise, a compile-time error occurs.</td></tr></table>

class Base {
    method_1() {}
    method_2(p: number) {}
}

class Derived extends Base {
    override method_1() {} // overriding
    method_2(p: string) {} // compile-time error
}

A constructor is defined in a subclass.

All base class constructors are available for call in all derived class constructors via super call (see Explicit Constructor Call).

class Base {
    constructor(p: number) {}
}

class Derived extends Base {
    constructor(p: string) {
        super(5)
    }
}
