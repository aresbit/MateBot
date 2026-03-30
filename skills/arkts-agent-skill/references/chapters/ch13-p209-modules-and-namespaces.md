# Chapter 13: Modules and Namespaces

Page range: 209-228

## Page 209

## INTERFACES

An interface declaration declares an interface type, i.e., a reference type that:

• Includes properties and methods as its members;

• Has no instance variables (fields);

• Usually declares one or more methods;

• Allows otherwise unrelated classes to provide implementations for the methods, and so implement the interface.

Creating an instance of interface type is not possible.

An interface can be declared direct extension of one or more other interfaces. If so, the interface inherits all members from the interfaces it extends. Inherited members can be optionally overridden or hidden.

A class can be declared to directly implement one or more interfaces. Any instance of a class implements all methods specified by its interface(s). A class implements all interfaces that its direct superclasses and direct superinterfaces implement. Interface inheritance allows objects to support common behaviors without sharing a superclass.

The value of a variable declared interface type can be a reference to any instance of a class that implements the specified interface. However, it is not enough for a class to implement all methods of an interface. A class or one of its superclasses must be actually declared to implement an interface. Otherwise, the class is not considered to implement the interface.

The rules of subtyping are discussed in detail in Subtyping for Non-Generic Classes and Interfaces and Subtyping for Generic Classes and Interfaces.

### 10.1 Interface Declarations

Interface declaration specifies a new named reference type.

The syntax of interface declarations is presented below:

interfaceDeclaration:
    'interface' identifier typeParameters?
    interfaceExtendsClause? '{' interfaceMember* '}'
;
interfaceExtendsClause:
    'extends' interfaceTypeList
;

(continues on next page)

## Page 210

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

## Page 211

• All methods inherited from superinterfaces refer to the same implementation, and this default implementation is the current interface method; or

• One method m in some superinterface overrides all other methods from other superinterfaces.

Otherwise, a compile-time error occurs.

interface I1 { foo () {} }
interface I2 { foo () {} }
interface II1 extends I1, I2 {
    foo () {} // foo() from II1 overrides both foo() from I1 and foo() from I2
}
interface II2 extends I1, I2 {
    // Compile-time error as foo() from I1 and foo() from I2 have different_
    →implementations
}
interface I3 extends I1 {}
interface I4 extends I1 {}
interface II3 extends I3, I4 {
    // OK, as foo() from I3 and foo() from I4 refer to the same implementation
}
class Base {}
class Derived extends Base {}
interface II1 {
    foo (p: Base) {}
}
interface II2 {
    foo (p: Derived) {}
}
interface II3 extends II1, II2 {}
    // foo() from II1 overrides foo() from II2

### 10.3 Interface Members

An interface declaration can contain interface members, i.e., its properties (see Interface Properties) and methods (see Interface Method Declarations).

The syntax of interface member is presented below:

interfaceMember
    : annotationUsage?
    ( interfaceProperty
    | interfaceMethodDeclaration
    | overloadInterfaceMethodDeclaration
)

The scope of declaration of a member m that the interface type I declares or inherits is specified in Scopes.

## Page 212

The usage of annotations is discussed in Using Annotations.

Interface members include:

• Members declared explicitly in the interface declaration;

• Members inherited from a direct superinterface (see Superinterfaces and Subinterfaces).

A compile-time error occurs if the method explicitly declared by the interface has the same name as the Object's public method.

interface I {
    toString (p: number): void // Compile-time error
    toString(): string { return "some string" } // Compile-time error
}

An interface inherits all members of the interfaces it extends (see Interface Inheritance).

A name in a declaration scope must be unique, i.e., the names of properties and methods of an interface type must not be the same (see Interface Declarations).

### 10.4 Interface Properties

Interface property can be defined in the form of a field or an accessor (a getter or a setter).

The syntax of interface property is presented below:

interfaceProperty:
  'readonly'? identifier '?' '?' '': 'type
  | 'get' identifier '(' ')' returnType
  | 'set' identifier '(' parameter ')'
;

An interface property is a required property (see Required Interface Properties) if it is one of the following:

• Explicit accessor, i.e., a getter or a setter; or

• Form of a field that has no ‘?’.

Otherwise, it is an optional property (see Optional Interface Properties).

If ‘?’ is used after the name of the property, then the property type is semantically equivalent to type | undefined.

interface I {
    property?: Type
}
// is the same as
interface I {
    property: Type | undefined
}

