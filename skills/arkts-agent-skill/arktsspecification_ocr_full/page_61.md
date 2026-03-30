<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Data Type</td><td style='text-align: center; word-wrap: break-word;'>Default Value</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number</td><td style='text-align: center; word-wrap: break-word;'>0 as number</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte</td><td style='text-align: center; word-wrap: break-word;'>0 as byte</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>short</td><td style='text-align: center; word-wrap: break-word;'>0 as short</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>int</td><td style='text-align: center; word-wrap: break-word;'>0 as int</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>long</td><td style='text-align: center; word-wrap: break-word;'>0 as long</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>+0.0 as float</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>double</td><td style='text-align: center; word-wrap: break-word;'>+0.0 as double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>char</td><td style='text-align: center; word-wrap: break-word;'>u0000</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>boolean</td><td style='text-align: center; word-wrap: break-word;'>false</td></tr></table>

Value undefined is the default value of each type to which this value can be assigned.

class A {
    f1: string | undefined
    f2?: boolean
}
let a = new A()
console.log (a.f1, a.f2)
// Output: undefined, undefined
