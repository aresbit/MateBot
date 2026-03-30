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
