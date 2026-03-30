—then the code below is valid:

class Derived extends Base {
    // invariance: parameter type and return type are unchanged
    override method_one(p: Base): Base {}

    // covariance for the return type: Derived is a subtype of Base
    override method_two(p: Derived): Derived {}

    // contravariance for parameter types: Base is a supertype for Derived
    override method_three(p: Base): Derived {}
}

On the contrary, the following code causes compile-time errors:

class Derived extends Base {

    // covariance for parameter types is prohibited
    override method_one(p: Derived): Base {}

    // contravariance for the return type is prohibited
    override method_tree(p: Derived): Base {}
}

### 15.6 Compatibility of Call Arguments

The following semantic checks must be performed to arguments from the left to the right when checking the validity of any function, method, constructor, or lambda call:

Step 1: All arguments in the form of spread expression (see Spread Expression) are to be linearized recursively to ensure that no spread expression is left at the call site.

Step 2: The following checks are performed on all arguments from left to right, starting from  $ \arg\_pos = 1 $ and  $ \arg\_pos = 1 $:

if parameter at position par_pos is of non-rest form, then

if  $ T_{\arg\_pos} <: T_{\text{par\_pos}} $, then increment  $ \arg\_pos $ and  $ \text{par\_pos} $ else a compile-time error occurs, exit Step 2

else // parameter is of rest form (see Rest Parameter)

if parameter is of rest_array_form, then

if T arg_pos <: T rest_array_type, then increment arg_pos else increment par_pos

else // parameter is of rest_tuple_form

for rest_tuple_pos in 1 .. rest_tuple_types.count do

if  $ T_{\text{arg\_pos}} <: T_{\text{rest\_tuple\_pos}} $, then increment  $ \text{arg\_pos} $ and  $ rest\_tuple\_pos $ else if  $ rest\_tuple\_pos < rest\_tuple\_types.count $, then increment  $ rest\_tuple\_pos $ else a compile-time error occurs, exit Step 2

end increment par_pos
