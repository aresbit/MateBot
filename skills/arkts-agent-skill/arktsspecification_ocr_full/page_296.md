#### 17.9.1 Function Overload Declarations

Function overload declaration allows declaring an overload alias for a set of functions (see Function Declarations).

The syntax is presented below:

overloadFunctionDeclaration:
'overload' identifier '{' qualifiedName (',' qualifiedName)* ','? '}'
;

A compile-time error occurs, if a qualified name does not refer to an accessible function.

A compile-time error occurs, if an overload alias is exported but an overloaded function is not:

export function foo1(p: string) {}
function foo2(p: number) {}
export overload foo { foo1, foo2 } // compile-time error, 'foo2' is not exported
overload bar { foo1, foo2 } // ok, as 'bar' is not exported

All overloaded functions must be in the same module or namespace scope (see Scopes). Otherwise, a compile-time error occurs. The erroneous overload declarations are represented in the example below:

import {foo1} from "something"

function foo2() {}

overload foo {foo1, foo2} // compile-time error

namespace N {
    export function fooN() {}
    namespace M {
        export function fooM() {}
    }
    overload goo {M.fooM, fooN} // compile-time error
}

overload bar {foo2, N.fooN} // compile-time error

#### 17.9.2 Class Method Overload Declarations

Method overload declaration allows declaring an overload alias as a class member (see Class Members) for a set of static or instance methods (see Method Declarations). The syntax is presented below:

overloadMethodDeclaration:
  overloadMethodModifier*
  'overload' identifier '{' identifier (',' identifier)* ','? '}'
;

overloadMethodModifier: 'static' | 'async';

Using method overload declaration and calling an overload alias are represented in the example below:
