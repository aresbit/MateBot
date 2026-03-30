#### 15.8.2 Overriding and Overloading in Interfaces

Context Semantic Check
A method is defined in a subinterface with the same name as the method in the superinterface.
If signatures are override-compatible (see Override-Compatible Signatures), then overriding is used. Otherwise, a compile-time error occurs.
A method is defined in a subinterface with the same name as the private method in the superinterface.
A compile-time error occurs.

interface Base {
    method_1()
    method_2(p: number)
    private foo() {} // private method with implementation body
}

interface Derived extends Base {
    method_1() // overriding
    method_2(p: string) // compile-time error: non-compatible signature
    foo(p: number): void // compile-time error: the same name as private method
}

Two or more methods with the same name are defined in TBD is used. the same interface.

interface anInterface {
    instance_method() // 1st signature
    instance_method(p: number) // 2nd signature
}

#### 15.8.3 Override-Compatible Signatures

If there are two classes Base and Derived, and class Derived overrides the method foo() of Base, then foo() in Base has signature  $ S_1 < V_1 $,  $ \ldots $  $ V_k > (U_1, \ldots, U_n) : U_{n+1} $, and foo() in Derived has signature  $ S_2 < W_1 $,  $ \ldots $  $ W_l > (T_1, \ldots, T_m) : T_{m+1} $ as in the example below:

class Base {
    foo <V1, ... Vk> (p1: U1, ... pn: Un): Un+1
}
class Derived extends Base {
    override foo <W1, ... Wl> (p1: T1, ... pm: Tm): Tm+1
}

The signature  $ S_{2} $ is override-compatible with  $ S_{1} $ only if all of the following conditions are met:

1. Number of parameters of both methods is the same, i.e., n = m.

2. Each parameter type  $ T_i $ is a supertype of  $ U_i $ for  $ i $ in 1..n (contravariance).