## Page 213

#### 10.4.1 Required Interface Properties

A required property defined in the form of a field implicitly defines the following:

• Getter, if the property is marked as readonly;

• Otherwise, both a getter and a setter with the same name.

A type annotation for the field defines return type for the getter and type of parameter for the setter.

As a result, the following declarations have the same effect:

interface Style {
    color: string
}

// is the same as
interface Style {
    get color(): string
    set color(s: string)
}

Note. A required property defined in a form of accessors does not define any additional entities in the interface.

A class that implements an interface with properties can also use a field or an accessor notation (see Implementing Required Interface Properties, Implementing Optional Interface Properties).

#### 10.4.2 Optional Interface Properties

An optional property can be defined in two forms:

• Short form identifier '?' '::' T; or

• Explicit form identifier ':' T | undefined.

In both cases, identifier has effective type T | undefined.

The optional property implicitly defines the following:

• A getter (if the property is marked as readonly);

• Otherwise, both a getter and a setter with the same name.

Accessors have implicitly defined bodies, in this aspect they are similar to Default Interface Method Declarations. However, ArkTS does not support explicitly defined accessors with bodies.

The following declaration:

interface I {
    num?: number
}

– implicitly declares two accessors:

interface I {
    get num(): number | undefined { return undefined }
    set num(x: number | undefined) { throw new InvalidStoreAccessError }
}

## Page 214

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

## Page 215

## ENUMERATIONS

Enumeration type enum specifies a distinct user-defined type with an associated set of named constants that define its possible values.

The syntax of enumeration declaration is presented below:

enumDeclaration:
    'const'? 'enum' identifier (':' type)? '{' enumConstantList? '}'
;
enumConstantList:
    enumConstant (',' enumConstant)* ','?
;
enumConstant:
    identifier ('=' constantExpression)?
;

Type const enum is supported for source-level compatibility with TypeScript. The modifier const is skipped as it has no impact on enum semantics in ArkTS.

Qualification by type is mandatory to access the enumeration constant, except enumeration constant initialization expressions:

enum Color { Red, Green, Blue }
let c: Color = Color.Red

enum Flags { Read, Write, ReadWrite = Read | Write }
// No need to use Flags.Read | Flags.Write in initialization

If enumeration type is exported, then all enumeration constants are exported along with the mandatory qualification.

For example, if Color is exported, then all constants like Color.Red are exported along with the mandatory qualification Color.

The value of an enum constant can be set as follows:

• Explicitly to a numeric constant expression (expression of type int or long) or to a constant expression of type string; or

• Implicitly by omitting the constant expression.

If constant expression is omitted, then the value of the enum constant is set implicitly to an integer value (see Enumeration Integer Values).

A compile-time error occurs if integer or string type enumeration constants are combined in a single enumeration.

## Page 216

A type to which all enumeration constant values belong is called enumeration base type. This type is int, long or string.

Any enumeration constant is of type enumeration. Implicit conversion (see Enumeration to Constants Type Conversions) of an enumeration constant to numeric types or type string depends on the type of constants.

In addition, all enumeration constant names must be unique. Otherwise, a compile-time error occurs.

enum E1 { A, B = "hello" } // compile-time error
enum E2 { A = 5, B = "hello" } // compile-time error
enum E3 { A = 5, A = 77 } // compile-time error
enum E4 { A = 5, B = 5 } // OK! values can be the same

Empty enum is supported as a corner case for compatibility with TypeScript.

enum Empty {} // OK

### 11.1 Enumeration Integer Values

The integer value of an enum constant is set implicitly if an enumeration constant specifies no value.

A constant expression of type int or long can be used to set the value explicitly:

enum Background { White = 0xFF, Grey = 0x7F, Black = 0x00 }
enum LongEnum { A = 0x7FFF_FFFF_1, B, C }

Choosing which type to use—int or long—is based on the same principle as for integer literals (see Integer Literals).

If all constants have no value, then the first constant is assigned the value zero. The other constant is assigned the value of the immediately preceding constant plus one.

If some but not all constants have their values set explicitly, then the values of the constants are set by the following rules:

• The constant which is the first and has no explicit value gets zero value.

• Constant with an explicit value has that explicit value.

• Constant that is not the first and has no explicit value takes the value of the immediately preceding constant plus one.

In the example below, the value of Red is 0, of Blue, 5, and of Green, 6:

enum Color { Red, Blue = 5, Green }

