#!/usr/bin/env python3
"""
External Memory 使用示例 - 基于 Manus Context Engineering 原则

阶段1实现的核心功能：
1. 分层存储 - 小内容存 SQLite，大内容存文件系统
2. Todo.md 注意力重定向 - 防止目标漂移
3. 可恢复压缩 - 用引用替换大内容
"""

from external_memory import get_external_memory, ExternalMemory, MemoryCompressor
from memory import get_memory, LocalMemory


def example_1_basic_external_storage():
    """示例1: 基础外部存储 - 存储大内容"""
    print("=" * 60)
    print("示例1: 基础外部存储")
    print("=" * 60)

    ext = get_external_memory()
    user_id = "user_demo"

    # 大代码片段 (超过 500 字符阈值)
    large_code = '''
def complex_ml_pipeline(data_path, model_config, training_params):
    """
    这是一个复杂的机器学习管道函数
    包含数据预处理、模型训练、评估和保存
    """
    # 数据预处理步骤
    raw_data = load_data(data_path)
    processed_data = preprocess(raw_data, normalize=True, encode_categorical=True)

    # 模型配置
    model = build_model(
        architecture=model_config['architecture'],
        layers=model_config['layers'],
        activation=model_config['activation']
    )

    # 训练循环
    for epoch in range(training_params['epochs']):
        loss = train_step(model, processed_data)
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Loss: {loss}")

    # 评估和保存
    metrics = evaluate_model(model, processed_data)
    save_model(model, training_params['output_path'])

    return model, metrics
''' * 5  # 让内容变大

    # 存储到外部记忆
    ref = ext.store_large_content(
        user_id=user_id,
        content=large_code,
        content_type="code",
        metadata={
            "language": "python",
            "topic": "machine_learning",
            "importance": "high"
        }
    )

    print(f"✓ 内容已外部存储")
    print(f"  引用ID: {ref.ref_id}")
    print(f"  文件路径: {ref.file_path}")
    print(f"  摘要: {ref.summary}")
    print(f"  原始大小: {ref.size_bytes} bytes")

    # 检索完整内容
    full_content = ext.retrieve_content(ref.ref_id)
    print(f"\n✓ 检索验证: {len(full_content)} 字符")

    return ref


def example_2_todo_md_management():
    """示例2: Todo.md 注意力管理 - Manus 核心技巧"""
    print("\n" + "=" * 60)
    print("示例2: Todo.md 注意力重定向")
    print("=" * 60)

    ext = get_external_memory()
    user_id = "user_demo"
    task_id = "implement_feature_x"

    # 创建任务目标文档 (Manus: 让 Agent 持续重写目标)
    todo_content = """# 当前任务: 实现用户认证系统

## 主要目标
实现一个基于 JWT 的用户认证系统，包括登录、注册和权限验证。

## 已完成 ✅
- [x] 设计数据库 schema
- [x] 实现密码哈希函数

## 待办事项 📝
- [ ] 实现登录 API 端点
- [ ] 实现注册 API 端点
- [ ] 添加 JWT token 生成
- [ ] 实现权限中间件
- [ ] 编写单元测试

## 关键决策 📋
- 使用 bcrypt 进行密码哈希
- JWT 过期时间设置为 24 小时
- Refresh token 机制待讨论

## 注意事项 ⚠️
- 不要在日志中记录密码
- 确保 CORS 配置正确
- 记得添加 rate limiting
"""

    # 更新 todo.md
    ext.update_todo_md(user_id, todo_content, task_id=task_id)
    print("✓ 已创建 todo.md")

    # 读取 todo.md (模拟每次请求时附加到上下文末尾)
    current_todo = ext.get_todo_md(user_id, task_id=task_id)
    print(f"\n✓ 读取 todo.md ({len(current_todo)} 字符)")
    print("\n【在提示词中的使用方式】")
    print("-" * 40)
    prompt_format = f"""
[用户输入]
帮我实现登录 API

[相关记忆]
...

{'='*40}
【当前任务目标 - 请始终保持关注】
{current_todo[:300]}...
{'='*40}
"""
    print(prompt_format)

    # 追加更新 (任务进展)
    ext.update_todo_md(
        user_id,
        "\n## 更新 2024-01-15\n登录 API 实现完成，正在处理注册逻辑",
        task_id=task_id,
        append=True
    )

    updated = ext.get_todo_md(user_id, task_id=task_id)
    print("✓ 已追加更新到 todo.md")

    # 列出所有任务
    tasks = ext.list_tasks(user_id)
    print(f"\n✓ 用户有 {len(tasks)} 个活跃任务")
    for task in tasks:
        print(f"  - {task['task_id']} (修改: {task['modified_at']})")


