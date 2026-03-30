# 适配指导案例
- slug: `arkts-more-cases`
- updatedDate: `2026-03-30 08:06:59`
- source: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-more-cases
- navigationAddress: `/hmos/hmos-dp1`

<span id="ZH-CN_TOPIC_0000002529443499"></span><span id="ZH-CN_TOPIC_0000002529443499"></span>

# 适配指导案例

<div>

本文通过具体应用场景中的案例，提供在ArkTS语法规则下将TS代码适配成ArkTS代码的建议。各章以ArkTS语法规则的英文名称命名，每个案例展示适配前的TS代码和适配后的ArkTS代码。

<div id="arkts-identifiers-as-prop-names" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-identifiers-as-prop-names"></span><span id="arkts-identifiers-as-prop-names"></span>

#### arkts-identifiers-as-prop-names

当属性名是有效的标识符（即不包含特殊字符、空格等，并且不以数字开头），可以直接使用而无需引号。

**应用代码**

``` typescript
interface W {
  bundleName: string
  action: string
  entities: string[]
}

let wantInfo: W = {
  'bundleName': 'com.huawei.hmos.browser',
  'action': 'ohos.want.action.viewData',
  'entities': ['entity.system.browsable']
}
```

**建议改法**

``` typescript
interface W {
  bundleName: string
  action: string
  entities: string[]
}

let wantInfo: W = {
  bundleName: 'com.huawei.hmos.browser',
  action: 'ohos.want.action.viewData',
  entities: ['entity.system.browsable']
}
```

</div>

<div id="arkts-no-any-unknown" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-any-unknown"></span><span id="arkts-no-any-unknown"></span>

#### arkts-no-any-unknown

</div>

<div id="按照业务逻辑将代码中的any-unknown改为具体的类型" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E6%8C%89%E7%85%A7%E4%B8%9A%E5%8A%A1%E9%80%BB%E8%BE%91%E5%B0%86%E4%BB%A3%E7%A0%81%E4%B8%AD%E7%9A%84any-unknown%E6%94%B9%E4%B8%BA%E5%85%B7%E4%BD%93%E7%9A%84%E7%B1%BB%E5%9E%8B"></span><span id="%E6%8C%89%E7%85%A7%E4%B8%9A%E5%8A%A1%E9%80%BB%E8%BE%91%E5%B0%86%E4%BB%A3%E7%A0%81%E4%B8%AD%E7%9A%84any-unknown%E6%94%B9%E4%B8%BA%E5%85%B7%E4%BD%93%E7%9A%84%E7%B1%BB%E5%9E%8B"></span>

#### \[h2\]按照业务逻辑，将代码中的any, unknown改为具体的类型

``` typescript
function printObj(obj: any) {
  console.info(obj);
}

printObj('abc'); // abc
```

**建议改法**

``` typescript
function printObj(obj: string) {
  console.info(obj);
}

printObj('abc'); // abc
```

</div>

<div id="标注jsonparse返回值类型" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E6%A0%87%E6%B3%A8jsonparse%E8%BF%94%E5%9B%9E%E5%80%BC%E7%B1%BB%E5%9E%8B"></span><span id="%E6%A0%87%E6%B3%A8jsonparse%E8%BF%94%E5%9B%9E%E5%80%BC%E7%B1%BB%E5%9E%8B"></span>

#### \[h2\]标注JSON.parse返回值类型

**应用代码**

``` typescript
class A {
  v: number = 0
  s: string = ''
  
  foo(str: string) {
    let tmpStr = JSON.parse(str);
    if (tmpStr.add != undefined) {
      this.v = tmpStr.v;
      this.s = tmpStr.s;
    }
  }
}
```

**建议改法**

``` typescript
class A {
  v: number = 0
  s: string = ''
  
  foo(str: string) {
    let tmpStr: Record<string, Object> = JSON.parse(str);
    if (tmpStr.add != undefined) {
      this.v = tmpStr.v as number;
      this.s = tmpStr.s as string;
    }
  }
}
```

</div>

<div id="使用record类型" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%BD%BF%E7%94%A8record%E7%B1%BB%E5%9E%8B"></span><span id="%E4%BD%BF%E7%94%A8record%E7%B1%BB%E5%9E%8B"></span>

#### \[h2\]使用Record类型

**应用代码**

``` typescript
function printProperties(obj: any) {
  console.info(obj.name);
  console.info(obj.value);
}
```

**建议改法**

``` typescript
function printProperties(obj: Record<string, Object>) {
  console.info(obj.name as string);
  console.info(obj.value as string);
}
```

</div>

<div id="arkts-no-call-signature" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-call-signature"></span><span id="arkts-no-call-signature"></span>

#### arkts-no-call-signature

使用函数类型进行替代。

**应用代码**

``` typescript
interface I {
  (value: string): void;
}

function foo(fn: I) {
  fn('abc');
}

foo((value: string) => {
  console.info(value);
})
```

**建议改法**

``` typescript
type I = (value: string) => void

function foo(fn: I) {
  fn('abc');
}

foo((value: string) => {
  console.info(value);
})
```

</div>

<div id="arkts-no-ctor-signatures-type" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-ctor-signatures-type"></span><span id="arkts-no-ctor-signatures-type"></span>

#### arkts-no-ctor-signatures-type

使用工厂函数（() =\> Instance）替代构造函数签名。

**应用代码**

``` typescript
class Controller {
  value: string = ''

  constructor(value: string) {
    this.value = value;
  }
}

type ControllerConstructor = {
  new (value: string): Controller;
}

class testMenu {
  controller: ControllerConstructor = Controller
  createController() {
    if (this.controller) {
      return new this.controller('123');
    }
    return null;
  }
}

let t = new testMenu();
console.info(t.createController()!.value);
```

**建议改法**

``` typescript
class Controller {
  value: string = ''

  constructor(value: string) {
    this.value = value;
  }
}

type ControllerConstructor = () => Controller;

class testMenu {
  controller: ControllerConstructor = () => {
    return new Controller('abc');
  }

  createController() {
    if (this.controller) {
      return this.controller();
    }
    return null;
  }
}

let t: testMenu = new testMenu();
console.info(t.createController()!.value);
```

</div>

<div id="arkts-no-indexed-signatures" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-indexed-signatures"></span><span id="arkts-no-indexed-signatures"></span>

#### arkts-no-indexed-signatures

使用Record类型进行替代。

**应用代码**

``` typescript
function foo(data: { [key: string]: string }) {
  data['a'] = 'a';
  data['b'] = 'b';
  data['c'] = 'c';
}
```

**建议改法**

``` typescript
function foo(data: Record<string, string>) {
  data['a'] = 'a';
  data['b'] = 'b';
  data['c'] = 'c';
}
```

</div>

<div id="arkts-no-typing-with-this" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-typing-with-this"></span><span id="arkts-no-typing-with-this"></span>

#### arkts-no-typing-with-this

使用具体类型替代this。

**应用代码**

``` typescript
class C {
  getInstance(): this {
    return this;
  }
}
```

**建议改法**

``` typescript
class C {
  getInstance(): C {
    return this;
  }
}
```

</div>

<div id="arkts-no-ctor-prop-decls" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-ctor-prop-decls"></span><span id="arkts-no-ctor-prop-decls"></span>

