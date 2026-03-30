#### 15.13.1 Extended Conditional Expressions

ArkTS provides extended semantics for conditional expressions to ensure better TypeScript alignment. It affects the semantics of the following:

• Ternary conditional expressions (see Ternary Conditional Expressions, Conditional-And Expression, Conditional-Or Expression, and Logical Complement);

• while and do statements (see while Statements and do Statements);

• for statements (see for Statements);

• if statements (see if Statements).

Note. The extended semantics is to be deprecated in one of the future versions of ArkTS.

The extended semantics approach is based on the concept of truthiness that extends the boolean logic to operands of non-boolean types.

Depending on the kind of a valid expression's type, the value of the valid expression can be handled as true or false as described in the table below:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Value Type Kind</td><td style='text-align: center; word-wrap: break-word;'>When false</td><td style='text-align: center; word-wrap: break-word;'>When true</td><td style='text-align: center; word-wrap: break-word;'>ArkTS Code Example to Check</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>string</td><td style='text-align: center; word-wrap: break-word;'>empty string</td><td style='text-align: center; word-wrap: break-word;'>non-empty string</td><td style='text-align: center; word-wrap: break-word;'>s.length == 0</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>boolean</td><td style='text-align: center; word-wrap: break-word;'>false</td><td style='text-align: center; word-wrap: break-word;'>true</td><td style='text-align: center; word-wrap: break-word;'>x</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>enum</td><td style='text-align: center; word-wrap: break-word;'>enum constant handled as false</td><td style='text-align: center; word-wrap: break-word;'>enum constant handled as true</td><td style='text-align: center; word-wrap: break-word;'>x.valueOf()</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number (double/float)</td><td style='text-align: center; word-wrap: break-word;'>0 or NaN</td><td style='text-align: center; word-wrap: break-word;'>any other number</td><td style='text-align: center; word-wrap: break-word;'>n != 0 &amp;&amp; !isNaN(n)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>any integer type</td><td style='text-align: center; word-wrap: break-word;'>== 0</td><td style='text-align: center; word-wrap: break-word;'>!= 0</td><td style='text-align: center; word-wrap: break-word;'>i != 0</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bigint</td><td style='text-align: center; word-wrap: break-word;'>== 0n</td><td style='text-align: center; word-wrap: break-word;'>!= 0n</td><td style='text-align: center; word-wrap: break-word;'>i != 0n</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>null or undefined</td><td style='text-align: center; word-wrap: break-word;'>always</td><td style='text-align: center; word-wrap: break-word;'>never</td><td style='text-align: center; word-wrap: break-word;'>x != null or x != undefined</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Union types</td><td style='text-align: center; word-wrap: break-word;'>When value is false according to this column</td><td style='text-align: center; word-wrap: break-word;'>When value is true according to this column</td><td style='text-align: center; word-wrap: break-word;'>x != null or x != undefined for union types with nullish types</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Any other nonNullish type</td><td style='text-align: center; word-wrap: break-word;'>never</td><td style='text-align: center; word-wrap: break-word;'>always</td><td style='text-align: center; word-wrap: break-word;'>new SomeType != null</td></tr></table>

Extended semantics of Conditional-And Expression and Conditional-Or Expression affects the resultant type of expressions as follows:

- Type of conditional-and expression A && B equals the type of B if the result of A is handled as true. Otherwise, the expression type equals the type of A.

• Type of conditional-or expression A || B equals the type of B if the result of A is handled as false. Otherwise, the expression type equals the type of A.

The way this approach works in practice is represented in the example below. Any nonzero number is handled as true. The loop continues until it becomes zero that is handled as false:

for (let i = 10; i; i--) {
    console.log(i)
}
/* And the output will be 10
    9

(continues on next page)
