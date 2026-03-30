interfaceTypeList:
    typeReference (',' typeReference)*
;

The identifier in an interface declaration specifies the interface name.

An interface declaration with typeParameters introduces a new generic interface (see Generics).

The scope of an interface declaration is defined in Scopes.

### 10.2 Superinterfaces and Subinterfaces

An interface declared with an extends clause extends all other named interfaces, and thus inherits all their members. Such other named interfaces are direct superinterfaces of a declared interface. A class that implements the declared interface also implements all interfaces that the interface extends.

A compile-time error occurs if:

• typeReference`in the extends clause refers directly to, or is an alias of non-interface type.

• Interface type named by typeReference is not Accessible.

Type arguments (see Type Arguments) of typeReference denote a parameterized type that is not well-formed (see Generic Instantiations).

• The extends graph has a cycle.

If an interface declaration (possibly generic) I <F₁, ..., Fₙ> (n ≥ 0) contains an extends clause, then the direct superinterfaces of the interface type I <F₁, ..., Fₙ> are the types given in the extends clause of the declaration of I.

All direct superinterfaces of the parameterized interface type I <T1, ..., Tn> are types ] <U1θ, ..., Ukθ>, if:

•  $ T_i $ ( $ 1 \leq i \leq n $) is the type of a generic interface declaration  $ I < F_1, \ldots, F_n > (n > 0) $;

• J <U₁, ..., Uₖ> is a direct superinterface of I <F₁, ..., Fₙ>; and

•  $ \theta $ is a substitution  $ [F_1 := T_1, \ldots, F_n := T_n] $.

The transitive closure of the direct superinterface relationship results in the superinterface relationship.

Interface I is a subinterface of K wherever K is a superinterface of I. Interface K is a superinterface of I if:

• I is a direct subinterface of K; or

• K is a superinterface of some interface J of which I is, in turn, a subinterface.

There is no single interface to which all interfaces are extensions (unlike class Object to which every class is an extension).

A compile-time error occurs if an interface depends on itself.

If superinterfaces have default implementations (see Default Interface Method Declarations) for some method m, then the following occurs:

• Method m with an override-compatible signature (see Override-Compatible Signatures) declared within the current interface overrides all other m methods inherited from superinterfaces; or
