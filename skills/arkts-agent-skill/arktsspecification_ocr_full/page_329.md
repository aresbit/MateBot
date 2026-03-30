### 20.7 OutOfMemoryError for Primitive Type Operations

The execution of some primitive type operations (e.g., increment, decrement, and assignment) can throw OutOfMemoryError (see Error Handling) if allocation of a new object is required but the available memory is not sufficient to perform it.

### 20.8 Make a Bridge Method for Overriding Method

Situations are possible where the compiler must create an additional bridge method to provide a type-safe call for the overriding method in a subclass of a generic class. Overriding is based on erased types (see Type Erasure). The situation is represented in the following example:

class B<T extends Object> {
    foo(p: T) {}
}

class D extends B<string> {
    foo(p: string) {} // original overriding method
}

In the example above, the compiler generates a bridge method with the name foo and signature (p: Object). The bridge method acts as follows:

- Behaves as an ordinary method in most cases, but is not accessible from the source code, and does not participate in overloading;

• Applies narrowing to argument types inside its body to match the parameter types of the original method, and invokes the original method.

The use of the bridge method is represented by the following code:

let d = new D()
d.foo("aa") // original method from 'D' is called
let b: B<string> = d
b.foo("aa") // bridge method with signature (p: Object) is called
// its body calls original method, using (p as string) to check the type of the argument

More formally, a bridge method  $ m(C_1, \ldots, C_n) $ is created in D, in the following cases:

• Class B comprises type parameters  $ B<T_1 $ extends  $ C_1 $, ...,  $ T_n $ extends  $ C_n> $;

• Subclass D is defined as class D extends B<X₁, ..., Xₙ>;

• Method m of class D overrides m from B with type parameters in signature, e.g.,  $ (T_1, \ldots, T_n) $;

• Signature of the overridden method m is not  $ (C_{1}, \ldots, C_{n}) $.
