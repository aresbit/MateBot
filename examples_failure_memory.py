#!/usr/bin/env python3
"""
Failure Memory 使用示例 - Manus 失败保留机制 (阶段3)

核心功能:
1. 错误类型自动分类
2. 失败记录与重复跟踪
3. 相关失败检索 (操作前展示)
4. 教训提取与提示词注入
"""

import os
import shutil
from failure_memory import get_failure_memory, record_failure, get_relevant_failures
from memory import get_memory


def example_1_basic_failure_recording():
    """示例1: 基础失败记录"""
    print("=" * 70)
    print("示例1: 基础失败记录 (Manus: Keep Failures in Context)")
    print("=" * 70)

    fm = get_failure_memory()
    user_id = "demo_user"

    # 清理之前的测试数据
    memory = get_memory()
    memory.clear_all(user_id)

    # 记录一些失败
    print("\n【记录失败 1: 语法错误】")
    record_failure(
        user_id=user_id,
        action="编译 C++ 代码",
        error_message="error: expected ';' before 'return'",
        context="编译 main.cpp 第 42 行",
        lesson="C++ 需要语句结束分号"
    )

    print("\n【记录失败 2: 逻辑错误】")
    record_failure(
        user_id=user_id,
        action="实现快速排序算法",
        error_message="逻辑错误: 递归未终止，导致栈溢出",
        context="实现 quicksort() 函数",
        lesson="需要检查递归基准条件: if (left >= right) return;"
    )

    print("\n【记录失败 3: API 使用错误】")
    record_failure(
        user_id=user_id,
        action="调用数据库 API",
        error_message="APIError: Invalid parameter 'limit' must be positive",
        context="调用 db.query(limit=-1)",
        lesson="API 参数需要验证，limit 必须为正数"
    )

    # 查看统计
    stats = fm.get_stats(user_id)
    print(f"\n【失败统计】")
    print(f"  独立失败数: {stats['total_unique']}")
    print(f"  总发生次数: {stats['total_occurrences']}")
    print(f"  错误类型分布: {stats['by_type']}")


def example_2_recurrence_tracking():
    """示例2: 重复失败跟踪"""
    print("\n" + "=" * 70)
    print("示例2: 重复失败跟踪 (Manus: 识别频繁错误模式)")
    print("=" * 70)

    fm = get_failure_memory()
    user_id = "demo_user_2"

    # 清理
    memory = get_memory()
    memory.clear_all(user_id)

    # 记录相同的失败多次
    action = "执行 SQL 查询"
    error = "SQLite Error: no such table: users"

    for i in range(3):
        record_failure(
            user_id=user_id,
            action=action,
            error_message=error,
            context=f"尝试 #{i+1}",
            lesson="需要先创建表或检查表名拼写"
        )

    # 获取用户的失败记录
    failures = fm.get_user_failures(user_id, resolved_only=False)
    print(f"\n【重复失败示例】")
    for f in failures:
        print(f"  操作: {f.action}")
        print(f"  错误: {f.error_message[:60]}...")
        print(f"  重复次数: {f.recurrence_count}")
        print(f"  教训: {f.lesson}")
        print()


def example_3_relevant_failure_retrieval():
    """示例3: 相关失败检索 (操作前展示)"""
    print("\n" + "=" * 70)
    print("示例3: 相关失败检索 (Manus: 防止重复犯错)")
    print("=" * 70)

    fm = get_failure_memory()
    user_id = "demo_user_3"

    # 清理
    memory = get_memory()
    memory.clear_all(user_id)

    # 记录多种失败
    failures = [
        ("编译 C++ 代码", "语法错误: missing ';' before '}'"),
        ("实现哈希表", "逻辑错误: 哈希冲突处理不当"),
        ("调用外部 API", "网络错误: Connection timeout"),
        ("配置数据库", "配置错误: 密码错误"),
        ("编写测试用例", "逻辑错误: 边界条件未覆盖"),
    ]

    for action, error in failures:
        record_failure(
            user_id=user_id,
            action=action,
            error_message=error,
            context="测试上下文",
            lesson=f"教训: {action} 需要注意"
        )

    # 测试相关检索
    test_actions = [
        "编译 C++ 代码",
        "实现数据结构",
        "调用网络 API",
    ]

    print("\n【相关失败检索测试】")
    for action in test_actions:
        relevant = fm.get_relevant_failures(user_id, action, limit=2)
        print(f"\n当前操作: '{action}'")
        print(f"  相关失败: {len(relevant)} 个")
        for i, f in enumerate(relevant, 1):
            print(f"  {i}. {f.action} → {f.error_message[:50]}...")


