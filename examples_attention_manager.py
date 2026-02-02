#!/usr/bin/env python3
"""
Attention Manager 使用示例 - Manus 注意力重定向机制 (阶段2)

核心功能:
1. KV-Cache 优化的提示词结构
2. 任务目标放在上下文末尾 (recency bias)
3. Todo.md 自动注入每个提示
"""

import os
import shutil
from attention_manager import AttentionManager, StablePromptBuilder, build_prompt


def example_1_basic_prompt_building():
    """示例1: 基础提示词构建"""
    print("=" * 70)
    print("示例1: 基础提示词构建 (Manus 风格)")
    print("=" * 70)

    am = AttentionManager()
    chat_id = "demo_user"

    # 创建任务
    am.create_task(chat_id, "重构数据库访问层，使用 Repository 模式")

    # 构建提示词
    prompt = am.build_optimized_prompt(
        user_input="帮我设计 UserRepository 接口",
        chat_id=chat_id,
        memories=[
            {"content": "之前决定使用 SQLite 作为数据库"},
            {"content": "项目使用 Modern C++20 标准"},
        ],
        include_meta_prompt=False,
    )

    print("\n【生成的提示词结构】")
    print("-" * 50)

    sections = prompt.split(am.SECTION_SEPARATOR.strip())
    for i, section in enumerate(sections, 1):
        lines = section.strip().split("\n")
        title = lines[0][:60] if lines else "Empty"
        content_preview = "\n".join(lines[1:3]) if len(lines) > 1 else ""
        print(f"\n[{i}] {title}")
        if content_preview:
            print(f"    {content_preview[:100]}...")
        print(f"    (长度: {len(section)} 字符)")

    # 统计信息
    stats = am.get_prompt_stats(prompt)
    print("\n【提示词统计】")
    print(f"  总字符数: {stats['total_chars']}")
    print(f"  总行数: {stats['total_lines']}")
    print(f"  段落数: {stats['section_count']}")
    print(f"  有任务复述: {stats['has_task_recitation']}")
    print(f"  静态前缀比例: {stats['static_prefix_ratio']:.1%}")


def example_2_attention_redirection():
    """示例2: 注意力重定向机制 (Manus 核心技巧)"""
    print("\n" + "=" * 70)
    print("示例2: 注意力重定向机制")
    print("=" * 70)

    am = AttentionManager()
    chat_id = "demo_user"

    # 创建复杂任务
    todo_content = """# 当前任务: 实现微服务架构

## 主要目标
将单体应用拆分为3个微服务：用户服务、订单服务、库存服务

## 已完成
- [x] 服务边界划分
- [x] API 契约设计

## 待办事项
- [ ] 实现用户服务 (当前进行中)
- [ ] 实现订单服务
- [ ] 实现库存服务
- [ ] 配置服务网格

## 关键决策
- 使用 gRPC 进行服务间通信
- 使用 Consul 作为服务发现
- 每个服务独立数据库

## 注意事项
⚠️ 不要直接访问其他服务的数据库
⚠️ 所有 API 变更需要向后兼容
⚠️ 记得实现熔断机制
"""

    am._external.update_todo_md(chat_id, todo_content, "microservice_task")
    am.set_task_id(chat_id, "microservice_task")

    # 构建提示词
    prompt = am.build_optimized_prompt(
        user_input="这个 SQL 查询怎么优化？",
        chat_id=chat_id,
        include_meta_prompt=False,
    )

    print("\n【注意任务目标放在哪里？】")
    print("-" * 50)

    # 显示提示词的开头和结尾
    lines = prompt.split("\n")
    print("\n提示词开头 (静态前缀):")
    print("  " + "\n  ".join(lines[:5]))

    print("\n... (中间内容) ...\n")

    print("提示词结尾 (任务目标 - 强化注意力):")
    # 找到任务复述部分
    for i, line in enumerate(lines):
        if "⚠️ 当前任务目标" in line:
            print("  " + "\n  ".join(lines[i:i+15]))
            break

    print("\n【Manus 原理说明】")
    print("  LLM 对上下文末尾的内容注意力更强 (recency bias)")
    print("  将任务目标放在末尾，可以防止 Agent 在长时间对话中偏离目标")


