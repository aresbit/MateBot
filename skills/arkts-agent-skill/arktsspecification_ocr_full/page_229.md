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
