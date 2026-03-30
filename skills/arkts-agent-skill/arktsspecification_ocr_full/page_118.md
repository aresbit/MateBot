Type of a field access expression is the type of a member field.

#### 7.9.1 Accessing Current Object Fields

The result of a field access expression is computed at runtime as described below.

a. Static field access (objectReference is evaluated in the form typeReference)

The evaluation of typeReference is performed. The result of a field access expression of a static field in a class is as follows:

• variable if the field is not readonly. The resultant value can be changed later.

• value if the field is readonly, except where field access occurs in a initializer block (see Static Initialization).

b. Instance field access (objectReference is evaluated in the form primaryExpression)

The evaluation of primaryExpression is performed. The result of field access expression of an instance field in a class or interface is as follows:

• variable if the field is not readonly. The resultant value can be changed later.

• value if the field is readonly, except where field access occurs in a constructor (see Constructor Declaration).

Only the primaryExpression type (not class type of an actual object referred at runtime) is used to determine the field to be accessed.

#### 7.9.2 Accessing SuperClass Properties

The form super.identifier is valid when accessing the superclass property via accessor (see Class Accessor Declarations). A compile-time error occurs if identifier in 'super.identifier' denotes a field.

class Base {
    get property(): number { return 1 }
    set property(p: number) {}
    field = 1234
}
class Derived extends Base {
    get property(): number { return super.property } // OK
    set property(p: number) { super.property = 42 } // OK
    foo () {
        super.field = 42 // compile-time error
        console.log (super.field) // compile-time error
    }
}
