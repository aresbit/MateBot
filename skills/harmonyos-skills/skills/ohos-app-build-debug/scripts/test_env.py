#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Environment Test
测试环境检测功能
"""

import sys
import os
from pathlib import Path

# 添加工具函数路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from env_detector import (
    DevEcoDetector,
    ToolchainDetector,
    detect_environment,
    print_detection_report,
    get_cached_environment,
    validate_cache
)

from ohos_utils import log_info, log_success, log_error, log_warning


def test_deveco_detection():
    """测试 DevEco Studio 检测"""
    log_info("=" * 60)
    log_info("测试 DevEco Studio 检测")
    log_info("=" * 60)
    print()

    detector = DevEcoDetector()
    deveco_info = detector.detect_all()

    if deveco_info:
        log_success("✓ DevEco Studio 检测成功")
        print(f"安装路径: {deveco_info.get('installation_path')}")
        print(f"平台: {deveco_info.get('platform')}")
        print(f"SDK 路径: {deveco_info.get('sdk_path')}")
        print(f"Java Home: {deveco_info.get('java_home')}")

        tools = deveco_info.get('tools', {})
        if tools:
            print("可用工具:")
            for name, path in tools.items():
                print(f"  {name}: {path}")
    else:
        log_warning("✗ 未检测到 DevEco Studio")

    print()
    return deveco_info  # 返回 deveco_info 而不是 True/False


def test_toolchain_detection(deveco_info=None):
    """测试工具链检测"""
    log_info("=" * 60)
    log_info("测试工具链检测")
    log_info("=" * 60)
    print()

    detector = ToolchainDetector(deveco_info)
    toolchain_info = detector.detect_all()

    print(f"检测源: {toolchain_info.get('source')}")
    print(f"Java Home: {toolchain_info.get('java_home')}")
    print(f"SDK Path: {toolchain_info.get('sdk_path')}")

    tools = toolchain_info.get('tools', {})
    if tools:
        print("可用工具:")
        for name, path in tools.items():
            print(f"  {name}: {path}")

    # 测试环境变量获取
    print()
    log_info("构建环境变量:")
    env = detector.get_build_environment()

    if env.get("JAVA_HOME"):
        print(f"  JAVA_HOME: {env['JAVA_HOME']}")

    if env.get("HDC_SERVER_PORT"):
        print(f"  HDC_SERVER_PORT: {env['HDC_SERVER_PORT']}")

    print(f"  PATH 包含: {len(env.get('PATH', '').split(os.pathsep))} 个目录")

    print()
    return toolchain_info


def test_cache():
    """测试缓存功能"""
    log_info("=" * 60)
    log_info("测试缓存功能")
    log_info("=" * 60)
    print()

    # 1. 清除旧缓存
    cache_file = os.path.expanduser("~/.ohos_build_debug_cache.json")
    if os.path.exists(cache_file):
        os.remove(cache_file)
        log_info("已清除旧缓存")

    # 2. 生成新缓存
    log_info("生成新缓存...")
    env_info = detect_environment(force_refresh=True)

    if env_info:
        # 3. 读取缓存
        log_info("读取缓存...")
        cached = get_cached_environment()

        if cached:
            log_success("✓ 缓存读取成功")

            # 4. 验证缓存
            log_info("验证缓存...")
            if validate_cache(cached):
                log_success("✓ 缓存验证通过")
            else:
                log_warning("⚠ 缓存验证失败")
        else:
            log_error("✗ 缓存读取失败")
    else:
        log_warning("环境检测失败，无法生成缓存")

    print()


def test_integration():
    """集成测试"""
    log_info("=" * 60)
    log_info("集成测试")
    log_info("=" * 60)
    print()

    log_info("使用统一的 detect_environment() 接口...")
    env_info = detect_environment(force_refresh=True)

    print()
    print_detection_report(env_info)

    return env_info


def main():
    """运行所有测试"""
    print()
    log_success("OHOS Build & Debug - 环境检测测试")
    print()

    # 测试 1: DevEco Studio 检测
    deveco_info = test_deveco_detection()

    # 测试 2: 工具链检测
    test_toolchain_detection(deveco_info)

    # 测试 3: 缓存功能
    test_cache()

    # 测试 4: 集成测试
    test_integration()

    log_success("测试完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        log_warning("测试被中断")
    except Exception as e:
        log_error(f"测试出错: {e}")
        import traceback
        traceback.print_exc()
