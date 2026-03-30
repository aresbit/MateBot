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
