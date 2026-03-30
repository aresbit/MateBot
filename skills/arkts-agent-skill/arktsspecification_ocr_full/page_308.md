(continued from previous page)

foo(c)
bar(c, 1)

// as a method call:
c.foo()
c.bar(1)

interface D {
    function foo1(this: D) {
        function bar1(this: D, n: number): void {
            function demo (d: D) {
                // as a function call:
                foo1(d)
                bar1(d, 1)
                
                // as a method call:
                    d.foo1()
                    d.bar1(1)
            }
            class E implements D {
                const e = new E
            
            // derived class is used as a receiver for a method call:
                e.foo1()
                e.bar1(1)
            
            // the same as a function call:
                foo1(e)
                bar1(e, 1)
            }
        }
    }
}

The keyword this can be used inside a function with receiver. It corresponds to the first parameter. Otherwise, a compile-time error occurs. The type of parameter this is called the receiver type (see Receiver Type).

If the receiver type is a class or interface type, then private or protected members are not accessible (see Accessible) within the body of a function with receiver. Only public members can be accessed:

class A {
    foo() { ... this.bar() ... }
    // function bar() is accessible here
    protected member_1 ...
    private member_2 ...
}

function bar(this: A) { ...
    this.foo() // Method foo() is accessible as it is public
    this.member_1 // Compile-time error as member_1 is not accessible
    this.member_2 // Compile-time error as member_2 is not accessible
    ...
}

let a = new A()
a.foo() // Ordinary class method is called
a.bar() // Function with receiver is called
