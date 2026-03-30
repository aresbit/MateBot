### 3.4 Named Types

Named types are classes, interfaces, enumerations, aliases, type parameters, and predefined types (see Predefined Types), except built-in arrays. Other types (i.e., array, function, and union types) are anonymous unless aliased. Respective named types are introduced by the following:

• Class declarations (see Classes),

• Interface declarations (see Interfaces),

• Enumeration declarations (see Enumerations),

• Type alias declarations (see Type Alias Declaration), and

• Type parameter declarations (see Type Parameters).

Classes, interfaces and type aliases with type parameters are generic types (see Generics). Named types without type parameters are non-generic types.

Type references (see Type References) refer to named types by specifying their type names and (where applicable) type arguments to be substituted for the type parameters of a named type.

### 3.5 Type References

Type reference refers to a type by one of the following:

• Simple or qualified type name (see Names),

• Type alias (see Type Alias Declaration).

Type reference that refers to a generic class or to an interface type is valid if it is a valid instantiation of a generic. Its type arguments can be provided explicitly or implicitly based on defaults.

The syntax of type reference is presented below:

typeReference:
    typeReferencePart ('.' typeReferencePart)*
;

typeReferencePart:
    identifier typeArguments?
;

let map: Map<string, number> // Map<string, number> is the type reference

class A<T> {...}

class C<T> {
    field1: A<T> // A<T> is a class type reference - class type reference
    field2: A<number> // A<number> is a type reference - class type reference
    foo (p: T) {} // T is a type reference - type parameter
    constructor () { /* some body to init fields */ }
}

type MyType<T> = A<T>[]
