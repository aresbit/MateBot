## • Object orientation

The ArkTS language supports the object-oriented programming (OOP) approach based on classes and interfaces. The major notions of this approach are as follows:

– Classes with single inheritance.

– Interfaces as abstractions to be implemented by classes, and

– Methods (class instance or interface methods) with overriding and dynamic dispatch mechanisms.

Object orientation is common in many if not all modern programming languages. It enables powerful, flexible, safe, clear, and adequate software design.

## • Modularity

The ArkTS language supports the component programming approach. It presumes that software is designed and implemented as a composition of modules.

A module in ArkTS is a standalone, independently compiled unit that combines various programming resources (types, classes, functions, and so on). A module can communicate with other modules by exporting all or some of its resources to, or importing from other modules.

## • Genericity

Some program entities in ArkTS can be type-parameterized. It means that an entity can represent a very high-level (abstract) concept. Providing more concrete type information constitutes the instantiation of an entity for a particular use case.

A classical illustration is the notion of a list that represents the ‘idea’ of an abstract data structure. An abstract notion can be turned into a concrete list by providing additional information (i.e., type of list elements).

A similar feature (generics or templates) supported by many programming languages enables making programs and program structures more generic and reusable, and serves as a basis of the generic programming paradigm.

## • Multitargeting

ArkTS provides an efficient application development solution for a wide range of devices. The developer-friendly ArkTS ecosystem is a cross-platform development providing a uniform programming environment for many popular platforms. It can generate optimized applications capable of operating under the limitations of lightweight devices, or realizing the full potential of any specific-target hardware.

### 1.2 Lexical and Syntactic Notation

This section introduces the notation known as context-free grammar. The notation is used throughout this specification to define the lexical and syntactic structure of a program.

The ArkTS lexical notation defines a set of rules, or productions that specify the structure of the elementary language parts called tokens. All tokens are defined in Lexical Elements. The set of tokens (identifiers, keywords, numbers/numeric literals, operator signs, delimiters), special characters (white spaces and line separators), and comments comprises the language's alphabet.

The tokens defined by the lexical grammar are terminal symbols of syntactic notation. Syntactic notation defines a set of productions starting from the goal symbol moduleDeclaration (see Modules and Namespaces). It is a sentence that consists of a single distinguished nonterminal, and describes how sequences of tokens can form syntactically correct programs.
