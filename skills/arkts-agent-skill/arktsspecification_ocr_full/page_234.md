namespace A.B {
    /*some declarations*/
}

The code above is the shortcut to the following code:

namespace A {
    export namespace B {
        /*some declarations*/
    }
}

This code illustrates the usage of declarations in the following case:

namespace A.B.C {
    export function foo() { ... }
}

A.B.C.foo() // Valid function call, as 'B' and 'C' are implicitly exported

If an ambient namespace (see Ambient Namespace Declarations) defined in a module (see Modules and Namespaces), then all ambient namespace declarations are accessible across all declarations and top-level statements of the module.

declare namespace A {
    function foo(): void
        type X = Array<number>
    }

    A.foo() // Valid function call, as 'foo' is accessible for top-level statements
    function foo() {
        A.foo() // Valid function call, as 'foo' is accessible here as well
    }
    class C {
        method () {
            A.foo() // Valid function call, as 'foo' is accessible here too
            let x: A.X = [] // Type A.X can be used
        }
    }
}

### 13.5 Export Directives

Export directive allows the following:

• Specifying a selective list of exported declarations with optional renaming;

• Specifying a name of one declaration;

• Exporting a type; or

• Re-exporting declarations from other modules.

The syntax of an export directive is presented below:
