(continued from previous page)

10

X++ // 'x' refers to the global variable

#### 4.7.7 Return Type

Function, method, or lambda return type defines the resultant type of the function, method, or lambda execution (see Function Call Expression, Method Call Expression, and Lambda Expressions). During the execution, the function, method, or lambda can produce a value of a type that is assignable to the return type (see Assignability).

The syntax of return type is presented below:

returnType:
    ':' (type | 'this')
;

If function or method return type is not void (see Type void), and the execution path of the function or method body has no return statement (see return Statements), then a compile-time error occurs.

A compile-time error occurs if lambda return type is not never (see Type never), and the execution path of a function, method, or lambda body has no return statement (see return Statements).

A special form of return type with the keyword this as type annotation can be used in class instance methods only (see Methods Returning this).

If function, method, or lambda return type is not specified, then it is inferred from its body (see Return Type Inference). If there is no body, then the function, method, or lambda return type is void (see Type void).

#### 4.7.8 Return Type Inference

A missing function, method, or lambda return type can be inferred from the function, method, or lambda body. A compile-time error occurs if return type is missing from a native function (see Native Functions).

The current version of ArkTS allows inferring return types at least under the following conditions:

• If there is no return statement, or if all return statements have no expressions, then the return type is void (see Type void).

• If there are k return statements (where k is 1 or more) with the same type expression R, then R is the return type.

• If there are k return statements (where k is 2 or more) with expressions of types  $ T_1 $,  $ \ldots $,  $ T_k $, then R is the union type (see Union Types) of these types ( $ T_1 \mid \ldots \mid T_k $), and its normalized version (see Union Types Normalization) is the return type. If at least one of return statements has no expression, then type undefined is added to the return type union.

• If a lambda body contains no return statement but at least one throw statement (see throw Statements), then the lambda return type is never (see Type never).

• If a function, a method, or a lambda is async (see Asynchronous API), a return type is inferred by applying the above rules, and the return type T is not Promise, then the return type is assumed to be Promise<T>.