def example_3_kv_cache_optimization():
    """示例3: KV-Cache 优化分析"""
    print("\n" + "=" * 70)
    print("示例3: KV-Cache 优化分析")
    print("=" * 70)

    builder = StablePromptBuilder()

    scenarios = [
        ("简短查询", "怎么写 Hello World?"),
        ("代码审查", "请审查这个函数的异常处理"),
        ("架构设计", "设计一个支持 10万 QPS 的缓存系统"),
    ]

    for scenario_name, user_input in scenarios:
        prompt, info = builder.build_with_cache_optimization(
            user_input=user_input,
            chat_id="demo",
            include_meta_prompt=False,
        )

        print(f"\n【{scenario_name}】")
        print(f"  缓存效率: {info['cache_efficiency']:.1%}")
        print(f"  总长度: {info['total_chars']} 字符")
        print(f"  优化建议: {info['optimization_hints'] or '无'}")

    print("\n【KV-Cache 优化原理】")
    print("  • 静态前缀占总提示的 70%+ 时可获得最佳缓存命中率")
    print("  • 缓存命中可降低 10 倍成本 (\$3/1M tokens → \$0.3/1M tokens)")
    print("  • 避免在前缀中使用时间戳、随机数、动态变量")


def example_4_task_management():
    """示例4: 任务管理流程"""
    print("\n" + "=" * 70)
    print("示例4: 任务管理流程")
    print("=" * 70)

    am = AttentionManager()
    chat_id = "demo_user"

    # 场景1: 创建任务
    print("\n【1. 创建新任务】")
    task_id = am.create_task(
        chat_id,
        "实现 JWT 认证中间件，支持 token 刷新和黑名单"
    )
    print(f"  任务ID: {task_id}")
    print(f"  目标: 实现 JWT 认证中间件...")

    # 场景2: 查看当前 todo
    print("\n【2. 查看当前 Todo】")
    todo = am._external.get_todo_md(chat_id, task_id)
    print(f"  {todo[:200]}...")

    # 场景3: 更新进度
    print("\n【3. 更新任务进度】")
    am._external.update_todo_md(
        chat_id,
        "\n\n## 进展更新\n- 完成 token 生成和验证\n- 正在实现刷新机制",
        task_id,
        append=True
    )
    updated_todo = am._external.get_todo_md(chat_id, task_id)
    print("  已追加更新到 todo.md")

    # 场景4: 多任务管理
    print("\n【4. 多任务管理】")
    am.create_task(chat_id, "优化数据库查询性能", "db_optimization")
    tasks = am._external.list_tasks(chat_id)
    print(f"  活跃任务数: {len(tasks)}")
    for t in tasks:
        print(f"    - {t['task_id']}")

    # 场景5: 切换当前任务
    print("\n【5. 切换当前任务】")
    am.set_task_id(chat_id, "microservice_task")  # 切换到另一个任务
    current = am.get_task_id(chat_id)
    print(f"  当前任务: {current}")


def example_5_quick_build_function():
    """示例5: 快捷构建函数"""
    print("\n" + "=" * 70)
    print("示例5: 快捷构建函数")
    print("=" * 70)

    # 使用快捷函数 (最简单的方式)
    prompt = build_prompt(
        user_input="解释 RAII 模式",
        chat_id="quick_demo",
        memories=[
            {"content": "用户是 C++ 初学者"},
            {"content": "之前学过智能指针"},
        ]
    )

    print("\n【使用 build_prompt() 快捷函数】")
    print(f"  生成的提示词长度: {len(prompt)} 字符")
    print(f"  包含任务目标: {'⚠️ 当前任务目标' in prompt}")

    # 显示部分结构
    sections = prompt.split("\n" + "=" * 50 + "\n")
    print(f"\n  段落数: {len(sections)}")
    for i, s in enumerate(sections[:3], 1):
        first_line = s.strip().split("\n")[0][:50]
        print(f"    [{i}] {first_line}...")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " Attention Manager 使用示例 (阶段2) ".center(68) + "║")
    print("║" + " Manus 注意力重定向 + KV-Cache 优化 ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    # 清理之前的测试数据
    import shutil
    demo_dir = "/home/ares/.matecode/external_memory/demo_user"
    if os.path.exists(demo_dir):
        shutil.rmtree(demo_dir)

    example_1_basic_prompt_building()
    example_2_attention_redirection()
    example_3_kv_cache_optimization()
    example_4_task_management()
    example_5_quick_build_function()

    print("\n" + "=" * 70)
    print("所有示例运行完成!")
    print("=" * 70)
    print("""
阶段2 核心改进总结:

1. 【KV-Cache 优化提示结构】
   - 静态前缀 (缓存友好)
   - 动态内容 (记忆、用户输入)
   - 任务目标 (末尾强化)

2. 【注意力重定向机制】
   - 每次请求自动附加 todo.md
   - 利用 LLM recency bias 保持目标专注
   - 防止长时间对话中的目标漂移

3. 【Telegram 命令集成】
   - /task <goal> - 创建新任务
   - /todo [update] - 查看/更新任务进度

4. 【提示词分析工具】
   - 缓存效率计算
   - 优化建议生成
""")