#### arkts-no-ctor-prop-decls

显式声明类属性，并在构造函数中手动赋值。

**应用代码**

``` typescript
class Person {
  constructor(readonly name: string) {}

  getName(): string {
    return this.name;
  }
}
```

**建议改法**

``` typescript
class Person {
  name: string
  constructor(name: string) {
    this.name = name;
  }

  getName(): string {
    return this.name;
  }
}
```

</div>

<div id="arkts-no-ctor-signatures-iface" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-ctor-signatures-iface"></span><span id="arkts-no-ctor-signatures-iface"></span>

#### arkts-no-ctor-signatures-iface

使用type定义工厂函数或普通函数类型。

**应用代码**

``` typescript
class Controller {
  value: string = ''

  constructor(value: string) {
    this.value = value;
  }
}

interface ControllerConstructor {
  new (value: string): Controller;
}

class testMenu {
  controller: ControllerConstructor = Controller
  createController() {
    if (this.controller) {
      return new this.controller('abc');
    }
    return null;
  }
}

let t = new testMenu();
console.info(t.createController()!.value);
```

**建议改法**

``` typescript
class Controller {
  value: string = ''

  constructor(value: string) {
    this.value = value;
  }
}

type ControllerConstructor = () => Controller;

class testMenu {
  controller: ControllerConstructor = () => {
    return new Controller('abc');
  }

  createController() {
    if (this.controller) {
      return this.controller();
    }
    return null;
  }
}

let t: testMenu = new testMenu();
console.info(t.createController()!.value);
```

</div>

<div id="arkts-no-props-by-index" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-props-by-index"></span><span id="arkts-no-props-by-index"></span>

#### arkts-no-props-by-index

可以将对象转换为Record类型，以便访问其属性。

**应用代码**

``` typescript
function foo(params: Object) {
    let funNum: number = params['funNum'];
    let target: string = params['target'];
}
```

**建议改法**

``` typescript
function foo(params: Record<string, string | number>) {
    let funNum: number = params['funNum'] as number;
    let target: string = params['target'] as string;
}
```

</div>

<div id="arkts-no-inferred-generic-params" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-inferred-generic-params"></span><span id="arkts-no-inferred-generic-params"></span>

#### arkts-no-inferred-generic-params

所有泛型调用都应显式标注泛型参数类型，如 Map\<string, T\>、.map\<T\>()。

**应用代码**

``` typescript
class A {
  str: string = ''
}
class B extends A {}
class C extends A {}

let arr: Array<A> = [];

let originMenusMap:Map<string, C> = new Map(arr.map(item => [item.str, (item instanceof C) ? item: null]));
```

**建议改法**

``` typescript
class A {
  str: string = ''
}
class B extends A {}
class C extends A {}

let arr: Array<A> = [];

let originMenusMap: Map<string, C | null> = new Map<string, C | null>(arr.map<[string, C | null]>(item => [item.str, (item instanceof C) ? item: null]));
```

**原因**

(item instanceof C) ? item: null 需要声明类型为C |
null，由于编译器无法推导出map的泛型类型参数，需要显式标注。

</div>

<div id="arkts-no-regexp-literals" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-regexp-literals"></span><span id="arkts-no-regexp-literals"></span>

#### arkts-no-regexp-literals

使用new RegExp(pattern, flags) 构造函数替代RegExp字面量。

**应用代码**

``` typescript
let regex: RegExp = /\s*/g;
```

**建议改法**

``` typescript
let regexp: RegExp = new RegExp('\\s*','g');
```

**原因**

如果正则表达式中使用了标志符，需要将其作为new RegExp()的参数。

</div>

<div id="arkts-no-untyped-obj-literals" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-untyped-obj-literals"></span><span id="arkts-no-untyped-obj-literals"></span>

#### arkts-no-untyped-obj-literals

</div>

<div id="从sdk中导入类型标注object-literal类型" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%BB%8Esdk%E4%B8%AD%E5%AF%BC%E5%85%A5%E7%B1%BB%E5%9E%8B%E6%A0%87%E6%B3%A8object-literal%E7%B1%BB%E5%9E%8B"></span><span id="%E4%BB%8Esdk%E4%B8%AD%E5%AF%BC%E5%85%A5%E7%B1%BB%E5%9E%8B%E6%A0%87%E6%B3%A8object-literal%E7%B1%BB%E5%9E%8B"></span>

#### \[h2\]从SDK中导入类型，标注object literal类型

**应用代码**

``` typescript
const area = { // 没有写明类型 不方便维护
  pixels: new ArrayBuffer(8),
  offset: 0,
  stride: 8,
  region: { size: { height: 1,width:2 }, x: 0, y: 0 }
}
```

**建议改法**

``` typescript
import { image } from '@kit.ImageKit';

const area: image.PositionArea = { // 写明具体类型
  pixels: new ArrayBuffer(8),
  offset: 0,
  stride: 8,
  region: { size: { height: 1, width: 2 }, x: 0, y: 0 }
}
```

</div>

<div id="用class为object-literal标注类型要求class的构造函数无参数" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E7%94%A8class%E4%B8%BAobject-literal%E6%A0%87%E6%B3%A8%E7%B1%BB%E5%9E%8B%E8%A6%81%E6%B1%82class%E7%9A%84%E6%9E%84%E9%80%A0%E5%87%BD%E6%95%B0%E6%97%A0%E5%8F%82%E6%95%B0"></span><span id="%E7%94%A8class%E4%B8%BAobject-literal%E6%A0%87%E6%B3%A8%E7%B1%BB%E5%9E%8B%E8%A6%81%E6%B1%82class%E7%9A%84%E6%9E%84%E9%80%A0%E5%87%BD%E6%95%B0%E6%97%A0%E5%8F%82%E6%95%B0"></span>

#### \[h2\]用class为object literal标注类型，要求class的构造函数无参数

**应用代码**

``` typescript
class Test {
  value: number = 1
  // 有构造函数
  constructor(value: number) {
    this.value = value;
  }
}

let t: Test = { value: 2 };
```

**建议改法1**

``` typescript
// 去除构造函数
class Test {
  value: number = 1
}

let t: Test = { value: 2 };
```

**建议改法2**

``` typescript
// 使用new
class Test {
  value: number = 1
  
  constructor(value: number) {
    this.value = value;
  }
}

let t: Test = new Test(2);
```

**原因**

``` typescript
class C {
  value: number = 1
  
  constructor(n: number) {
    if (n < 0) {
      throw new Error('Negative');
    }
    this.value = n;
  }
}

let s: C = new C(-2);   //抛出异常
let t: C = { value: -2 }; //ArkTS不支持
```

如果允许使用C来标注object literal的类型，变量t会导致行为的二义性。ArkTS禁止通过object literal绕过这一行为。

</div>

<div id="用classinterface为object-literal标注类型要求使用identifier作为object-literal的key" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E7%94%A8classinterface%E4%B8%BAobject-literal%E6%A0%87%E6%B3%A8%E7%B1%BB%E5%9E%8B%E8%A6%81%E6%B1%82%E4%BD%BF%E7%94%A8identifier%E4%BD%9C%E4%B8%BAobject-literal%E7%9A%84key"></span><span id="%E7%94%A8classinterface%E4%B8%BAobject-literal%E6%A0%87%E6%B3%A8%E7%B1%BB%E5%9E%8B%E8%A6%81%E6%B1%82%E4%BD%BF%E7%94%A8identifier%E4%BD%9C%E4%B8%BAobject-literal%E7%9A%84key"></span>

