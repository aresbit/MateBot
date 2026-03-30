# Chapter 1: Introduction

Page range: 1-8

## Page 1

ArkTS Specification

Release 1.2.0

## Page 2

## Page 3

1 Introduction 1  
1.1 Overall Description 1  
1.2 Lexical and Syntactic Notation 2  
1.3 Terms and Definitions 3  
  
2 Lexical Elements 9  
2.1 Use of Unicode Characters 9  
2.2 Lexical Input Elements 9  
2.3 White Spaces 9  
2.4 Line Separators 10  
2.5 Tokens 10  
2.6 Identifiers 11  
2.7 Keywords 12  
2.8 Operators and Punctuators 13  
2.9 Literals 14  
2.9.1 Numeric Literals 14  
2.9.2 Integer Literals 14  
2.9.3 Floating-Point Literals 16  
2.9.4 Bigint Literals 17  
2.9.5 Boolean Literals 18  
2.9.6 String Literals 18  
2.9.7 Multiline String Literal 20  
2.9.8 Null Literal 20  
2.9.9 Undefined Literal 20  
  
2.10 Comments 21  
2.11 Semicolons 21  
  
3 Types 23  
3.1 Predefined Types 24  
3.2 User-Defined Types 24  
3.3 Using Types 25  
3.4 Named Types 27  
3.5 Type References 27  
3.6 Value Types 28  
3.6.1 Numeric Types 28  
3.6.2 Integer Types and Operations 29  
3.6.3 Floating-Point Types and Operations 30  
3.6.4 Type boolean 31  
3.7 Reference Types 31  
3.8 Type Any 32

## Page 4

3.9 Type Object ..... 32  
3.10 Type never ..... 33  
3.11 Type void ..... 33  
3.12 Type undefined ..... 35  
3.13 Type null ..... 35  
3.14 Type string ..... 35  
3.15 Type bigint ..... 36  
3.16 Literal Types ..... 36  
3.16.1 String Literal Types ..... 37  
3.17 Array Types ..... 37  
3.17.1 Resizable Array Types ..... 37  
3.17.2 Readonly Array Types ..... 39  
3.18 Tuple Types ..... 39  
3.18.1 Readonly Tuple Types ..... 40  
3.19 Function Types ..... 40  
3.19.1 Type Function ..... 42  
3.20 Union Types ..... 43  
3.20.1 Union Types Normalization ..... 45  
3.20.2 Access to Common Union Members ..... 45  
3.20.3 Keyof Types ..... 47  
3.21 Nullish Types ..... 47  
3.22 Default Values for Types ..... 48  
  
4 Names, Declarations and Scopes ..... 51  
4.1 Names ..... 51  
4.2 Declarations ..... 52  
4.3 Scopes ..... 53  
4.4 Accessible ..... 54  
4.5 Type Declarations ..... 55  
4.5.1 Type Alias Declaration ..... 55  
4.6 Variable and Constant Declarations ..... 56  
4.6.1 Variable Declarations ..... 56  
4.6.2 Constant Declarations ..... 58  
4.6.3 Assignability with Initializer ..... 58  
4.6.4 Type Inference from Initializer ..... 58  
4.7 Function Declarations ..... 59  
4.7.1 Signatures ..... 60  
4.7.2 Parameter List ..... 60  
4.7.3 Readonly Parameters ..... 61  
4.7.4 Optional Parameters ..... 61  
4.7.5 Rest Parameter ..... 62  
4.7.6 Shadowing by Parameter ..... 64  
4.7.7 Return Type ..... 65  
4.7.8 Return Type Inference ..... 65  
  
5 Generics ..... 67  
5.1 Type Parameters ..... 67  
5.1.1 Type Parameter Constraint ..... 68  
5.1.2 Type Parameter Default ..... 69  
5.1.3 Type Parameter Variance ..... 70  
5.2 Generic Instantiations ..... 71  
5.2.1 Type Arguments ..... 72  
5.2.2 Explicit Generic Instantiations ..... 72  
5.2.3 Implicit Generic Instantiations ..... 73

## Page 5

5.3 Utility Types ..... 74  
5.3.1 Awaited Utility Type ..... 74  
5.3.2 NonNullable Utility Type ..... 75  
5.3.3 Partial Utility Type ..... 75  
5.3.4 Required Utility Type ..... 76  
5.3.5 Readonly Utility Type ..... 77  
5.3.6 Record Utility Type ..... 77  
5.3.7 Utility Type Private Fields ..... 78  
  
6 Contexts and Conversions ..... 81  
6.1 Assignment-like Contexts ..... 81  
6.2 String Operator Contexts ..... 82  
6.3 Numeric Operator Contexts ..... 83  
6.3.1 Numeric Conversions for Relational and Equality Operands ..... 83  
6.4 Implicit Conversions ..... 84  
6.4.1 Widening Numeric Conversions ..... 84  
6.4.2 Enumeration to Constants Type Conversions ..... 84  
6.5 Numeric Casting Conversions ..... 85  
  
