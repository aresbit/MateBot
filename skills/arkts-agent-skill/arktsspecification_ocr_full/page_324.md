abstract class MyAnno {
    readonly name: string
    readonly attrs: readonly number[]
}

The use of such a class is represented in following example:

@MyAnno({name: "someName", attr: [1, 2]})
class A {}

let my: MyAnno = // call of reflection library to get instance of annotation for type A
console.log(my.name) // output: someName