#### \[h2\]用class/interface为object literal标注类型，要求使用identifier作为object literal的key

**应用代码**

``` typescript
class Test {
  value: number = 0
}

let arr: Test[] = [
  {
    'value': 1
  },
  {
    'value': 2
  },
  {
    'value': 3
  }
]
```

**建议改法**

``` typescript
class Test {
  value: number = 0
}
let arr: Test[] = [
  {
    value: 1
  },
  {
    value: 2
  },
  {
    value: 3
  }
]
```

</div>

<div id="使用record类型为object-literal标注类型要求使用字符串作为object-literal的key" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%BD%BF%E7%94%A8record%E7%B1%BB%E5%9E%8B%E4%B8%BAobject-literal%E6%A0%87%E6%B3%A8%E7%B1%BB%E5%9E%8B%E8%A6%81%E6%B1%82%E4%BD%BF%E7%94%A8%E5%AD%97%E7%AC%A6%E4%B8%B2%E4%BD%9C%E4%B8%BAobject-literal%E7%9A%84key"></span><span id="%E4%BD%BF%E7%94%A8record%E7%B1%BB%E5%9E%8B%E4%B8%BAobject-literal%E6%A0%87%E6%B3%A8%E7%B1%BB%E5%9E%8B%E8%A6%81%E6%B1%82%E4%BD%BF%E7%94%A8%E5%AD%97%E7%AC%A6%E4%B8%B2%E4%BD%9C%E4%B8%BAobject-literal%E7%9A%84key"></span>

#### \[h2\]使用Record类型为object literal标注类型，要求使用字符串作为object literal的key

**应用代码**

``` typescript
let obj: Record<string, number | string> = {
  value: 123,
  name: 'abc'
}
```

**建议改法**

``` typescript
let obj: Record<string, number | string> = {
  'value': 123,
  'name': 'abc'
}
```

</div>

<div id="函数参数类型包含index-signature" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0%E7%B1%BB%E5%9E%8B%E5%8C%85%E5%90%ABindex-signature"></span><span id="%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0%E7%B1%BB%E5%9E%8B%E5%8C%85%E5%90%ABindex-signature"></span>

#### \[h2\]函数参数类型包含index signature

**应用代码**

``` typescript
function foo(obj: { [key: string]: string}): string {
  if (obj != undefined && obj != null) {
    return obj.value1 + obj.value2;
  }
  return '';
}
```

**建议改法**

``` typescript
function foo(obj: Record<string, string>): string {
  if (obj != undefined && obj != null) {
    return obj.value1 + obj.value2;
  }
  return '';
}
```

</div>

<div id="函数实参使用了object-literal" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E5%87%BD%E6%95%B0%E5%AE%9E%E5%8F%82%E4%BD%BF%E7%94%A8%E4%BA%86object-literal"></span><span id="%E5%87%BD%E6%95%B0%E5%AE%9E%E5%8F%82%E4%BD%BF%E7%94%A8%E4%BA%86object-literal"></span>

#### \[h2\]函数实参使用了object literal

**应用代码**

``` typescript
(fn) => {
  fn({ value: 123, name:'' });
}
```

**建议改法**

``` typescript
class T {
  value: number = 0
  name: string = ''
}

(fn: (v: T) => void) => {
  fn({ value: 123, name: '' });
}
```

</div>

<div id="classinterface-中包含方法" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__classinterface-%E4%B8%AD%E5%8C%85%E5%90%AB%E6%96%B9%E6%B3%95"></span><span id="classinterface-%E4%B8%AD%E5%8C%85%E5%90%AB%E6%96%B9%E6%B3%95"></span>

#### \[h2\]class/interface 中包含方法

**应用代码**

``` typescript
interface T {
  foo(value: number): number
}

let t:T = { foo: (value) => { return value } };
```

**建议改法1**

``` typescript
interface T {
  foo: (value: number) => number
}

let t:T = { foo: (value) => { return value } };
```

**建议改法2**

``` typescript
class T {
  foo: (value: number) => number = (value: number) => {
    return value;
  }
}

let t:T = new T();
```

**原因**

class/interface中声明的方法应被所有实例共享。ArkTS不支持通过object
literal改写实例方法。ArkTS支持函数类型的属性。

</div>

<div id="export-default对象" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__export-default%E5%AF%B9%E8%B1%A1"></span><span id="export-default%E5%AF%B9%E8%B1%A1"></span>

#### \[h2\]export default对象

**应用代码**

``` typescript
export default {
  onCreate() {
    // ...
  },
  onDestroy() {
    // ...
  }
}
```

**建议改法**

``` typescript
class Test {
  onCreate() {
    // ...
  }
  onDestroy() {
    // ...
  }
}

export default new Test()
```

</div>

<div id="通过导入namespace获取类型" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E9%80%9A%E8%BF%87%E5%AF%BC%E5%85%A5namespace%E8%8E%B7%E5%8F%96%E7%B1%BB%E5%9E%8B"></span><span id="%E9%80%9A%E8%BF%87%E5%AF%BC%E5%85%A5namespace%E8%8E%B7%E5%8F%96%E7%B1%BB%E5%9E%8B"></span>

#### \[h2\]通过导入namespace获取类型

**应用代码**

``` typescript
// test.d.ets
declare namespace test {
  interface I {
    id: string;
    type: number;
  }

  function foo(name: string, option: I): void;
}

export default test;

// app.ets
import test from 'test';

let option = { id: '', type: 0 };
test.foo('', option);
```

**建议改法**

``` typescript
// test.d.ets
declare namespace test {
  interface I {
    id: string;
    type: number;
  }

  function foo(name: string, option: I): void;
}

export default test;

// app.ets
import test from 'test';

let option: test.I = { id: '', type: 0 };
test.foo('', option);
```

**原因**

对象字面量缺少类型，根据test.foo分析可以得知，option的类型来源于声明文件，那么只需要将类型导入即可。

在test.d.ets中，I定义在namespace中。在ets文件中，先导入namespace，再通过名称获取相应的类型。

</div>

<div id="object-literal传参给object类型" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__object-literal%E4%BC%A0%E5%8F%82%E7%BB%99object%E7%B1%BB%E5%9E%8B"></span><span id="object-literal%E4%BC%A0%E5%8F%82%E7%BB%99object%E7%B1%BB%E5%9E%8B"></span>

#### \[h2\]object literal传参给Object类型

**应用代码**

``` typescript
function emit(event: string, ...args: Object[]): void {}

emit('', {
  'action': 11,
  'outers': false
});
```

**建议改法**

``` typescript
function emit(event: string, ...args: Object[]): void {}

let emitArg: Record<string, number | boolean> = {
   'action': 11,
   'outers': false
}

emit('', emitArg);
```

</div>

<div id="arkts-no-obj-literals-as-types" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-obj-literals-as-types"></span><span id="arkts-no-obj-literals-as-types"></span>

#### arkts-no-obj-literals-as-types

