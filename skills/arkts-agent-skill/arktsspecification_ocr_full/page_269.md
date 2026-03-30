3. If return type  $ T_{m+1} $ is this, then  $ U_{n+1} $ is this, or any of superinterfaces or superclass of the current type. Otherwise, return type  $ T_{m+1} $ is a subtype of  $ U_{n+1} $ (covariance).

4. Number of type parameters of either method is the same, i.e., k = 1.

5. Constraints of  $ W_{1}, \ldots, W_{1} $ are to be contravariant (see Invariance, Covariance and Contravariance) to the appropriate constraints of  $ V_{1}, \ldots, V_{k} $.

The following rule applies to generics:

• Derived class must have type parameter constraints to be subtype (see Subtyping) of the respective type parameter constraint in the base type;

• Otherwise, a compile-time error occurs.

class Base {}
class Derived extends Base {}
class A1 <CovariantTypeParameter extends Base> {}
class B1 <CovariantTypeParameter extends Derived> extends A1<CovariantTypeParameter> {}
// OK, derived class may have type compatible constraint of type parameters

class A2 <ContravariantTypeParameter extends Derived> {}
class B2 <ContravariantTypeParameter extends Base> extends A2<ContravariantTypeParameter>
→ {}
// Compile-time error, derived class cannot have non-compatible constraints of type_parameters

The semantics is represented in the examples below:

### 1. Class/Interface Types

interface Base {
    param(p: Derived): void
        ret(): Base
}

interface Derived extends Base {
    param(p: Base): void // Contravariant parameter
        ret(): Derived // Covariant return type
}

### 2. Function Types

interface Base {
    param(p: (q: Base)=>Derived): void
        ret(): (q: Derived)=> Base
}

interface Derived extends Base {
    param(p: (q: Derived)=>Base): void // Covariant parameter type, contravariant_
    →return type
    ret(): (q: Base)=>Derived // Contravariant parameter type, covariant_
    →return type
}

### 3. Union Types