def example_4_lesson_extraction_and_prompt_formatting():
    """示例4: 教训提取与提示词格式化"""
    print("\n" + "=" * 70)
    print("示例4: 教训提取与提示词格式化 (用于提示词注入)")
    print("=" * 70)

    fm = get_failure_memory()
    user_id = "demo_user_4"

    # 清理
    memory = get_memory()
    memory.clear_all(user_id)

    # 记录带有教训的失败
    failures_data = [
        {
            "action": "实现文件解析器",
            "error": "运行时错误: 缓冲区溢出",
            "lesson": "必须检查输入大小，使用 std::vector.reserve() 预分配"
        },
        {
            "action": "设计数据库模式",
            "error": "逻辑错误: 未规范化导致数据冗余",
            "lesson": "遵循第三范式，消除传递依赖"
        },
        {
            "action": "编写并发代码",
            "error": "竞态条件: 多个线程同时修改共享变量",
            "lesson": "使用互斥锁保护共享资源，或使用原子操作"
        },
    ]

    for data in failures_data:
        record_failure(
            user_id=user_id,
            action=data["action"],
            error_message=data["error"],
            context="测试",
            lesson=data["lesson"]
        )

    # 获取失败并格式化
    failures = fm.get_user_failures(user_id, resolved_only=False, limit=5)
    formatted = fm.format_for_prompt(failures, max_chars=800)

    print("\n【格式化后的失败经验 (用于提示词注入)】")
    print("-" * 50)
    print(formatted)
    print("-" * 50)

    # 测试教训提取
    print("\n【教训提取测试】")
    test_responses = [
        """这是一个正常响应，没有教训。""",
        """-- lesson
遇到错误时应该先检查日志，再尝试修复。
--""",
        """其他内容
-- lesson
多线程编程必须加锁保护共享状态。
--
更多内容""",
    ]

    for resp in test_responses:
        lesson = fm.extract_lesson_from_response(resp)
        if lesson:
            print(f"  提取到教训: {lesson[:60]}...")
        else:
            print(f"  未提取到教训")


def example_5_integration_with_attention_manager():
    """示例5: 与 AttentionManager 集成"""
    print("\n" + "=" * 70)
    print("示例5: 与 AttentionManager 集成 (完整工作流)")
    print("=" * 70)

    from attention_manager import AttentionManager

    am = AttentionManager()
    user_id = "demo_user_5"

    # 清理
    memory = get_memory()
    memory.clear_all(user_id)

    # 先记录一些失败
    fm = get_failure_memory()
    record_failure(
        user_id=user_id,
        action="实现 JSON 解析器",
        error_message="解析错误: 无效的 JSON 格式",
        lesson="使用 try-catch 处理解析异常，验证输入格式"
    )

    record_failure(
        user_id=user_id,
        action="优化数据库查询",
        error_message="性能错误: N+1 查询问题",
        lesson="使用 JOIN 或批量查询减少数据库往返"
    )

    # 构建提示词，自动包含相关失败
    prompt = am.build_optimized_prompt(
        user_input="帮我实现一个 JSON 解析器",
        chat_id=user_id,
        include_meta_prompt=False,
    )

    print("\n【生成的提示词中是否包含失败经验？】")
    print("-" * 50)

    if "【⚠️ 相关失败经验 - 避免重复犯错】" in prompt:
        print("✓ 包含失败经验部分")

        # 提取失败经验部分
        sections = prompt.split(am.SECTION_SEPARATOR.strip())
        for section in sections:
            if "相关失败经验" in section:
                print("\n失败经验内容:")
                print("-" * 30)
                lines = section.strip().split("\n")
                for line in lines[:10]:  # 只显示前10行
                    print(f"  {line}")
                break
    else:
        print("✗ 未包含失败经验部分")

    print("\n【Manus 原则应用】")
    print("  • 失败保留在上下文中，而不是被清理")
    print("  • 在尝试类似操作前展示历史失败")
    print("  • 创建自我纠正的反馈循环")


def cleanup():
    """清理测试数据"""
    demo_users = ["demo_user", "demo_user_2", "demo_user_3", "demo_user_4", "demo_user_5"]
    memory = get_memory()
    for user in demo_users:
        memory.clear_all(user)


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " Failure Memory 使用示例 (阶段3) ".center(68) + "║")
    print("║" + " Manus: Keep Failures in Context ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    try:
        example_1_basic_failure_recording()
        example_2_recurrence_tracking()
        example_3_relevant_failure_retrieval()
        example_4_lesson_extraction_and_prompt_formatting()
        example_5_integration_with_attention_manager()

        print("\n" + "=" * 70)
        print("所有示例运行完成!")
        print("=" * 70)
        print("""
阶段3 核心改进总结:

1. 【失败保留机制】
   - 错误分类 (8种类型，自动检测)
   - 重复失败跟踪 (识别模式)
   - 教训提取 (-- lesson 格式)

2. 【相关失败检索】
   - 在操作前检索历史失败
   - 相关性评分 (操作匹配度 + 重复次数)
   - 格式化注入提示词

3. 【注意力管理器集成】
   - 自动添加到提示词 (失败经验部分)
   - 防止重复犯错 (Manus 第5课)

4. 【Telegram 命令】
   - /failures - 查看失败统计和记录
   - /lessons - 查看已学到的教训
   - /failures resolve <ID> - 标记为已解决

预期效果:
  • 减少错误重复率 ~42% (Manus 研究)
  • 创建自我纠正的反馈循环
  • 显性化隐式知识 (失败 → 教训)
""")

    finally:
        cleanup()
        print("\n✅ 测试数据已清理")