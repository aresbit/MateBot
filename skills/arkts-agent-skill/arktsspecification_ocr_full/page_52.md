let tuple : [number, string] = [1, ""]
for (let index = 0; index < tuple.length; index++) { // compile-time error
    // no 'length' property
    let element: Object = tuple[index]
    // do something with the element
}

Any tuple type is assignable (see Assignability) to class Object (see Type Object).

An empty tuple is a corner case. It is only added to support TypeScript compatibility:

let empty: [] = [] // empty tuple with no elements in it

#### 3.18.1 Readonly Tuple Types

If an tuple type has the prefix  $ \underline{\text{are}} $  $ \underline{\text{are}} $  $ \underline{\text{are}} $  $ \underline{\text{are}} $  $ \underline

let x: readonly [number, string] = [1, "abc"]
x[0] = 42 // compile-time error as tuple itself is readonly

### 3.19 Function Types

Function type can be used to express the expected signature of a function. A function type consists of the following:

• Optional type parameters;

• List of parameters (which can be empty);

• Optional return type.

The syntax of function type is as follows:

functionType:
    '(' ftParameterList? ')' ftReturnType
;
ftParameterList:
    ftParameter (',' ftParameter)* (',' ftRestParameter)?
    | ftRestParameter
;
ftParameter:
    identifier ('？')？ '：' type
;
ftRestParameter:

(continues on next page)