### 11.2 Enumeration String Values

A string value for enumeration constants must be set explicitly:

## Page 217

enum Commands { Open = "fopen", Close = "fclose" }

### 11.3 Enumeration Operations

The value of an enumeration constant can be converted to type string by using the method toString:

enum Color { Red, Green = 10, Blue }
let c: Color = Color.Green
console.log(c.toString()) // prints: 10

The name of enumeration type can be indexed by the value of this enumeration type to get the name of the constant:

enum Color { Red, Green = 10, Blue }
let c: Color = Color.Green
console.log(Color[c]) // prints: Green

If several enumeration constants have the same value, then the textually last constant has the priority:

enum E { One = 1, one = 1, oNe = 1 }
console.log(E.fromValue(1)) // prints: oNe

Additional methods available for enumeration types and constants are discussed in Enumeration Methods in the chapter Experimental Features.

## Page 218

## Page 219

## ERROR HANDLING

ArkTS is designed to provide first-class support in responding to, and recovering from different error situations in a program. Normal program execution can be interrupted by the occurrence of situations of two kinds:

• Runtime errors (e.g., null pointer dereferencing, array bounds checking, or division by zero);

• Operation completion failures (e.g., the task of reading and processing data from a file on disk can fail if the file does not exist on a specified path, read permissions are not available, or else).

The term error in this Specification denotes all kinds of error situations.

### 12.1 Errors

Error is the base class of all error situations. Defining a new error class is normally not required because essential error classes for various cases (e.g., RangeError) are defined in the standard library (see Standard Library).

However, a developer can handle a new error situation by using Error class itself, or by a subclass of Error. An example of error handling is provided below:

class UnknownError extends Error { // User-defined error class
    error: Error
    constructor (error: Error) {
        super()
        this.error = error
    }
}

function get_array_element<T>(array: T[], index: number): T | null {
    try {
        return array[index] // access array
    }
    catch (error) {
        if (error instanceof RangeError) // invalid index detected
            return null
        }
    }
}

## Page 220

(continued from previous page)

throw new UnknownError(error) // Unknown error occurred

16
17
18

In most cases, errors are raised by the ArkTS runtime system, or by the standard library (see Standard Library) code.

New error situations can be created and raised by throw statements (see throw Statements).

Errors are handled by using try statements (see try Statements).

Note. Not every error can be recovered.

function handleAll(
    actions : () => void,
    handling_actions : () => void)
{
    try {
        actions()
    }
    catch (x) { // Type of x is Error handling_actions()
        }
    }
}

## Page 221

## MODULES AND NAMESPACES

Programs in ArkTS are structured as sequences of elements ready for compilation called modules. Each module creates its own scope (see Scopes). Variables, functions, classes, interfaces, or other declarations of a module are only accessible (see Accessible) within such a scope if not explicitly exported.

A variable, function, class, interface, or other declarations exported from a module must be imported first by the module that is to use them.

All modules are stored in a file system or a database (see Modules in Host System).

A module can optionally consist of the following four parts:

1. Import directives that enable referring imported declarations in a module;

2. Top-level declarations;

3. Top-level statements; and

4. Re-export directives.

The syntax of module is presented below:

moduleDeclaration:
    importDirective* (topDeclaration | topLevelStatements | exportDirective)*
;

Every module can directly use all exported entities from the standard library (see Standard Library Usage).

// Hello, world! module
function main() {
    console.log("Hello, world!") // console is defined in the standard library
}

If a module has at least one top-level ambient declaration (see Ambient Declarations) then all other declarations must be ambient as well and no top-level statements (see Top-Level Statements). Otherwise, a compile-time error occurs.

declare let x: number
function main() {}
// compile-time error: ambient and non-ambient declarations are mixed

## Page 222

### 13.1 Import Directives

Import directives make entities exported from other modules (see Modules and Namespaces) available for use in the current module by using different binding forms. These directives have no effect during the program execution.

An import declaration has the following two parts:

• Import path that determines from what module to import;

- Import bindings that define what entities, and in what form (either qualified or unqualified) the current module can use.

The syntax of import directives is presented below:

import Directive:
    'import ' 'type'? bindings 'from' import Path
;

bindings:
    defaultBinding
    | (defaultBinding ',')? allBinding
    | (defaultBinding ',')? selectiveBindings
;

allBinding:
    '*' bindingAlias
;

bindingAlias:
    'as' identifier
