# Chapter 14: Ambient Declarations

Page range: 229-236

## Page 229

### 13.3 Top-Level Declarations

Top-level declarations declare top-level types (class, interface, or enum see Type Declarations), top-level variables (see Variable Declarations), constants (see Constant Declarations), functions (see Function Declarations, overloads (see Overload Declarations), namespaces (see Namespace Declarations), or other declarations (see Ambient Declarations, Annotations, Functions with Receiver, Accessors with Receiver). Top-level declarations can be exported.

The syntax of top-level declarations is presented below:

topDeclaration:
('export' 'default'?)?
annotationUsage?
( typeDeclaration
| variableDeclarations
| constantDeclarations
| functionDeclaration
| overloadFunctionDeclaration
| namespaceDeclaration
| ambientDeclaration
| annotationDeclaration
| accessorDeclaration
| functionWithReceiverDeclaration
| accessorWithReceiverDeclaration
)

export let x: number[], y: number

The usage of annotations is discussed in Using Annotations.

#### 13.3.1 Exported Declarations

Top-level declarations can use export modifiers that make the declarations accessible (see Accessible) in other modules by using import (see Import Directives). The same result may be achieved using export directive (see Export Directives) for the top-level declaration. The declarations which are not exported as mentioned above can be used only inside the module they are declared in.

export class Point {}
export let Origin = new Point(0, 0)
export function Distance(p1: Point, p2: Point): number {
    // ...
}

In addition, only one top-level declaration can be exported by using the default export directive. It allows specifying no declared name when importing (see Default Import Binding for details). A compile-time error occurs if more than one top-level declaration is marked as default.

export default let PI = 3.141592653589

Another supported form of export default is using an expression as export default target. This export directive effectively means that an anonymous constant variable is created with a value equal to the value of the expression evaluation result.

## Page 230

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

## Page 231

code is called before any use of namespace members (see Static Initialization for detail).

The usage of a namespace is represented in the example below:

namespace NS1 {
    export function foo() { }
    export let variable = 1234
    export const constant = 1234
    export let someVar: string

    // Will be called before any use of NS1 members
    static {
        someVar = "some string"
        console.log("Init for NS1 done")
    }
    export function bar() {}
}

namespace NS2 {
    export const constant = 1
    // Will never be called since NS2 members are never used
    static {
        console.log("Init for NS2 done")
    }
    export function bar() {}
}

export function bar() {} // That is a different bar()

if (NS1.variable == NS1.constant) {
    NS1.variable = 4321
}

NS1.bar() // namespace bar() is called
bar() // top-level bar() is called

Note. An exported namespace entity can be used in the form of a qualifiedName outside a namespace in the same module. Any namespace entity can be and typically is used inside a namespace without qualification, i.e., without a namespace name. A qualifiedName inside a namespace can be used for a namespace entity only when the entity is exported. Using a qualifiedName for non-exported entity both inside and outside a namespace causes a compile-time error:

namespace NS {
    export let a: number = 1
    let b = 2

    export function foo() {
        let v: number
        v = a // OK, no qualification
        v = NS.a // OK, `a` exported
    }

    export function bar() {
        let v: number
        v = b // OK, no qualification

(continues on next page)

## Page 232

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

## Page 233

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

## Page 234

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

## Page 235

exportDirective:
    selectiveExportDirective
| singleExportDirective
| exportTypeDirective
| reExportDirective
;

#### 13.5.1 Selective Export Directive

Top-level declarations can be made exported by using a selective export directive. The selective export directive provides an explicit list of names of the declarations to be exported. Optional renaming allows having the declarations exported with new names.

The syntax of selective export directive is presented below:

selectiveExportDirective:
'export' selectiveBindings
;

A selective export directive uses the same selective bindings as an import directive:

export { d1, d2 as d3 }

The above directive exports ‘d1’ by its name, and ‘d2’ as ‘d3’. The name ‘d2’ is not accessible (see Accessible) in the modules that import this module.

#### 13.5.2 Single Export Directive

Single export directive allows specifying the declaration to be exported from the current module by using the declaration's own name, or anonymously.

The syntax of single export directive is presented below:

singleExportDirective:
  'export'
  (identifier
    | 'default' (expression | identifier)
    | '{' identifier 'as' 'default' '}'
)
;

If default is present, then only one such export directive is possible in the current module. Otherwise, a compile-time error occurs.

The directive in the example below exports variable 'v' by its name:

## Page 236

export v
let v = 1

The directive in the example below exports class ‘A’ by its name as default export:

class A {}
export default A
export {A as default} // such syntax is also acceptable

The directive in the example below exports a constant variable anonymously:

class A {}
export default new A

Single export directive acts as re-export when the declaration referred to by identifier is imported.

import {v} from "some location"
export v

#### 13.5.3 Export Type Directive

An export directive can have a type modifier exclusively for a better syntactic compatibility with TypeScript (also see Import Type Directive).

The export type directive syntax is presented below:

exportTypeDirective:
    'export' 'type' selectiveBindings
;

ArkTS supports no additional semantic checks for entities exported by using export type directives.

#### 13.5.4 Re-Export Directive

In addition to exporting what is declared in the module, it is possible to re-export declarations that are part of other modules' export. A particular declaration or all declarations can be re-exported from a module. When re-exporting, new names can be given. This action is similar to importing but has the opposite direction.

The syntax of re-export directive is presented below:

reExportDirective:
'export'
('*' bindingAlias?
| selectiveBindings
| '{' 'default' bindingAlias? '}'
)

(continues on next page)
