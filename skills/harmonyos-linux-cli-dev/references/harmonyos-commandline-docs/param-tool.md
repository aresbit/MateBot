# param工具

- slug: `param-tool`
- updatedDate: `2026-03-30 08:12:30`
- source: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/param-tool
- navigationAddress: `/hmos/hmos-dp1`

# param工具

param是为开发人员提供用于操作系统参数的工具，该工具只支持标准系统。

#### 环境要求

- 获取hdc工具，执行hdc shell。
- 正常连接设备。
#### param工具命令列表

#### 获取param支持的命令

- 获取param支持的命令，命令格式如下：
param -h
获取param支持的命令，命令格式如下：

```bash
param -h
```

#### 获取系统参数信息

- 显示匹配name的系统参数信息，命令格式如下：
param ls [-r] [name]
示例
显示匹配name的系统参数信息，命令格式如下：

```bash
param ls [-r] [name]
```

示例

#### 获取系统参数的值

- 获取指定name系统参数的值，命令格式如下：
param get [name]
示例
获取指定name系统参数的值，命令格式如下：

```bash
param get [name]
```

示例

#### 设置系统参数的值

- 设置指定name系统参数的值为value，命令格式如下：
param set name value
示例
设置指定name系统参数的值为value，命令格式如下：

```bash
param set name value
```

示例

#### 等待系统参数值匹配

- 同步等待指定name系统参数与指定值value匹配，命令格式如下：
param wait name [value] [timeout]
示例
同步等待指定name系统参数与指定值value匹配，命令格式如下：

```bash
param wait name [value] [timeout]
```

示例

#### 保存persist(可持久化)参数

- 保存persist(可持久化)参数到工作空间，命令格式如下：
param save
示例
保存persist(可持久化)参数到工作空间，命令格式如下：

```bash
param save
```

示例