def example_3_tiered_memory_integration():
    """示例3: 分层记忆系统集成"""
    print("\n" + "=" * 60)
    print("示例3: 分层记忆系统 (LocalMemory + ExternalMemory)")
    print("=" * 60)

    # 使用内存数据库演示
    mem = LocalMemory(db_path=":memory:")
    user_id = "user_demo"

    # 添加小内容 (< 500 字符) - 直接存 SQLite
    small_content = "Python 使用缩进来表示代码块"
    mem.add(user_id, small_content, message_type="tip")
    print(f"✓ 小内容已直接存储 (SQLite)")

    # 添加大内容 (> 500 字符) - 自动转存文件系统
    large_content = """
-- memory
ctx  = src/auth/jwt_handler.py
type = api
desc = JWT token 实现细节

关键实现要点:
1. 使用 PyJWT 库进行 token 编码/解码
2. 密钥存储在环境变量 JWT_SECRET 中
3. Token 包含 user_id, role, exp 字段
4. 验证失败时抛出 401 Unauthorized

代码示例:
```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

注意事项:
- 不要在 payload 中存储敏感信息
- 定期轮换密钥
- 实现 token 黑名单机制用于登出
"""

    mem.add(user_id, large_content, message_type="code_reference")
    print(f"✓ 大内容已自动转存文件系统 (保留引用在 SQLite)")

    # 搜索记忆
    results = mem.search(user_id, "JWT token", limit=5)
    print(f"\n✓ 搜索 'JWT token': 找到 {len(results)} 条结果")

    for i, r in enumerate(results, 1):
        print(f"\n  [{i}] {r['content'][:100]}...")
        if r.get('_has_full_content'):
            print(f"      ↳ 有完整外部内容可用")
            # 获取完整内容
            full = mem.get_full_content(r)
            print(f"      ↳ 完整内容: {len(full)} 字符")

    # 格式化用于提示词 (紧凑模式)
    print(f"\n✓ 格式化用于提示词 (紧凑):")
    formatted = mem.format_for_prompt(results, max_chars=500, expand_external=False)
    print(formatted[:300] + "...")

    # 格式化用于提示词 (展开模式)
    print(f"\n✓ 格式化用于提示词 (展开外部引用):")
    formatted_full = mem.format_for_prompt(results, max_chars=2000, expand_external=True)
    print(formatted_full[:500] + "...")


def example_4_memory_compression():
    """示例4: 显式内存压缩"""
    print("\n" + "=" * 60)
    print("示例4: 显式内存压缩")
    print("=" * 60)

    compressor = MemoryCompressor()
    user_id = "user_demo"

    # 场景1: 小内容不压缩
    small = "记住使用 context managers"
    compressed, ref = compressor.compress_if_needed(user_id, small, "tip")
    print(f"✓ 小内容 (<500 chars): 不压缩")
    print(f"  输出: '{compressed}'")
    print(f"  有外部引用: {ref is not None}")

    # 场景2: 大内容自动压缩
    large = "重要设计决策: " + "详细说明..." * 200
    compressed2, ref2 = compressor.compress_if_needed(
        user_id, large, "design_decision",
        metadata={"project": "auth_system", "reviewed": True}
    )
    print(f"\n✓ 大内容 (>{len(large)} chars): 自动压缩")
    print(f"  压缩后: '{compressed2[:80]}...'")
    print(f"  有外部引用: {ref2 is not None}")
    if ref2:
        print(f"  引用ID: {ref2.ref_id}")
        print(f"  文件大小: {ref2.size_bytes} bytes")


def example_5_storage_stats():
    """示例5: 存储统计"""
    print("\n" + "=" * 60)
    print("示例5: 存储统计")
    print("=" * 60)

    ext = get_external_memory()

    # 全局统计
    stats = ext.get_storage_stats()
    print("全局存储统计:")
    print(f"  总文件数: {stats['total_files']}")
    print(f"  总大小: {stats['total_bytes'] / 1024:.2f} KB")
    print(f"  按类型分布: {stats['by_type']}")

    # 用户特定统计
    user_stats = ext.get_storage_stats("user_demo")
    print(f"\n用户 'user_demo' 统计:")
    print(f"  用户文件数: {user_stats.get('user_files', 0)}")
    print(f"  用户数据大小: {user_stats.get('user_bytes', 0) / 1024:.2f} KB")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " ExternalMemory 使用示例 ".center(58) + "║")
    print("║" + " 基于 Manus Context Engineering 原则 ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # 运行所有示例
    example_1_basic_external_storage()
    example_2_todo_md_management()
    example_3_tiered_memory_integration()
    example_4_memory_compression()
    example_5_storage_stats()

    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)
    print("""
关键设计要点 (来自 Manus):

1. 【可恢复压缩】大内容存文件系统，记忆只存引用
   - 减少上下文窗口占用
   - 按需检索完整内容

2. 【Todo.md 注意力重定向】
   - 每次请求时将 todo.md 放在上下文末尾
   - 利用 LLM 的近期偏好(recency bias)保持目标专注
   - 持续重写目标防止漂移

3. 【分层存储架构】
   - Tier 1: 工作记忆 (当前对话)
   - Tier 2: SQLite (快速访问记忆)
   - Tier 3: 文件系统 (大内容归档)
""")
