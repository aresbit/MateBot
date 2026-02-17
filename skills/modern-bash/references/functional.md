# Bash 函数式编程模式

## 核心思想

Bash 虽然是一门命令式语言，但其管道和命令替换机制允许我们使用函数式编程风格。关键是将命令视为纯函数（输入→输出），管道视为函数组合。

## 基础模式

### 1. 纯函数 (Pure Functions)

```bash
# 纯函数：无副作用，相同输入→相同输出
uppercase() {
    echo "${1^^}"
}

add() {
    echo $(( $1 + $2 ))
}

# 使用：
result=$(add 3 5)  # result = 8
```

### 2. 函数组合 (Function Composition)

```bash
# 使用管道组合函数
process_data() {
    cat "$1" \
        | filter_valid \
        | transform \
        | aggregate
}

# 或使用命令替换 (嵌套组合)
result=$(transform $(filter_valid "$input"))
```

### 3. 高阶函数 (Higher-Order Functions)

```bash
# 接受函数作为参数
map() {
    local fn="$1"
    while read -r item; do
        "$fn" "$item"
    done
}

# 返回函数 (通过生成代码)
curry_add() {
    local a="$1"
    echo "add_$a() { echo \$(( $a + \$1 )); }"
}

# 使用
eval "$(curry_add 5)"
add_5 3  # 输出 8
```

## 常用高阶函数实现

### Map

```bash
map() {
    local func="$1"
    shift
    local item

    if [[ $# -eq 0 ]]; then
        # 从stdin读取
        while IFS= read -r item; do
            "$func" "$item"
        done
    else
        # 从参数读取
        for item in "$@"; do
            "$func" "$item"
        done
    fi
}

# 示例
double() { echo $(( $1 * 2 )); }

$ map double 1 2 3 4 5
2
4
6
8
10

$ seq 1 5 | map double
2
4
6
8
10
```

### Filter

```bash
filter() {
    local predicate="$1"
    shift
    local item

    if [[ $# -eq 0 ]]; then
        while IFS= read -r item; do
            "$predicate" "$item" && echo "$item"
        done
    else
        for item in "$@"; do
            "$predicate" "$item" && echo "$item"
        done
    fi
}

# 示例
is_even() { (( $1 % 2 == 0 )); }
is_positive() { (( $1 > 0 )); }

$ seq -5 5 | filter is_even | filter is_positive
2
4
```

### Reduce / Fold

```bash
reduce() {
    local func="$1"
    local acc="$2"
    shift 2
    local item

    if [[ $# -eq 0 ]]; then
        while IFS= read -r item; do
            acc=$("$func" "$acc" "$item")
        done
    else
        for item in "$@"; do
            acc=$("$func" "$acc" "$item")
        done
    fi
    echo "$acc"
}

# 示例
add() { echo $(( $1 + $2 )); }
multiply() { echo $(( $1 * $2 )); }
max() { echo $(( $1 > $2 ? $1 : $2 )); }

$ reduce add 0 1 2 3 4 5
15

$ seq 1 5 | reduce multiply 1
120
```

### Take / Drop

```bash
take() {
    local n="$1"
    local count=0
    local item

    while IFS= read -r item && (( count < n )); do
        echo "$item"
        (( count++ ))
    done
}

drop() {
    local n="$1"
    local count=0
    local item

    while IFS= read -r item; do
        if (( count >= n )); then
            echo "$item"
        fi
        (( count++ ))
    done
}

# 示例
$ seq 1 100 | take 5
1
2
3
4
5

$ seq 1 10 | drop 8
9
10
```

## 惰性求值模拟

Bash 是严格求值的，但我们可以用进程替换模拟惰性序列：

```bash
# 生成器函数
generator() {
    local i=0
    while true; do
        echo $i
        (( i++ ))
    done
}

# 惰性处理 (不会无限循环，因为 take 只读取5行)
generator | take 5

# 斐波那契数列生成器
fib() {
    local a=0 b=1
    while true; do
        echo $a
        local tmp=$(( a + b ))
        a=$b
        b=$tmp
    done
}

$ fib | take 10
0
1
1
2
3
5
8
13
21
34
```

## 函数组合器

### Compose (右到左组合)

```bash
compose() {
    local fns=("$@")
    local item

    while IFS= read -r item; do
        local result="$item"
        for (( i = ${#fns[@]} - 1; i >= 0; i-- )); do
            result=$(echo "$result" | "${fns[$i]}")
        done
        echo "$result"
    done
}

# 示例: (f ∘ g)(x) = f(g(x))
double() { echo $(( $1 * 2 )); }
add_one() { echo $(( $1 + 1 )); }

$ echo 5 | compose double add_one  # double(add_one(5)) = 12
12
```

### Pipe (左到右组合)

```bash
pipe() {
    local fns=("$@")
    local item

    while IFS= read -r item; do
        local result="$item"
        for fn in "${fns[@]}"; do
            result=$(echo "$result" | "$fn")
        done
        echo "$result"
    done
}

# 示例: pipe(f, g)(x) = g(f(x))
$ echo 5 | pipe add_one double  # double(add_one(5)) = 12
12
```

## Maybe / Optional 模式

```bash
# 模拟 Maybe 类型
some() { echo "some:$1"; }
none() { echo "none"; }

is_some() { [[ "$1" == some:* ]]; }
is_none() { [[ "$1" == "none" ]]; }

get_or_default() {
    local maybe="$1"
    local default="$2"

    if is_some "$maybe"; then
        echo "${maybe#some:}"
    else
        echo "$default"
    fi
}

# 使用
maybe_divide() {
    local a="$1" b="$2"
    if (( b == 0 )); then
        none
    else
        some $(( a / b ))
    fi
}

result=$(maybe_divide 10 0)
get_or_default "$result" "undefined"  # 输出: undefined

result=$(maybe_divide 10 2)
get_or_default "$result" "undefined"  # 输出: 5
```

## 实际应用示例

### 日志分析管道

```bash
#!/bin/bash

# 纯函数定义
extract_ip() { cut -d' ' -f1; }

count_requests() {
    sort | uniq -c | sort -rn
}

filter_status() {
    local code="$1"
    awk -v code="$code" '$9 == code'
}

# 函数式管道
analyze_logs() {
    local logfile="$1"
    local status_code="${2:-404}"

    cat "$logfile" \
        | filter_status "$status_code" \
        | extract_ip \
        | count_requests \
        | head -10
}

analyze_logs access.log 404
```

### 批量文件处理

```bash
#!/bin/bash

# 纯函数
get_extension() {
    local filename="$1"
    echo "${filename##*.}"
}

is_image() {
    local ext
    ext=$(get_extension "$1" | tr '[:upper:]' '[:lower:]')
    [[ "$ext" == "jpg" || "$ext" == "png" || "$ext" == "gif" ]]
}

# 高阶函数应用
process_images() {
    local width="${1:-800}"

    # 获取所有图片 → 处理
    ls -1 | while read -r file; do
        is_image "$file" && echo "$file"
    done | while read -r image; do
        convert "$image" -resize "${width}x" "resized_${image}"
    done
}
```

## 总结

| 函数式概念 | Bash 实现 |
|-----------|----------|
| 纯函数 | 使用 `echo` 输出，无副作用 |
| 函数组合 | 管道 `\|` |
| 高阶函数 | 接受函数名参数，用 `"$fn"` 调用 |
| Map | `while read` 循环应用函数 |
| Filter | `while read` + 条件判断 |
| Reduce | 累积变量 + 循环 |
| 惰性求值 | 进程替换 + 按需读取 |