使用interface显式定义结构类型。

**应用代码**

``` typescript
type Person = { name: string, age: number }
```

**建议改法**

``` typescript
interface Person {
  name: string,
  age: number
}
```

</div>

<div id="arkts-no-noninferrable-arr-literals" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-noninferrable-arr-literals"></span><span id="arkts-no-noninferrable-arr-literals"></span>

#### arkts-no-noninferrable-arr-literals

显式声明数组元素的类型（使用interface或class），并为数组变量添加类型注解。

**应用代码**

``` typescript
let permissionList = [
  { name: '设备信息', value: '用于分析设备的续航、通话、上网、SIM卡故障等' },
  { name: '麦克风', value: '用于反馈问题单时增加语音' },
  { name: '存储', value: '用于反馈问题单时增加本地文件附件' }
]
```

**建议改法**

为对象字面量声明类型。

``` typescript
class PermissionItem {
  name?: string
  value?: string
}

let permissionList: PermissionItem[] = [
  { name: '设备信息', value: '用于分析设备的续航、通话、上网、SIM卡故障等' },
  { name: '麦克风', value: '用于反馈问题单时增加语音' },
  { name: '存储', value: '用于反馈问题单时增加本地文件附件' }
]
```

</div>

<div id="arkts-no-method-reassignment" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-method-reassignment"></span><span id="arkts-no-method-reassignment"></span>

#### arkts-no-method-reassignment

使用函数类型的类字段（class field）代替原型方法。

**应用代码**

``` typescript
class C {
  add(left: number, right: number): number {
    return left + right;
  }
}

function sub(left: number, right: number): number {
  return left - right;
}

let c1 = new C();
c1.add = sub;
```

**建议改法**

``` typescript
class C {
  add: (left: number, right: number) => number =
    (left: number, right: number) => {
      return left + right;
    }
}

function sub(left: number, right: number): number {
  return left - right;
}

let c1 = new C();
c1.add = sub;
```

</div>

<div id="arkts-no-polymorphic-unops" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-polymorphic-unops"></span><span id="arkts-no-polymorphic-unops"></span>

#### arkts-no-polymorphic-unops

使用 Number.parseInt()、new Number() 等显式转换函数。

**应用代码**

``` typescript
let a = +'5'; // 使用操作符隐式转换
let b = -'5';
let c = ~'5';
let d = +'string';
```

**建议改法**

``` typescript
let a = Number.parseInt('5'); // 使用Number.parseInt显示转换
let b = -Number.parseInt('5');
let c = ~Number.parseInt('5');
let d = new Number('123');
```

</div>

<div id="arkts-no-type-query" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-type-query"></span><span id="arkts-no-type-query"></span>

#### arkts-no-type-query

使用类、接口或类型别名替代typeof，避免依赖变量做类型推导。

**应用代码**

``` typescript
// module1.ts
class C {
  value: number = 0
}

export let c = new C()

// module2.ts
import { c } from './module1'
let t: typeof c = { value: 123 };
```

**建议改法**

``` typescript
// module1.ts
class C {
  value: number = 0
}

export { C }

// module2.ts
import { C } from './module1'
let t: C = { value: 123 };
```

</div>

<div id="arkts-no-in" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-in"></span><span id="arkts-no-in"></span>

#### arkts-no-in

</div>

<div id="使用objectkeys判断属性是否存在" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%BD%BF%E7%94%A8objectkeys%E5%88%A4%E6%96%AD%E5%B1%9E%E6%80%A7%E6%98%AF%E5%90%A6%E5%AD%98%E5%9C%A8"></span><span id="%E4%BD%BF%E7%94%A8objectkeys%E5%88%A4%E6%96%AD%E5%B1%9E%E6%80%A7%E6%98%AF%E5%90%A6%E5%AD%98%E5%9C%A8"></span>

#### \[h2\]使用Object.keys判断属性是否存在

**应用代码**

``` typescript
function test(str: string, obj: Record<string, Object>) {
  return str in obj;
}
```

**建议改法**

``` typescript
function test(str: string, obj: Record<string, Object>) {
  for (let i of Object.keys(obj)) {
    if (i == str) {
      return true;
    }
  }
  return false;
}
```

</div>

<div id="arkts-no-destruct-assignment" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-destruct-assignment"></span><span id="arkts-no-destruct-assignment"></span>

#### arkts-no-destruct-assignment

使用索引访问元素或手动赋值代替解构赋值。

**应用代码**

``` typescript
let map = new Map<string, string>([['a', 'a'], ['b', 'b']]);
for (let [key, value] of map) {
  console.info(key);
  console.info(value);
}
```

**建议改法**

使用数组。

``` typescript
let map = new Map<string, string>([['a', 'a'], ['b', 'b']]);
for (let arr of map) {
  let key = arr[0];
  let value = arr[1];
  console.info(key);
  console.info(value);
}
```

</div>

<div id="arkts-no-types-in-catch" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-types-in-catch"></span><span id="arkts-no-types-in-catch"></span>

#### arkts-no-types-in-catch

使用无类型 catch (error)，然后通过类型断言处理。

**应用代码**

``` typescript
import { BusinessError } from '@kit.BasicServicesKit'

try {
  // ...
} catch (e: BusinessError) {
  console.error(e.message, e.code);
}
```

**建议改法**

``` typescript
import { BusinessError } from '@kit.BasicServicesKit'

try {
  // ...
} catch (error) {
  let e: BusinessError = error as BusinessError;
  console.error(e.message, e.code);
}
```

</div>

<div id="arkts-no-for-in" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-for-in"></span><span id="arkts-no-for-in"></span>

#### arkts-no-for-in

使用 Object.entries(obj) + for of 替代 for in。

**应用代码**

``` typescript
interface Person {
  [name: string]: string
}
let p: Person = {
  name: 'tom',
  age: '18'
};

for (let t in p) {
  console.info(p[t]);  // info: "tom", "18"
}
```

**建议改法**

``` typescript
let p: Record<string, string> = {
  'name': 'tom',
  'age': '18'
};

for (let ele of Object.entries(p)) {
  console.info(ele[1]);  // info: "tom", "18"
}
```

</div>

<div id="arkts-no-mapped-types" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-mapped-types"></span><span id="arkts-no-mapped-types"></span>

#### arkts-no-mapped-types

使用 Record\<K, T\> 替代映射类型。

**应用代码**

``` typescript
class C {
  a: number = 0
  b: number = 0
  c: number = 0
}
type OptionsFlags = {
  [Property in keyof C]: string
}
```

**建议改法**

``` typescript
class C {
  a: number = 0
  b: number = 0
  c: number = 0
}

type OptionsFlags = Record<keyof C, string>
```

</div>

<div id="arkts-limited-throw" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-limited-throw"></span><span id="arkts-limited-throw"></span>

#### arkts-limited-throw

将对象转换为Error，或创建新的Error实例抛出。

**应用代码**

``` typescript
import { BusinessError } from '@kit.BasicServicesKit'

function ThrowError(error: BusinessError) {
  throw error;
}
```

**建议改法**

``` typescript
import { BusinessError } from '@kit.BasicServicesKit'

function ThrowError(error: BusinessError) {
  throw error as Error;
}
```

**原因**

