- The expression the value stores;

– A reference to the class instance for the names of instance entities; or

- Name of the class for static entities.

ArkTS supports using the same identifier as names of a static entity and of an instance entity. The two names are distinguishable by the context, which is either a name of a class for static entities or an expression that denotes an instance.

• A name declared inside an interface (interface level scope) is accessible (see Accessible) inside and outside that interface (default public).

• The scope of a type parameter name in a class or interface declaration is that entire declaration, excluding static member declarations.

• The scope of a type parameter name in a function declaration is that entire declaration (function type parameter scope).

• The scope of a name declared inside the body of a function or a method declaration is the body of that declaration from the point of declaration and up to the end of the body (method or function scope). This scope is also applied to function or method parameter names.

• The scope of a name declared inside a block is the body of the block from the point of the name declaration and up to the end of the block (block scope).

function foo() {
    let x = y // compile-time error - y is not accessible yet
    let y = 1
}

Scopes of two names can overlap (e.g., when statements are nested). If scopes of two names overlap, then:

• The innermost declaration takes precedence; and

• Access to the outer name is not possible.

Class, interface, and enum members can only be accessed by applying the dot operator ‘.’ to an instance. Accessing them otherwise is not possible.

### 4.4 Accessible

Entity is considered accessible if it belongs to the current scope (see Scopes) and means that its name can be used for different purposes as follows:

• Type name is used to declare variables, constants, parameters, class fields, or interface properties;

• Function or method name is used to call the function or method;

• Variable name is used to read or change the value of the variable;

• Name of a module introduced as a result of import with Bind All with Qualified Access (see Bind All with Qualified Access) is used to deal with exported entities.
