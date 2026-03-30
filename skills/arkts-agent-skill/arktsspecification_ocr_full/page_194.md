(continued from previous page)

let y = new C()
console.log(y.f) // runtime or compile-time error

Note. Access to a field with late initialization in most cases is less performant than access to other fields.

TypeScript uses the term definite assignment assertion for the notion similar to late initialization. However, ArkTS uses stricter rules.

#### 9.6.6 Overriding Fields

When extending a class or implementing interfaces, a field declared in a superclass or a superinterface can be overridden by a field with the same name, and the same static or non-static modifier status. Using the keyword override is not required. The new declaration acts as redeclaration.

A compile-time error occurs if:

• Field marked with the modifier override does not override a field from a superclass.

• Field declaration contains the modifier static along with the modifier override.

• Types of the overriding field and of the overridden field are different.

class C {
    field: number = 1
}

class D extends C {
    field: string = "aa" // compile-time error: type is not the same
    override no_field = 1224 // compile-time error: no overridden field in the base_
    →class
        static override field: string = "aa" // compile-time error: static cannot override
}

Initializers of overridden fields are preserved for execution, and the initialization is normally performed in the context of superclass constructors.

class C {
    field: number = this.init()
    private init() {
        console.log("Field initialization in C")
        return 123
    }
}

class D extends C {
    override field: number = 123 // field can be explicitly marked as overridden
}

class Derived extends D {
    field = this.init_in_derived()
    private init_in_derived() {
        console.log("Field initialization in Derived")
        return 42
    }
}

(continues on next page)
