# API Migration Checklist

按下面顺序逐项排查，命中则最小修复：

## 1. file/proc 接口

- `struct file_operations` 是否需要迁移到新字段命名
- `proc_create` 场景是否改为 `proc_ops`

## 2. timer 与延迟执行

- `timer_setup` 与回调签名是否匹配
- tasklet/workqueue 是否仍符合当前上下文约束

## 3. 资源与生命周期

- 优先 `devm_*` 管理资源
- `probe` 失败路径是否完整释放

## 4. 内存与用户态拷贝

- `copy_to_user/copy_from_user` 返回值处理
- `get_user_pages*` 新旧调用差异

## 5. 中断与并发

- `request_irq/free_irq` 参数一致性
- 自旋锁/原子变量/屏障是否仍满足语义

## 6. 日志与诊断

- 用 `pr_*` 替代裸 `printk` 风格
- 错误路径必须给可定位日志

## 7. 回归点

- 模块加载/卸载
- 基本 IO path
- suspend/resume（若适用）
