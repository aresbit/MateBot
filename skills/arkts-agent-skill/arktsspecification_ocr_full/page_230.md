The export can be imported only by providing a name for the constant variable that is exported by using this export directive. Otherwise, a compile-time error occurs.

// File1
class A {
    foo () {}
}
export default new A

// File2
import {default as a} from "File1"

a.foo() // Calling method foo() of class A where 'a' is an instance of type A
a = new A // Compile-time error as 'a' is a constant variable

// File3
import * as a from "File1" /* Compile-time error: such form of import
cannot be used for the default export */

If a function, a variable, a constant, or an accessor is exported, or an exported class field or method is public, then any type declared in the current module and used in their declaration must be exported. Otherwise, a compile-time error occurs.

// Module
export function foo (p: SomeType): SomeType { ... } // Type 'SomeType' is not exported
export let v: SomeType // Type 'SomeType' is not exported
export class SomeClass {
    field: SomeType // Type 'SomeType' is not exported
    foo (p: SomeType): SomeType { ... } // Type 'SomeType' is not exported
}
class SomeType {}

### 13.4 Namespace Declarations

Namespace declaration introduces the qualified name to be used as a qualifier for access to each exported entity of the namespace.

The syntax of namespace declarations is presented below:

namespaceDeclaration:
    'namespace' qualifiedName
    '{' namespaceMember* staticBlock? namespaceMember* '}'
;

namespaceMember:
    topDeclaration | exportDirective
;

Namespace can have an initializer block (staticBlock in namespace declaration syntax above). The initializer block is called only in case when at least one of exported namespace members is used in the program. It is guaranteed that its