;

defaultBinding:
    identifier
;

selectiveBindings:
    nameBinding (',' nameBinding)*
;

nameBinding:
    identifier bindingAlias?
    | 'default' 'as' identifier
;

importPath:
    StringLiteral
;

Each binding adds a declaration or declarations to the scope of a module (see Scopes). Any declaration added so must be distinguishable in the declaration scope (see Declarations).

Import with type modifier is discussed in Import Type Directive.

A compile-time error occurs if:

• Declaration added to the scope of a module by a binding is not distinguishable;

## Page 223

• Module imports itself directly: importPath refers to the file in which the current module is stored; or

#### 13.1.1 Bind All with Qualified Access

Import binding * as A binds the single named entity A to the declaration scope of the current module.

A qualified name consisting of A and the name of entity A.name is used to access any entity exported from the module as defined by the import path.

Import Usage
import * as Math from "..."
    let x = Math.sin(1.0)

This form of import is recommended because it simplifies the reading and understanding of the source code when all exported entities are prefixed with the name of the imported module.

#### 13.1.2 Default Import Binding

Default import binding allows importing a declaration exported from a module as default export. Knowing the actual name of a declaration is not required as the new name is given at importing. A compile-time error occurs if another form of import is used to import an entity initially exported as default.

There are two forms of default import binding:

• Single identifier;

• Special form of selective import with the keyword default.

import DefaultExportedItemBindedName from ".../someFile"
import {default as DefaultExportedItemNewName} from ".../someFile"
function foo() {
    let v1 = new DefaultExportedItemBindedName()
    // instance of class 'SomeClass' to be created here
    let v2 = new DefaultExportedItemNewName()
    // instance of class 'SomeClass' to be created here
}

// SomeFile
export default class SomeClass {}

// Or
class SomeClass {}
export default SomeClass

## Page 224

#### 13.1.3 Selective Binding

Selective binding allows to bind an entity exported as identifier, or an entity exported by default (see Default Import Binding).

Binding with identifier binds an exported entity with the name identifier to the declaration scope of the current module. If no binding alias is present, then the entity is added to the declaration scope under the original name. Otherwise, the identifier specified in binding alias is used. In the latter case, the bounded entity is no longer accessible (see Accessible) under the original name.

If an identifier denotes an overload alias (see Function Overload Declarations), then all its accessible overloaded functions, either imported or not, are considered in the process of Overload Resolution for call validity.

// File1
export function f1(p: number) {}
export function f2(p: string) {}
export overload foo {f1, f2}

// File2
import {foo} from "File1" // Note: f1 and f2 are not mandatory imported
foo(5) // f1() is called
foo("a string") // f2() is called

// File3
import {foo, f1} from "File1" // Note: f1 is accessible as well
f1(5) // f1() is called
foo(6) // f1() is called
foo("a string") // f2() is called

Selective binding that uses exported entities is represented in the examples below:

export const PI = 3.14
export function sin(d: number): number {}

Note. The import path of the module is irrelevant and replaced for ‘​…’ in the examples below:

import {sin}

A single import statement can list several names as follows:

## Page 225

import Usage

import {sin, PI} from "..."
    let x = sin(PI)

import {sin as Sine, PI}
    let x = Sine(PI)
    ...
    ...

Complex cases with several bindings mixed on one import path are discussed below in Several Bindings for One Import Path.

#### 13.1.4 Import Type Directive

An import directive can have a type modifier exclusively for a better syntactic compatibility with TypeScript (also see Export Type Directive). ArkTS supports no additional semantic checks for entities imported by using import type directives.

The semantic checks performed by the compiler in TypeScript but not in ArkTS are represented by the following code:

// File module.ets
console.log("Module initialization code")

export class Class1 {/*body*/}

class Class2 {}
export type {Class2}

// MainProgram.ets
import {Class1} from "./module.ets"
import type {Class2} from "./module.ets"

let c1 = new Class1() // OK
let c2 = new Class2() // Compile-time error in Typescript, OK in ArkTS

#### 13.1.5 Import Path

Import path is a string literal that determines where and how an imported module is to be searched for.

Import path can include the following:

• Initial dot ‘.’ or two dots ‘..’ followed by the slash character ‘/’.

## Page 226

• One or more path components (the subset of characters and case sensitivity of path components must follow the path rules of a host filesystem).

• Slash characters separating components of the path.

