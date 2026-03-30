}

Note. A namespace must be exported to be used in another module:

// File1
namespace Space1 {
    export function foo() { ... }
    export let variable = 1234
    export const constant = 1234
}
export namespace Space2 {
    export function foo(p: number) { ... }
    export let variable = "1234"
}

// File2
import {Space2 as Space1} from "File1"

// compile-time error - there is no variable or constant called 'constant'
if (Space1.variable == Space1.constant) {
    // compile-time error - incorrect assignment as type 'number'
    // is not compatible with type 'string'
    Space1.variable = 4321
}
Space1.foo() // compile-time error - there is no function 'foo()'
Space1.foo(1234) // OK

Note. Embedded namespaces are allowed:

namespace ExternalSpace {
    export function foo() { ... }
    export let variable = 1234
    export namespace EmbeddedSpace {
        export const constant = 1234
    }
}

if (ExternalSpace.variable == ExternalSpace.EmbeddedSpace.constant) {
    ExternalSpace.variable = 4321
}

Note. Namespaces with identical namespace names in a single module merge their exported declarations into a single namespace. A duplication causes a compile-time error. Exported and non-exported declarations with the same name are also considered a compile-time error. Only one of the merging namespaces can have an initializer. Otherwise, a compile-time error occurs.

// One source file
namespace A {

(continues on next page)
