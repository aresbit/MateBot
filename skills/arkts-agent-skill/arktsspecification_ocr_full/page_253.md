#### 15.2.1 Subtyping for Non-Generic Classes and Interfaces

S for non-generic classes and interfaces is a direct subclass or subinterface of T (or of Object type) when one of the following conditions is true:

• Class S is a direct subtype of class T (S<:T) if T is mentioned in the extends clause of S (see Class Extension Clause):

// Illustrating S<:T
class T {}
class S extends T {}
function foo(t: T) {}

// Using T
foo(new T)

// Using S (S<:T)
foo(new S)

• Class S is a direct subtype of class Object (S<:Object) if S has no Class Extension Clause:

// Illustrating S<:Object
class S {}
function foo(o: Object) {}

// Using Object
foo(new Object)

// Using S (S<:Object)
foo(new S)

• Class S is a direct subtype of interface T (S<:T) if T is mentioned in the implements clause of S (see Class Implementation Clause):

// Illustrating S<:T
// S is class, T is interface
interface T {}
class S implements T {}
function foo(t: T) {}
let s: S = new S

// Using T
let t: T = s
foo(t)

// Using S (S<:T)
foo(s)

• Interface S is a direct subtype of interface T (S<:T) if T is mentioned in the extends clause of S (see Superinterfaces and Subinterfaces):

// Illustrating S<:T
// S is interface, T is interface
interface T {}
interface S extends T {}

(continues on next page)
