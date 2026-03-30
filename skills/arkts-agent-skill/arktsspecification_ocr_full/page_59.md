#### 3.20.3 Keyof Types

Keyof type is a special form of a union type that is built by using the keyword keyof. The keyword keyof is applied to a class or an interface type (see Classes and Interfaces). The resultant new type is a union of names (as string literal types) of all accessible members (see Accessible) of the class or the interface type.

The syntax of keyof type is presented below:

keyofType:
'keyof' typeReference
;

A compile-time error occurs if typeReference is neither a class nor an interface type. The semantics of type keyof is represented by the example below:

class A {
    field: number
    method() {}
}
type KeysOfA = keyof A // "field" | "method"
let a_keys: KeysOfA = "field" // OK
a_keys = "any string different from field or method"
// Compile-time error: invalid value for the type KeysOfA

If a class or an interface is empty, then its type keyof is equivalent to type never:

class A {} // Empty class
type KeysOfA = keyof A // never

### 3.21 Nullish Types

ArkTS has nullish types that are in fact a specific form of union types (see Union Types).

T | null or T | undefined or T | undefined | null can be used as the type to specify a nullish version of type T.

All predefined types except Type Any, and all user-defined types are non-nullish types. Non-nullish types cannot have a null or undefined value at runtime.

A variable declared to have type T | null can hold the values of type T and its derived types, or the value null. Such a type is called a nullable type.

A variable declared to have type T | undefined can hold the values of type T and its derived types, or the value undefined.

A variable declared to have type T | null | undefined can hold values of type T and its derived types, and the values undefined or null.

Nullish type is a reference type (see Union Types). A reference that is null or undefined is called a nullish value.

An operation that is safe with no regard to the presence or absence of nullish values (e.g., re-assigning one nullable value to another) can be used 'as is' for nullish types.

The following nullish-safe options exist for dealing with nullish type T:
