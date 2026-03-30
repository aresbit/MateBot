// File1.d.ets
export declare namespace A { // namespace itself must be exported
    function foo(): void
        type X = Array<number>
    }

    // File2.ets
    import {A} from 'File1.d.ets'

    A.foo() // Valid function call, as 'foo' is accessible for top-level statements
    function foo() {
        A.foo() // Valid function call, as 'foo' is accessible here as well
    }
    class C {
        method() {
            A.foo() // Valid function call, as 'foo' is accessible here too
            let x: A.X = [] // Type A.X can be used
        }
    }
}

A compile-time error occurs if an ambient namespace declaration contains an exportDirective that refers to a declaration which is not a part of the namespace.

export declare namespace A {
    export {foo} // compile-time error: no 'foo' in namespace 'A'
}
function foo() {}

#### 14.6.1 Implementing Ambient Namespace Declaration

If an ambient namespace is implemented in ArkTS, a namespace with the same name must be declared (see Namespace Declarations) as the top-level declaration of a module. All namespace names of a nested namespace (i.e. a namespace embedded into another namespace) must be the same as in ambient context.
