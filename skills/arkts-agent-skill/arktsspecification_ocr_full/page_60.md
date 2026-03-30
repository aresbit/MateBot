• Using safe operations:

– Safe method call (see Method Call Expression for details);

– Safe field access expression (see Field Access Expression for details);

– Safe indexing expression (see Indexing Expressions for details);

– Safe function call (see Function Call Expression for details);

• Converting from T | null or T | undefined to T:

-  $  \text{on } T \mid \text{null or } T \mid \text{undefined to } T  $:
- Cast Expression;
- Ensure-not-nullish expression (see Ensure-Not-Nullish Expression for details);
Supplying a value to be used if a nullish value is present:
-coalescing expression (see Nullish-Coalescing Expression for details).

Note. Nullish types are not compatible with type Object:

function nullish (
    o: Object, nullish1: null, nullish2: undefined, nullish3: null | undefined
    nullish4: AnyClassOrInterfaceType | null | undefined
) {
    o = nullish1 /* compile-time error - type 'null' is not compatible with Object */
    o = nullish2 /* compile-time error - type 'undefined' is not compatible with Object */
    o = nullish3 /* compile-time error - type 'null|undefined' is not compatible with Object */
    o = nullish4 /* compile-time error - type 'AnyClassOrInterfaceType|null|undefined' is not compatible with Object */
}

### 3.22 Default Values for Types

Note. This ArkTS feature is experimental.

So-called default values are used by the following types for variables that require no explicit initialization (see Variable Declarations):

• Value Types:

• Type undefined and all its supertypes

All other types, including reference types, enumeration types, and type parameters have no default values.

Default values of value types are as follows:
