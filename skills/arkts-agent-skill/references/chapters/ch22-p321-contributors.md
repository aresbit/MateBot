# Chapter 22: Contributors

Page range: 321-353

## Page 321

### 18.3 Exporting and Importing Annotations

An annotation can be exported and imported. However, a few forms of export and import directives are supported.

An annotation declaration to be exported must be marked with the keyword export as follows:

// a.ets
export @interface MyAnno {}

If an annotation is imported as a part of an imported module, then the annotation is accessed by its qualified name:

// b.ets
import * as ns from "./a"

@ns.MyAnno
class C {/*body*/}

Unqualified import is also allowed:

// b.ets
import { MyAnno } from "./a"

@MyAnno
class C {/*body*/}

An annotation is not a type. Using export type or import type notations to export or import annotations is forbidden:

import type { MyAnno } from "./a" // compile-time error

Annotations are forbidden in the following cases:

• Export default,

• Import default,

• Rename in export, and

• Rename in import.

import {MyAnno as Anno} from "./a" // compile-time error

### 18.4 Ambient Annotations

The syntax of ambient annotations is presented below:

ambientAnnotationDeclaration:
'declare' annotationDeclaration
;

Such a declaration does not introduce a new annotation but provides type information that is required to use the annotation. The annotation itself must be defined elsewhere. A runtime error occurs if no annotation corresponds to the ambient annotation used in the program.

## Page 322

An ambient annotation and the annotation that implements it must be exactly identical, including field initialization:

// a.d.ets
export declare @interface NameAnno{name: string = ""}

// a.ets
export @interface NameAnno{name: string = ""} // ok

The code in the example below is incorrect because the ambient declaration is not identical to the annotation declaration:

// a.d.ets
export declare @interface VersionAnno{version: number} // initialization is missing

// a.ets
export @interface VersionAnno{version: number = 1}

An ambient declaration can be imported and used in exactly the same manner as a regular annotation:

// a.d.ets
export declare @interface MyAnno {}

// b.ets
import { MyAnno } from "./a"

@MyAnno
class C {/*body*/}

If an annotation is applied to an ambient declaration in the .d.ets file (see the example below), then the annotation is to be applied to the implementation declaration manually, because the annotation is not automatically applied to the declaration that implements the ambient declaration:

// a.d.ets
export declare @interface MyAnno {}

@MyAnno
declare class C {}

### 18.5 Standard Annotations

Standard annotation is an annotation that is defined in Standard Library, or implicitly defined in the compiler (built-in annotation). Standard annotation is usually known to the compiler. It modifies the semantics of the declaration it is applied to.

An annotation that annotates a declaration of another annotation is called meta-annotation.

## Page 323

#### 18.5.1 Retention Annotation

@Retention is a standard meta-annotation that is used to annotate a declaration of another annotation. A compile-time error occurs if it is used in other places.

The annotation has a single field policy of type string. It is typically used as follows:

@Retention({policy: "RUNTIME"})
@interface MyAnno {} // this annotation uses "RUNTIME" policy
@MyAnno //
class C {}

The value of this field determines at which point an annotation is used, and discarded after use. The retention policies can be of three types:

• “SOURCE”

Annotations that use “SOURCE” policy are processed at compile time, and are discarded after compilation;

• "BYTECODE"

Metadata specified in annotations that use “BYTECODE” policy are saved into the bytecode file, but are discarded at runtime.

• "RUNTIME"

Metadata specified in annotations that use “RUNTIME” policy are saved into the bytecode file, are retained and can be accessed at runtime.

The default retention policy is “BYTECODE”.

A compile-time error occurs if any other string literal is used as the value of policy field.

As @Retention has a single field, it can be used with a short notation (see Using Single Field Annotations) as follows:

@Retention("SOURCE")
@interface Author {name: string} // this annotation uses "SOURCE" policy

### 18.6 Runtime Access to Annotations

For an annotation with retention policy (see Retention Annotation) BYTECODE or RUNTIME an abstract class with the name of the annotation is implicitly declared. All fields of this class are reasonably. If a field is of an array type, the array type is also readonly.

For the following annotation:

@Retention("RUNTIME")
@interface MyAnno {
    name: string
    attrs: number[]
}

—the abstract class is declared:

## Page 324

abstract class MyAnno {
    readonly name: string
    readonly attrs: readonly number[]
}

The use of such a class is represented in following example:

@MyAnno({name: "someName", attr: [1, 2]})
class A {}

let my: MyAnno = // call of reflection library to get instance of annotation for type A
console.log(my.name) // output: someName

## Page 325

## STANDARD LIBRARY

The Standard Library of the ArkTS language defines the required set of types, variables, constants, functions, and annotations that provide APIs for effective and convenient programming.

The Standard Library has two parts: the common part provides TypeScript compatibility, and the ArkTS-specific part adds more advanced features.

A detailed description of all elements of the standard library is covered in a separate document that is a part of the ArkTS distribution package.

## Page 326

## Page 327

## IMPLEMENTATION DETAILS

Important implementation details are discussed in this section.

### 20.1 Import Path Lookup

If an import path <some path>/name is resolved to a path in the folder 'name', then the compiler executes the following lookup sequence:

• If the folder contains the file index.ets, then this file is imported as a module written in ArkTS;

• If the folder contains the file index.ts, then this file is imported as a module written in TypeScript.

### 20.2 Modules in Host System

Modules are created and stored in a manner that is determined by the host system. The exact manner modules are stored in a file system is determined by a particular implementation of the compiler and other tools.

A simple implementation stores every module in a single file.

### 20.3 Getting Type Via Reflection

The ArkTS standard library (see Standard Library) provides a pseudogeneric static method Type.from<T>() to be processed by the compiler in a specific way during compilation. A call to this method allows getting a value of type Type that represents type T at runtime.

let type_of_int: Type = Type.from<int>()
    let type_of_string: Type = Type.from<string>()
    let type_of_number: Type = Type.from<number>()
    let type_of_Object: Type = Type.from<Object>()

class UserClass {}
let type_of_user_class: Type = Type.from<UserClass>()

(continues on next page)

## Page 328

(continued from previous page)

interface SomeInterface {}
let type_of_interface: Type = Type.from<SomeInterface>()

If type T used as type argument is affected by Type Erasure, then the function returns value of type Type for effective type of T but not for T itself:

let type_of_array1: Type = Type.from<int[]>( ) // value of Type for Array<>
let type_of_array2: Type = Type.from<Array<number>>() // the same Type value

### 20.4 Ensuring Module Initialization

The ArkTS standard library (see Standard Library) provides a top-level function initModule() with one parameter of string type. A call to this function ensures that the module referred by the argument is available, and that its initialization (see Static Initialization) is performed. An argument must be a string literal. Otherwise, a compile-time error occurs.

The current module has no access to the exported declarations of the module referred by the argument. If such module is not available or any other runtime issue occurs then a proper exception is thrown.

initModule (@ohos/library/src/main/ets/pages/Index")

### 20.5 Generic and Function Types Peculiarities

The current compiler and runtime implementations use type erasure. Type erasure affects the behavior of generics and function types. It is expected to change in the future. A particular example is provided in the last bullet point in the list of compile-time errors in InstanceOf Expression.

### 20.6 Keyword struct and ArkUI

The current compiler reserves the keyword struct because it is used in legacy ArkUI code. This keyword can be used as a replacement for the keyword class in Class Declarations. Class declarations marked with the keyword struct are processed by the ArkUI plugin and replaced with class declarations that use specific ArkUI types.

## Page 329

### 20.7 OutOfMemoryError for Primitive Type Operations

The execution of some primitive type operations (e.g., increment, decrement, and assignment) can throw OutOfMemoryError (see Error Handling) if allocation of a new object is required but the available memory is not sufficient to perform it.

### 20.8 Make a Bridge Method for Overriding Method

Situations are possible where the compiler must create an additional bridge method to provide a type-safe call for the overriding method in a subclass of a generic class. Overriding is based on erased types (see Type Erasure). The situation is represented in the following example:

class B<T extends Object> {
    foo(p: T) {}
}

class D extends B<string> {
    foo(p: string) {} // original overriding method
}

In the example above, the compiler generates a bridge method with the name foo and signature (p: Object). The bridge method acts as follows:

- Behaves as an ordinary method in most cases, but is not accessible from the source code, and does not participate in overloading;

• Applies narrowing to argument types inside its body to match the parameter types of the original method, and invokes the original method.

The use of the bridge method is represented by the following code:

let d = new D()
d.foo("aa") // original method from 'D' is called
let b: B<string> = d
b.foo("aa") // bridge method with signature (p: Object) is called
// its body calls original method, using (p as string) to check the type of the argument

More formally, a bridge method  $ m(C_1, \ldots, C_n) $ is created in D, in the following cases:

• Class B comprises type parameters  $ B<T_1 $ extends  $ C_1 $, ...,  $ T_n $ extends  $ C_n> $;

• Subclass D is defined as class D extends B<X₁, ..., Xₙ>;

• Method m of class D overrides m from B with type parameters in signature, e.g.,  $ (T_1, \ldots, T_n) $;

• Signature of the overridden method m is not  $ (C_{1}, \ldots, C_{n}) $.

## Page 330

## Page 331

## GRAMMAR SUMMARY

literal: Literal;
identifier: Identifier;

indexType: 'number';

type:
  annotationUsage?
  ( typeReference
  | 'readonly'? arrayType
  | 'readonly'? tupleType
  | functionType
  | functionTypeWithReceiver
  | unionType
  | keyofType
  | StringLiteral
)
| '(' type ')'
;

typeReference:
  typeReferencePart ('.' typeReferencePart)*
;

typeReferencePart:
  identifier typeArguments?
;

arrayType:
  type '[' '']
;

## Page 332

## Page 333

## CONTRIBUTORS

Language design lead:

• Nedoria Aleksei

Contributors:

• Bronnikov Georgy

• Gavrin Evgeny

• Huo Qingyi

• Kanatov Alexey

• Nedoria Aleksei

• Olshevsky Vladimir

• Pavlyuk Alexander

• Pei Jiajun

• Polyakov Alexander

• Pukhov Vsevolod

• Qiu Yu

• Rubanov Vladimir

• Soldatov Anton

• Solomennikov Dmitry

• Trubenkov Dmitrii

• Velikanov Michael

• Xian Yuqiang

• Zouev Evgeniy

Technical writer:

• Baranov Dmitry

## Page 334

## Page 335

## A

abrupt completion, 90–92, 95, 102, 106, 111, 113, 122, 123, 141–144, 148, 153, 164, 165, 276

abstract, 186

abstract class, 98, 168, 169, 172, 186, 312

abstract concept, 2

abstract data structure, 2

abstract declaration, 3, 202

abstract function, 268, 278

abstract keyword, 293

abstract method, 98, 108, 169, 171, 172, 186, 187, 195

abstract method call, 108

abstract modifier, 168, 169, 185–187, 189

abstract notion, 2

abstract symbol, 3

abstraction, 2

access, 36, 38, 40, 47, 53, 54, 65, 78, 79, 91, 105, 106, 110, 111, 113, 141, 144, 164, 176–182, 191, 194, 195, 198, 202, 203, 211, 212, 216, 217, 219, 221–223, 226, 227, 235, 236, 253, 254, 260, 261, 263, 273, 275, 279, 284, 296, 297, 302, 305, 309, 311, 316, 317

access constructor, 88

access expression, 142

access modifier, 54, 167, 177, 178, 189, 191, 194, 202, 254, 285

accessibility, 51, 53, 54, 65, 74, 79, 99, 106, 148, 159, 169, 171, 176–178, 180, 191, 194, 195, 198, 202, 203, 212, 216–218, 221–223, 226, 236, 254, 275, 279, 283, 296, 297, 305

accessible, 260

accessible constructor, 178, 194

accessible declaration, 217, 222, 236

accessible entity, 54

accessible function, 284

accessible interface type, 171

accessible member, 195

accessible member field, 99, 106

accessible method, 285

accessible scope, 53

accessible type, 178

processor, 46, 100, 101, 106, 167, 173, 175–177, 184,

190, 195, 200–202, 254, 295, 299, 302, 303

accessor declaration, 100, 106, 177, 184, 217, 299

accessor modifier, 189, 190

accessor with receiver, 217, 295, 299

accessor with receiver declaration, 299

addition, 13, 130

additive expression, 29, 83, 130, 150

additive operator, 29, 30, 130, 131, 150

alias, 23, 24, 27, 38, 41, 45, 55, 56, 169, 198, 216, 287, 288

alignment, 137, 264

allocation, 148, 317

alpha-numeric character, 214

ambient, 229

ambient processor declaration, 232

ambient annotation, 310

ambient call signature, 233

ambient call signature declaration, 233

ambient class, 233–235

ambient class declaration, 232, 233

ambient constant, 230

ambient constructor, 229

ambient constructor declaration, 232

ambient context, 230, 233, 234, 236

ambient declaration, 217, 229, 282, 310

ambient field declaration, 232

ambient function, 229, 230

ambient function declaration, 230

ambient indexer, 234

ambient indexer declaration, 233

ambient interface, 234

ambient interface declaration, 234, 235

ambient iterable, 234

ambient iterable declaration, 234, 235

ambient method, 229, 232

ambient method declaration, 232

ambient namespace, 222, 235, 236

ambient namespace declaration, 235, 236

ambient overload function, 231

ambient overload function declaration, 231

AND operator, 138

annotation, 26, 35, 57–59, 147, 155, 159, 176, 188, 200,

## Page 336

217, 238, 268, 282, 301, 305–312

annotation declaration, 305–310

annotation field, 306, 307

annotation name, 308

anonymous class, 100, 102

anonymous type, 27, 55, 56

any, 24

Any type, 45

any type, 68

API, 269

arbitrary large integer, 36

arbitrary signature, 281

argument, 42, 60–64, 88, 92, 103, 104, 109, 114, 194, 227, 239, 269, 274, 281, 287, 295, 302, 304, 305, 316

argument expression, 83

argument type, 70, 177, 251, 317

arithmetic operator, 83

ArkUI code, 316

ArkUI plugin, 316

ArkUI type, 316

array, 24, 27, 32, 38, 39, 55, 58, 61, 67, 68, 71, 73, 90, 92, 95–97, 104, 111, 114, 141, 143, 158, 240, 247, 251, 271, 274–276, 306, 316

array access, 111

array access expression, 90

array argument, 63

array bounds checking, 207

array creation, 271, 276

array creation expression, 114, 275, 276

array declaration, 38, 273

array dimension, 275

array element, 32, 38, 40, 56, 81, 90, 95–97, 110, 142–144, 247, 273, 275

array element type, 90, 247

array indexing, 110

array indexing expression, 90, 110, 111, 142, 143

array initialization, 96

array initializer, 95

array instance, 37, 114, 274, 275

array length, 3, 37–39, 90, 95, 111, 142, 143, 273

array literal, 45, 47, 81, 89, 95–97, 103, 116, 117, 237, 252, 271, 273, 275, 308

array literal expression, 95

array of arrays, 276

array operation, 38

array reference expression, 90, 110, 142

array reference subexpression, 143

array size, 271

array type, 3, 23, 25, 26, 32, 37, 38, 61–63, 72, 95, 103, 110, 240, 249, 251, 271, 273, 298, 308, 311

array value, 37

assign, 238, 273

assignability, 28, 38, 40, 41, 57, 58, 62, 63, 65, 68,

73, 76, 77, 82, 96, 99, 117, 141, 142, 163, 165, 197, 238, 240, 249, 251, 273, 275, 279, 282

assignable type, 65, 73, 76, 77, 251

assignment, 33, 38–40, 42, 47, 49, 57, 61, 81, 84, 89–92, 96, 103, 113, 141–144, 159, 163, 180–182, 204, 238, 249, 263, 275, 317

assignment context, 28, 81

assignment expression, 58, 141–144

assignment operator, 57, 91, 141, 143

assignment-like context, 81, 84, 238–240

assignment-like contexts, 58

associativity, 91, 126, 130, 138, 140

asymmetric relationship, 249

async function, 75, 268, 269, 278

async lambda, 268

async mark, 147

async method, 186, 268, 279

async modifier, 186, 230, 268, 271

async type, 66

asynchronous API, 269

asynchronous launch, 271

asynchronous operation, 269

asynchronous programming, 267

automatic transition, 2

available memory, 317

await expression, 269

await operator, 91

awaited, 75

## B

backslash, 19

backslash character, 214

backspace, 19

backtick, 20, 145

backward compatibility, 268

balanced braces, 154

base, 129, 250

base class, 169, 183, 194, 207, 249, 256

base type, 84, 249, 257

base URL, 214

basic coroutine, 270

BigInt, 28

bigint, 24, 28, 29, 131

bigint comparison, 133

bigint literal, 18, 36

bigint operand, 133

bigint type, 32, 36, 83, 125, 131, 133, 135, 139

binary, 14

binary expression, 121

binary numeric expression, 239

binary operation, 143, 144

binary operator, 30, 82, 91, 126–131, 239

bind all, 54

binding, 210–213, 215, 216, 224

## Page 337

bitwise AND operand, 139

bitwise complement, 125

bitwise complement expression, 125, 126

bitwise complement operator, 29, 30, 125

bitwise exclusive OR operand, 139

bitwise expression, 83, 138, 139

bitwise inclusive OR operand, 139

bitwise logical AND operator, 132

bitwise operator, 91, 138, 150

block, 54, 60, 107, 108, 148, 154, 156, 161, 163, 164, 187, 188, 293, 294, 303

block notation, 303

block of code, 191

block scope, 54, 155, 156

block statement, 154

body, 54, 60, 185, 202

Boolean, 31

boolean, 29, 31, 49, 66, 82, 115, 246

boolean comparison, 134

Boolean literal, 18

boolean logic, 264

boolean logical expression, 139

boolean operator, 139

boolean operand, 139, 140

boolean relational operator, 134

boolean type, 28, 30, 31, 65, 125, 132, 134, 135, 138–140, 145, 155, 157, 264, 306

boolean value, 145

bound, 245

bound entity, 212, 215

bounded instance, 137

bounded object, 137

brace, 95

break, 162

bracket, 95, 110

break statement, 156, 159, 160, 162

bridge method, 254, 317

built-in annotation, 310

built-in array, 27

built-in getter, 76

built-in setter, 76

byte, 28, 29, 49, 84, 86

built-in type, 36, 38, 273

bytecode, 311

bytecode file, 311

## C

call, 63, 88, 91, 103, 107–109, 184, 194, 212, 219, 226, 260, 263, 270, 274, 280, 281, 283, 288, 289, 296, 302, 303, 310, 316

call argument, 88, 109, 251

call context, 81

call expression, 148, 280

call parameter type, 96

call method, 181

call site, 104, 260, 283, 291

collapsible class type, 280

calllable type, 233, 280, 281, 286

callback, 269

callee, 109

caller scope, 165

candidate, 260

captured by lambda, 148, 149

captured variable, 148, 149

carriage return character, 10

case sensitivity, 214

cast, 29, 31, 116

cast conversion, 118

cast expression, 48, 90, 96, 116, 117, 150, 261

cast operator, 29, 30, 91, 116

casting conversion, 4, 86, 96, 150, 254

catch clause, 163–165

chaining, 91

chaining operator, 88, 107–110, 113, 144

catch identifier, 164

char, 14, 49

char literal, 272

char type, 272

character, 3, 9, 35, 36, 272

character literal, 272

character type, 28

check, 117, 182, 251

circular dependency, 181

circular reference, 43

class, 27, 32, 40, 47, 51, 53, 67–71, 73, 74, 76, 88, 93–95, 97–99, 102, 104–108, 110, 114, 115, 135, 161, 168–173, 175–182, 184, 185, 187, 188, 190, 193–195, 197–199, 201, 207, 217, 245, 254, 256, 257, 262, 263, 271, 275, 277, 279, 280, 287–289, 291, 293–295, 297, 301, 302, 307

class accessor, 184, 188

class accessor declaration, 175, 188

class body, 167, 176–179, 192, 194

class constructor, 167, 180, 255

class declaration, 27, 55, 167, 168, 171, 176, 179, 181, 184, 195, 293, 305, 307, 316

class declaration body, 184

class declaration scope, 177

class extension, 169, 242, 293

class extension clause, 169

class field, 99, 171, 177

class fields, 180

class implementation clause, 171

class inheritance, 271

class instance, 54, 92, 97, 102, 148, 176, 177, 179–181, 191, 233, 234

class instance creation expression, 114, 115

## Page 338

class instance expression, 114

class instance method, 65

class instantiation, 191

class interface, 271

class iterator, 158

class keyword, 316

class level scope, 4, 54

class member, 53, 54, 167, 176–178, 284

class method, 172, 176, 184, 190, 232, 261, 268, 282, 284

class method declaration, 184

class method overload declaration, 291

class name, 168, 198

class type, 23, 25, 32, 43, 46, 73, 76, 77, 98, 99, 104–106, 116, 168, 169, 171, 253, 257, 276, 280, 281, 293, 298

class variable, 253

class-composite context, 99

class-level scope, 167

code readability, 252

clause, 169

closure, 240

comma, 13

comma-separated argument expression, 92

comma-separated list, 98

command-line argument, 228

comment, 2, 4, 9, 10, 21

common subset, 1

commutative operation, 126, 130

comparison operator, 29, 30

commutative operator, 134, 138

comparison, 13, 31, 133–135

compatibility, 24, 28, 36, 38, 40, 48, 68, 78, 89, 97, 109, 162, 202, 204, 213, 220, 229, 233–235, 251, 259, 263, 268, 273, 280, 282, 300

compatible code, 280

compatible expression, 89

compilation, 110, 195, 214, 275, 316

compilation environment, 214

compilation tool, 263

compile time, 23, 89, 107, 118, 150, 180, 261, 263, 275, 282, 288, 297, 306, 311

compile time error, 273

compile type, 259

compile-time error, 4

compile-time warning, 4

compile-time error, 16, 17, 33, 38–41, 43, 44, 46, 47, 52, 56, 57, 59–62, 65, 66, 69–78, 82, 88, 89, 93, 94, 96–110, 112–118, 121–125, 127–134, 136, 138–141, 144, 145, 147, 148, 155–163, 168–173, 175, 179, 181–194, 198–200, 202–204, 209–211, 214, 216–220, 223, 225, 226, 229, 230, 236–239, 250, 252, 254–257, 268, 274–276, 278–290, 292–294, 296–300, 302, 303, 305–308, 311, 316



compile-time feature, 2

compile-time polymorphism, 259

compile-time warning, 135, 229, 259

compile-time-error, 135

compiler, 23, 56, 66, 103, 112, 181, 182, 192, 213, 214, 227, 253, 254, 278, 279, 310, 315–317

compiler environment, 214

compiler-known signature, 278, 279

complement expression, 125

complement operator, 31

completion, 122, 207

completion failure, 207

compliance, 85, 86

component programming, 2

composite literal context, 81

compound assignment expression, 143

compound assignment operator, 143, 144

compound-assignment operator, 91

concatenation, 30, 31, 81, 145

concatenation operator, 36

concrete method, 186

concurrency, 267, 269, 271

concurrent execution, 263

conditional evaluation, 139

conditional expression, 125, 155, 253

conditional operator, 29, 30, 91, 150

conditional-and expression, 83, 139, 264, 265

conditional-and operator, 31, 121, 139, 150

conditional-or expression, 83, 140, 264, 265

conditional-or operator, 31, 121, 140, 150

configuration file, 214

console, 209

const, 159

const declaration, 154

const enum, 203

const enum type, 262

const keyword, 229, 235

const modifier, 203

constant, 4, 29, 30, 51, 53, 58, 81, 84, 85, 103, 162, 203–205, 217, 220, 252, 276

constant declaration, 4, 17, 58, 81, 217, 225, 230, 238, 252

constant expression, 40, 89, 116, 130, 150, 203, 204, 237, 252, 275, 306

constant field, 180

constant value, 134

constant variable, 218, 224

constant-time operation, 38, 273

constraint, 67, 68, 73, 89, 107, 239, 245, 257, 258, 262

construct, 1, 26, 271

constructed value, 77

constructor, 29, 30, 60, 62, 81, 102–104, 106, 114, 115, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 76

constructor, 29, 30, 60, 62, 81, 102–104, 106, 114, 115, 120, 161, 163, 167, 168, 176–178, 181, 191,

## Page 339

193–195, 229, 251, 254, 255, 259, 271, 273–276, 280, 282, 289, 293, 294, 301

constructor body, 115, 161, 191–195, 229

constructor call, 81, 92, 115, 191–195, 251, 255

constructor call statement, 104

constructor declaration, 181, 191, 194, 293, 294

constructor keyword, 191

constructor name, 294

constructor overload, 176

constructor overload declaration, 289, 294

constructor overloading, 271

constructor parameter, 191

constructor type, 178

contained expression, 104

container, 78

context, 12, 41, 55, 74, 81, 82, 84, 89, 95–100, 104, 105, 113, 148, 155, 183, 214, 229, 237–240, 252, 253, 255, 259, 269, 302

context-free grammar, 4

context-free grammar, 2

contiguous memory location, 38

continue statement, 156, 160

contravariance, 70, 246, 247, 249, 250, 258

contravariance pattern, 190

contravariant, 70, 257

contravariant parameter, 257

contravariant parameter type, 257

contravariant return type, 247, 257

contravariant type parameter, 262

control, 153, 188, 260

control transfer, 159–163

conversion, 31, 41, 44, 48, 61, 81–86, 96, 110, 122–125, 128, 130, 131, 133, 136, 139, 142, 143, 145, 204, 205, 249, 252, 275

converted type, 133, 136

convertibility, 123, 124, 139

convertible expression, 122

convertible type, 122–125, 130, 133, 136

core, 267

coroutine, 87, 88, 263, 267–271

coroutine stack, 165

covariance, 70, 246, 247, 249, 250, 257

covariance pattern, 190

covariant, 70

covariant parameter type, 257

covariant return type, 247, 257

covariant type parameter, 262

creation, 197

creation expression, 92

cross-platform development, 2

curly brace, 98, 145

custom synchronization, 269

cyclic dependency, 57

## D

data analysis, 267

data entity, 253

data member, 179

data race, 269

data type, 49

database, 267

deadlock, 263

deallocation, 2

decimal, 14, 18, 82

decimal form, 30

decimal number, 17

declaration, 21, 43, 51, 53–55, 57, 59, 74, 93, 158, 159, 171, 176, 177, 182–186, 188, 197, 198, 202, 211, 216–218, 220, 222–226, 229, 230, 236, 238, 249, 253, 277, 285–287, 289, 295, 297, 305–307, 310–312, 316

declaration annotation, 311

declaration body, 154

declaration name, 223

declaration scope, 52, 167, 176, 200, 211, 212, 215

declare, 229

declared class member, 167

declared entity, 52, 306

declared function, 93

declared interface, 198

declared name, 218

declared type, 104, 229, 235

declaring class, 178

decrement, 113, 150, 317

decrement expression, 122, 123

decrement operator, 29–31, 89, 91, 122, 123, 150

decrementation, 122, 123

default, 69, 99, 227

default constructor, 194, 195

default export directive, 217, 218

default implementation, 235, 294

default keyword, 211, 235

default method, 294

default target, 218

default type, 67, 69, 239

default value, 48, 57, 61, 101, 180, 182, 187, 230, 263, 274–276, 303

definite assignment assertion, 182

delimiter, 2

denormalization, 31

denormalized number, 31

denormalized value, 31

derived class, 54, 169, 178, 207, 256, 257, 271, 295, 297

derived class constructor, 255

derived interface, 295

derived type, 47, 249

difference type, 248

## Page 340

dimension expression, 275, 276

direct call expression, 104

direct extension, 197

direct implementation, 197

direct subclass, 169, 170, 263

direct subinterface, 198

direct superclass, 169, 177, 195

direct superinstance, 177

direct superinterface, 42, 171, 195, 198, 200, 202, 245

direct supertype, 240, 245

directive, 210, 223, 224

dispatch, 107, 263

distinct argument, 73

distinct generic declaration, 73

distinct type, 76, 77

distinguishable functions, 53

dividend, 127–129

division, 127, 128

division operator, 29, 127, 128

divisor, 127–129, 164

do statement, 157, 160, 264

dot operator, 54

dot-separated name, 92

double, 28, 30, 49

double infinity, 85

double NaN, 85

double quotes, 19

double type, 85

DSL support, 302

dual semantics, 35

dynamic dispatch, 107, 263, 278

dynamically created object, 2

dynamically dispatched overriding, 2

## E

effective type, 117, 261, 262

element type, 38

else-block, 156

embedded expression, 145, 146

embedded namespace, 220, 221, 236

embedded type, 74

empty body, 187, 293

empty string, 264

enclosing context, 155

enclosing statement, 160

end marker, 3

ensure-not-nullish expression, 48, 120

entity, 51, 53, 54, 63, 67, 92, 93, 173, 201, 209–212, 215, 216, 219, 224, 229, 235, 236, 252–254, 259, 260, 263, 282, 283, 290, 300, 303, 306, 308

entity declaration, 53

entry point, 227, 228

entry point function, 227, 228  

enum, 204, 217, 271  

enum constant, 203, 204  

enum declaration, 55  

enum member, 54  

enum type, 32  

enumeration, 27, 28, 169, 203, 205, 262  

enumeration base type, 204, 262  

enumeration constant, 84, 134, 203–205, 276, 277  

enumeration constant value, 134, 204  

enumeration declaration, 27, 203  

enumeration integer value, 134, 204  

enumeration method, 271, 276  

enumeration relational operator, 134  

enumeration string value, 134  

enumeration type, 23, 25, 28, 48, 82, 84, 85, 134, 135, 150, 203–205, 276, 277, 306  

enumeration type constant, 150  

enumeration type declaration, 229, 235  

environment, 165  

environment variable, 214  

equality, 35, 128, 136  

equality expression, 83, 134, 135, 137, 150  

equality operator, 29, 91, 134, 135, 137, 150, 272  

erased type, 317  

error, 29, 31, 33, 90–92, 127, 129, 131, 148, 153, 154, 163–165, 182, 195, 207, 208, 226, 275, 317  

error handling, 207  

error object, 90, 163  

error situation, 208  

escape character, 20  

escape sequence, 19, 272  

evaluation, 87–92, 95, 102, 103, 106, 109, 111, 113, 115, 116, 118, 120–123, 127, 134, 135, 139–145, 147–150, 153, 156–158, 161, 162, 180, 181, 276, 278  

evaluation result, 218  

exception, 263, 316  

exclusive OR operator, 138  

executable code, 184, 229  

execution, 90, 95, 102, 148, 153–155, 157, 160–162, 164, 165, 186, 192, 194, 207, 227, 261  

execution path, 65, 192  

execution transfer, 162  

exit condition, 160  

explicit call, 280  

explicit constructor call, 194  

explicit initialization, 48  

explicit instantiation, 67  

exponent, 129  

exponentiation, 91, 129  

export, 54, 210–212, 216–220, 223–225, 309  

export annotation, 309  

export default, 309

## Page 341

export directive, 218, 223, 224, 309

export function, 221

export keyword, 306, 309

export modifier, 217

export namespace, 222

export target, 218

export type, 213, 224, 309

exported declaration, 217, 218, 220, 223

exported entity, 51, 54, 93

expression, 3, 4, 23, 35, 54, 61, 66, 78, 81–84, 87–92, 95, 97–99, 101–104, 108–110, 113–116, 118, 120–126, 130, 132, 139–141, 143–145, 148, 150, 154–159, 161–163, 180, 184, 191, 193, 203, 204, 218, 226, 237–240, 251, 252, 264, 269, 275, 276, 280, 282, 289, 294, 295, 300, 306–308

expression evaluation, 90

expression statement, 154, 226

expression type, 66, 82, 85, 89, 90, 108, 114, 139, 162, 264

expression value, 81, 157, 162

extended conditional expression, 125, 145, 157, 264

extended equality, 137

extended exponent, 142

extended semantics, 140, 264

extends clause, 169, 198, 293

extends graph, 169, 198

extends keyword, 68

extends Object clause, 169

extension, 197–199, 214, 293

extension clause, 192, 242

## F

factory, 281

factory parameter, 281

field, 46, 51, 75, 81, 99, 100, 102, 105, 106, 110, 113, 141, 144, 167, 173, 175–177, 179–184, 188, 189, 197, 200, 201, 299, 302, 303, 308, 311

field access, 106, 113, 144, 180, 261

field access expression, 48, 105, 106, 113, 180

field annotation, 308

field declaration, 81, 177, 179, 180

field initialization, 180, 183, 310

field initializer, 168, 180–182, 192, 194

field modifier, 179

field name, 79

field overriding, 183

field type, 99, 141

field value, 182, 188

'ld with late initialization, 179, 181, 182, 192

file, 214, 315

file path, 214

file path, 214

file system, 315

filesystem, 214

final class, 168, 271, 293

final keyword, 293

final method, 187, 189, 271, 293

final modifier, 168, 169, 184–186

finally block, 164

finally clause, 163, 164

finite value, 127, 128, 131, 133

first-match algorithm, 260

fit into (v.), 4

fixed array type, 23

fixed-size array type, 4

fixed-size array, 37, 90, 240, 247, 273

fixed-size array argument, 64

fixed-size array type, 32, 64, 97, 247, 273

flexibility, 278, 295

float, 28, 30, 49, 84

float infinity, 85

float NaN, 85

float type, 85

float zero, 85

floating-point addition, 130

floating-point arithmetic, 130

floating-point calculation, 91

floating-point comparison, 133

floating-point division, 127, 128

floating-point equality test, 136

floating-point expression, 31

floating-point infinity, 85, 86

floating-point literal, 17, 237

floating-point number, 30, 31, 124

floating-point operand, 86, 128, 131, 133, 137

floating-point operation, 30, 31, 127, 128, 131

floating-point operator, 31

floating-point remainder, 129

floating-point remainder operation, 128, 129

floating-point subtraction, 131

floating-point type, 28, 30, 31, 38, 82, 84, 86, 127, 128, 131, 275

floating-point value, 31, 124, 133, 137

floating-type multiplication, 126

flush to zero, 31

folder, 214, 315

for statement, 155, 158, 160, 264

for-of loop, 158

for-of statement, 155, 158, 160, 279

for-of type annotation, 159

for-of type statement, 282

for-variable, 282

form feed, 10, 19

formal parameter, 81, 147

fractional part, 275

## Page 342

function, 27, 33, 34, 40, 51, 55, 57, 60, 62–69, 71, 73, 74, 81, 93, 96, 103, 104, 109, 136, 137, 155, 160–164, 169, 217, 220, 226, 227, 229, 230, 238, 251–254, 259, 260, 263, 270, 271, 277, 278, 282–284, 290, 292, 295, 298, 299, 301, 304, 307, 316

function body, 60, 65, 148, 161, 228–230, 268, 292

function body declaration, 54

function call, 39, 40, 48, 53, 60, 61, 65, 81, 89, 92, 108, 109, 113, 251, 261, 263, 283, 295, 297, 299, 303, 304

function call expression, 65, 108, 109

function declaration, 4, 54, 60, 147, 217, 230, 284, 295

function increment, 178

function name, 54, 277, 295

function object, 42, 137

function overload, 284

function overload declaration, 231, 284

function overloading, 271

function parameter, 57, 65

function reference, 93, 290

function return type, 66, 252

function scope, 4, 54

function signature, 40, 93

Function type, 42

function type, 23, 25, 26, 32, 40–42, 71, 72, 108, 135, 147, 148, 246, 257, 295, 298–300, 302–304, 316

function type equality operator, 137

function type parameter scope, 4, 54

function type with receiver, 25, 299–301

function types conversion, 4

function with receiver, 104, 217, 295–297, 299, 302

function with receiver declaration, 295

functional object, 109

functionality, 267, 271, 295

## G

general import, 213

generic, 2, 4, 67, 69, 73, 74, 89, 198, 249, 257, 261, 283, 300, 316

generic class, 27, 68, 70, 71, 168, 208, 245, 278, 317

generic class declaration, 171

generic declaration, 67, 68, 73, 198

generic entity, 71

generic function, 60, 68, 74, 93, 297

generic instantiation, 67, 68, 71, 73, 93, 94, 115, 198, 252, 283

generic interface, 68, 70, 171, 198, 245, 278

generic method, 74, 93, 94

generic parameter, 67

generic tuple, 262

generic type, 4, 27, 34, 35, 56, 69, 70, 73, 101, 115, 245, 249, 262

genericity, 2

get-accessor, 189, 299

getter, 76, 77, 173, 188–190, 200–202, 299

getter body, 189

getter parameter, 190

goal symbol, 2, 3, 4

gradual underflow, 31

grammar, 5

grammar production, 3

grammar rule, 3, 88



## H

hard keyword, 12

hardware, 267

header, 185

hexadecimal, 14, 19

hidden field, 173, 175

hidden member, 197

hiding, 197

high-level language, 2

high-level sequence, 192

horizontal tab, 19

horizontal tabulation, 10

host system, 315

## I

identifier, 2, 10–13, 26, 27, 51, 60, 61, 98, 99, 106, 113, 156, 160, 162, 168, 179, 184, 188, 191, 198, 201, 211, 212, 224, 284, 285

identity, 249

identity conversion, 84

IEEE 754, 30, 31, 84–86, 126–131, 133, 136

if statement, 155, 156, 253, 264

immutable variable, 155

implementation, 30, 31, 66, 136, 167, 169, 171–175, 183, 184, 186, 187, 190, 191, 197–199, 201, 202, 214, 233, 234, 236, 242, 254, 255, 271, 278, 279, 288, 291, 293–295, 310, 315

implementation clause, 242

implementation method, 187

implementing, 167

implements clause, 171

implicit conversion, 17, 145, 249

import, 54, 209, 211, 213–218, 224–226, 284, 309, 310

import annotation, 309

import binding, 210–215, 217

import declaration, 210, 215

import default, 309

import directive, 209–211, 213, 215, 217, 223, 309

import outcome, 215

import path, 210, 211, 213–215, 225, 315

import statement, 213

## Page 343

import type, 211, 213, 309

import type directive, 213

imported declaration, 209

imported entity, 93

imported file, 214

imported function, 93

imported module, 226, 309

in keyword, 70

in-place type declaration, 25

in-position, 70

in-variance, 67

inclusive OR operator, 138

incompatibility, 273

increment, 113, 150, 251, 317

increment expression, 122, 123

increment operator, 29–31, 89, 91, 122, 123, 150

incrementation, 122

index, 78, 273

index expression, 40, 78, 110–113

index parameter, 278

index subexpression, 142–144

indexable type, 38, 110, 233, 277

indexing, 36, 92, 111, 233

indexing expression, 48, 78, 92, 110–113, 142–144, 277, 278

indexing expression evaluation, 278

indistinguishable type, 249

inference, 57, 66, 302

inference type, 101

inferred type, 58, 59, 65, 66, 74, 89, 95–98, 100, 116, 125, 148, 158, 159, 189, 190, 228, 237, 239, 253, 263, 279

infinite operand, 131

infinite value, 131

infinity, 85, 91, 124, 127–129, 131, 133

infinity double, 85

inheritance, 2, 32, 176, 177, 179, 184–186, 190, 195, 197, 198, 200, 202, 254, 271, 280, 285, 286, 288, 295, 306

inherited class member, 167

inherited field, 184

inherited member, 177, 195, 197

initial value, 39, 40, 81, 102

initialization, 48, 57, 76, 77, 95, 101, 102, 114, 115, 148, 155, 158, 176, 180–183, 191, 192, 226, 229, 238, 263, 276, 310, 316

initialization expression, 97

initializer, 57, 59, 99, 150, 161, 180, 181, 183, 220, 221, 229, 232, 238, 240, 262, 306

initializer block, 106, 161, 167, 176, 177, 180, 219

initializer declaration, 232

initializer expression, 57–59, 95–97, 181, 230

innermost declaration, 54

instance, 32–34, 54, 78, 92, 97, 102, 114, 115, 135, 137, 147, 148, 158, 159, 180, 181, 186, 187, 191,



instance creation expression, 97, 148, 191

instance entity, 54

instance field, 106, 179–181, 183, 191, 192

instance field access, 106

instance field initializer, 181

instance member, 51, 53, 167

instance method, 94, 104, 105, 107–109, 186, 188, 194, 202, 255, 281, 284, 293, 297, 303

instance method call, 105

instance name, 180

instance own field, 191

instance variable, 197

instanceof, 253

instanceof expression, 115, 261, 316

instanceof operator, 115

instantiated generic type, 115

instantiation, 27, 34, 35, 67–74, 93, 114, 115, 168, 171, 180, 197, 245, 262, 280, 281

int, 16, 28, 29, 49, 84

int type, 86, 204, 227, 275

integer, 14, 16, 18, 30, 31, 36, 38, 126, 129, 130, 273, 275

integer addition, 91, 130

integer arithmetic, 130

integer bitwise operator, 29, 30, 139

integer conversion, 252

integer division, 90, 91, 127, 132

integer equality test, 136

integer expression, 228

integer literal, 16, 204, 237, 239

integer multiplication, 91, 126

integer number, 273

integer operand, 127, 128, 133, 137

integer operator, 29

integer overflow, 127

integer remainder, 90, 91, 128

integer subtraction, 131

integer type, 28, 29, 82, 84, 86, 110, 111, 125, 131, 139, 203, 204, 252, 264, 275

integer value, 18, 29, 124, 127, 131, 203, 204, 275

interface, 27, 32, 51, 54, 67, 68, 70, 71, 73, 74, 93, 94, 100–102, 104, 106, 107, 169, 171, 173, 175, 176, 182, 183, 186, 187, 190, 197–202, 217, 234, 245, 255, 256, 263, 271, 277–279, 287, 288, 291, 294, 295, 302, 306, 307

interface body, 202, 294

interface declaration, 27, 55, 197, 198, 200

interface field, 81

interface inheritance, 202

interface keyword, 306

interface level scope, 5, 54

interface member, 53, 54, 200

## Page 344

interface method, 172, 190, 202, 235, 282, 288

interface method declaration, 202, 294

interface name, 198

interface property, 101, 200–202

interface type, 23, 25, 27, 29, 32, 43, 46, 47, 51, 73, 76, 77, 98, 100, 101, 104, 116, 171, 197, 198, 200, 242, 253, 257, 296, 298

interface type declaration, 245

interface type variable, 51

intersection type, 248

invariance, 70, 249, 250, 257

invariant, 70

invariant type parameter, 262

invocation, 263, 280, 281

iterable class, 158, 279, 280

iterable class instance, 234

iterable interface, 158, 279

iterable type, 158, 159, 279, 286

iteration, 158–160

iterator, 159, 279, 280

## K

key, 78, 101, 112, 113, 142, 144  

key type, 101, 102, 112  

key-value pair, 142, 144  

keyof keyword, 47  

keyof type, 47  

keyword, 2, 5, 10, 12, 13, 18, 21  

keyword null, 35  

keyword super, 54  

keyword this, 54  

keyword undefined, 35

## L

label, 156, 160

label identifier, 160

lambda, 34, 42, 62, 65, 66, 92, 148, 149, 156, 247, 270, 299, 301–304

lambda body, 105, 147, 148, 161, 302, 303

lambda call, 81, 148

lambda code, 253

lambda expression, 65, 92, 104, 108, 147–149, 156, 252, 268, 271, 295, 301, 307

lambda expression call, 148

lambda expression type, 148

lambda expression with receiver, 87, 88, 295, 301–303, 307

lambda function, 275

lambda parameter, 148, 302

lambda receiver type, 302

lambda return type, 148

lambda signature, 147, 148, 302

lambda with receiver, 298, 299

lambda with receiver body, 302

language element, 305

late initialization, 182

launch function, 271

lazy operator, 121

left shift, 132

length property, 273

let, 159

let declaration, 154

lexical element, 2

lexical grammar, 2, 3

lexical input, 9, 10

lexical input element, 10

lexical notation, 2

lexical structure, 2

line separator, 2, 9, 10, 21, 305

line separator character, 10

linearization, 5, 45

linkage, 90

literal, 5, 10, 14, 16, 18, 20, 35, 36, 78, 89, 92, 96, 102, 112, 113, 150

literal expression, 97

literal type, 20, 23, 25, 32, 36, 37, 44, 45, 48, 59, 102, 112, 245, 262

literal value, 18, 44

local declaration, 154, 307

local variable, 84, 253

logical complement, 125, 264

logical complement expression, 125

logical complement operator, 125

logical expression, 83, 138, 139

logical operator, 31, 91, 138, 139, 150

long, 16, 28, 29, 49, 84

long type, 36, 86, 204

lookup sequence, 315

loop, 156, 158–160, 265

loop body, 156, 159

loop index variable, 158

loop iteration, 158, 160

loop label, 156

loop scope, 159

loop statement, 156, 159, 160, 162

loss of information, 30, 82, 127, 128, 131

loss of precision, 129

low-level representation, 2

low-order bit, 126, 130

lowest-order bit, 132

lvalue, 89

## M

magnitude, 128, 129, 131

maintainability, 2

managed overloading, 259, 260, 271, 282

mandatory call, 192

mandatory parameter, 41

## Page 345

mapped value, 113

mask value, 132

match (v.), 5

member, 53, 176, 177, 186, 197

member access, 91

member field, 106

memory location, 38, 273

meta-annotation, 310, 311

metadata, 305, 311

metasymbol, 3, 5

method, 5, 29, 30, 32–34, 36, 38, 42, 46, 51, 54, 57, 60

62, 64–68, 71, 73–77, 81, 88, 93, 94, 101, 103

107, 108, 110, 115, 155, 160, 161, 163, 167

171, 172, 176–180, 184–191, 197, 199, 200

202, 205, 229, 235, 250–254, 256, 257, 259

263, 269, 271, 277, 279–282, 284, 286–288

291–293, 295, 297, 302–304, 307, 316, 317

method body, 65, 66, 104, 148, 161, 169, 186, 187, 193

202, 229, 279, 293, 294

method body declaration, 54

method call, 39, 40, 48, 60, 61, 81, 82, 89, 92, 107, 108, 113, 163, 184, 232, 251, 261, 263, 280, 295, 299, 300, 303, 304, 316

method call expression, 65, 92, 107, 108, 115, 184, 263, 295

method declaration, 169, 172, 177, 184–187, 191, 200, 268, 282, 293, 294

method member, 177

method modifier, 108, 184, 189, 285

method name, 54, 184, 202, 291

method overload, 176, 261, 284

method overload declaration, 284, 285, 288

method overload signature, 256

method overloading, 271

method overriding, 254, 271

method parameter, 57, 65

method parameter name, 54

method reference, 93, 94, 137, 291

method return type, 66, 108, 252

method scope, 5, 54

method signature, 94, 186, 188, 202, 254

migration, 2

mode of evaluation, 153

modelling, 267

modification, 159

modifier, 54, 159, 168, 169, 180, 182, 185, 187, 211

modifier async, 230, 271

modifier const, 159

modifier declare, 229

modifier export, 218

modifier let, 159

modifier static, 180

modularity, 2

module, 2, 53, 54, 74, 93, 150, 209–211, 213–215, 217, 220, 222–227, 229, 236, 262, 263, 284, 297, 315, 316

module initialization, 316

module level scope, 5, 53

multiline comment, 21

multiline string, 18, 20, 145, 146

multiline string literal, 20

multimedia processing, 267

multiplication, 126, 127, 132

multiplication operator, 127

multiplicative expression, 30, 83, 125, 150

multiplicative operator, 29, 30, 125, 150

multitargeting, 2

mutable variable, 155

## N

name, 51–57, 60, 65, 93, 205, 211, 212, 215–217, 256, 259, 277, 280, 286, 289–291, 294, 297, 305

name binding, 213

name-value pair, 98, 99, 102

named class, 102

named constant, 203

named constructor, 93

named entity, 52

named function, 60

named reference, 92–94, 263, 294

named store location, 57

named type, 25, 27

named variable, 144

namespace, 53, 93, 217, 219–222, 235, 262, 263, 282, 284

namespace declaration, 53, 217, 219, 236, 262

namespace level scope, 53

namespace name, 220, 236

namespace scope, 284

namespace variable, 219

NaN, 31, 86, 124, 127–129, 131, 133, 135, 137, 265

Nan, 85

NaN value, 91

narrowed type, 253

narrowing, 252, 253

narrowing conversion, 5

native, 286

native constructor, 191, 293

native function, 60, 66, 268, 271, 292

native keyword, 292, 293

native method, 187, 271, 292, 293

native modifier, 186, 189

nearest value, 31

negation, 124, 131

negative infinity, 86, 133, 137

negative integer, 127, 128

negative integer value, 275

## Page 346

negative zero, 131, 133, 137  

nested literal, 95  

nested loop, 276  

nested multiline string, 146  

nested namespace, 236  

nested statement, 54, 162  

nested union type, 45  

never, 24  

never type, 32, 33, 45, 47, 65, 66, 116  

new expression, 280  

newline character, 10  

no-argument return statement, 268  

no-break space, 10  

non-generic, 5  

non-generic type, 5  

non-abstract class, 168, 169  

non-abstract instance method, 186  

non-abstract method, 186  

non-abstract subclass, 186  

non-alias, 45  

non-aliased type, 28  

non-ambient declaration, 230  

non-ambient interface, 235  

non-ambient method, 232  

non-boolean type, 264  

non-class type, 169  

non-compatible signature, 256  

non-empty body, 293  

non-empty string, 264  

non-exported declaration, 220  

non-generic class, 73, 242  

non-generic entity, 71  

non-generic function, 73  

non-generic interface, 73  

non-generic method, 73  

non-generic type, 27  

non-generic type alias, 73  

non-initialized variable, 57  

non-interface type, 198  

non-native constructor, 191  

non-negative integer number, 38  

non-nullish type, 45, 47, 106, 113, 121  

non-nullish variant, 120  

non-nullish-type, 68  

non-numeric type, 111  

non-optional field, 175  

non-optional parameter, 104  

non-optional property, 101  

non-relative import path, 214  

non-relative path, 214  

non-standalone expression, 89  

non-static class, 171, 177  

non-static entity, 176  

non-static field, 168, 179–181, 190, 194

non-static field declaration, 181

non-static member, 176

non-static method, 186

non-static modifier, 182, 292

non-string operand, 82, 239

non-union type, 45

nonterminal, 2, 3, 5

nonterminal symbol, 3, 5

nonzero, 264

nonzero double, 85

nonzero operand, 131

nonzero value, 31

normal completion, 90–92, 102, 111, 113, 123, 124, 141–144, 148, 150, 153, 163–165, 187, 207

normal execution, 207

normal method call, 280

normalization, 43, 45, 66

normalized union type, 45

notation, 61, 177, 180, 201, 221, 303, 308, 309, 311

notion, 182

null, 24, 26, 49, 113, 120, 137, 253

null expression, 162

null literal, 20, 35

null pointer dereferencing, 207

null reference, 20

null safety, 47

null type, 32, 35, 36, 75, 245

null-coalescing operator, 91

nullable array, 26

nullable reference type, 48

nullable type, 5, 47

nullish expression, 265

nullish object reference, 106

nullish type, 20, 35, 47, 48, 82, 108, 110, 113, 120, 121, 181, 264

nullish value, 6, 47, 48, 107, 109, 110, 113, 120, 121

nullish-coalescing assignment, 143

nullish-coalescing expression, 48, 121

nullish-coalescing operator, 121

nullish-safe option, 47, 48

nullish-type, 68

number, 2, 18, 49, 78, 264, 275, 291, 292

number type, 28, 30, 246

numeric base type, 84

numeric casting, 122

numeric casting conversion, 85, 86, 122

numeric constant expression, 203

numeric context, 83

numeric conversion, 83, 84, 86, 135, 136

numeric equality, 136, 137

numeric equality operator, 29, 30, 135, 136

numeric expression, 265

numeric literal, 2, 230

numeric literal type, 45

## Page 347

numeric_operation, 130

numeric_operation, 31

numeric_operator, 29, 30, 81, 239, 240

numeric_operator_context, 239

numeric_promotion, 29–31

numeric_relational_operator, 29, 30, 133, 134

numeric_type, 28–31, 36, 45, 78, 83–85, 97, 110, 116, 122, 124, 125, 127–131, 133, 136, 138, 139, 204, 239, 306

numeric_type_operand, 131

numeric_types_conversion, 31, 83, 110, 122, 124, 125, 127, 128, 130, 133, 136, 139

numeric_value, 84, 86, 135

numeric_widening, 124

numeric_widening_conversion, 130

Object, 24, 28, 164, 169, 177, 194, 197, 198, 200, 242, 245, 251

object, 2, 32, 35, 38, 40, 58, 68, 89, 105, 106, 114, 130, 162, 186, 191, 197, 199, 240, 275, 279, 293, 317

object_field, 192

Object_literal, 252

object_literal, 76–78, 81, 97–102, 104, 116, 237, 307, 308

object_literal_expression, 98

object_orientation, 2

object_reference, 105–107, 261, 286, 288, 295

object_reference_expression, 106, 110, 111, 113

object_reference_subexpression, 144

Object_type, 45

object_type, 254

object-oriented, 2

object-oriented_programming (OOP), 263, 271

octal, 14

OOP (object-oriented_programming), 2, 271

operand, 6, 29–31, 82, 83, 86, 91, 115, 116, 122, 124–137, 139–145, 237, 239, 272

operand_expression, 126, 130, 138, 144, 145

operand_null, 82

operand_string, 130

operand_type, 132, 237

operand_value, 124–126, 130, 139

operation, 6, 30, 36, 124, 130, 261, 263, 317

operation_overflow, 131

operation_sign, 6

operation_type, 37

operational_function, 304

operator, 10, 13, 20, 29, 30, 38, 40, 90, 91, 110, 115, 118, 120, 121, 123–125, 128, 130, 132–134, 136, 138, 141, 162, 251

operator_in_programming_languages), 6

operator_context, 130

evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation_evaluation

operator evaluation, 90

operator precedence, 91

operator sign, 2

operator undefined, 82

operator validity test, 28

optional annotation, 147

optional arbitrary code, 192

optional argument, 304

optional field, 175, 179, 180, 182

optional identifier, 191

optional name, 191

optional parameter, 41, 60, 61, 63, 147, 189, 230, 246, 275, 303, 304, 307

optional property, 76, 101, 200–202

ordinary function, 278

ordinary method, 279, 286, 288, 317

original variable, 149

out keyword, 70

out-variance, 67

overflow, 29, 31, 124, 126–132

overlap, 54

overlapping, 135

overload, 176, 217, 232, 283, 285, 286, 291

overload alias, 94, 212, 282–286, 288–292

overload alias name, 291

overload declaration, 107, 109, 176, 212, 217, 259–261, 271, 282–291, 294

overload keyword, 282

overload resolution, 107, 109, 261, 283

overload set, 283

overload signature, 187, 202, 217, 256, 259, 260, 282, 284, 285

overloaded constructor, 289

overloaded entity, 282, 283, 291

overloaded function, 212, 284, 286, 290

overloaded interface, 287

overloaded method, 285–288, 291, 292

overloading, 6, 227, 240, 254, 259, 282, 317

overloading signature, 184

overridden field, 183

overridden member, 197

overridden method, 188, 291, 293, 317

override, 183, 184, 288

override compatibility, 257, 258

override keyword, 182

override method, 250

override modifier, 169, 185, 187

override-compatibility, 254–256

override-compatible, 256

override-compatible signature, 172, 190, 195, 199, 202, 249, 254–257

overriding, 2, 88, 167, 172, 182–184, 186–188, 190, 195, 197, 202, 239, 240, 245, 250, 254–256, 258, 259, 278, 286, 291, 293, 294, 317

overriding entity, 249

## Page 348

overriding field, 182–184

overriding method, 187, 189, 317

own (adj.), 6

own field, 179

## P

paragraph separator character, 10

parallel-run coroutine, 267

parameter, 33, 60, 65, 93, 104, 105, 109, 148, 188, 189, 194, 201, 227, 230, 246, 247, 249, 251, 253, 257, 258, 263, 275, 281, 295, 296, 299, 301, 303, 304, 307, 316

parameter constraint, 239

parameter declaration, 147

parameter list, 40, 60, 62

parameter name, 41, 54, 60, 62, 300

parameter type, 41, 61, 190, 246, 247, 250, 252, 259, 262

parameter with default value, 61

parameterization, 67, 68, 73

parameterized class type, 171

parameterized declaration, 73

parameterized interface, 198

parameterized type, 198

parameterless constructor, 99, 102, 275, 276

parameterless function type, 281

parameterless method, 279

parent class, 254

parenthesis, 13, 26, 91, 92, 115, 142, 308

parenthesized expression, 104, 150

path, 207, 315

path component, 214

path mapping, 214

path rule, 214

pattern, 88

performance, 267

permutation, 249

platform API, 235

platform-dependent code, 293

point of declaration, 54, 263

policy, 311

polymorphism, 282

polymorphism by name, 259, 282

positive infinity, 86, 133, 137

positive zero, 131, 133, 137

postfix, 29, 30, 113, 120, 122

postfix operator, 91

precedence, 26, 54, 91, 134

predefined constant, 29, 31, 272

predefined constructor, 29, 31, 272

predefined method, 29, 31, 272

predefined numeric types conversion, 29–31, 125, 133

predefined operator, 90

predefined reference type, 18

predefined type, 23, 24, 27, 28, 42, 44, 83, 123

predefined type declaration, 47

predefined value type, 143, 150

prefix, 16, 17, 29, 30, 40, 62–64, 113, 120, 123, 150, 229, 235, 302, 305, 306

prefix operator, 91

prefix readonly, 26, 39, 60, 61

primary constructor, 191–193

primary expression, 105, 110, 113

primary name, 24

primitive type, 317

primitive type operation, 317

primordial class, 194

private, 177, 178, 195, 285, 286

private field, 79, 173, 175, 190

private member, 169, 178, 296

private method, 170, 202, 254–256, 294

private modifier, 186

production, 2, 3, 6

program completion, 270

program entity, 2, 67

program entry point, 226, 227

promise, 75

promise object, 269

promoted operand value, 124

promoted type, 130, 132

promoted value, 124

promoting, 130

promotion, 124, 125, 132

propagation, 165

property, 42, 76, 77, 100, 101, 173–175, 179, 197, 200–202, 308

property length, 38

property type, 200

protected, 177, 178, 285

protected member, 296

protected modifier, 178

provably distinct instantiation, 73

proxy, 269

pseudogeneric static method, 316

public, 177, 178, 255, 285, 286

public member, 296

public method, 200

public modifier, 178, 194

punctuator, 6, 10, 13

## Q

qualification, 179, 203, 269

qualified access, 51, 54

qualified form, 210

qualified import, 53

qualified name, 6, 51, 53, 92, 93, 109, 176, 177, 179, 180, 211, 216, 219, 221, 284, 309

## Page 349

qualified type name, 27, 29

qualifier, 219

## R

radix, 14, 17, 18

re-assignment, 47

re-export, 223–225

re-export declaration, 225

re-export directive, 209, 225

re-exported declaration, 225

re-exporting declaration, 223

read permission, 207

readability, 17, 18, 303

readonly, 40, 45, 70, 90, 97, 106, 173, 174, 180, 193, 201, 202

readonly array, 141, 142

readonly array type, 39

readonly field, 102, 106, 174, 180, 183, 311

readonly modifier, 180

readonly name, 312

readonly parameter, 61

readonly tuple, 141, 142

readonly type, 26, 77

reassignment, 77

receiver, 253, 295, 297

receiver body, 302

receiver parameter, 298, 299, 303

receiver type, 296–299, 302, 303

record, 110

record access expression, 142, 144

record element, 144

record indexing expression, 93, 113, 142, 144

record instance, 113, 142, 144

Record type, 78

record type, 101, 110, 112, 116

record utility type, 78

recursive reference, 56

recursive replacement, 28

reference, 32, 197

reference expression, 110, 111

reference subexpression, 142

reference type, 32, 35, 36, 40, 43, 47, 48, 51, 82, 106, 110, 113, 142, 143, 167, 168, 197

reflexive closure, 240

rejected promise, 270

rejection handler, 270

relational expression, 83, 132

relational operator, 31, 35, 91, 132, 134, 150

relative import path, 214

relative location, 214

relative path, 214

remainder operation, 128, 129

remainder operator, 29, 31, 90, 128, 129

renaming, 223, 309

repeatable annotation, 308

replacement, 28

required parameter, 60

required property, 77, 200, 201

reserved word, 12

sidable array, 38, 92, 114, 240, 273, 275

sidable array type, 6, 37, 38

resolution, 136, 214, 269

resolution process, 260

resolving, 214

rest parameter, 41, 60, 62–64, 104, 246, 251

restriction, 78, 112, 181, 233, 234

retention annotation, 311

retention policy, 311

return, 33, 154, 164

return expression, 161

return statement, 65, 66, 148, 154, 161, 187, 193, 226, 227, 268

return type, 33, 34, 40, 60, 65, 66, 108, 109, 147, 148, 154, 161, 177, 187–191, 201, 227, 230, 234, 246, 252, 257, 258, 268, 279, 299

right shift, 132

root coroutine, 269

round to nearest, 31

round toward zero, 31

round-to-nearest mode, 84, 127, 128, 131

round-toward-zero, 86

rounding, 84, 127, 128, 131

rounding mode, 31

rounding rule, 85, 86

rounding rules, 86

rounding toward zero, 31

routine, 128, 262

runtime, 36, 38, 47, 90, 103, 105, 106, 111, 116, 117, 122, 123, 125, 130, 132, 135, 139–143, 148, 149, 164, 165, 180–182, 254, 263, 271, 273, 276, 311, 316

runtime check, 117, 247

runtime error, 42, 84–86, 90, 110, 116–118, 207, 235, 273, 275, 310

runtime evaluation, 148, 263, 276

runtime expression, 271

runtime implementation, 316

runtime polymorphism, 254

runtime system, 208, 247

runtime type, 263

## S

safe field access, 48, 106

safe function call, 48

safe indexing expression, 48

safe method call, 48, 107

safe operation, 48

safety, 263

## Page 350

scope, 51, 53–55, 67, 147, 156, 165, 167, 168, 176, 198, 200, 211, 215, 216, 225, 263, 284, 303

scope of a name, 6

secondary constructor, 191, 193

selective binding, 212, 223

selective export, 223

selective export directive, 223

selective import, 211

semantic check, 108, 109, 115, 195, 202, 213, 224, 251, 253, 255, 256

semantic correctness check, 109

semantic equivalent, 200

semantic rule, 237, 239

semantic term, 237

semantics, 47, 135, 137, 140, 180, 191, 193, 203, 226, 231, 232, 239, 240, 257, 261, 264, 265, 269, 282, 283, 305, 310

semi-automatic transition, 2

semicolon, 13, 21, 187, 293, 303

separator, 3, 51, 145, 303

sequence, 3, 35

set, 260

set of functions, 284

set of methods, 284

set of values, 272

set-accessor, 189, 299

setter, 76, 77, 100, 144, 173, 174, 188–190, 200–202, 299

setter parameter, 190

shadow, 184

shadow parameter, 147

shadowing, 65, 147, 185, 195, 197, 198

shift expression, 30, 83, 131, 132, 150

shift operation, 132

shared memory, 267

shift distance, 131, 132

shift, 131, 132

side effect, 89, 126, 130, 134, 138–140

sign-extension, 132

shortcut notation, 221

shift operator, 91, 131, 150

short, 28, 29, 49, 84, 86

signature, 40, 46, 52, 60, 186–188, 202, 228, 249, 254, 256, 257, 259–261, 277–279, 281, 283, 287, 299, 317

signature resolution, 260

signed infinity, 31, 127, 128, 131

simple assignment operator, 91, 141

signed zero, 31

signed integer comparison, 133

simple name, 7, 51, 53, 92, 93, 212, 216, 303

signed shift operator, 29, 30

signed right shift, 131

simple type name, 27, 29

simulation, 267

single quote, 19, 272

slash character, 214

smart cast, 115, 118, 253, 261

smart compiler, 252

smart type, 252–254, 261

smart typing, 253

soft keyword, 12, 13

source, 214, 311

source code, 10, 23, 317

source file, 315

source-level compatibility, 203

space, 10, 305

space allocation, 276

special character, 2

specified type, 263

state, 28, 32

spread, 104

standard library, 30, 38, 128, 207–209, 216

spread expression, 63, 64, 88, 103, 251

spread operator, 62–64, 251

standard annotation, 310, 311

square bracket, 13, 40

statement, 21, 90, 153–158, 160, 161, 163, 165, 225–227

standalone expression, 89, 145, 237–239

statement execution, 153

static, 180

static block, 176, 177, 262

static class, 171

static data member, 179

static dispatch, 263, 297

static entity, 54, 176

static field, 106, 179, 180, 262, 263

static field access, 106

static initialization, 219, 262, 263, 316

static initializer, 268

static keyword, 293

static member, 7, 51, 53, 54, 88, 167, 176, 177

static member declaration, 54

static method, 36, 94, 107–109, 184–186, 189, 276, 280, 281, 284, 316

static method call, 108

static modifier, 182, 185–187, 292

static overload alias, 285

static override field, 183

static type, 65, 253, 254

statically typed language, 23

sting concatenation, 130

sting literal, 316

sting type, 130

storage, 211, 225, 315

storage management, 2, 315

## Page 351

string, 18, 24, 26, 28–32, 35–37, 42, 45, 66, 73, 81, 89, 110–113, 130, 135, 143, 145, 158, 162, 173, 201, 220, 246, 251, 262, 264, 278, 291, 292, 299, 304

string comparison, 133

string concatenation, 30, 36, 130, 143, 239

string concatenation operator, 29–31, 145, 146

string context, 82, 83

string conversion, 82, 83, 130, 239

string element, 111

string indexing, 111

string interpolation, 20

string interpolation expression, 145

string length, 111

string literal, 18–20, 35, 36, 145, 214, 230, 245, 311

string literal type, 78, 135

string object, 36, 130

string operand, 82

string operator, 239, 240

string operator context, 239

string relational operator, 133, 134

string type, 32, 36, 78, 82, 85, 111, 113, 118, 130, 135, 145, 150, 203–205, 227, 239, 245, 278, 306, 311

string value, 36, 111, 133, 134, 205

strong typing, 252

struct keyword, 316

structured concurrency, 267

structured coroutine, 270

structuring rule, 3

subclass, 105, 168–170, 177, 187, 188, 208, 240, 254, 255, 263, 286, 291, 293, 317

subclasssubinterface, 242

subcomponent (derived component, child component), 7

subexpression, 90, 110, 142, 143

subinterface, 171, 177, 198, 240, 254, 256, 288

subset, 189, 214

substitution, 171, 198

subtraction, 13, 122–124, 131

subtype, 32, 68, 73, 90, 115, 117, 239, 240, 242, 245–250, 257, 259, 269, 279

subtyping, 37, 41, 45, 59, 68, 70, 105, 115, 239, 240, 245–249, 257, 279, 300

super, 88, 181, 192, 195

super call, 255

super keyword, 148, 180, 185, 194

superclass, 88, 99, 105–107, 167–169, 171, 179, 180, 182–184, 187, 193–195, 197, 240, 242, 245, 254, 255, 257, 286, 291

superclass constructor, 183, 194

superclass constructor call, 194

superclass property, 106

supercomponent (base component, parent component),

7

superconstructor, 192

superinstance, 177

superinterface, 167, 171–173, 175, 179, 182–184, 195, 197, 198, 202, 240, 242, 245, 254, 256, 257, 288

supertype, 34, 37, 48, 59, 97, 240, 242, 245, 247, 250, 254, 259, 261

surrounding class, 302

surrounding context, 252

surrounding function, 155, 160, 161

surrounding interface, 302

surrounding method, 155, 160, 161

surrounding scope, 165

surrounding type, 148

switch expression, 161, 162

switch statement, 159–162

sybtyping, 117

synchronization, 263, 267

syntactic grammar, 3, 10, 21

syntactic notation, 2

syntactic structure, 2

syntactical form, 114

syntax, 1, 38–41, 62, 65, 67, 68, 88, 92, 95, 102–105, 107, 108, 114, 115, 118, 125, 130–132, 134, 138–141, 145, 150, 154–164, 169, 171, 176, 179, 184, 191, 197, 200, 202, 203, 209, 210, 213, 217, 219, 223–225, 229–235, 269, 272, 275, 284, 288, 289, 294, 299, 301–303, 306–308, 310

syntax production, 21

## T

target type, 82, 83, 85, 86, 89, 90, 116, 117, 237, 239, 261

template, 2

terminal, 3, 7

termination, 161

terminal symbol, 3, 7, 9, 10

ternary conditional expression, 31, 145, 264

ternary conditional operator, 29–31, 145, 150

ternary operator, 91

then-block, 156

third-party library API, 235

this, 181, 192, 302

this keyword, 65, 104, 105, 148, 180, 185, 186, 188, 192, 194, 295, 296, 299, 301, 302

this method, 181

this statement, 188

throw, 31, 33

throw statement, 163, 208

thrown object, 163

thrown value, 163

token, 2, 7, 9, 10, 13, 51

tokenization, 7, 10

## Page 352

top-level declaration, 209, 217, 218, 223, 236, 295, 299, 307

top-level function, 316

top-level overload declaration, 290

top-level statement, 60, 161, 209, 222, 225–227, 236, 262

top-level statements, 227

top-level type, 217

top-level variable, 65, 217

trailing comma, 95, 98

trailing lambda, 107, 302–304

trailing lambda call, 107, 108

transitive closure, 170, 198, 240

traversing, 279

treemap, 214

truncated number, 31

truncation, 31, 36, 125, 128, 131, 132, 139

truthiness, 264

try block, 163, 165

try statement, 163, 165, 208

try-catch, 164

tuple, 40, 95, 97, 104, 141, 251

tuple argument, 63

tuple type, 23, 25, 26, 40, 61–63, 72, 103, 240, 249, 262

two's-complement format, 126, 130

two's-complement integer, 132

two's-complement representation, 124

two's-complement value, 124

type, 24, 28, 44, 49, 51, 58–60, 63, 73, 76–79, 81, 89, 90, 92, 96, 97, 99, 104, 107, 110–113, 115, 117, 120–122, 132, 135, 155, 157, 158, 163, 169, 171, 176, 182, 188, 204, 205, 211, 224, 237–240, 245–247, 249, 252, 253, 257, 261–263, 275, 277, 278, 281, 288, 295, 298, 306, 307, 309, 310, 316

type alias, 25, 27–29, 38, 41, 45, 55, 56, 67, 68, 71, 73, 249, 306

type alias declaration, 27, 56, 249

type annotation, 34–36, 57–59, 65, 89, 96, 108, 109, 147, 201, 230, 252, 282

type argument, 27, 29, 34, 35, 56, 68, 69, 71–74, 93, 94, 171, 198, 262, 283, 316

type boolean, 138

type call expression, 280, 281

type cast, 115

type char, 272

type checking, 259

type declaration, 23, 40, 43, 47, 55, 85, 154, 217, 226

type enum, 203

type enumeration, 204

type erasure, 115, 117, 261, 262, 316, 317

type for annotation field, 306

type identity, 38, 249

type in parentheses, 25

type inference, 23, 45, 47, 58, 59, 65, 66, 74, 81, 89, 95–100, 116, 125, 147, 148, 189, 190, 238–240, 252, 279

type instantiation, 69

type int, 83, 84, 203, 275

type Iterator, 279

type mapping, 261, 262

type modifier, 211, 213

type name, 27, 29, 36, 115, 280

type null, 20

type of expression, 237

type parameter, 23, 25, 27, 32, 34, 48, 54, 56, 60, 67–71, 73, 107, 115, 120, 147, 177, 239, 245, 249, 257, 258, 262, 276, 283, 296, 298, 317

type parameter declaration, 27

type parameter scope, 7

type parameterized entity, 2

type preservation, 262

type property, 101

type readonly, 77

type reference, 7, 25, 27–29, 68, 115

type safety, 45, 247, 252

type string, 35, 204

type structure, 26

type undefined, 21

type void, 65

type-safe call, 317

typed catch clause, 163

typeof expression, 118

typeof operator, 91

types conversion, 139

## U

unary bitwise complement expression, 125  

unary expression, 83, 122  

unary logical complement expression, 125  

unary minus, 124, 150  

unary minus operator, 30  

unary negation operation, 124  

unary numeric expression, 239  

unary numeric promotion, 124  

unary operator, 29, 30, 91, 122, 124, 125, 150  

unary plus, 124, 150  

unary plus expression, 124  

unary plus operator, 30, 124  

undefined, 24, 61, 109, 113, 120, 137, 180  

undefined literal, 21, 35  

undefined type, 32, 34–36, 41, 48, 49, 75, 245  

undefined value, 47, 101  

underflow, 29, 31, 127–129, 131  

underscore character, 16–18  

unhandled promise, 270

## Page 353

unhandled rejection, 270

Unicode character, 9, 11

Unicode code point, 9, 11, 272

Unicode code unit, 35

Unicode escape sequence, 19

Unicode input character, 10

Unicode Standard, 11

uninitialized field, 181

union, 32, 43, 44, 71, 107, 169, 279

union component type, 98

union type, 23, 25–27, 32, 43–45, 47, 55, 66, 72, 78, 97, 98, 101, 102, 112, 120, 121, 136, 246, 249, 253, 258, 264

union type normalization, 68, 97, 145, 246

unqualified form, 210

unqualified identifier, 67

unqualified import, 309

unqualified name, 51, 53

unsigned right shift, 131

unsigned shift operator, 29, 30

user-defined entity, 74

user-defined getter, 76

user-defined setter, 76

user-defined type, 23, 25, 28, 47, 203

user-defined type declaration, 47

utility type, 67, 74, 75, 77–79, 101, 110, 112, 116, 169

## V

value, 13, 16, 23, 24, 28, 30, 33–36, 38, 40, 42–44, 54, 57, 58, 78, 81, 84, 85, 89–92, 95, 99, 101–105, 111–113, 116, 118, 122–126, 128, 132–135, 137, 141–144, 163, 180, 188, 192, 193, 197, 202–205, 218, 230, 249, 252, 263, 272, 274, 276, 277, 306–308, 311, 316

value equality, 136, 137, 272

value equality operator, 272

value name, 36

value set, 131, 142

value set conversion, 124

value type, 28, 36, 45, 78, 101, 150, 264, 316

variable, 7, 28, 32, 33, 37, 38, 48, 51, 53, 57, 58, 76–78, 81, 84, 88, 89, 91, 93, 96, 97, 106, 110, 111, 122–126, 141–144, 149, 158, 159, 197, 217, 220, 238, 253, 262, 263, 277, 282, 316

variable declaration, 7, 57, 81, 96, 179, 217, 225, 252

variance, 67, 70, 71, 245, 249, 250

variance interleaving, 71

variance modifier, 70, 71

vertical tab, 19

virtual machine, 90

void, 24

void type, 32, 34, 65, 66, 161, 227

## Z

## W

well-formed instantiation, 73

well-formed parameterized type, 198

while statement, 157, 160, 264

white space, 2, 7, 9, 10, 305

widening, 29, 31, 84, 136, 239

widening conversion, 7, 110, 136

widening numeric conversion, 83, 125, 127, 128, 130, 136, 139

zero-extension, 132

zero-width joiner, 11

zero-width no-break space, 10

zero-width non-joiner, 11