7 Expressions ..... 87  
7.1 Evaluation of Expressions ..... 88  
7.1.1 Type of Expression ..... 89  
7.1.2 Normal and Abrupt Completion of Expression Evaluation ..... 90  
7.1.3 Order of Expression Evaluation ..... 91  
7.1.4 Operator Precedence ..... 91  
7.1.5 Evaluation of Arguments ..... 92  
7.1.6 Evaluation of Other Expressions ..... 92  
7.2 Literal ..... 92  
7.3 Named Reference ..... 92  
7.3.1 Function Reference ..... 93  
7.3.2 Method Reference ..... 94  
7.4 Array Literal ..... 95  
7.4.1 Array Literal Type Inference from Context ..... 95  
7.4.2 Array Type Inference from Types of Elements ..... 97  
7.5 Object Literal ..... 97  
7.5.1 Object Literal of Class Type ..... 99  
7.5.2 Object Literal of Interface Type ..... 100  
7.5.3 Object Literal of Record Type ..... 101  
7.5.4 Object Literal Evaluation ..... 102  
7.6 Spread Expression ..... 102  
7.7 Parenthesized Expression ..... 104  
7.8 this Expression ..... 104  
7.9 Field Access Expression ..... 105  
7.9.1 Accessing Current Object Fields ..... 106  
7.9.2 Accessing SuperClass Properties ..... 106  
7.10 Method Call Expression ..... 107  
7.10.1 Step 1: Selection of Type to Use ..... 107  
7.10.2 Step 2: Selection of Method ..... 107  
7.10.3 Step 3: Checking Method Modifiers ..... 107  
7.10.4 Type of Method Call Expression ..... 108  
7.11 Function Call Expression ..... 108  
7.12 Indexing Expressions ..... 109  
7.12.1 Array Indexing Expression ..... 110  
7.12.2 String Indexing Expression ..... 111

## Page 6

7.12.3 Record Indexing Expression ..... 112  
7.13 Chaining Operator ..... 113  
7.14 New Expressions ..... 114  
7.15 InstanceOf Expression ..... 115  
7.16 Cast Expression ..... 116  
7.16.1 Type Inference in Cast Expression ..... 116  
7.16.2 Runtime Checking in Cast Expression ..... 117  
7.17 TypeOf Expression ..... 118  
7.18 Ensure-Not-Nullish Expression ..... 120  
7.19 Nullish-Coalescing Expression ..... 121  
7.20 Unary Expressions ..... 121  
7.20.1 Postfix Increment ..... 122  
7.20.2 Postfix Decrement ..... 122  
7.20.3 Prefix Increment ..... 123  
7.20.4 Prefix Decrement ..... 123  
7.20.5 Unary Plus ..... 123  
7.20.6 Unary Minus ..... 124  
7.20.7 Bitwise Complement ..... 124  
7.20.8 Logical Complement ..... 125  
7.21 Multiplicative Expressions ..... 125  
7.21.1 Multiplication ..... 126  
7.21.2 Division ..... 127  
7.21.3 Remainder ..... 128  
7.21.4 Exponentiation ..... 129  
7.22 Additive Expressions ..... 129  
7.22.1 String Concatenation ..... 130  
7.22.2 Additive Operators for Numeric Types ..... 130  
7.23 Shift Expressions ..... 131  
7.24 Relational Expressions ..... 132  
7.24.1 Numeric Relational Operators ..... 133  
7.24.2 String Relational Operators ..... 133  
7.24.3 Boolean Relational Operators ..... 134  
7.24.4 Enumeration Relational Operators ..... 134  
7.25 Equality Expressions ..... 134  
7.25.1 Numeric Equality Operators ..... 136  
7.25.2 Function Type Equality Operators ..... 137  
7.25.3 Extended Equality with null or undefined ..... 137  
7.26 Bitwise and Logical Expressions ..... 138  
7.26.1 Integer Bitwise Operators ..... 138  
7.26.2 Boolean Logical Operators ..... 139  
7.27 Conditional-And Expression ..... 139  
7.28 Conditional-Or Expression ..... 140  
7.29 Assignment ..... 140  
7.29.1 Simple Assignment Operator ..... 141  
7.29.2 Compound Assignment Operators ..... 142  
7.29.3 Left-Hand-Side Expressions ..... 144  
7.30 Ternary Conditional Expressions ..... 144  
7.31 String Interpolation Expressions ..... 145  
7.32 Lambda Expressions ..... 146  
7.32.1 Lambda Signature ..... 147  
7.32.2 Lambda Body ..... 148  
7.32.3 Lambda Expression Type ..... 148  
7.32.4 Runtime Evaluation of Lambda Expressions ..... 148  
7.33 Constant Expressions ..... 150

## Page 7

