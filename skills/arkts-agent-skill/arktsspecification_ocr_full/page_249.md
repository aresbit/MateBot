## SEMANTIC RULES

This Chapter contains semantic rules to be used throughout this Specification document. The description of the rules is more or less informal. Some details are omitted to simplify the understanding.

### 15.1 Semantic Essentials

The section gives a brief introduction to the major semantic terms and their usage in several contexts.

#### 15.1.1 Type of Standalone Expression

Standalone expression (see Type of Expression) is an expression for which there is no target type in the context where the expression is used.

The type of a standalone expression is determined as follows:

• In case of Numeric Literals, the type is the default type of a literal:

- Type of Integer Literals is int or long;

– Type of Floating-Point Literals is double or float.

• In case of Constant Expressions, the type is inferred from operand types and operations.

• In case of an Array Literal, the type is inferred from the elements (see Array Type Inference from Types of Elements).

• Otherwise, a compile-time error occurs. Specifically, a compile-time error occurs if an object literal is used as a standalone expression.

The situation is represented in the example below:

function foo() {
    1     // type is 'int'
    1.0     // type is 'number'
    [1.0, 2.0]    // type is number[]
    [1, "aa"]    // type is (int | string)
}