throw语句中值的类型必须为Error或者其继承类，如果继承类是一个泛型，会有编译期报错。建议使用as将类型转换为Error。

</div>

<div id="arkts-no-standalone-this" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-standalone-this"></span><span id="arkts-no-standalone-this"></span>

#### arkts-no-standalone-this

</div>

<div id="函数内使用this" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E5%87%BD%E6%95%B0%E5%86%85%E4%BD%BF%E7%94%A8this"></span><span id="%E5%87%BD%E6%95%B0%E5%86%85%E4%BD%BF%E7%94%A8this"></span>

#### \[h2\]函数内使用this

**应用代码**

``` typescript
function foo() {
  console.info(this.value);
}

let obj = { value: 'abc' };
foo.apply(obj);
```

**建议改法1**

使用类的方法实现,如果该方法被多个类使用,可以考虑采用继承的机制。

``` typescript
class Test {
  value: string = ''
  constructor (value: string) {
    this.value = value
  }
  
  foo() {
    console.info(this.value);
  }
}

let obj: Test = new Test('abc');
obj.foo();
```

**建议改法2**

将this作为参数传入。

``` typescript
function foo(obj: Test) {
  console.info(obj.value);
}

class Test {
  value: string = ''
}

let obj: Test = { value: 'abc' };
foo(obj);
```

**建议改法3**

将属性作为参数传入。

``` typescript
function foo(value: string) {
  console.info(value);
}

class Test {
  value: string = ''
}

let obj: Test = { value: 'abc' };
foo(obj.value);
```

</div>

<div id="class的静态方法内使用this" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__class%E7%9A%84%E9%9D%99%E6%80%81%E6%96%B9%E6%B3%95%E5%86%85%E4%BD%BF%E7%94%A8this"></span><span id="class%E7%9A%84%E9%9D%99%E6%80%81%E6%96%B9%E6%B3%95%E5%86%85%E4%BD%BF%E7%94%A8this"></span>

#### \[h2\]class的静态方法内使用this

**应用代码**

``` typescript
class Test {
  static value: number = 123
  static foo(): number {
    return this.value
  }
}
```

**建议改法**

``` typescript
class Test {
  static value: number = 123
  static foo(): number {
    return Test.value
  }
}
```

</div>

<div id="arkts-no-spread" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-spread"></span><span id="arkts-no-spread"></span>

#### arkts-no-spread

使用Object.assign()、手动赋值或数组方法替代扩展运算符。

**应用代码**

``` typescript
// test.d.ets
declare namespace test {
  interface I {
    id: string;
    type: number;
  }

  function foo(): I;
}

export default test

// app.ets
import test from 'test';

let t: test.I = {
  ...test.foo(),
  type: 0
}
```

**建议改法**

``` typescript
// test.d.ets
declare namespace test {
  interface I {
    id: string;
    type: number;
  }

  function foo(): I;
}

export default test

// app.ets
import test from 'test';

let t: test.I = test.foo();
t.type = 0;
```

**原因**

ArkTS中，对象布局在编译期是确定的。如果需要将一个对象的所有属性展开赋值给另一个对象可以通过逐个属性赋值语句完成。在本例中，需要展开的对象和赋值的目标对象类型恰好相同，可以通过改变该对象属性的方式重构代码。

</div>

<div id="arkts-no-ctor-signatures-funcs" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-ctor-signatures-funcs"></span><span id="arkts-no-ctor-signatures-funcs"></span>

#### arkts-no-ctor-signatures-funcs

在class内声明属性，而不是在构造函数上。

**应用代码**

``` typescript
class Controller {
  value: string = ''
  constructor(value: string) {
    this.value = value
  }
}

type ControllerConstructor = new (value: string) => Controller;

class testMenu {
  controller: ControllerConstructor = Controller
  createController() {
    if (this.controller) {
      return new this.controller('abc');
    }
    return null;
  }
}

let t = new testMenu()
console.info(t.createController()!.value)
```

**建议改法**

``` typescript
class Controller {
  value: string = ''
  constructor(value: string) {
    this.value = value;
  }
}

type ControllerConstructor = () => Controller;

class testMenu {
  controller: ControllerConstructor = () => { return new Controller('abc') }
  createController() {
    if (this.controller) {
      return this.controller();
    }
    return null;
  }
}

let t: testMenu = new testMenu();
console.info(t.createController()!.value);
```

</div>

<div id="arkts-no-globalthis" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-globalthis"></span><span id="arkts-no-globalthis"></span>

#### arkts-no-globalthis

ArkTS不支持globalThis。一方面无法为globalThis添加静态类型，只能通过查找方式访问其属性，导致额外性能开销。另一方面，无法为globalThis的属性标记类型，无法保证操作的安全性和高性能。

<div class="note">

