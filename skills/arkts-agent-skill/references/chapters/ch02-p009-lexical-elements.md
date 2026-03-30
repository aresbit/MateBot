# Chapter 2: Lexical Elements

Page range: 9-22

## Page 9

15.1.1 Type of Standalone Expression ..... 237  
15.1.2 Specifics of Assignment-like Contexts ..... 238  
15.1.3 Specifics of Variable Initialization Context ..... 238  
15.1.4 Specifics of Numeric Operator Contexts ..... 239  
15.1.5 Specifics of String Operator Contexts ..... 239  
15.1.6 Other Contexts ..... 239  
15.1.7 Specifics of Type Parameters ..... 239  
15.1.8 Semantic Essentials Summary ..... 240  
15.2 Subtyping ..... 240  
15.2.1 Subtyping for Non-Generic Classes and Interfaces ..... 241  
15.2.2 Subtyping for Generic Classes and Interfaces ..... 242  
15.2.3 Subtyping for Literal Types ..... 245  
15.2.4 Subtyping for Union Types ..... 246  
15.2.5 Subtyping for Function Types ..... 246  
15.2.6 Subtyping for Fixed-Size Array Types ..... 247  
15.2.7 Subtyping for Intersection Types ..... 248  
15.2.8 Subtyping for Difference Types ..... 248  
15.3 Type Identity ..... 248  
15.4 Assignability ..... 249  
15.5 Invariance, Covariance and Contravariance ..... 249  
15.6 Compatibility of Call Arguments ..... 250  
15.7 Type Inference ..... 251  
15.7.1 Type Inference for Numeric Literals ..... 252  
15.7.2 Smart Types ..... 253  
15.8 Overriding ..... 254  
15.8.1 Overriding in Classes ..... 254  
15.8.2 Overriding and Overloading in Interfaces ..... 256  
15.8.3 Override-Compatible Signatures ..... 256  
15.9 Overloading ..... 259  
15.9.1 Overload Resolution ..... 260  
15.10 Type Erasure ..... 261  
15.11 Static Initialization ..... 262  
15.11.1 Static Initialization Safety ..... 263  
15.12 Dispatch ..... 263  
15.13 Compatibility Features ..... 263  
15.13.1 Extended Conditional Expressions ..... 264  
16 Concurrency ..... 267  
16.1 Introductory Note ..... 267  
16.2 Concurrency Subsystem Overview ..... 267  
16.2.1 Major Concurrency Features ..... 267  
16.3 Asynchronous API ..... 268  
16.3.1 Async Functions ..... 268  
16.3.2 Async Lambdas ..... 268  
16.3.3 Async Methods ..... 268  
16.3.4 await ..... 268  
16.3.5 Promise ..... 269  
16.3.6 Unhandled Rejected Promises ..... 270  
16.4 Coroutines (Experimental) ..... 270  
17 Experimental Features ..... 271  
17.1 Type char ..... 271  
17.1.1 Character Literals ..... 272  
17.1.2 Character Equality Operators ..... 272

## Page 10

