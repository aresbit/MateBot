#### 17.9.5 Overload Alias Name Same As Function Name

A name of a top-level overload declaration can be the same as the name of an overloaded function. This situation is represented in the following example:

function foo(n: number): number {/*body1*/}
function fooString(s: number): string {/*body2*/}

overload foo {foo, fooString}

foo(1)    // overload alias is used to call 'foo'
foo("aa") // overload alias is used to call 'fooString'

Using an overload alias causes no ambiguity for it is considered at the call site only, i.e., an overload alias is not considered in the following situations:

• List of the overloaded entities (see Function Overload Declarations);

• Function Reference.

function foo(n: number): number {/*body1*/}
function fooString(s: number): string {/*body2*/}
overload foo {foo, fooString}

let func1 = foo // function 'foo' is used, not overload alias

If the name of an overload alias is the same as the name of a function that is not listed as an overloaded function, then a compile-time error occurs as follows:

function foo(n: number) {/*body1*/}
function fooString(s: number) {/*body2*/}
function fooBoolean(b: boolean) {/*body3*/}

overload foo { // compile-time error
    fooBoolean, fooString
}

#### 17.9.6 Overload Alias Name Same As Method Name

A name of a class or interface overload declaration can be the same as the name of an overloaded method. As one example, a method defined in a superclass can be used as one of overloaded methods in a same-name subclass overload declaration. This important case is represented by the following example:

class C {
    foo(n: number): number {/*body*/}
}
class D implements C {
    fooString(s: number): string {/*body*/}
}

(continues on next page)