The slash character ‘/’ is used in import paths irrespective of the host system. The backslash character is not used in this context.

In most file systems, an import path looks like a file path. Relative (see below) and non-relative import paths have different resolutions that map the import path to a file path of the host system.

The compiler uses its own algorithm to locate a module source that processes the import path. If the import path specifies no file extension, then the compiler can append some according to its own rules and priorities. If the import path refers to a folder, then the way to handle the case is determined by the actual compiler. If the compiler cannot locate a module source definitely, then a compile-time error occurs.

A relative import path starts with ‘./’ or ‘../’. Examples of relative paths are presented below:

"./components/entry"
"./constants/http"

Resolving relative import is relative to the importing file. Relative import is used on modules to maintain their relative location.

import * asUtils from"./mytreeutils"

Other import paths are non-relative.

Resolving a non-relative path depends on the compilation environment. The definition of the compiler environment can be particularly provided in a configuration file or environment variables.

The base URL setting is used to resolve a path that starts withத்‌த்‌த்‌த்‌

{
    "baseUrl": "/home/project",
    "paths": {
        "std": "/arkts/stdlib"
    }
}

In the example above, /net/http is resolved to /home/project/net/http, and std/components/treemap to /arkts/stdlib/components/treemap.

File name, placement, and format are implementation-specific.

If the above configuration is in effect, the first path maps directly to filesystem after applying baseUrl, while std in the second path is replaced for /arkts/stdlib. Examples of non-relative paths are presented below.

"/net/http"
"std/components/treemap"

## Page 227

#### 13.1.6 Several Bindings for One Import Path

The same bound entities can use the following:

• Several import bindings,

• One import directive, or several import directives with the same import path:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>In one import directive</td><td style='text-align: center; word-wrap: break-word;'>import {sin, cos} from &quot;...</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>In several import directives</td><td style='text-align: center; word-wrap: break-word;'>import {sin} from &quot;...import {cos} from &quot;...</td></tr></table>

No conflict occurs in the above example, because the import bindings define disjoint sets of names.

The order of import bindings in an import declaration has no influence on the outcome of the import.

The rules below prescribe what names must be used to add bound entities to the declaration scope of the current module if multiple bindings are applied to a single name:

## Page 228

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Case</td><td style='text-align: center; word-wrap: break-word;'>Sample</td><td style='text-align: center; word-wrap: break-word;'>Rule</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>A name is explicitly used without an alias in several bindings.</td><td style='text-align: center; word-wrap: break-word;'>import {sin, sin} from &quot;...&quot;</td><td style='text-align: center; word-wrap: break-word;'>OK. The compile-time warning is recommended.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>A name is used explicitly without alias in one binding.</td><td style='text-align: center; word-wrap: break-word;'>import {sin} from &quot;...&quot;</td><td style='text-align: center; word-wrap: break-word;'>OK. No warning.</td></tr><tr><td rowspan="2">A name is explicitly used without alias, and implicitly with alias.</td><td style='text-align: center; word-wrap: break-word;'>import {sin} from &quot;...&quot;</td><td rowspan="2">OK. Both the name and qualified name can be used: sin and M.sin are accessible.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>import * as M from &quot;...&quot;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>A name is explicitly used with alias.</td><td style='text-align: center; word-wrap: break-word;'>import {sin as Sine} from &quot;...&quot;</td><td style='text-align: center; word-wrap: break-word;'>OK. Only alias is accessible for the name, but not the original name: • Sine is accessible; • sin is not accessible.</td></tr><tr><td rowspan="2">A name is explicitly used with alias, and implicitly with alias.</td><td style='text-align: center; word-wrap: break-word;'>import {sin as Sine} from &quot;...&quot;</td><td rowspan="2">OK. Both options can be used: • Sine is accessible; • M.sin is accessible.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>import * as M from &quot;...&quot;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>A name is explicitly used with alias several times.</td><td style='text-align: center; word-wrap: break-word;'>import {sin as Sine, sin as SIN} from &quot;...&quot;</td><td style='text-align: center; word-wrap: break-word;'>OK. Both aliases are accessible. But warning can be displayed.</td></tr></table>

### 13.2 Standard Library Usage

All entities exported from the standard library (see Standard Library) are accessible as simple names (see Accessible) in any module. Using these names as programmer-defined entities at module scope causes a compile-time error in accordance to Declarations.

console.log("Hello, world!") // ok, 'console' is defined in the library

let console = 5 // compile-time error