17.2 Fixed-Size Array Types ..... 273  
17.2.1 Fixed-Size Array Creation ..... 273  
17.3 Resizable Array Creation Expressions ..... 274  
17.3.1 Runtime Evaluation of Array Creation Expressions ..... 276  
17.4 Enumerations Experimental ..... 276  
17.4.1 Enumeration Methods ..... 276  
17.5 Indexable Types ..... 277  
17.6 Iterable Types ..... 279  
17.7 Callable Types ..... 280  
17.7.1 Callable Types with $_invoke Method ..... 280  
17.7.2 Callable Types with $_instantiate Method ..... 281  
17.8 Statements ..... 282  
17.8.1 For-of Explicit Type Annotation ..... 282  
17.9 Overload Declarations ..... 282  
17.9.1 Function Overload Declarations ..... 284  
17.9.2 Class Method Overload Declarations ..... 284  
17.9.3 Interface Method Overload Declarations ..... 287  
17.9.4 Constructor Overload Declarations ..... 289  
17.9.5 Overload Alias Name Same As Function Name ..... 290  
17.9.6 Overload Alias Name Same As Method Name ..... 290  
17.10 Native Functions and Methods ..... 292  
17.10.1 Native Functions ..... 292  
17.10.2 Native Methods ..... 293  
17.10.3 Native Constructors ..... 293  
17.11 Classes Experimental ..... 293  
17.11.1 Final Classes ..... 293  
17.11.2 Final Methods ..... 293  
17.11.3 Constructor Names ..... 294  
17.12 Default Interface Method Declarations ..... 294  
17.13 Adding Functionality to Existing Types ..... 295  
17.13.1 Functions with Receiver ..... 295  
17.13.2 Receiver Type ..... 298  
17.13.3 Accessors with Receiver ..... 298  
17.13.4 Function Types with Receiver ..... 299  
17.13.5 Lambda Expressions with Receiver ..... 300  
17.13.6 Implicit this in Lambda with Receiver Body ..... 302  
17.14 Trailing Lambdas ..... 303  
  
8 Annotations ..... 305  
18.1 Declaring Annotations ..... 305  
18.1.1 Types of Annotation Fields ..... 306  
18.2 Using Annotations ..... 307  
18.2.1 Using Single Field Annotations ..... 308  
18.3 Exporting and Importing Annotations ..... 309  
18.4 Ambient Annotations ..... 309  
18.5 Standard Annotations ..... 310  
18.5.1 Retention Annotation ..... 311  
18.6 Runtime Access to Annotations ..... 311  
  
9 Standard Library ..... 313  
  
10 Implementation Details ..... 315  
20.1 Import Path Lookup ..... 315  
20.2 Modules in Host System ..... 315

## Page 11

20.3 Getting Type Via Reflection ..... 315  
20.4 Ensuring Module Initialization ..... 316  
20.5 Generic and Function Types Peculiarities ..... 316  
20.6 Keyword struct and ArkUI ..... 316  
20.7 OutOfMemoryError for Primitive Type Operations ..... 317  
20.8 Make a Bridge Method for Overriding Method ..... 317  
  
21 Grammar Summary ..... 319  
  
22 Contributors ..... 321  
  
Index ..... 323

## Page 12

## Page 13

## INTRODUCTION

This document presents complete information on the new common-purpose, multiparadigm programming language called ArkTS.

### 1.1 Overall Description

The ArkTS language combines and supports features that have already proven helpful and powerful in many well-known programming languages.

ArkTS supports imperative, object-oriented, functional, and generic programming paradigms, and combines them safely and consistently.

At the same time, ArkTS does not support features that allow software developers to write dangerous, unsafe, or inefficient code. In particular, the language uses the strong static typing principle. Object types are determined by their declarations, and no dynamic type change is allowed. The semantic correctness is checked at compile time.

ArkTS is designed as a part of the modern language manifold. To provide an efficient and safely executable code, the language takes flexibility and power from TypeScript and its predecessor JavaScript, and the static typing principle from Java and Kotlin. The overall design keeps the ArkTS syntax style similar to that of those languages, and some of its important constructs are almost identical to theirs on purpose.

In other words, there is a significant common subset of features of ArkTS on the one hand, and of TypeScript, JavaScript, Java, and Kotlin on the other. Consequently, the ArkTS style and constructs are no puzzle for the TypeScript and Java users who can intuitively sense the meaning of most constructs of the new language even if not understand them completely.

This stylistic and semantic similarity permits smoothly migrating the applications originally written in TypeScript, Java, or Kotlin to ArkTS.

Like its predecessors, ArkTS is a relatively high-level language. It means that the language provides no access to low-level machine representations. As a high-level language, ArkTS supports automatic storage management, i.e., all dynamically created objects are deallocated automatically soon after they are no longer available, and deallocating them explicitly is not required.

ArkTS is not merely a language, but rather a comprehensive software development ecosystem that facilitates the creation of software solutions in various application domains.

