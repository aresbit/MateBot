# Bash 静态语义与动态语义分析

## 静态语义 (Static Semantics)

静态语义关注代码的**结构合法性**和**编译时**可确定的属性,无需实际执行代码。

### 1. 词法分析 (Lexical Analysis)

```bash
function ..() {
    for i in $(seq 1 $1); do cd ..; done
}
```

**词法单元(Tokens)识别:**

| Token类型 | Token值 | 说明 |
|---------|---------|------|
| KEYWORD | `function` | 函数定义关键字 |
| IDENTIFIER | `..` | 函数名标识符 |
| SYMBOL | `()` | 参数列表(空) |
| SYMBOL | `{` | 函数体开始 |
| KEYWORD | `for` | 循环关键字 |
| IDENTIFIER | `i` | 循环变量 |
| KEYWORD | `in` | in关键字 |
| SYMBOL | `$(` | 命令替换开始 |
| COMMAND | `seq` | 外部命令 |
| NUMBER | `1` | 字面量 |
| VARIABLE | `$1` | 位置参数 |
| SYMBOL | `)` | 命令替换结束 |
| SYMBOL | `;` | 语句分隔符 |
| KEYWORD | `do` | 循环体开始 |
| COMMAND | `cd` | 内建命令 |
| IDENTIFIER | `..` | 相对路径 |
| SYMBOL | `;` | 语句分隔符 |
| KEYWORD | `done` | 循环体结束 |
| SYMBOL | `}` | 函数体结束 |

### 2. 语法分析 (Syntactic Analysis)

**抽象语法树(AST):**

```
FunctionDefinition
├── name: ".."
├── parameters: []  (空参数列表)
└── body: CompoundCommand
    └── ForLoop
        ├── variable: "i"
        ├── wordlist: CommandSubstitution
        │   └── Command
        │       ├── name: "seq"
        │       └── args: [Literal(1), ParameterExpansion($1)]
        └── body: CompoundList
            └── SimpleCommand
                ├── name: "cd"
                └── args: [".."]
```

### 3. 类型与作用域分析

**变量作用域:**

```
全局作用域
└── 函数 ".." 的作用域
    ├── $1: 位置参数(隐式声明,函数作用域)
    └── i: 循环变量(默认全局,未使用local)
        ├── 作用域污染风险: 高
        └── 建议: 应声明为 local i
```

**变量绑定时机:**
- `$1`: 函数调用时绑定
- `i`: 循环开始时绑定(每次迭代更新)

**命名空间分析:**
- `..`: 函数名,位于全局命名空间
- 潜在冲突: 可能覆盖同名命令/别名

### 4. 静态语义检查

**合法性验证:**

✅ **通过的检查:**
- 函数名 `..` 语法合法(虽不常见)
- 括号匹配正确
- 关键字使用正确
- 命令替换语法正确

⚠️ **潜在问题:**
- 循环变量 `i` 未使用 `local` 声明(作用域泄漏)
- 变量 `i` 在循环体中未被使用(死代码/无意义绑定)
- 缺少参数校验(`$1` 可能为空或非数字)
- 函数返回值未定义(隐式返回最后一条命令的退出码)

**类型一致性(弱类型):**
- `seq 1 $1` 期望 `$1` 为数字,但Bash不强制类型检查
- 运行时才会暴露类型错误

---

## 动态语义 (Dynamic Semantics)

动态语义描述代码**执行时的行为**和**状态变化**。

### 1. 执行环境初始化

**调用前状态:**
```
环境 E₀:
├── 当前工作目录: /home/user/projects/app/src/components
├── 位置参数: 未绑定
└── 全局变量: {各种环境变量}
```

**调用:** `.. 3`

**参数绑定:**
```
环境 E₁ = E₀ + {$1 ↦ "3"}
```

### 2. 执行语义(操作语义)

采用**小步语义(Small-Step Semantics)**描述执行过程:

#### 步骤1: 命令替换求值

```
⟨$(seq 1 $1), E₁⟩ →
⟨$(seq 1 3), E₁⟩ →  [参数展开]
⟨seq 1 3执行⟩ →     [fork子进程]
⟨"1 2 3", E₁⟩       [捕获stdout]
```

**子进程执行:**
- 创建子shell
- 执行 `/usr/bin/seq 1 3`
- 输出: `1\n2\n3`
- 父进程读取并进行**字段分割**(IFS)
- 结果列表: `["1", "2", "3"]`

#### 步骤2: For循环展开

**第一次迭代 (i=1):**
```
环境 E₂ = E₁ + {i ↦ "1"}
⟨cd .., E₂⟩ →
⟨chdir(".."), E₂⟩ →  [系统调用]
⟨成功, E₃⟩
其中 E₃ = E₂ + {PWD ↦ "/home/user/projects/app/src"}
```

**第二次迭代 (i=2):**
```
环境 E₄ = E₃ + {i ↦ "2"}
⟨cd .., E₄⟩ →
⟨chdir(".."), E₄⟩ →
⟨成功, E₅⟩
其中 E₅ = E₄ + {PWD ↦ "/home/user/projects/app"}
```

**第三次迭代 (i=3):**
```
环境 E₆ = E₅ + {i ↦ "3"}
⟨cd .., E₆⟩ →
⟨chdir(".."), E₆⟩ →
⟨成功, E₇⟩
其中 E₇ = E₆ + {PWD ↦ "/home/user/projects"}
```

#### 步骤3: 循环终止

```
⟨done, E₇⟩ → ⟨退出码: 0, E₇⟩
```

### 3. 状态转换图

```
初始状态 S₀
    PWD = /home/user/projects/app/src/components
    $1 = "3"
    i = undefined
    ↓
    [$(seq 1 3) 求值]
    ↓
中间状态 S₁
    wordlist = ["1", "2", "3"]
    i = undefined
    ↓
    [for循环初始化]
    ↓
迭代状态 S₂ (i=1)
    PWD = /home/user/projects/app/src/components
    i = "1"
    ↓
    [cd ..]
    ↓
迭代状态 S₃ (i=2)
    PWD = /home/user/projects/app/src  ← 副作用
    i = "2"
    ↓
    [cd ..]
    ↓
迭代状态 S₄ (i=3)
    PWD = /home/user/projects/app  ← 副作用
    i = "3"
    ↓
    [cd ..]
    ↓
最终状态 S₅
    PWD = /home/user/projects  ← 副作用
    i = "3"  ← 作用域泄漏
    返回码 = 0
```

### 4. 副作用分析

**可观测副作用:**

1. **文件系统状态变化:**
   - `PWD` 环境变量修改(3次)
   - 进程当前工作目录变化(3次系统调用)

2. **环境变量污染:**
   - 全局变量 `i` 被设置为 `"3"`(因未使用local)
   - `OLDPWD` 环境变量更新

3. **子进程创建:**
   - 命令替换创建一个子shell执行 `seq`

**数据依赖:**
```
$1 (输入) → seq命令 → 循环次数 → PWD变化次数
```

### 5. 求值策略

Bash使用**严格求值(Eager Evaluation)**:

1. **参数展开:** `$1` 在命令替换前立即求值
2. **命令替换:** `$(seq 1 $1)` 在循环开始前完全求值
3. **循环列表:** 预先生成完整列表,非惰性
4. **循环体:** 每次迭代立即执行 `cd ..`

**与惰性求值对比:**
- Haskell惰性版本: `take n $ repeat (cd "..")`
- Bash严格版本: 必须预先计算所有迭代值

---

## 语义等价变换

### 保持动态语义的重写

**原始版本:**
```bash
function ..() {
    for i in $(seq 1 $1); do cd ..; done
}
```

**语义等价版本1(消除未使用变量):**
```bash
function ..() {
    for _ in $(seq 1 $1); do cd ..; done
}
```

**语义等价版本2(直接字符串展开):**
```bash
function ..() {
    cd $(printf '../%.0s' $(seq 1 $1))
}
```

**语义等价版本3(递归定义):**
```bash
function ..() {
    [ $1 -gt 0 ] && cd .. && .. $(($1 - 1))
}
```

### 改进静态语义的版本

```bash
function ..() {
    local count="${1:-1}"  # 默认值,改进静态语义
    local i                # 显式作用域

    # 参数校验
    [[ ! "$count" =~ ^[0-9]+$ ]] && {
        echo "Error: 参数必须是正整数" >&2
        return 1
    }

    for i in $(seq 1 "$count"); do
        cd .. || return $?  # 错误处理
    done
}
```

---

## 形式化语义规则

### 大步语义(Big-Step Semantics)

使用推理规则表示:

```
[CommandSubst]
⟨cmd, E⟩ ⇓ output
─────────────────────────
⟨$(cmd), E⟩ ⇓ output


[ForLoop]
⟨wordlist, E⟩ ⇓ [w₁, w₂, ..., wₙ]
∀i ∈ [1,n]: ⟨body, E + {var ↦ wᵢ}⟩ ⇓ Eᵢ
─────────────────────────────────────
⟨for var in wordlist; do body; done, E⟩ ⇓ Eₙ


[FunctionCall]
⟨body, E + {$1 ↦ arg1, ...}⟩ ⇓ E'
─────────────────────────────
⟨func_name arg1 ..., E⟩ ⇓ E'
```

### 指称语义(Denotational Semantics)

```
⟦function ..() { ... }⟧ = λn. λpwd. pwd ↑ n

其中:
  pwd ↑ 0 = pwd
  pwd ↑ (n+1) = parent(pwd ↑ n)
  parent("/a/b/c") = "/a/b"
```

---

## 执行复杂度分析

### 时间复杂度:
- 命令替换: O(n) - seq生成n个数字
- 循环: O(n) - 迭代n次
- 每次cd: O(1) - 系统调用
- **总计: O(n)**

### 空间复杂度:
- wordlist存储: O(n) - 存储"1 2 3..."
- 调用栈: O(1) - 非递归版本
- **总计: O(n)**

### 系统调用:
- fork: 1次(命令替换)
- exec: 1次(seq命令)
- chdir: n次(cd操作)

---

## 总结

### 静态语义特征:
- ✅ 语法合法
- ⚠️ 缺少类型检查
- ⚠️ 作用域管理不严格
- ⚠️ 缺少错误处理

### 动态语义特征:
- 严格求值策略
- 明显的副作用(改变PWD)
- 状态依赖执行
- 线性时间复杂度

### 关键洞察:
这个函数展示了**命令式编程**与**函数式思想**的混合:
- 命令式: 显式循环,状态修改
- 函数式: 函数抽象,可组合性

其核心语义是一个**状态转换函数**: `State → State`,将当前目录映射到n级父目录,体现了**副作用计算**的本质。
