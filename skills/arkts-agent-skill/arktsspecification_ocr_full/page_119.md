### 7.10 Method Call Expression

A method call expression calls a static or instance method of a class or an interface. Dynamic dispatch (see Dispatch) is used during program execution to perform a call in case of an instance method.

The syntax of method call expression is presented below:

methodCallExpression:
    objectReference('.' | '?.') identifier typeArguments? arguments block?
;

The syntax form that has a block associated with the method call is a special form called trailing lambda call (see Trailing Lambdas for details).

A method call with ‘? . ’ (see Chaining Operator) is called a safe method call because it handles nullish values safely.

There are several steps that determine and check the method to be called at compile time (see Step 1: Selection of Type to Use, Step 2: Selection of Method, and Step 3: Checking Method Modifiers).

#### 7.10.1 Step 1: Selection of Type to Use

The object reference is used to determine the type in which to search for the method. Three forms of object reference are possible:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Form of Object Reference</td><td style='text-align: center; word-wrap: break-word;'>Type to Use</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>typeReference</td><td style='text-align: center; word-wrap: break-word;'>Type denoted by typeReference.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>expression of type  $ T $</td><td style='text-align: center; word-wrap: break-word;'>T if  $ T $ is a class, interface, or union;  $ T $&#x27;s constraint (Type Parameter Constraint) if  $ T $ is a type parameter. A compile-time error occurs otherwise.</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>super</td><td style='text-align: center; word-wrap: break-word;'>The superclass of the class that contains the method call.</td></tr></table>

#### 7.10.2 Step 2: Selection of Method

After the type to use is known, the method to call must be determined. If a method name in the call refers an overload declaration (see Overload Declarations), then Overload Resolution is used to select the method to call. A compile-time error occurs if no method is available to call.

#### 7.10.3 Step 3: Checking Method Modifiers

In this step, the single method to call is known, and the following set of semantic checks must be performed:

• If the method call has the form typeReference.identifier, then typeReference refers to a class, and the method must be declared static. Otherwise, a compile-time error occurs.
