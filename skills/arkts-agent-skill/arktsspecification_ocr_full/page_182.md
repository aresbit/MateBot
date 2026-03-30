class Base {
    /* All methods are accessible in the class where they were declared */
    public publicMethod () {
        this.protectedMethod()
        this.privateMethod()
    }
    protected protectedMethod () {
        this.publicMethod()
        this.privateMethod()
    }
    private privateMethod () {
        this.publicMethod();
        this.protectedMethod()
    }
}
class Derived extends Base {
    foo () {
        this.publicMethod() // OK
        this.protectedMethod() // OK
        this.privateMethod() // compile-time error:
            // the private method is inaccessible
    }
}

The transitive closure of a direct subclass relationship is the subclass relationship. Class A can be a subclass of class C if:

• Class A is the direct subclass of C; or

• Class A is a subclass of some class B, which is in turn a subclass of C (i.e., the definition applies recursively).

Class C is a superclass of class A if A is its subclass.

### 9.3 Class Implementation Clause

A class can implement one or more interfaces. Interfaces to be implemented by a class are listed in the implements clause. Interfaces listed in this clause are direct superinterfaces of the class.

The syntax of class implementation clause is presented below:

implementsClause:
    'implements' interfaceTypeList
;
interfaceTypeList:
    typeReference (',' typeReference)*
;

A compile-time error occurs if typeReference fails to name an accessible interface type (see Accessible).
