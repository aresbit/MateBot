## GENERICS

Class, interface, type alias, method, and function are program entities that can be parameterized in ArkTS by one or several types. An entity so parameterized introduces a generic declaration (called a generic for brevity).

Types used as generic parameters in a generic are called type parameters (see Type Parameters).

A generic must be instantiated in order to be used. Generic instantiation is the action that transforms a generic into a real program entity (non-generic class, interface, union, array, method, or function), or into another generic instantiation. Instantiation (see Generic Instantiations) can be performed either explicitly or implicitly.

ArkTS has special types that look similar to generics syntax-wise, and allow creating new types during compilation (see Utility Types).

### 5.1 Type Parameters

Type parameter is declared in the type parameter section. It can be used as an ordinary type inside a generic.

Syntax-wise, a type parameter is an unqualified identifier with a proper scope (see Scopes for the scope of type parameters). Each type parameter can have a constraint (see Type Parameter Constraint). A type parameter can have a default type (see Type Parameter Default), and can specify its in- or out- variance (see Type Parameter Variance).

The syntax of type parameter is presented below:

typeParameters:
    '<' typeParameterList '>'
;

typeParameterList:
    typeParameter (',' typeParameter)*
;

typeParameter:
    ('in' | 'out')? identifier constraint? typeParameterDefault?
;

constraint:
    'extends' type
;

(continues on next page)
