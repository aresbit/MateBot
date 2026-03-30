get num(): number { return 42 } // compile-time error, wrong overriding
set num(x: number) {} // compile-time error, wrong overriding
}

### 9.7 Method Declarations

Methods declare executable code that can be called.

The syntax of class method declarations is presented below:

classMethodDeclaration:
    methodModifier* identifier typeParameters? signature block?
;

methodModifier:
    'abstract'
| 'static'
| 'final'
| 'override'
| 'native'
| 'async'
;

The identifier in a class method declaration defines the method name that can be used to refer to a method (see Method Call Expression).

Methods with the final modifier is an experimental feature discussed in detail in Final Methods.

A compile-time error occurs if:

• Method modifier appears more than once in a method declaration;

• Body of a class declaration declares a method but the name of that method is already used for a field in the same declaration.

A non-static method declared in a class can do the following:

• Implement a method inherited from a superinterface or superinterfaces (see Implementing Interface Methods);

• Override a method inherited from a superclass (see Overriding in Classes);

• Act as method declaration of a new method.

A static method declared in a class can do the following:

• Shadow a static method inherited from a superclass (see Static Methods);

• Act as method declaration of a new static method.