![](https://contentcenter-vali-drcn.dbankcdn.cn/pvt_2/DeveloperAlliance_scene_100_1/bd/v3/QCJD4I3dThuv-IwDew2aKw/note_3.0-zh-cn.png?HW-CC-KV=V1&HW-CC-Date=20260330T132417Z&HW-CC-Expire=86400&HW-CC-Sign=4ED5899526E7F7D61C7AD9EFC7F7B23403B55A517C818A888EFC0DE4F52E377A)<span class="notetitle">
</span>

<div class="notebody">

1.  建议按照业务逻辑根据import/export语法实现数据在不同模块的传递。

2.  必要情况下，可以通过构造的**单例对象**来实现全局对象的功能。（不能在har中定义单例对象，har在打包时会在不同的hap中打包两份，无法实现单例。）

</div>

</div>

**构造单例对象**

``` typescript
// 构造单例对象
export class GlobalContext {
  private constructor() {}
  private static instance: GlobalContext;
  private _objects = new Map<string, Object>();

  public static getContext(): GlobalContext {
    if (!GlobalContext.instance) {
      GlobalContext.instance = new GlobalContext();
    }
    return GlobalContext.instance;
  }

  getObject(value: string): Object | undefined {
    return this._objects.get(value);
  }

  setObject(key: string, objectClass: Object): void {
    this._objects.set(key, objectClass);
  }
}
```

**应用代码**

``` typescript
// file1.ts

export class Test {
  value: string = '';
  foo(): void {
    globalThis.value = this.value;
  }
}

// file2.ts

globalThis.value;
```

**建议改法**

``` typescript
// file1.ts

import { GlobalContext } from '../GlobalContext'

export class Test {
  value: string = '';
  foo(): void {
    GlobalContext.getContext().setObject('value', this.value);
  }
}

// file2.ts

import { GlobalContext } from '../GlobalContext'

GlobalContext.getContext().getObject('value');
```

</div>

<div id="arkts-no-func-apply-bind-call" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-func-apply-bind-call"></span><span id="arkts-no-func-apply-bind-call"></span>

#### arkts-no-func-apply-bind-call

</div>

<div id="使用标准库中接口" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%BD%BF%E7%94%A8%E6%A0%87%E5%87%86%E5%BA%93%E4%B8%AD%E6%8E%A5%E5%8F%A3"></span><span id="%E4%BD%BF%E7%94%A8%E6%A0%87%E5%87%86%E5%BA%93%E4%B8%AD%E6%8E%A5%E5%8F%A3"></span>

#### \[h2\]使用标准库中接口

**应用代码**

``` typescript
let arr: number[] = [1, 2, 3, 4];
let str = String.fromCharCode.apply(null, Array.from(arr));
```

**建议改法**

``` typescript
let arr: number[] = [1, 2, 3, 4];
let str = String.fromCharCode(...Array.from(arr));
```

</div>

<div id="bind定义方法" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__bind%E5%AE%9A%E4%B9%89%E6%96%B9%E6%B3%95"></span><span id="bind%E5%AE%9A%E4%B9%89%E6%96%B9%E6%B3%95"></span>

#### \[h2\]bind定义方法

**应用代码**

``` typescript
class A {
  value: string = ''
  foo: Function = () => {}
}

class Test {
  value: string = '1234'
  obj: A = {
    value: this.value,
    foo: this.foo.bind(this)
  }
  
  foo() {
    console.info(this.value);
  }
}
```

**建议改法1**

``` typescript
class A {
  value: string = ''
  foo: Function = () => {}
}

class Test {
  value: string = '1234'
  obj: A = {
    value: this.value,
    foo: (): void => this.foo()
  }
  
  foo() {
    console.info(this.value);
  }
}
```

**建议改法2**

``` typescript
class A {
  value: string = ''
  foo: Function = () => {}
}

class Test {
  value: string = '1234'
  foo: () => void = () => {
    console.info(this.value);
  }
  obj: A = {
    value: this.value,
    foo: this.foo
  }
}
```

</div>

<div id="使用apply" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%BD%BF%E7%94%A8apply"></span><span id="%E4%BD%BF%E7%94%A8apply"></span>

#### \[h2\]使用apply

**应用代码**

``` typescript
class A {
  value: string;
  constructor (value: string) {
    this.value = value;
  }

  foo() {
    console.info(this.value);
  }
}

let a1 = new A('1');
let a2 = new A('2');

a1.foo();
a1.foo.apply(a2);
```

**建议改法**

``` typescript
class A {
  value: string;
  constructor (value: string) {
    this.value = value;
  }

  foo() {
    this.fooApply(this);
  }

  fooApply(a: A) {
    console.info(a.value);
  }
}

let a1 = new A('1');
let a2 = new A('2');

a1.foo();
a1.fooApply(a2);
```

</div>

<div id="arkts-limited-stdlib" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-limited-stdlib"></span><span id="arkts-limited-stdlib"></span>

#### arkts-limited-stdlib

</div>

<div id="objectfromentries" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__objectfromentries"></span><span id="objectfromentries"></span>

#### \[h2\]Object.fromEntries()

**应用代码**

``` typescript
let entries = new Map([
  ['foo', 123],
  ['bar', 456]
]);

let obj = Object.fromEntries(entries);
```

**建议改法**

``` typescript
let entries = new Map([
  ['foo', 123],
  ['bar', 456]
]);

let obj: Record<string, Object> = {};
entries.forEach((value, key) => {
  if (key != undefined && key != null) {
    obj[key] = value;
  }
})
```

</div>

<div id="严格模式检查strictmodeerror" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%B8%A5%E6%A0%BC%E6%A8%A1%E5%BC%8F%E6%A3%80%E6%9F%A5strictmodeerror"></span><span id="%E4%B8%A5%E6%A0%BC%E6%A8%A1%E5%BC%8F%E6%A3%80%E6%9F%A5strictmodeerror"></span>

#### 严格模式检查(StrictModeError)

</div>

<div id="strictpropertyinitialization" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__strictpropertyinitialization"></span><span id="strictpropertyinitialization"></span>

#### \[h2\]strictPropertyInitialization

**应用代码**

``` typescript
interface I {
  name:string
}

class A {}

class Test {
  a: number;
  b: string;
  c: boolean;
  d: I;
  e: A;
}
```

**建议改法**

``` typescript
interface I {
  name:string
}

class A {}

class Test {
  a: number;
  b: string;
  c: boolean;
  d: I = { name:'abc' };
  e: A | null = null;
  constructor(a:number, b:string, c:boolean) {
    this.a = a;
    this.b = b;
    this.c = c;
  }
}
```

</div>

<div id="type---null-is-not-assignable-to-type-" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__type---null-is-not-assignable-to-type-"></span><span id="type---null-is-not-assignable-to-type-"></span>

#### \[h2\]Type \*\*\* | null is not assignable to type \*\*\*

**应用代码**

``` typescript
class A {
  bar() {}
}
function foo(n: number) {
  if (n === 0) {
    return null;
  }
  return new A();
}
function getNumber() {
  return 5;
}
let a:A = foo(getNumber());
a.bar();
```

**建议改法**

``` typescript
class A {
  bar() {}
}
function foo(n: number) {
  if (n === 0) {
    return null;
  }
  return new A();
}
function getNumber() {
  return 5;
}

let a: A | null = foo(getNumber());
a?.bar();
```

</div>

<div id="严格属性初始化检查" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%B8%A5%E6%A0%BC%E5%B1%9E%E6%80%A7%E5%88%9D%E5%A7%8B%E5%8C%96%E6%A3%80%E6%9F%A5"></span><span id="%E4%B8%A5%E6%A0%BC%E5%B1%9E%E6%80%A7%E5%88%9D%E5%A7%8B%E5%8C%96%E6%A3%80%E6%9F%A5"></span>

#### \[h2\]严格属性初始化检查

在class中，如果一个属性没有初始化，且没有在构造函数中被赋值，ArkTS将报错。

**建议改法**

1.一般情况下，**建议按照业务逻辑**在声明时初始化属性，或者在构造函数中为属性赋值。如：

``` typescript
//code with error
class Test {
  value: number
  flag: boolean
}

//方式一，在声明时初始化
class Test {
  value: number = 0
  flag: boolean = false
}

//方式二，在构造函数中赋值
class Test {
  value: number
  flag: boolean
  constructor(value: number, flag: boolean) {
    this.value = value;
    this.flag = flag;
  }
}
```

2.对于对象类型（包括函数类型）A，如果不确定如何初始化，建议按照以下方式之一进行初始化：

​ 方式(i) prop: A | null = null

​ 方式(ii) prop?: A

​ 方式三(iii) prop： A | undefined = undefined

  - 从性能角度看，null类型仅用于编译期的类型检查，不会影响虚拟机性能。而undefined |
    A被视为联合类型，运行时可能产生额外开销。
  - 从代码可读性、简洁性的角度来说，prop?:A是prop： A | undefined =
    undefined的语法糖，**推荐使用可选属性的写法**。

</div>

<div id="严格函数类型检查" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%B8%A5%E6%A0%BC%E5%87%BD%E6%95%B0%E7%B1%BB%E5%9E%8B%E6%A3%80%E6%9F%A5"></span><span id="%E4%B8%A5%E6%A0%BC%E5%87%BD%E6%95%B0%E7%B1%BB%E5%9E%8B%E6%A3%80%E6%9F%A5"></span>

#### \[h2\]严格函数类型检查

**应用代码**

``` typescript
function foo(fn: (value?: string) => void, value: string): void {}

foo((value: string) => {}, ''); //error
```

**建议改法**

``` typescript
function foo(fn: (value?: string) => void, value: string): void {}

foo((value?: string) => {}, '');
```

**原因**

例如，在以下的例子中，如果编译期不开启严格函数类型的检查，那么该段代码可以编译通过，但是在运行时会产生非预期的行为。具体来看，在foo的函数体中，一个undefined被传入fn（这是可以的，因为fn可以接受undefined），但是在代码第6行foo的调用点，传入的(value:
string) =\> { console.info(value.toUpperCase())
}的函数实现中，始终将参数value当做string类型，允许其调用toUpperCase方法。如果不开启严格函数类型的检查，那么这段代码在运行时，会出现在undefined上无法找到属性的错误。

``` typescript
function foo(fn: (value?: string) => void, value: string): void {
  let v: string | undefined = undefined;
  fn(v);
}

foo((value: string) => { console.info(value.toUpperCase()) }, ''); // Cannot read properties of undefined (reading 'toUpperCase')
```

为了避免运行时的非预期行为，开启严格类型检查时，这段代码将无法编译通过，需要提醒开发者修改代码，确保程序安全。

</div>

<div id="严格空值检查" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%B8%A5%E6%A0%BC%E7%A9%BA%E5%80%BC%E6%A3%80%E6%9F%A5"></span><span id="%E4%B8%A5%E6%A0%BC%E7%A9%BA%E5%80%BC%E6%A3%80%E6%9F%A5"></span>

#### \[h2\]严格空值检查

**应用代码**

``` typescript
class Test {
  private value?: string;
  
  public printValue () {
    console.info(this.value.toLowerCase());
  }
}

let t = new Test();
t.printValue();
```

**应用代码运行时错误原因**

编译期不开启严格空值检查，应用代码可以通过编译，但是在运行时会报错。

因为t的属性value为undefined，在调用printValue方法时，由于在该方法内未对this.value的值进行空值检查，直接按照string类型访问其属性，导致了运行时的错误。

**建议改法**

在编写代码时，建议减少可空类型的使用。如果对变量、属性标记了可空类型，那么在使用它们之前，需要进行空值的判断，根据是否为空值处理不同的逻辑。

``` typescript
class Test {
  private value?: string;

  public printValue () {
    if (this.value) {
      console.info(this.value.toLowerCase());
    }
  }
}

let t = new Test();
t.printValue();
```

</div>

<div id="函数返回类型不匹配" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E5%87%BD%E6%95%B0%E8%BF%94%E5%9B%9E%E7%B1%BB%E5%9E%8B%E4%B8%8D%E5%8C%B9%E9%85%8D"></span><span id="%E5%87%BD%E6%95%B0%E8%BF%94%E5%9B%9E%E7%B1%BB%E5%9E%8B%E4%B8%8D%E5%8C%B9%E9%85%8D"></span>

#### \[h2\]函数返回类型不匹配

**应用代码**

``` typescript
class Test {
  handleClick: (action: string, externInfo?: string) => void | null = null;
}
```

**建议改法**

在这种写法下，函数返回类型被解析为 void | undefined，需要添加括号用来区分union类型。

``` typescript
class Test {
  handleClick: ((action: string, externInfo?: string) => void) | null = null;
}
```

</div>

<div id="type---null-is-not-assignable-to-type--1" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__type---null-is-not-assignable-to-type--1"></span><span id="type---null-is-not-assignable-to-type--1"></span>

#### \[h2\]Type '\*\*\* | null' is not assignable to type '\*\*\*'

**应用代码**

``` typescript
class A {
  value: number
  constructor(value: number) {
    this.value = value;
  }
}

function foo(v: number): A | null {
  if (v > 0) {
    return new A(v);
  }
  return null;
}

let a: A = foo();
```

**建议改法1**

修改变量a的类型：let a: A | null = foo()。

``` typescript
class A {
  value: number
  constructor(value: number) {
    this.value = value;
  }
}

function foo(v: number): A | null {
  if (v > 0) {
    return new A(v);
  }
  return null;
}

let a: A | null = foo(123);

if (a != null) {
  // 非空分支
} else {
  // 处理null
}
```

**建议改法2**

如果确定此处调用foo一定返回非空值，可以使用非空断言\!。

``` typescript
class A {
  value: number
  constructor(value: number) {
    this.value = value;
  }
}

function foo(v: number): A | null {
  if (v > 0) {
    return new A(v);
  }
  return null;
}

let a: A = foo(123)!;
```

</div>

<div id="cannot-invoke-an-object-which-is-possibly-undefined" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__cannot-invoke-an-object-which-is-possibly-undefined"></span><span id="cannot-invoke-an-object-which-is-possibly-undefined"></span>

#### \[h2\]Cannot invoke an object which is possibly 'undefined'

**应用代码**

``` typescript
interface A {
  foo?: () => void
}

let a:A = { foo: () => {} };
a.foo();
```

**建议改法1**

``` typescript
interface A {
  foo: () => void
}
let a: A = { foo: () => {} };
a.foo();
```

**建议改法2**

``` typescript
interface A {
  foo?: () => void
}

let a: A = { foo: () => {} };
if (a.foo) {
  a.foo();
}
```

**原因**

在原先代码的定义中，foo是可选属性，可能为undefined，对undefined的调用会导致报错。建议根据业务逻辑判断是否需要将foo设为可选属性。如果确实需要，那么在访问该属性后需要进行空值检查。

</div>

<div id="variable--is-used-before-being-assigned" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__variable--is-used-before-being-assigned"></span><span id="variable--is-used-before-being-assigned"></span>

#### \[h2\]Variable '\*\*\*' is used before being assigned

**应用代码**

``` typescript
class Test {
  value: number = 0
}

let a: Test
try {
  a = { value: 1};
} catch (e) {
  a.value;
}
a.value;
```

**建议改法**

``` typescript
class Test {
  value: number = 0
}

let a: Test | null = null;
try {
  a = { value:1 };
} catch (e) {
  if (a) {
    a.value;
  }
}

if (a) {
  a.value;
}
```

**原因**

对于primitive types，可以根据业务逻辑赋值，例如0，''，false。

对于对象类型，可以将其类型修改为与null的联合类型，并赋值为null。使用时需要进行非空检查。

</div>

<div id="function-lacks-ending-return-statement-and-return-type-does-not-include-undefined" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__function-lacks-ending-return-statement-and-return-type-does-not-include-undefined"></span><span id="function-lacks-ending-return-statement-and-return-type-does-not-include-undefined"></span>

#### \[h2\]Function lacks ending return statement and return type does not include 'undefined'.

**应用代码**

``` typescript
function foo(a: number): number {
  if (a > 0) {
    return a;
  }
}
```

**建议改法1**

根据业务逻辑，在else分支中返回合适的数值。

**建议改法2**

``` typescript
function foo(a: number): number | undefined {
  if (a > 0) {
    return a;
  }
  return
}
```

</div>

<div id="arkts-strict-typing-required" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-strict-typing-required"></span><span id="arkts-strict-typing-required"></span>

#### arkts-strict-typing-required

删除忽略注释，为所有变量显式声明类型。

**应用代码**

``` typescript
// @ts-ignore
var a: any = 123;
```

**建议改法**

``` typescript
let a: number = 123;
```

**原因**

ArkTS不支持通过注释的方式绕过严格类型检查。首先将注释（// @ts-nocheck或者//
@ts-ignore）删去，再根据报错信息修改其他代码。

</div>

<div id="importing-arkts-files-to-js-and-ts-files-is-not-allowed" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__importing-arkts-files-to-js-and-ts-files-is-not-allowed"></span><span id="importing-arkts-files-to-js-and-ts-files-is-not-allowed"></span>

#### Importing ArkTS files to JS and TS files is not allowed

</div>

<div id="arkts-no-tsdeps" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-tsdeps"></span><span id="arkts-no-tsdeps"></span>

#### arkts-no-tsdeps

不允许.ts、.js文件import.ets文件源码。

**建议改法**

方式1.将.ts文件的后缀修改为ets，并按ArkTS语法规则适配代码。

方式2.将.ets文件中被.ts文件依赖的代码单独抽取到.ts文件中。

</div>

<div id="arkts-no-special-imports" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-special-imports"></span><span id="arkts-no-special-imports"></span>

#### arkts-no-special-imports

改为使用普通import { ... } from '...' 导入类型。

**应用代码**

``` typescript
import type {A, B, C, D } from '***'
```

**建议改法**

``` typescript
import {A, B, C, D } from '***'
```

</div>

<div id="arkts-no-classes-as-obj" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-classes-as-obj"></span><span id="arkts-no-classes-as-obj"></span>

#### arkts-no-classes-as-obj

</div>

<div id="使用class构造实例" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E4%BD%BF%E7%94%A8class%E6%9E%84%E9%80%A0%E5%AE%9E%E4%BE%8B"></span><span id="%E4%BD%BF%E7%94%A8class%E6%9E%84%E9%80%A0%E5%AE%9E%E4%BE%8B"></span>

#### \[h2\]使用class构造实例

**应用代码**

``` typescript
class Controller {
  value: string = ''
  constructor(value: string) {
    this.value = value
  }
}

interface ControllerConstructor {
  new (value: string): Controller;
}

class TestMenu {
  controller: ControllerConstructor = Controller
  createController() {
    if (this.controller) {
      return new this.controller('abc');
    }
    return null;
  }
}

let t = new TestMenu();
console.info(t.createController()!.value);
```

**建议改法**

``` typescript
class Controller {
  value: string = ''

  constructor(value: string) {
    this.value = value;
  }
}

type ControllerConstructor = () => Controller;

class TestMenu {
  controller: ControllerConstructor = () => {
    return new Controller('abc');
  }

  createController() {
    if (this.controller) {
      return this.controller();
    }
    return null;
  }
}

let t: TestMenu = new TestMenu();
console.info(t.createController()!.value);
```

</div>

<div id="访问静态属性" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E8%AE%BF%E9%97%AE%E9%9D%99%E6%80%81%E5%B1%9E%E6%80%A7"></span><span id="%E8%AE%BF%E9%97%AE%E9%9D%99%E6%80%81%E5%B1%9E%E6%80%A7"></span>

#### \[h2\]访问静态属性

**应用代码**

``` typescript
class C1 {
  static value: string = 'abc'
}

class C2 {
  static value: string = 'def'
}

function getValue(obj: any) {
  return obj['value'];
}

console.info(getValue(C1));
console.info(getValue(C2));
```

**建议改法**

``` typescript
class C1 {
  static value: string = 'abc'
}

class C2 {
  static value: string = 'def'
}

function getC1Value(): string {
  return C1.value;
}

function getC2Value(): string {
  return C2.value;
}

console.info(getC1Value());
console.info(getC2Value());
```

</div>

<div id="arkts-no-side-effects-imports" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-side-effects-imports"></span><span id="arkts-no-side-effects-imports"></span>

#### arkts-no-side-effects-imports

改用动态import。

**应用代码**

``` typescript
import 'module'
```

**建议改法**

``` typescript
import('module')
```

</div>

<div id="arkts-no-func-props" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-no-func-props"></span><span id="arkts-no-func-props"></span>

#### arkts-no-func-props

使用class来组织多个相关函数。

**应用代码**

``` typescript
function foo(value: number): void {
  console.info(value.toString());
}

foo.add = (left: number, right: number) => {
  return left + right;
}

foo.sub = (left: number, right: number) => {
  return left - right;
}
```

**建议改法**

``` typescript
class Foo {
  static foo(value: number): void {
    console.info(value.toString());
  }

  static add(left: number, right: number): number {
    return left + right;
  }

  static sub(left: number, right: number): number {
    return left - right;
  }
}
```

</div>

<div id="arkts-limited-esobj" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__arkts-limited-esobj"></span><span id="arkts-limited-esobj"></span>

#### arkts-limited-esobj

使用具体类型（如number, string）或接口代替不明确的ESObject。

**应用代码**

``` typescript
// testa.ts
export function foo(): any {
  return null;
}

// main.ets
import {foo} from './testa'
let e0: ESObject = foo();

function f() {
  let e1 = foo();
  let e2: ESObject = 1;
  let e3: ESObject = {};
  let e4: ESObject = '';
}
```

**建议改法**

``` typescript
// testa.ts
export function foo(): any {
  return null;
}

// main.ets
import {foo} from './testa'
interface I {}

function f() {
  let e0: ESObject = foo();
  let e1: ESObject = foo();
  let e2: number = 1;
  let e3: I = {};
  let e4: string = '';
}
```

</div>

<div id="拷贝" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E6%8B%B7%E8%B4%9D"></span><span id="%E6%8B%B7%E8%B4%9D"></span>

#### 拷贝

</div>

<div id="浅拷贝" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E6%B5%85%E6%8B%B7%E8%B4%9D"></span><span id="%E6%B5%85%E6%8B%B7%E8%B4%9D"></span>

#### \[h2\]浅拷贝

**TypeScript**

``` typescript
function shallowCopy(obj: object): object {
  let newObj = {};
  Object.assign(newObj, obj);
  return newObj;
}
```

**ArkTS**

``` typescript
function shallowCopy(obj: object): object {
  let newObj: Record<string, Object> = {};
  for (let key of Object.keys(obj)) {
    newObj[key] = obj[key];
  }
  return newObj;
}
```

</div>

<div id="深拷贝" class="section">

<span id="ZH-CN_TOPIC_0000002529443499__%E6%B7%B1%E6%8B%B7%E8%B4%9D"></span><span id="%E6%B7%B1%E6%8B%B7%E8%B4%9D"></span>

#### \[h2\]深拷贝

**TypeScript**

``` typescript
function deepCopy(obj: object): object {
  let newObj = Array.isArray(obj) ? [] : {};
  for (let key in obj) {
    if (typeof obj[key] === 'object') {
      newObj[key] = deepCopy(obj[key]);
    } else {
      newObj[key] = obj[key];
    }
  }
  return newObj;
}
```

**ArkTS**

``` typescript
function deepCopy(obj: object): object {
  let newObj: Record<string, Object> | Object[] = Array.isArray(obj) ? [] : {};
  for (let key of Object.keys(obj)) {
    if (typeof obj[key] === 'object') {
      newObj[key] = deepCopy(obj[key]);
    } else {
      newObj[key] = obj[key];
    }
  }
  return newObj;
}
```

</div>

</div>

<div>

</div>
