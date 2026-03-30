If the initializer expression contains one of the above patterns, then a compile-time error occurs.

If allowed in the code, the above restrictions can break the consistency of class instances as shown in the following examples:

class C {
    a = this     // Compile-time error

    f1 = this.foo()  // Compile-time error as 'this' method is invoked

    f2 = "a string field"

    foo(): string {
        // Type safety requires fields to be initialized before access
        console.log(this.f1, this.f2)
        return this.f2
    }

    class B {}
    function foo(f: () => B) { return f() }
    class A {
        field1 = foo(() => this.field2)  // Compile-time error as this is used in the_
        → initializer code
        field2 = new B
    }
}

#### 9.6.5 Fields with Late Initialization

Field with late initialization must be an instance field. If it is defined as static, then a compile-time error occurs.

Field with late initialization cannot be of a nullish type (see Nullish Types). Otherwise, a compile-time error occurs.

As all other fields, a field with late initialization must be initialized before it is used for the first time. However, this field can be initialized later and not within a class declaration. Initialization of this field can be performed in a constructor (see Constructor Declaration), although it is not mandatory.

Field with late initialization cannot have field initializers or be an optional field (see Optional Fields). Field with late initialization must be initialized explicitly, even though its type has a default value.

The fact of initialization of field with late initialization is checked when the field value is read. The check is normally performed at runtime. If the compiler identifies an error situation, then the error is reported at compile time:

class C {
    f!: string
}

let x = new C()
x.f = "aa"
console.log(x.f) // ok

(continues on next page)