The ArkTS ecosystem includes the language along with its compiler, accompanying documents, guidelines, tutorials, the standard library (see Standard Library), and a set of additional tools that perform transition from other languages (currently, TypeScript and Java) to ArkTS automatically or semi-automatically.

The ArkTS language as a whole is characterized by the following:

## Page 14

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

## Page 15

Lexical and syntactic grammars are defined as a range of productions, and each production is comprised of the following:

• Abstract symbol (nonterminal) as its left-hand side,

• Sequence of one or more nonterminal and terminal symbols as its right-hand side,

• Character ‘:’ as a separator between the left- and right-hand sides, and

• Character ‘;’ as the end marker.

A grammar starts from the goal symbol and specifies the language, i.e., the set of possible sequences of terminal symbols that can result from repeatedly replacing any nonterminal in the left-hand-side sequence for a right-hand side of the production.

Grammar can use the following additional symbols (sometimes called metasymbols) in the right-hand side of a grammar production along with terminal and nonterminal symbols:

• Vertical line ‘|’ to specify alternatives.

• Question mark ‘?’ to specify an optional occurrence (zero- or one-time) of the preceding terminal or nonterminal.

• Asterisk ‘*’ to mark a terminal or nonterminal that can occur zero or more times.

• Parentheses ‘(’ and ‘)’ to enclose any sequence of terminals and/or nonterminals marked with the metasymbols ‘?’ or ‘*’.

The metasymbols specify the structuring rules for terminal and nonterminal sequences. However, they are not part of terminal symbol sequences that comprise the resultant program text.

The example below represents a production that specifies a list of expressions:

expressionList:
    expression (',' expression)* ','?
;

This production introduces the following structure defined by the nonterminal expressionList. The expression list must consist of a sequence of expressions separated by the terminal symbol ‘,’. The sequence must have at least one expression. The list is optionally terminated by the terminal symbol ‘,’.

All grammar rules are presented in the Grammar section (see Grammar Summary) of this Specification.

### 1.3 Terms and Definitions

This section contains the alphabetical list of important terms found in the Specification, and their ArkTS-specific definitions. Such definitions are not generic and can differ significantly from the definitions of the same terms as used in other languages, application areas, or industries.

abstract declaration

– an ordinary interface method declaration that specifies the method’s name and signature.

array length

– the number of elements in a resizable array.

array type

– a type that consists of more than one element.

## Page 16

## casting conversion

– a conversion of an operand of a cast expression to an explicitly specified type.

## class level scope

– a name that is declared inside a class, and is accessible inside the class and sometimes outside that class by means of an access modifier, or via a derived class).

## comment

– a piece of text, insignificant for the syntactic grammar, that is added to a stream in order to document and compliment source code.

## compile-time error

– a text message displayed by the compiler if an error is identified in a program code that prevents the code to be generated.

## compile-time warning

– a text message displayed by the compiler if a program code is found to have some logical inconsistencies, and it is recommended that the programmer reconsider the design and actual coding.

## constant

– see constant declaration.

## constant declaration

– declaration that introduces a new variable to which an immutable initial value can be assigned only once at the time of instantiation.

## context-free grammar

– grammar in which the left-hand side of each production rule consists of only a single nonterminal symbol.

## expression

– a formula for calculating values. An expression has the syntactic form that is a composition of operators and parentheses, where parentheses are used to change the order of calculation. The default order of calculation is determined by operator preferences.

### fit into (v.)

– belong, or be implicitly convertible to an entity (see Widening Numeric Conversions).

## fixed-size array type

– a built-in type that consists of more than one element, and has its length set only once to achieve a better performance.

## function declaration

– a declaration that specifies names, signatures, and bodies when introducing a named function.

## function scope

– same as method scope.

## function type parameter scope

– a scope of a type parameter name in a function declaration. It is identical to that entire declaration.

## function types conversion

– a conversion of one function type to another.

## generic

– see generic type.

## generic type

– a named type (class or interface) that has type parameters.

## goal symbol

