A compile-time error occurs if arrayElementType is a type parameter:

class A<T> {
    foo() {
        new T[2] // compile-time error: cannot create an array of type parameter_
    }
}

#### 17.3.1 Runtime Evaluation of Array Creation Expressions

The evaluation of an array creation expression at runtime is performed as follows:

1. The dimension expressions are evaluated. The evaluation is performed left-to-right. If any expression evaluation completes abruptly, then the expressions to the right of it are not evaluated.

2. The values of dimension expressions are checked. If the value of any dimension expression is less than zero, then NegativeArraySizeError is thrown.

3. Space for the new array is allocated. If the available space is not sufficient to allocate the array, then OutOfMemoryError is thrown, and the evaluation of the array creation expression completes abruptly.

4. When an array with one dimension is created, each element of that array is initialized to its default value if type default value is defined (Default Values for Types). If the default value for an element type is not defined, but the element type is a class type, then its parameterless constructor is used to create the value of each element.

5. When array with several dimensions is created, the array creation effectively executes a set of nested loops of depth n-1.

### 17.4 Enumerations Experimental

Several experimental features described below are available for enumerations.

#### 17.4.1 Enumeration Methods

Several static methods are available to handle each enumeration type as follows:

• Method static values() returns an array of enumeration constants in the order of declaration.

• Method static getValueOf(name: string) returns an enumeration constant with the given name, or throws an error if no constant with such name exists.

• Method static fromValue(value: T), where T is the base type of the enumeration, returns an enumeration constant with a given value, or throws an error if no constant has such a value.
