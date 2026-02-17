# Bash 字符串处理技巧

## 核心理念

Bash 中一切都是字符串。理解字符串操作是掌握 Bash 的关键。

## 基础操作

### 字符串定义与引用

```bash
# 单引号：字面量，不展开
str1='Hello $USER'  # 输出: Hello $USER

# 双引号：允许变量和命令替换
str2="Hello $USER"  # 输出: Hello username
str3="Date: $(date)"

# 无引号：单词分割 + 通配符展开（危险）
str4=hello world    # 两个参数，不是单个字符串
```

### 字符串长度

```bash
str="hello"
${#str}              # 输出: 5
```

## 字符串截取

```bash
str="/home/user/documents/file.txt"

${str:0:4}           # /hom (从0开始，取4个字符)
${str:6}             # ser/documents/file.txt
${str:(-8)}          # file.txt (从右数8个字符)

# 删除最短匹配 (从左边)
${path#*/}           # home/user/file.txt

# 删除最长匹配 (从左边)
${path##*/}          # file.txt

# 删除最短匹配 (从右边)
${path%/*}           # /home/user
${path%.*}           # /home/user/file
```

## 字符串替换

```bash
str="hello world, hello bash"

${str/hello/Hi}      # Hi world, hello bash (替换第一个)
${str//hello/Hi}     # Hi world, Hi bash (替换所有)
${str/#hello/Hi}     # Hi world, hello bash (开头匹配)
${str/%bash/shell}   # hello world, hello shell (结尾匹配)
```

## 大小写转换

```bash
# Bash 4.0+ 方法
str="Hello World"
${str^^}             # HELLO WORLD (全部大写)
${str,,}             # hello world (全部小写)
${str~~}             # hELLO wORLD (大小写翻转)

# 兼容旧版本的方法
echo "$str" | tr '[:lower:]' '[:upper:]'
```

## 字符串匹配

```bash
str="hello world"

# 检查包含
[[ $str == *world* ]] && echo "contains 'world'"

# 检查开头
[[ $str == hello* ]] && echo "starts with 'hello'"

# 正则匹配
[[ $str =~ ^h.*d$ ]] && echo "matches regex"
```

## 字符串分割

```bash
# 按空格分割
str="apple banana cherry"
read -ra fruits <<< "$str"
echo "${fruits[1]}"  # banana

# 按特定字符分割
IFS=',' read -ra parts <<< "a,b,c,d"
echo "${parts[2]}"   # c
```

## 实际应用

### 路径操作

```bash
filepath="/home/user/project/src/main.sh"

filename=${filepath##*/}           # main.sh
dirname=${filepath%/*}             # /home/user/project/src
extension=${filename##*.}          # sh
basename=${filename%.*}            # main
```

### 日志格式化

```bash
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    printf "[%s] %-5s | %s\n" "$timestamp" "$level" "$message"
}
```

## 性能注意事项

```bash
# 慢：每次循环都创建新字符串
result=""
for i in {1..10000}; do
    result="$result $i"
done

# 快：使用数组
arr=()
for i in {1..10000}; do
    arr+=("$i")
done
result="${arr[*]}"
```
