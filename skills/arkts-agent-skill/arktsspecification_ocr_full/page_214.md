If the default setter is not overridden in a class that implements the interface, InvalidStoreAccessError is thrown at attempt to set value of an optional property. See also Implementing Optional Interface Properties.

### 10.5 Interface Method Declarations

An ordinary interface method declaration specifies the method name and signature, and is called abstract. Its implicit accessibility is public.

An interface method can have a body (see Default Interface Method Declarations) as an experimental feature.

The syntax of interface method declaration is presented below:

interfaceMethodDeclaration:

    identifier signature

| interfaceDefaultMethodDeclaration

;

### 10.6 Interface Inheritance

Interface I inherits all properties and methods from its direct superinterfaces. Semantic checks are described in Overriding and Overloading in Interfaces.

Note. The semantic rules of methods apply to properties because any interface property implicitly defines a getter, a setter, or both.

Private methods defined in superinterfaces are not accessible (see Accessible) in the interface body.

A compile-time error occurs if interface I declares a private method m with a signature compatible with the instance method  $ m' $ (see Override-Compatible Signatures) that has any access modifier in the superinterface of I.
