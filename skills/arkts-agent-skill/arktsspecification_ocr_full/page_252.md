#### 15.1.8 Semantic Essentials Summary

Major semantic terms are listed below:

• Type of Expression;

• Assignment-like Contexts:

• Type Inference from Initializer;

• Numeric Operator Contexts;

• String Operator Contexts;

• Subtyping;

• Assignability;

• Overriding;

• Overloading;

• Type Inference.

### 15.2 Subtyping

Subtype relationship between types S and T, where S is a subtype of T (recorded as S<:T), means that any object of type S can be safely used in any context to replace an object of type T. The opposite relation (recorded as T:>S) is called supertype relationship. Each type is its own subtype and supertype (S<:S and S:>S).

By the definition of S<:T, type T belongs to the set of supertypes of type S. The set of supertypes includes all direct supertypes (discussed in subsections), and all their respective supertypes. More formally speaking, the set is obtained by reflexive and transitive closure over the direct supertype relation.

The terms subclass, subinterface, superclass, and superinterface are used in the following sections as synonyms for subtype and supertype when considering non-generic classes, generic classes, or interface types.

If a relationship of two types is not described in one of the following sections, then the types are not related to each other. Specifically, two Resizable Array Types and two Tuple Types are not related to each other, except where they are identical (see Type Identity).

class Base {}
class Derived extends Base {}

function not_a_subtype (
    ab: Array<Base>, ad: Array<Derived>,
    tb: [Base, Base], td: [Derived, Derived],
) {
    ab = ad // Compile-time error
    tb = td // Compile-time error
}
