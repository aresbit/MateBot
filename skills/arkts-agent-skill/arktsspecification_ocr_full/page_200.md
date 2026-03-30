class C {
    foo(): this {
        return this
    }
}

The return type of an overridden method in a subclass must also be this:

class C {
    foo(): this {
        return this
    }
}

class D extends C {
    foo(): this {
        return this
    }
}

let x = new C().foo() // type of 'x' is 'C'
let y = new D().foo() // type of 'y' is 'D'

Otherwise, a compile-time error occurs.

### 9.8 Class Accessor Declarations

Class accessors are often used instead of fields to add additional control for operations of getting or setting a field value. An accessor can be either a getter or a setter.

The syntax of class accessor declarations is presented below:

class AccessorDeclaration:
    class AccessorModifier*
    ( 'get' identifier '(' ')' returnType? block?
    | 'set' identifier '(' parameter ')' block?
)
;
class AccessorModifier:
    'abstract'
| 'static'
| 'final'
| 'override'
| 'native'
;

Accessor modifiers are a subset of method modifiers. The allowed accessor modifiers have exactly the same meaning as the corresponding method modifiers (see Abstract Methods for the modifier abstract, Static Methods for the modifier
