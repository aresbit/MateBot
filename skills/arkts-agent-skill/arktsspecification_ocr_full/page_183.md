// File1
interface I { } // Not exported

// File2
import {I} from "File1"
class C implements I {}

// Compile-time error I is not accessible

If some interface is repeated as a direct superinterface in a single implements clause (even if that interface is named differently), then all repetitions are ignored.

For the class declaration C <F₁, ..., Fₙ>(n ≥ 0, C ≠ Object):

- Direct superinterfaces of class type C <F₁, ..., Fₙ> are the types specified in the implements clause of the declaration of C (if there is an implements clause).

For the generic class declaration C <F₁, ..., Fₙ> (n > 0):

• Direct superinterfaces of the parameterized class type C < T₁, ..., Tₙ> are all types I < U₁θ, ..., Uₖθ> if:

-  $ T_i $ ( $ 1 \leq i \leq n $) is a type;

– I <U₁, …, Uₖ> is the direct superinterface of C <F₁, …, Fₙ>; and

− θ is the substitution  $ [F_1 := T_1, \ldots, F_n := T_n] $.

Interface type I is a superinterface of class type C if I is one of the following:

• Direct superinterface of C;

- Superinterface of J which is in turn a direct superinterface of C (see Superinterfaces and Subinterfaces that defines superinterface of an interface); or

• Superinterface of the direct superclass of C.

A class implements all its superinterfaces.

A compile-time error occurs if a class implements two interface types that represent different instantiations of the same generic interface (see Generics).

If a class is not declared abstract, then:

• Any abstract method of each direct superinterface is implemented (see Inheritance) by a declaration in that class.

• The declaration of an existing method is inherited from a direct superclass, or a direct superinterface.

A compile-time error occurs if a class field has the same name as a method from one of superinterfaces implemented by the class, except when one is static and the other is not.

#### 9.3.1 Implementing Interface Methods

If superinterfaces have more than one default implementation (see Default Interface Method Declarations) for some method m, then:

• The class that implements these interfaces has method that overrides m (see Override-Compatible Signatures); or

• There is a single interface method with default implementation that overrides all other methods; or
