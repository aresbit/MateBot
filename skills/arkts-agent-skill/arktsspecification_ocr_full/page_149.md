1 5 == 5 // true
2 5 != 5 // false
3
4 5 === 5 // true
5
6 5 == new Number(5) // true
7 5 === new Number(5) // true
8
9 5 == 5.0 // true

#### 7.25.2 Function Type Equality Operators

If both operands refer to the same function object, then the comparison returns true. When comparing method references, not only the same method must be used, but also its bounded instances must be equal.

function foo() {}
function bar() {}
function goo(p: number) {}

foo == foo // true, same function object
foo == bar // false, different function objects
foo == goo // false, different function objects

class A {
    method() {}
    static method() {}
    foo () {}
}
const a = new A
a.method == a.method // true, same function object
A.method == A.method // true, same function object

const aa = new A
a.method == aa.method /* false, different function objects
    as 'a' and 'aa' are different bounded objects */
a.method == a.foo // false, different function objects

#### 7.25.3 Extended Equality with null or undefined

ArkTS provides extended semantics for equalities with null and undefined to ensure better alignment with TypeScript.

If one operand in an equality expression is null, and other is undefined, then the operator '!=' returns true, and the operator '!==' returns false:
