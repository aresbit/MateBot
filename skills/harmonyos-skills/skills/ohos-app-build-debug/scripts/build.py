#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Build Script
编译 HarmonyOS/OpenHarmony 应用
"""

import sys
import os
import argparse
from pathlib import Path

# 添加工具函数路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from ohos_utils import (
    log_info, log_success, log_error, log_warning,
    run_command, check_project, get_bundle_name,
    find_hap_file, get_file_size, get_build_environment
)

# 尝试导入环境检测
try:
    from env_detector import detect_environment, print_detection_report
    ENV_DETECTION_AVAILABLE = True
except ImportError:
    ENV_DETECTION_AVAILABLE = False


def build_app(project_dir: str = ".", mode: str = "debug",
              module_name: str = "entry", show_env: bool = False) -> int:
    """
    编译应用

    Args:
        project_dir: 项目根目录
        mode: 编译模式 (debug/release)
        module_name: 模块名称
        show_env: 是否显示环境检测信息

    Returns:
        0 成功, 非0 失败
    """
    log_info("开始编译 HarmonyOS/OpenHarmony 应用...")
    print()

    # 0. 环境检测（可选显示）
    if show_env and ENV_DETECTION_AVAILABLE:
        try:
            env_info = detect_environment()
            print_detection_report(env_info)
        except Exception as e:
            log_warning(f"环境检测失败: {e}")

    # 1. 检查项目结构
    log_info("检查项目结构...")
    if not check_project(project_dir):
        return 1
    print()

    # 2. 读取项目配置
    log_info("读取项目配置...")
    bundle_name = get_bundle_name(project_dir)
    if not bundle_name:
        return 1
    log_success(f"bundleName: {bundle_name}")
    print()

    # 3. 执行编译
    log_info(f"编译应用 (模式: {mode})...")
    print("```bash")

    # 构建编译命令
    build_cmd = [
        "hvigorw", "assembleHap",
        "--mode", "module",
        "-p", f"module={module_name}@default",
        "-p", "product=default"
    ]

    if mode == "release":
        build_cmd.extend(["-p", "buildMode=release"])

    print(" ".join(build_cmd))
    print("```")
    print()

    # 切换到项目目录执行
    original_dir = os.getcwd()
    os.chdir(project_dir)

    code, stdout, stderr = run_command(build_cmd, check=False, use_detected_env=True)

    os.chdir(original_dir)

    if code != 0:
        log_error("编译失败")
        log_info("请检查编译日志中的错误信息")
        if stderr:
            print(stderr)
        return 1

    log_success("编译成功")
    print()

    # 4. 查找编译产物
    log_info("查找编译产物...")
    hap_file = find_hap_file(project_dir, module_name)

    if not hap_file:
        log_error("未找到 HAP 文件")
        return 1

    file_size = get_file_size(hap_file)
    log_success(f"文件大小: {file_size}")
    print()

    # 5. 显示编译结果摘要
    log_info("编译摘要:")
    print(f"  模式: {mode}")
    print(f"  模块: {module_name}")
    print(f"  包名: {bundle_name}")
    print(f"  产物: {hap_file}")
    print()

    log_success("编译完成")

    # 输出 HAP 文件路径供后续使用
    print(hap_file)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="编译 HarmonyOS/OpenHarmony 应用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 使用默认设置编译 debug 版本
  %(prog)s -m release               # 编译 release 版本
  %(prog)s --dir /path/to/project   # 指定项目目录
  %(prog)s --module entry           # 指定模块名称
  %(prog)s --show-env               # 显示环境检测信息
        """
    )

    parser.add_argument(
        "-m", "--mode",
        choices=["debug", "release"],
        default="debug",
        help="编译模式 (默认: debug)"
    )

    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="项目根目录 (默认: 当前目录)"
    )

    parser.add_argument(
        "--module",
        default="entry",
        help="模块名称 (默认: entry)"
    )

    parser.add_argument(
        "--show-env",
        action="store_true",
        help="显示环境检测信息"
    )

    args = parser.parse_args()

    return build_app(args.dir, args.mode, args.module, args.show_env)


if __name__ == "__main__":
    sys.exit(main())
