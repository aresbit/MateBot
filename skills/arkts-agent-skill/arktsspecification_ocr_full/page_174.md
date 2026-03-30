switchStatement:
    (identifier ':()? 'switch' ('expression ')' switchBlock
    ;
switchBlock
    : '{' caseClause* defaultClause? caseClause* '}'
    ;
caseClause
    : 'case' expression ':' statement*
    ;
defaultClause
    : 'default' ':' statement*
    ;

The switch expression type must be of type char, byte, short, int, long, string, or enum.

If available, an optional identifier allows the break statement to transfer control out of a nested switch or loop statement (see break Statements).

A compile-time error occurs if not all of the following is true:

• Every case expression type is assignable (see Assignability) to the type of the switch statement expression.

• In a switch statement expression of type enum, every case expression associated with the switch statement is of type enum.

• No two case constant expressions (see Constant Expressions) have identical values.

• No case expression is null.

let arg = prompt("Enter a value?");
switch (arg) {
    case '0':
        case '1':
            console.log('One or zero')
            break
        case '2':
            console.log('Two')
            break
    default:
        console.log('An unknown value')
}

The execution of a switch statement starts from the evaluation of the switch expression.

The value of the switch expression is compared repeatedly to the value of case expressions starting from the top till the first match. The match means that particular case expression value equals the value of the switch expression in terms of the operator ‘==’. However, if the expression value is of type string, then the equality for strings determines the equality.

So, in case of match execution is transferred to the set of statements of the caseClause where match occurred. If this set of statements executes break statement then the whole switch statement terminates. If no break statement was executed then execution continues through all remaining caseClause*s as well as *defaultClause at last if it is present. If no match occurred and defaultClause is present then it is executed.
