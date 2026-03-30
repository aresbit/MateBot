interface BaseSuperType {}
interface Base extends BaseSuperType {
    // Overriding for parameters
    param<T extends Derived, U extends Base>(p: T | U): void

    // Overriding for return type
    ret<T extends Derived, U extends Base>(): T | U
}

interface Derived extends Base {
    // Overriding kinds for parameters, Derived <: Base
    param<T extends Base, U extends Object>(
        p: Base | BaseSuperType // contravariant parameter type: Derived | Base <: Base_
    ) : void
    // Overriding kinds for return type
    ret<T extends Base, U extends BaseSuperType>(): T | U
}

### 4. Type Parameter Constraint

interface Base {
    param<T extends Derived>(p: T): void
        ret<T extends Derived>(); T
}

interface Derived extends Base {
    param<T extends Base>(p: T): void
    →parameters
        ret<T extends Base>(); T
    →return type
}

Override compatibility with Object is represented in the example below:

interface Base {
    kinds_of_parameters<T extends Derived, U extends Base> ( // It represents all_
        →possible kinds of parameter type
        p01: Derived,
        p02: (q: Base)=>Derived,
        p03: number,
        p04: T | U,
        p05: E1,
        p06: Base[],
        p07: [Base, Base]
    ): void
    kinds_of_return_type(): Object // It can be overridden by all subtypes of Object
}
interface Derived extends Base {
    kinds_of_parameters( // Object is a supertype for all class types
        p1: Object,
        p2: Object,
        p3: Object,
    )
}