– a sentence that consists of a single distinguished nonterminal (moduleDeclaration). The goal symbol describes how sequences of tokens can form syntactically correct programs.

## Page 17

## grammar

– set of rules that describe what possible sequences of terminal and nonterminal symbols a programming language interprets as correct.

Grammar is a range of productions. Each production comprises an abstract symbol (nonterminal) as its left-hand side, and a sequence of nonterminal and terminal symbols as its right-hand side. Each production contains the characters ‘:’ as a separator between the left- and right-hand sides, and ‘;’ as the end marker.

## interface level scope

– a name declared inside an interface is considered to have interface level scope, and is accessible inside and outside the interface.

## keyword

– one of reserved words that have their meanings permanently predefined in the language.

## linearization

– de-nesting of all nested types in a union type to present them in the form of a flat line that includes no more union types.

## literal

– a representation of a value type.

### match (v.)

– correspond to an entity.

## metasymbol

– additional symbols ‘|’, ‘?’, ‘*’, ‘(’, and ‘)’ that can be used along with terminal and nonterminal symbols in the right-hand side of a grammar production.

## method

– an ordered 3-tuple consisting of type parameters, argument types, and return types.

## method scope

– a scope of a name declared immediately inside the body of a method (function) declaration. Method scope is identical to the body of that method (function) declaration from the place of declaration and up to the end of the body.

## module level scope

– a name in the module level scope that is applicable to modules only, and is accessible throughout the entire module and in other modules if exported.

## narrowing conversion

– a conversion that can cause a loss information about the overall magnitude of a numeric value, and potentially a loss of precision and range.

## non-generic

– see non-generic type.

## non-generic type

– a named type (class or interface) that has no type parameters.

## nonterminal

see nonterminal symbol.

## nonterminal symbol

– a syntactically variable token that results from the successive application of production rules.

## nullable type

– a variable declared to have the value null, or type T | null that can hold values of type T and its derived types.

## Page 18

## nullish value

– a reference which is null or undefined.

## operand

– an argument of an operation. Syntactically, operands have the form of simple or qualified identifiers that refer to variables or members of structured objects. In turn, operands can be operators whose preferences ('priorities') are higher than the preference of a given operator.

## operation

- an informal notion that signifies an action or a process of operator evaluation.

## operation sign

– a language token that signifies an operator and conventionally denotes a usual mathematical operator, e.g., ‘+’ for addition, ‘/’ for division, etc. However, some languages allow using identifiers to denote operators, and/or arbitrarily combining characters that are not tokens in the alphabet of that language (i.e., operator signs).

## operator (in programming languages)

– the term can have several meanings as follows:

(1) a token that denotes the action to be performed on a value (addition, subtraction, comparison, etc.).

(2) a syntactic construct that denotes an elementary calculation within an expression. An operator normally consists of an operator sign and one or more operands.

In unary operators that have a single operand, the operator sign can be placed either in front of or after an operand (prefix and postfix unary operator respectively).

If both operands are available, then the operator sign can be placed between the two (infix binary operator). A conditional operator with three operands is called ternary.

Some operators have special notations. For example, an indexing operator has a conventional form like a[i] while formally being a binary operator.

Some languages treat operators as syntactic sugar, i.e., a conventional version of a more common construct or function call. Therefore, an operator like a+b is conceptually handled as the call +(a,b), where the operator sign plays the role of a function name, and the operands are function call arguments.

## overloading

– a language feature that allows using a single name to call several functions (in the general sense, i.e., including methods and constructors) with different signatures and different bodies.

### own (adj.)

– of a member textually declared in a class, interface, type, etc., as opposed to members inherited from base class (superclass), base interfaces (superinterface), base type (supertype), etc.

## production

– a sequence of terminal and nonterminal symbols that a programming language interprets as correct.

## punctuator

– a token that serves to separate, complete, or otherwise organize program elements and parts: commas, semicolons, parentheses, square brackets, etc.

## qualified name

– a name that consists of a sequence of identifiers separated with the token ‘. ’.

## resistable array type

