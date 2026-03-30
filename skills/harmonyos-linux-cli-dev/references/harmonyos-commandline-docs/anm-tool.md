# anm工具

- slug: `anm-tool`
- updatedDate: `2026-03-30 08:12:29`
- source: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/anm-tool
- navigationAddress: `/hmos/hmos-dp1`

# anm工具

Advanced Notification Manager（通知管理工具，简称anm）是实现通知打印、设置通知参数等功能的工具，为开发者提供基本的通知调试和测试能力，例如打印已发布通知详细信息、设置通知缓存个数、使能通知等。

#### 环境要求

在使用本工具前，开发者需要先获取hdc工具，执行hdc shell。

当前工具仅支持在eng版本中使用，在user版本中使用会出现报错/bin/sh: anm: inaccessible or not found.。

#### anm工具命令列表

#### 帮助命令（help）

```bash
# 显示anm相关的帮助信息
anm help
```

#### 打印命令（dump）

```bash
# 打印通知相关信息
anm dump [<options>]
```

打印命令参数列表

示例
：

```bash
# 打印活跃的通知信息
anm dump -A
```

#### 设置命令（setting）

```bash
# 设置通知参数
anm setting [<options>]
```

设置命令参数列表

设置通知是否支持跨设备协同至指定类型设备。

anm setting -k <deviceType>:<status>

说明：
从API version 18开始，新增支持该命令参数。

deviceType表示需要指定的设备类型。取值范围包括：wearable（智能穿戴设备）、litewearable（轻量级智能穿戴设备）、headset（可穿戴式音频设备）。

status表示需要指定的跨设备协同开关状态。取值为0表示开关为关闭状态，取值为1表示开关为打开状态。

设置指定应用的通知是否支持跨设备协同至指定类型设备。

anm setting -b <deviceType>:<bundleName>:<uid>:<status>

说明：
从API version 18开始，新增支持该命令参数。

deviceType表示需要指定的设备类型。取值范围包括：wearable（智能穿戴设备）、litewearable（轻量级智能穿戴设备）、headset（可穿戴式音频设备）。

status表示需要指定的跨设备协同开关状态。取值为0表示开关为关闭状态，取值为1表示开关为打开状态。

设置指定渠道的通知是否支持通知跨设备协同至指定类型设备。

anm setting -o <deviceType>:<slotType>:<status>

说明：
从API version 18开始，新增支持该命令参数。

deviceType表示需要指定的设备类型。取值范围包括：wearable（智能穿戴设备）、litewearable（轻量级智能穿戴设备）、headset（可穿戴式音频设备）。

slotType表示需要指定的通知渠道类型。 取值范围参考
SlotType
。

status表示需要指定的跨设备协同开关状态。取值为0表示开关为关闭状态，取值为1表示开关为打开状态。

示例
：

```bash
# 设置保存在内存中的最近通知的最大数量为100个
anm setting -c 100

# 设置通知跨设备协同至wearable类型设备的开关为打开状态
anm setting -k wearable:1

# 设置包名为example，uid为10100的应用通知跨设备协同至litewearable类型设备的开关为关闭状态
anm setting -b litewearable:example:10100:0

# 设置渠道类型为0的通知跨设备协同至headset类型设备的开关为打开状态
anm setting -o headset:0:1
```
