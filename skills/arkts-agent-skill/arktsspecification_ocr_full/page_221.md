## MODULES AND NAMESPACES

Programs in ArkTS are structured as sequences of elements ready for compilation called modules. Each module creates its own scope (see Scopes). Variables, functions, classes, interfaces, or other declarations of a module are only accessible (see Accessible) within such a scope if not explicitly exported.

A variable, function, class, interface, or other declarations exported from a module must be imported first by the module that is to use them.

All modules are stored in a file system or a database (see Modules in Host System).

A module can optionally consist of the following four parts:

1. Import directives that enable referring imported declarations in a module;

2. Top-level declarations;

3. Top-level statements; and

4. Re-export directives.

The syntax of module is presented below:

moduleDeclaration:
    importDirective* (topDeclaration | topLevelStatements | exportDirective)*
;

Every module can directly use all exported entities from the standard library (see Standard Library Usage).

// Hello, world! module
function main() {
    console.log("Hello, world!") // console is defined in the standard library
}

If a module has at least one top-level ambient declaration (see Ambient Declarations) then all other declarations must be ambient as well and no top-level statements (see Top-Level Statements). Otherwise, a compile-time error occurs.

declare let x: number
function main() {}
// compile-time error: ambient and non-ambient declarations are mixed