– a built-in type that consists of more than one element, and can have the number of constituent elements changed at runtime.

## scope of a name

– a region of program code within which an entity—as declared by that name—can be accessed or referred to by its simple name without any qualification.

## Page 19

## simple name

– a name that consists of a single identifier.

## static member

– a class member that is not related to a particular class instance. A static member can be used across an entire program by using a qualified name notation (qualification is the name of a class).

## subcomponent (derived component, child component)

– a component produced by, inherited from, and dependent from another component.

## supercomponent (base component, parent component)

– a component from which another component is derived.

## terminal

– see terminal symbol.

## terminal symbol

– a syntactically invariable token (i.e., a syntactic notation defined directly by an invariable form of the lexical grammar that defines a set of productions starting from the goal symbol).

## token

– an elementary part of a programming language: identifier, keyword, operator and punctuator, or literal. Tokens are lexical input elements that form the vocabulary of a language, and can act as terminal symbols of the language's syntactic grammar.

## tokenization

– finding the longest sequence of characters that forms a valid token (i.e., establishing a token) in the process of codebase reading by the machine.

## type parameter scope

– the scope of a name of a type parameter that is declared in a class or an interface. Type parameter scope is identical to the entire declaration (except static member declarations).

## type reference

– references that refer to named types by specifying their type names and type arguments, where applicable, to be substituted for type parameters of the named type.

## variable

– see variable declaration.

## variable declaration

– a declaration that introduces a new named variable to which a modifiable initial value can be assigned.

## white space

– lexical input elements that separates tokens from one another in order to improve the source code readability and avoid ambiguities.

## widening conversion

– a conversion that causes no loss of information about the overall magnitude of a numeric value.

## Page 20

## Page 21

## LEXICAL ELEMENTS

This chapter discusses the lexical structure of the ArkTS programming language.

### 2.1 Use of Unicode Characters

1ne ArkTS programming language uses characters of the Unicode Character set $ ^{1} $ as its terminal symbols. It uses the Unicode UTF-16 encoding to represent text in sequences of 16-bit code units.

The term Unicode code point is used in this specification only where such representation is relevant to refer the reader to Unicode Character set and UTF-16 encoding. Where such representation is irrelevant to the discussion, the generic term character is used.

### 2.2 Lexical Input Elements

The language has the following types of lexical input elements:

• White Spaces.

• Line Separators.

• Tokens, and

• Comments.

### 2.3 White Spaces

White spaces are lexical input elements that separate tokens from one another. White spaces include the following:

• Space (U+0020),

• Horizontal tabulation (U+0009),

## Page 22

• Vertical tabulation (U+000B),

• Form feed (U+000C),

• No-break space  $ (U+00A0) $, and

• Zero-width no-break space (U+FEFF).

White spaces improve source code readability and help avoiding ambiguities. White spaces are ignored by the syntactic grammar (see Grammar Summary). White spaces never occur within a single token, but can occur within a comment.

### 2.4 Line Separators

Line separators are lexical input elements that separate tokens from one another and divide sequences of Unicode input characters into lines. Line separators include the following:

• Newline character (U+000A or ASCII <LF>)

• Carriage return character (U+000D or ASCII <CR>)

• Line separator character (U+2028 or ASCII <LS>), and

• Paragraph separator character (U+2029 or ASCII <PS>)

Line separators improve source code readability. Any sequence of line separators is considered a single separator.

Line separators are often treated as white spaces, except where line separators have special meanings. See Semicolons for more details.

### 2.5 Tokens

Tokens form the vocabulary of the language. There are four classes of tokens:

• Identifiers,

• Keywords,

• Operators and Punctuators, and

• Literals.

Token is the only lexical input element that can act as a terminal symbol of the syntactic grammar (see Grammar Summary). In the process of tokenization, the next token is always the longest sequence of characters that form a valid token. Tokens are separated by white spaces (see White Spaces), operators, or punctuators (see Operators and Punctuators). White spaces are ignored by the syntactic grammar (see Grammar Summary).
