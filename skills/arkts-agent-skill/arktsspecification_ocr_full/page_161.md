function foo() {
    let y: int = 1
    let x = () => { return y + 1 } // 'y' is *captured*.
    console.log(x()) // Output: 2
}

The captured variable is not a copy of the original variable. If the value of the variable captured by the lambda changes, then the original variable is implied to change:

function foo() {
    let y: int = 1
    let x = () => { y++ } // 'y' is *captured*.
    console.log(y) // Output: 1
    x()
    console.log(y) // Output: 2
}

Capturing within the function scope is highlighted by the following example:

function capturingFunction() { // Function scope
    let v: number = 0 // A captured variable
    return (p: number) => {
        console.log("Previous value: ", v, " new value: ", p)
        v = p
    }
}

const func1 = capturingFunction()
const func2 = capturingFunction()
// Note: func1 and func2 are two different function type instances
func1(11) // Previous value: 0 new value: 11
func2(22) // Previous value: 0 new value: 22
func1(33) // Previous value: 11 new value: 33
func2(44) // Previous value: 22 new value: 44
/* Note:
    func1 calls work with their own version of variable 'v'
    func2 calls work with their own version of variable 'v'
*/

Capturing within the loop scope is highlighted by the following example:

const l = () => {}
const storage = [1, 1, 1, 1, 1] // fill array with some lambdas

for (let index = 0; index < 5; index++) {
    storage [index] = () => { console.log("Index ", index) }
    // Every lambda captures loop index variable
}
for (let index = 0; index < 5; index++) {
    storage[index]() // Captured indices printed
}
