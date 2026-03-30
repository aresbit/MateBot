# TYPES

This chapter introduces the notion of type that is one of the fundamental concepts of ArkTS and other programming languages. Type classification as accepted in ArkTS is discussed below along with all aspects of using types in programs written in the language.

The type of an entity is conventionally defined as the set of values the entity (variable) can take, and the set of operators applicable to the entity of a given type.

ArkTS is a statically typed language. It means that the type of every declared entity and every expression is known at compile time. The type of an entity is either set explicitly by a developer, or inferred implicitly (see Type Inference) by the compiler.

The types integral to ArkTS are called predefined types (see Predefined Types).

The types introduced, declared, and defined by a developer are called user-defined types. All user-defined types must have complete type declarations presented as source code in ArkTS.

ArkTS types are summarized in the table below:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Predefined Types</td><td style='text-align: center; word-wrap: break-word;'>User-Defined Types</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte, short, int, long, float, double, number, boolean, char, string, bigint, Any, Object, never, void, undefined, null, Array&lt;T&gt; or T[], FixedArray&lt;T&gt;</td><td style='text-align: center; word-wrap: break-word;'>class types, interface types, array types, fixed array types, tuple types, union types, literal types, function types, type parameters, enumeration types</td></tr></table>

Note. Type number is an alias to double.

Most predefined types have aliases to improve TypeScript compatibility as follows:
