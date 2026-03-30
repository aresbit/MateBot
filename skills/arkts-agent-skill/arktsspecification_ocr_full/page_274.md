• Type Parameter Constraint for Type Parameters.

• Instantiation of the same generic type (see Explicit Generic Instantiations) for generic types (see Generics), with its type arguments selected in accordance with Type Parameter Variance as outlined below:

– Covariant type parameters are instantiated with the constraint type;

– Contravariant type parameters are instantiated with the type never;

– Invariant type parameters are instantiated with no type argument, i.e., Array<T> is instantiated as Array<>.

• Union type constructed from the effective types of types T1 | T2 ... Tn within the original union type for Union Types in the form T1 | T2 ... Tn.

• Same for Array Types in the form T[] as for generic type Array<T>.

• Instantiation of FixedArray for FixedArray<T> instantiations, with the effective type of type argument T preserved.

• Instantiation of an internal generic function type with respect to the number of parameter types n for Function Types in the form (P1, P2 ..., Pn) => R. Parameter types P1, P2 ... Pn are instantiated with Any, and the return type R is instantiated with type never.

- Instantiation of an internal generic tuple type with respect to the number of element types n for Tuple Types in the form [T1, T2 ..., Tn].

• String for String Literal Types.

• Enumeration base type of the same const enum type for const enum types (see Enumerations).

• Otherwise, the original type is preserved.

### 15.11 Static Initialization

Static initialization is a routine performed once for each class (see Classes), namespace (see Namespace Declarations), or module (see Modules and Namespaces).

Static initialization execution involves the execution of the following:

• Initializers of variables or static fields;

• Top-level statements;

• Code inside a static block.

Static initialization is performed before the first execution of one of the following operations:

• Invocation of a static method or function of an entity scope;

• Access to a static field or variable of an entity scope;

• Instantiation of an entity that is an interface or class;

• Static initialization of a direct subclass of an entity that is a class.

Note. None of the operations above invokes a static initialization recursively if the static initialization of the same entity is not complete.

Note. For namespaces, the code in a static block is executed only when namespace members are used in the program (an example is provided in Namespace Declarations).
