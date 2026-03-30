export function foo() { console.log("1st A.foo() exported") }
function bar() { }
export namespace C {
    export function too() { console.log("1st A.C.too() exported") }
}

namespace B {
    namespace A {
        export function goo() {
            A.foo() // calls exported foo()
            foo()    /* calls exported foo() as well as all A namespace declarations are merged into one */
            A.C.moo()
        }
        //export function foo() { }
        //Compile-time error as foo() was already defined
        //function foo() { console.log("2nd A.foo() non-exported") }
        //Compile-time error as foo() was already defined as exported
    }

    namespace A.C {
        export function moo() {
            too() // too() accessible when namespace C and too() are both exported
            A.C.too()
        }
    }

    A.goo()

    //File
    namespace A {
        export function foo() { ... }
        export function bar() { ... }
    }

    namespace A {
        function goo() { bar() } // exported bar() is accessible in the same namespace
        export function foo() { ... } // Compile-time error as foo() was already defined
    }

    namespace X {
        static {
            namespace X {
                static {} // Compile-time error as only one initializer allowed
            }
        }
    }
}

Note. A namespace name can be a qualified name. It is a shortcut notation of embedded namespaces as represented below:
