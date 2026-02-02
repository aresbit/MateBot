#!/usr/bin/env python3
"""
KV-Cache 使用示例 - 核心KV-Cache存储实现 (阶段4)

核心功能:
1. 真正的KV-Cache存储（非仅结构优化）
2. 基于静态前缀哈希和用户ID的缓存键生成
3. TTL缓存失效策略
4. 缓存命中率统计
"""

import os
import time
from kv_cache import get_kv_cache, cache_prompt, get_cached_prompt, get_cache_stats
from attention_manager import AttentionManager


def example_1_basic_cache_operations():
    """示例1: 基础缓存操作"""
    print("=" * 70)
    print("示例1: 基础缓存操作")
    print("=" * 70)

    # 获取缓存实例
    cache = get_kv_cache()

    # 模拟静态前缀和用户ID
    static_prefix = """【系统指令 - MateCode 编程助手】
你是一个专业的软件开发助手，擅长现代C++和TypeScript开发。"""
    user_id = "test_user_123"

    # 生成缓存键
    cache_key = cache.generate_cache_key(static_prefix, user_id)
    print(f"生成的缓存键: {cache_key}")
    print()

    # 模拟提示词
    full_prompt = f"""{static_prefix}

【用户输入】
帮我设计一个用户认证系统。

【当前任务】
实现JWT认证流程。
"""

    # 存储到缓存
    print("存储提示词到缓存...")
    success = cache.store_prompt(
        cache_key=cache_key,
        full_prompt=full_prompt,
        static_prefix=static_prefix,
        user_id=user_id,
        ttl_seconds=60  # 60秒TTL
    )
    print(f"存储成功: {success}")
    print()

    # 从缓存获取
    print("从缓存获取提示词...")
    cached = cache.get_cached_prompt(cache_key)
    if cached:
        print("✅ 缓存命中!")
        print(f"获取的提示词长度: {len(cached)} 字符")
        print(f"前100字符: {cached[:100]}...")
    else:
        print("❌ 缓存未命中")
    print()

    # 获取统计信息
    stats = cache.get_stats()
    print("缓存统计:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def example_2_cache_hit_miss_simulation():
    """示例2: 缓存命中/未命中模拟"""
    print("\n" + "=" * 70)
    print("示例2: 缓存命中/未命中模拟")
    print("=" * 70)

    cache = get_kv_cache()
    static_prefix = "Test static prefix"
    user_id = "simulation_user"

    # 第一次查询 - 应未命中
    print("第一次查询 (预期: 未命中)...")
    cache_key = cache.generate_cache_key(static_prefix, user_id)
    cached = cache.get_cached_prompt(cache_key)
    print(f"结果: {'未命中' if cached is None else '命中'}")
    print()

    # 存储缓存
    prompt = f"{static_prefix}\n\nUser query: How to optimize SQL?"
    cache.store_prompt(cache_key, prompt, static_prefix, user_id, ttl_seconds=30)

    # 第二次查询 - 应命中
    print("第二次查询 (预期: 命中)...")
    cached = cache.get_cached_prompt(cache_key)
    print(f"结果: {'命中' if cached else '未命中'}")
    print()

    # 统计信息
    stats = cache.get_stats()
    print(f"命中率: {stats['hit_rate']:.1%} (命中: {stats['hit_count']}, 未命中: {stats['miss_count']})")


def example_3_attention_manager_integration():
    """示例3: 与AttentionManager集成"""
    print("\n" + "=" * 70)
    print("示例3: 与AttentionManager集成")
    print("=" * 70)

    am = AttentionManager()
    chat_id = "demo_chat_456"

    # 创建任务（用于任务目标）
    am.create_task(chat_id, "实现KV-Cache系统集成测试")

    # 第一次构建 - 应未命中
    print("第一次构建提示词 (预期: 缓存未命中)...")
    prompt1, cache_info1 = am.build_optimized_prompt_with_cache(
        user_input="如何测试KV-Cache性能？",
        chat_id=chat_id,
        ttl_seconds=30
    )
    print(f"缓存命中: {cache_info1['cache_hit']}")
    print(f"来源: {cache_info1.get('source', 'unknown')}")
    print(f"提示词长度: {len(prompt1)} 字符")
    print()

    # 第二次相同查询 - 应命中
    print("第二次相同查询 (预期: 缓存命中)...")
    prompt2, cache_info2 = am.build_optimized_prompt_with_cache(
        user_input="如何测试KV-Cache性能？",
        chat_id=chat_id,
        ttl_seconds=30
    )
    print(f"缓存命中: {cache_info2['cache_hit']}")
    print(f"来源: {cache_info2.get('source', 'unknown')}")
    print(f"提示词长度: {len(prompt2)} 字符")
    print()

    # 验证两次提示词相同
    if prompt1 == prompt2:
        print("✅ 两次提示词相同 (缓存工作正常)")
    else:
        print("❌ 两次提示词不同 (可能有问题)")

    # 获取缓存统计
    stats = am.get_cache_stats()
    print(f"\n缓存统计: 命中率 {stats['hit_rate']:.1%}")


def example_4_cache_invalidation():
    """示例4: 缓存失效"""
    print("\n" + "=" * 70)
    print("示例4: 缓存失效")
    print("=" * 70)

    cache = get_kv_cache()
    static_prefix = "Cache invalidation test"
    user_id = "invalidation_user"

    cache_key = cache.generate_cache_key(static_prefix, user_id)
    prompt = f"{static_prefix}\n\nTest content."

    # 存储缓存（短TTL）
    cache.store_prompt(cache_key, prompt, static_prefix, user_id, ttl_seconds=2)

    # 立即获取 - 应命中
    print("立即获取 (预期: 命中)...")
    cached = cache.get_cached_prompt(cache_key)
    print(f"结果: {'命中' if cached else '未命中'}")

    # 等待TTL过期
    print("等待3秒让缓存过期...")
    time.sleep(3)

    # 再次获取 - 应未命中（已过期）
    print("过期后获取 (预期: 未命中)...")
    cached = cache.get_cached_prompt(cache_key)
    print(f"结果: {'命中' if cached else '未命中'}")

    # 清理缓存
    cleared = cache.clear_cache()
    print(f"\n清理缓存: 删除了 {cleared} 个条目")


def example_5_convenience_functions():
    """示例5: 便捷函数使用"""
    print("\n" + "=" * 70)
    print("示例5: 便捷函数使用")
    print("=" * 70)

    static_prefix = "Convenience function test"
    user_id = "conv_user"
    prompt = f"{static_prefix}\n\nTesting convenience functions."

    # 使用便捷函数缓存
    print("使用 cache_prompt() 缓存...")
    success = cache_prompt(static_prefix, user_id, prompt, ttl_seconds=60)
    print(f"缓存成功: {success}")

    # 使用便捷函数获取
    print("使用 get_cached_prompt() 获取...")
    cached = get_cached_prompt(static_prefix, user_id)
    if cached:
        print(f"✅ 获取成功，长度: {len(cached)} 字符")

    # 使用便捷函数获取统计
    stats = get_cache_stats()
    print(f"\n全局缓存统计: {stats['hit_rate']:.1%} 命中率")


def main():
    """运行所有示例"""
    print("KV-Cache 系统示例 - 阶段4实现")
    print("=" * 70)

    try:
        example_1_basic_cache_operations()
        example_2_cache_hit_miss_simulation()
        example_3_attention_manager_integration()
        example_4_cache_invalidation()
        example_5_convenience_functions()

        print("\n" + "=" * 70)
        print("所有示例完成!")
        print("=" * 70)

        # 最终统计
        cache = get_kv_cache()
        stats = cache.get_stats()
        print(f"\n最终缓存统计:")
        for key, value in stats.items():
            if key not in ['cache_dir', 'db_path']:
                print(f"  {key}: {value}")

    except Exception as e:
        print(f"\n❌ 示例执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()