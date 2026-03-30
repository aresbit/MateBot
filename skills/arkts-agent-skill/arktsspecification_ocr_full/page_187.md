The implementation of an optional interface property as a field is represented in the example below:

interface I {
    num?: number
}
class C implements I {
    num?: number = 42
}

For the example above, the private hidden field and the required accessors are defined implicitly for the class C overriding accessors from the interface:

class C implements I {
    private $$_num: number = 42 // the exact name of the field is implementation specific
    get num(): number | undefined { return this.$_num }
    set num(n: number | undefined) { this.$_num = n }
}

If a property is implemented by accessors (see Class Accessor Declarations), then it is acceptable to implement only one accessor for an optional field, and use default implementation for another accessor as represented in the following example:

interface I {
    num?: number
}

class C1 implements I { // OK, both default implementations
    }

    class C2 implements I { // OK, default implementation used for get set num(n: number | undefined) { this.$_num = n }
    }

    class C3 implements I { // OK, both explicit implementations get num(): number | undefined { return this.$_num }
    set num(n: number | undefined) { this.$_num = n }
}

A compile-time error occurs, if an optional property in an interface is implemented as non-optional field:

interface I {
    num?: number
}

class C implements I {
    num: number = 42 // compile-time error, must be optional
}
