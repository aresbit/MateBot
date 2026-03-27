# Getting Started (Driver Modernization)

## 目标

在最短时间内把旧驱动从“编译失败”拉回到“可编译、可加载、可做基础验证”。

## 30 分钟救火流程

1. 保存基线错误
- `make -C /lib/modules/$(uname -r)/build M=$PWD V=1 modules > build.log 2>&1`
- 只截取前 50 行首个报错链。

2. 定位第一阻塞
- 先修类型/宏/函数签名变更。
- 暂不处理风格告警和性能优化。

3. 单主题改动 + 复编译
- 一次只修一类问题。
- 每次改动后立即 `make` 验证。

4. 最小运行验证
- `insmod` 或 `modprobe`
- 检查 `dmesg` 中 `probe`/`remove`/irq 关键日志

## 不要做的事

- 不要在首轮迁移做大规模重构。
- 不要在缺乏证据时猜测 API 行为。
- 不要跨多个模块同时改动。