Statements ..... 153  
8.1 Normal and Abrupt Statement Execution ..... 153  
8.2 Expression Statements ..... 153  
8.3 Block ..... 154  
8.4 Local Declarations ..... 154  
8.5 if Statements ..... 155  
8.6 Loop Statements ..... 156  
8.7 while Statements and do Statements ..... 157  
8.8 for Statements ..... 157  
8.9 for-of Statements ..... 158  
8.10 break Statements ..... 159  
8.11 continue Statements ..... 160  
8.12 return Statements ..... 161  
8.13 switch Statements ..... 161  
8.14 throw Statements ..... 163  
8.15 try Statements ..... 163  
8.15.1 catch Clause ..... 164  
8.15.2 finally Clause ..... 164  
8.15.3 try Statement Execution ..... 165  
  
Classes ..... 167  
9.1 Class Declarations ..... 167  
9.1.1 Abstract Classes ..... 168  
9.2 Class Extension Clause ..... 169  
9.3 Class Implementation Clause ..... 170  
9.3.1 Implementing Interface Methods ..... 171  
9.3.2 Implementing Required Interface Properties ..... 172  
9.3.3 Implementing Optional Interface Properties ..... 174  
9.4 Class Members ..... 176  
9.5 Access Modifiers ..... 177  
9.5.1 Private Access Modifier ..... 178  
9.5.2 Protected Access Modifier ..... 178  
9.5.3 Public Access Modifier ..... 178  
9.6 Field Declarations ..... 179  
9.6.1 Static and Instance Fields ..... 179  
9.6.2 Readonly (Constant) Fields ..... 180  
9.6.3 Optional Fields ..... 180  
9.6.4 Field Initialization ..... 180  
9.6.5 Fields with Late Initialization ..... 181  
9.6.6 Overriding Fields ..... 182  
9.7 Method Declarations ..... 184  
9.7.1 Static Methods ..... 185  
9.7.2 Instance Methods ..... 186  
9.7.3 Abstract Methods ..... 186  
9.7.4 Async Methods ..... 186  
9.7.5 Overriding Methods ..... 187  
9.7.6 Native Methods ..... 187  
9.7.7 Method Body ..... 187  
9.7.8 Methods Returning this ..... 187  
9.8 Class Accessor Declarations ..... 188  
9.9 Constructor Declaration ..... 190  
9.9.1 Formal Parameters ..... 191  
9.9.2 Constructor Body ..... 191  
9.9.3 Explicit Constructor Call ..... 194

## Page 8

9.9.4 Default Constructor ..... 194  
9.10 Inheritance ..... 195  
10 Interfaces ..... 197  
10.1 Interface Declarations ..... 197  
10.2 Superinterfaces and Subinterfaces ..... 198  
10.3 Interface Members ..... 199  
10.4 Interface Properties ..... 200  
10.4.1 Required Interface Properties ..... 201  
10.4.2 Optional Interface Properties ..... 201  
10.5 Interface Method Declarations ..... 202  
10.6 Interface Inheritance ..... 202  
11 Enumerations ..... 203  
11.1 Enumeration Integer Values ..... 204  
11.2 Enumeration String Values ..... 204  
11.3 Enumeration Operations ..... 205  
12 Error Handling ..... 207  
12.1 Errors ..... 207  
13 Modules and Namespaces ..... 209  
13.1 Import Directives ..... 210  
13.1.1 Bind All with Qualified Access ..... 211  
13.1.2 Default Import Binding ..... 211  
13.1.3 Selective Binding ..... 212  
13.1.4 Import Type Directive ..... 213  
13.1.5 Import Path ..... 213  
13.1.6 Several Bindings for One Import Path ..... 215  
13.2 Standard Library Usage ..... 216  
13.3 Top-Level Declarations ..... 217  
13.3.1 Exported Declarations ..... 217  
13.4 Namespace Declarations ..... 218  
13.5 Export Directives ..... 222  
13.5.1 Selective Export Directive ..... 223  
13.5.2 Single Export Directive ..... 223  
13.5.3 Export Type Directive ..... 224  
13.5.4 Re-Export Directive ..... 224  
13.6 Top-Level Statements ..... 225  
13.7 Program Entry Point ..... 227  
14 Ambient Declarations ..... 229  
14.1 Ambient Constant Declarations ..... 230  
14.2 Ambient Function Declarations ..... 230  
14.3 Ambient Overload Function Declarations ..... 231  
14.4 Ambient Class Declarations ..... 231  
14.4.1 Ambient Indexer ..... 233  
14.4.2 Ambient Call Signature ..... 233  
14.4.3 Ambient Iterable ..... 233  
14.5 Ambient Interface Declarations ..... 234  
14.6 Ambient Namespace Declarations ..... 235  
14.6.1 Implementing Ambient Namespace Declaration ..... 236  
15 Semantic Rules ..... 237  
15.1 Semantic Essentials ..... 237
