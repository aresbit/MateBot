# sp.h 参考索引

> 本文件是 sp.h 的 API 参考索引。使用 Ctrl+F 搜索关键词查找相关定义。
> 所有函数签名以 `SP_API` 开头，表示这是公共 API。

## 目录

- [类型系统](#类型系统)
- [基础宏](#基础宏)
- [字符串 (sp_str)](#字符串-sp_str)
- [动态数组 (sp_dyn_array)](#动态数组-sp_dyn_array)
- [哈希表 (sp_ht)](#哈希表-sp_ht)
- [内存分配](#内存分配)
- [文件系统 (sp_os)](#文件系统-sp_os)
- [进程 (sp_ps)](#进程-sp_ps)
- [日志 (sp_log)](#日志-sp_log)
- [错误处理](#错误处理)

---

## 类型系统

### 整数类型

```c
typedef int8_t   s8;   // 有符号8位
typedef int16_t  s16;  // 有符号16位
typedef int32_t  s32;  // 有符号32位
typedef int64_t  s64;  // 有符号64位
typedef uint8_t  u8;   // 无符号8位
typedef uint16_t u16;  // 无符号16位
typedef uint32_t u32;  // 无符号32位
typedef uint64_t u64;  // 无符号64位
```

### 浮点类型

```c
typedef float    f32;  // 32位浮点
typedef double   f64;  // 64位浮点
```

### 字符类型

```c
typedef char     c8;   // UTF-8字符
typedef wchar_t  c16;  // 宽字符
```

### 核心结构体

```c
// 字符串类型（ptr + len，无需null终止）
typedef struct {
  const c8* data;
  u32 len;
} sp_str_t;

// 可选值类型
#define sp_opt(T) struct { T value; sp_optional_t some; }

typedef enum {
  SP_OPT_NONE = 0,
  SP_OPT_SOME = 1,
} sp_optional_t;
```

---

## 基础宏

### 初始化宏

| 宏 | 用途 |
|----|------|
| `SP_ZERO_INITIALIZE()` | 零初始化结构体 |
| `SP_ZERO_STRUCT(T)` | 返回类型T的零值 |
| `SP_NULLPTR` | 空指针常量 |
| `SP_NULL` | 空值常量 |

### 工具宏

| 宏 | 用途 |
|----|------|
| `SP_MAX(a, b)` | 最大值 |
| `SP_MIN(a, b)` | 最小值 |
| `SP_SWAP(T, a, b)` | 交换两个变量 |
| `SP_UNUSED(x)` | 标记未使用变量 |
| `SP_CARR_LEN(arr)` | 编译时数组长度 |

### 循环宏

| 宏 | 用途 |
|----|------|
| `sp_for(it, n)` | 遍历 0 到 n-1 |
| `sp_for_range(it, low, high)` | 遍历范围 |
| `sp_carr_for(arr, it)` | 遍历C数组 |

---

## 字符串 (sp_str)

### 字符串创建

```c
// 从字面量创建（编译时常量，零分配）
sp_str_t sp_str_lit(const c8* str);

// 从C字符串创建视图（运行时计算长度）
sp_str_t sp_str_view(const c8* str);

// 从C字符串复制（分配内存）
sp_str_t sp_str_from_cstr(const c8* str);

// 创建子字符串
sp_str_t sp_str_sub(sp_str_t str, u32 index, u32 len);
```

### 字符串查询

```c
// 获取长度
u32 sp_str_len(sp_str_t str);

// 检查是否为空
bool sp_str_empty(sp_str_t str);

// 比较
bool sp_str_equal(sp_str_t a, sp_str_t b);

// 前缀/后缀检查
bool sp_str_starts_with(sp_str_t str, sp_str_t prefix);
bool sp_str_ends_with(sp_str_t str, sp_str_t suffix);

// 查找
u32 sp_str_find(sp_str_t str, sp_str_t substr);
u32 sp_str_find_char(sp_str_t str, c8 ch);
```

### 字符串操作

```c
// 复制
sp_str_t sp_str_copy(sp_str_t str);

// 修剪
sp_str_t sp_str_trim(sp_str_t str);
sp_str_t sp_str_trim_left(sp_str_t str);
sp_str_t sp_str_trim_right(sp_str_t str);

// 大小写转换
sp_str_t sp_str_to_upper(sp_str_t str);
sp_str_t sp_str_to_lower(sp_str_t str);

// 分割
sp_dyn_array(sp_str_t) sp_str_split(sp_str_t str, sp_str_t delim);
```

### C字符串操作

```c
// C字符串长度
u32 sp_cstr_len(const c8* str);

// C字符串比较
bool sp_cstr_equal(const c8* a, const c8* b);

// 复制C字符串到sp_str_t
sp_str_t sp_cstr_to_str(const c8* str);
```

---

## 动态数组 (sp_dyn_array)

### 类型声明

```c
// 声明动态数组类型
sp_dyn_array(T) array = SP_NULLPTR;

// 简写形式
sp_da(T) array = SP_NULLPTR;
```

### 数组操作

| 宏 | 用途 |
|----|------|
| `sp_dyn_array_push(arr, value)` | 添加元素到末尾 |
| `sp_dyn_array_pop(arr)` | 移除并返回最后一个元素 |
| `sp_dyn_array_back(arr)` | 获取最后一个元素 |
| `sp_dyn_array_clear(arr)` | 清空数组（保留容量） |
| `sp_dyn_array_free(arr)` | 释放数组内存 |
| `sp_dyn_array_size(arr)` | 获取元素数量 |
| `sp_dyn_array_capacity(arr)` | 获取容量 |
| `sp_dyn_array_reserve(arr, n)` | 预留容量 |
| `sp_dyn_array_resize(arr, n)` | 调整大小 |

### 数组遍历

```c
// 遍历动态数组
sp_dyn_array_for(arr, it) {
  // arr[it] 访问元素
}
```

---

## 哈希表 (sp_ht)

### 类型声明

```c
// 声明哈希表：键类型, 值类型
sp_ht(key_type, value_type) ht = SP_NULLPTR;
```

### 基本操作

```c
// 设置哈希和比较函数
void sp_ht_set_fns(ht, hash_fn, compare_fn);

// 插入
void sp_ht_insert(ht, key, value);

// 查找（返回指针）
value_type* sp_ht_getp(ht, key);

// 检查键是否存在
bool sp_ht_key_exists(ht, key);

// 删除
void sp_ht_remove(ht, key);

// 清空
void sp_ht_clear(ht);

// 大小
u32 sp_ht_size(ht);
```

### 遍历

```c
sp_ht_for(ht, it) {
  key_type* key = sp_ht_it_getkp(ht, it);
  value_type* val = sp_ht_it_getp(ht, it);
}
```

### 内置哈希函数

```c
u64 sp_ht_hash_str(const void* key);
bool sp_ht_compare_str(const void* a, const void* b);
```

---

## 内存分配

### 基础分配

```c
// 分配内存（自动清零）
void* sp_alloc(u64 size);

// 分配并清零
void* sp_alloc_zero(u64 size);

// 重新分配
void* sp_realloc(void* ptr, u64 new_size);

// 释放内存
void sp_free(void* ptr);

// 分配字符串副本
c8* sp_strdup(const c8* str);
```

### 内存操作

```c
void* sp_memset(void* dest, s32 val, u64 n);
void* sp_memcpy(void* dest, const void* src, u64 n);
void* sp_memmove(void* dest, const void* src, u64 n);
s32   sp_memcmp(const void* a, const void* b, u64 n);
```

---

## 文件系统 (sp_os)

### 路径操作

```c
// 当前工作目录
sp_str_t sp_os_get_cwd(void);

// 路径拼接
sp_str_t sp_os_path_join(sp_str_t a, sp_str_t b);

// 路径存在性检查
bool sp_os_path_exists(sp_str_t path);
bool sp_os_path_is_file(sp_str_t path);
bool sp_os_path_is_dir(sp_str_t path);

// 绝对路径
sp_str_t sp_os_path_absolute(sp_str_t path);
```

### 文件操作

```c
// 读取整个文件
sp_str_t sp_os_read_file(sp_str_t path);

// 写入文件
bool sp_os_write_file(sp_str_t path, sp_str_t content);

// 追加到文件
bool sp_os_append_file(sp_str_t path, sp_str_t content);

// 删除文件
bool sp_os_remove_file(sp_str_t path);

// 复制文件
bool sp_os_copy_file(sp_str_t src, sp_str_t dst);
```

### 目录操作

```c
// 创建目录
bool sp_os_mkdir(sp_str_t path);

// 删除目录
bool sp_os_rmdir(sp_str_t path);

// 列出目录内容
sp_dyn_array(sp_str_t) sp_os_list_dir(sp_str_t path);
```

---

## 进程 (sp_ps)

### 运行命令

```c
typedef struct {
  sp_str_t stdout;
  sp_str_t stderr;
  s32 status;
} sp_ps_result_t;

// 同步运行命令
sp_ps_result_t sp_ps_run(sp_str_t command);
```

### 进程管理

```c
// 启动子进程
sp_ps_t* sp_ps_spawn(sp_str_t command);

// 等待进程结束
s32 sp_ps_wait(sp_ps_t* ps);

// 终止进程
bool sp_ps_kill(sp_ps_t* ps);
```

---

## 日志 (sp_log)

### 日志宏

```c
// 基本日志
SP_LOG(format, ...);

// 致命错误（终止程序）
SP_FATAL(format, ...);
```

### 格式化宏

| 宏 | 类型 |
|----|------|
| `SP_FMT_S32(val)` | s32 |
| `SP_FMT_U32(val)` | u32 |
| `SP_FMT_S64(val)` | s64 |
| `SP_FMT_U64(val)` | u64 |
| `SP_FMT_F32(val)` | f32 |
| `SP_FMT_F64(val)` | f64 |
| `SP_FMT_CSTR(val)` | const c8* |
| `SP_FMT_STR(val)` | sp_str_t |
| `SP_FMT_BOOL(val)` | bool |
| `SP_FMT_CHAR(val)` | c8 |
| `SP_FMT_PTR(val)` | void* |

### 格式化函数

```c
// 格式化到字符串
sp_str_t sp_format(const c8* fmt, ...);
```

### 颜色语法

```c
// 前景色
{:fg red}       {:fg green}     {:fg blue}
{:fg yellow}    {:fg magenta}   {:fg cyan}
{:fg white}     {:fg black}

// 亮前景色
{:fg bright-red}    {:fg bright-green}  等等

// 背景色
{:bg red}  等等

// 重置
{:reset}
```

---

## 错误处理

### 断言宏

```c
SP_ASSERT(condition);           // 断言条件为真
SP_ASSERT_FMT(cond, fmt, ...);  // 带消息的断言
SP_UNREACHABLE();               // 标记不可达代码
SP_UNREACHABLE_CASE();          // switch 默认分支
```

### 错误传播宏

```c
// 如果expr非零，返回expr
sp_try(expr);

// 如果expr非零，返回指定的错误码
sp_try_as(expr, err);

// 如果条件为假，返回
sp_require(condition);

// 如果条件为假，返回错误码
sp_require_as(condition, err);
```

### 可选值宏

```c
sp_opt_set(opt, value);     // 设置可选值
sp_opt_get(opt);            // 获取可选值
sp_opt_some(value);         // 创建Some值
sp_opt_none();              // 创建None值
sp_opt_is_null(opt);        // 检查是否为None
```

---

## 线程/并发

### 线程

```c
// 创建线程
sp_thread_t sp_thread_create(sp_thread_fn fn, void* arg);

// 等待线程结束
void sp_thread_join(sp_thread_t thread);

// 获取当前线程ID
u64 sp_thread_current_id(void);
```

### 互斥锁

```c
sp_mutex_t mutex = SP_ZERO_INITIALIZE();

void sp_mutex_init(sp_mutex_t* mutex);
void sp_mutex_lock(sp_mutex_t* mutex);
void sp_mutex_unlock(sp_mutex_t* mutex);
void sp_mutex_destroy(sp_mutex_t* mutex);
```

### 原子操作

```c
s32 sp_atomic_inc(sp_atomic_s32_t* val);
s32 sp_atomic_dec(sp_atomic_s32_t* val);
s32 sp_atomic_add(sp_atomic_s32_t* val, s32 add);
s32 sp_atomic_load(sp_atomic_s32_t* val);
void sp_atomic_store(sp_atomic_s32_t* val, s32 new_val);
```

---

## 时间

```c
// 当前时间戳（纳秒）
u64 sp_tm_now_ns(void);

// 当前时间戳（微秒）
u64 sp_tm_now_us(void);

// 当前时间戳（毫秒）
u64 sp_tm_now_ms(void);

// 睡眠
void sp_tm_sleep_ms(u32 ms);
void sp_tm_sleep_us(u32 us);
```

---

## 快速查找表

### 常用任务速查

| 任务 | API |
|------|-----|
| 创建字符串 | `sp_str_lit("text")` |
| 比较字符串 | `sp_str_equal(a, b)` |
| 检查空字符串 | `sp_str_empty(str)` |
| 分配内存 | `sp_alloc(size)` |
| 添加数组元素 | `sp_dyn_array_push(arr, val)` |
| 遍历数组 | `sp_dyn_array_for(arr, i)` |
| 插入哈希表 | `sp_ht_insert(ht, key, val)` |
| 读取文件 | `sp_os_read_file(path)` |
| 日志输出 | `SP_LOG("msg {}", SP_FMT_S32(x))` |
| 零初始化 | `SP_ZERO_INITIALIZE()` |

### 命名约定

| 前缀 | 含义 |
|------|------|
| `sp_` | 公共API函数/类型 |
| `sp_str_` | 字符串操作 |
| `sp_cstr_` | C字符串操作 |
| `sp_dyn_array_` / `sp_da` | 动态数组 |
| `sp_ht_` | 哈希表 |
| `sp_os_` | 操作系统/文件系统 |
| `sp_ps_` | 进程 |
| `sp_tm_` | 时间 |
| `SP_` | 宏常量 |
| `SP_FMT_` | 格式化宏 |
