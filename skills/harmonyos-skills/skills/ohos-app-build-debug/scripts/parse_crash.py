#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Crash Parse Script
解析 release 应用崩溃堆栈
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# 添加工具函数路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from ohos_utils import (
    log_info, log_success, log_error, log_warning,
    run_command, check_hstack, find_symbol_dirs, generate_timestamp_filename
)


def parse_crash(crash_file: str = None, crash_content: str = None,
                project_dir: str = ".", module_name: str = "entry",
                build_mode: str = "release", output_dir: str = None) -> int:
    """
    解析崩溃堆栈

    Args:
        crash_file: crash 文件或目录路径
        crash_content: 直接提供的 crash 堆栈内容
        project_dir: 项目根目录
        module_name: 模块名称
        build_mode: 编译模式
        output_dir: 输出目录

    Returns:
        0 成功, 非0 失败
    """
    log_info("解析崩溃堆栈...")
    print()

    # 1. 检查 hstack 工具
    if not check_hstack():
        return 1
    print()

    # 2. 确定 crash 输入
    crash_input = None
    is_file = False

    if crash_file:
        crash_path = Path(crash_file)
        if crash_path.is_file():
            crash_input = str(crash_path.absolute())
            is_file = True
            log_info(f"crash 文件: {crash_input}")
        elif crash_path.is_dir():
            crash_input = str(crash_path.absolute())
            is_file = True
            log_info(f"crash 目录: {crash_input}")
        else:
            log_error(f"crash 文件或目录不存在: {crash_file}")
            return 1
    elif crash_content:
        crash_input = crash_content
        log_info("crash 内容已提供")
    else:
        log_error("请提供 crash 文件或堆栈内容")
        log_info("用法: python parse_crash.py (-f crash文件 | -c \"堆栈内容\")")
        return 1

    print()

    # 3. 查找符号文件
    log_info("查找符号文件...")

    sourcemap_dir, namecache_dir, so_dir = find_symbol_dirs(
        project_dir, module_name, build_mode
    )

    # 检查 sourcemap
    use_sourcemap = False
    if Path(sourcemap_dir).exists() and list(Path(sourcemap_dir).iterdir()):
        log_success(f"sourcemap: {sourcemap_dir}")
        use_sourcemap = True
    else:
        log_warning(f"未找到 sourcemap 目录: {sourcemap_dir}")
        sourcemap_dir = None

    # 检查 nameCache
    use_namecache = False
    if Path(namecache_dir).exists() and list(Path(namecache_dir).iterdir()):
        log_success(f"nameCache: {namecache_dir}")
        use_namecache = True
    else:
        log_warning(f"未找到 nameCache 目录: {namecache_dir}")
        namecache_dir = None

    # 检查 so 目录
    use_so = False
    if Path(so_dir).exists() and list(Path(so_dir).iterdir()):
        log_success(f"so: {so_dir}")
        use_so = True
    else:
        log_warning(f"未找到 so 目录: {so_dir}")
        so_dir = None

    print()

    # 验证至少有一个符号文件
    if not use_sourcemap and not use_so:
        log_error("未找到任何符号文件")
        log_info("请确保已编译 release 版本")
        log_info("sourcemap 与 so 文件至少需要提供一项")
        return 1

    # 4. 构建解析命令
    hstack_cmd = ["hstack"]

    if is_file:
        # 文件或目录
        hstack_cmd.extend(["-i", crash_input])

        # 设置输出目录
        if not output_dir:
            output_dir = f"./crash_output_{generate_timestamp_filename('crash', '').rstrip('.jpeg')}"

        hstack_cmd.extend(["-o", output_dir])
    else:
        # 直接的堆栈内容
        hstack_cmd.extend(["-c", crash_input])

        # 如果指定了输出目录
        if output_dir:
            hstack_cmd.extend(["-o", output_dir])

    # 添加符号文件参数
    if sourcemap_dir:
        hstack_cmd.extend(["-s", sourcemap_dir])

    if so_dir:
        hstack_cmd.extend(["--so", so_dir])

    if namecache_dir:
        hstack_cmd.extend(["-n", namecache_dir])

    # 5. 执行解析
    log_info("解析堆栈...")
    print("```bash")
    print(" ".join(hstack_cmd))
    print("```")
    print()

    # 对于 -c 参数，使用 shell 执行以正确处理引号
    if not is_file:
        cmd_str = " ".join(hstack_cmd)
        code = os.system(cmd_str)
    else:
        code, _, stderr = run_command(hstack_cmd, check=False)

    print()

    if code != 0:
        log_error("解析失败")
        log_info("请检查:")
        log_info("  1. crash 堆栈格式是否正确")
        log_info("  2. 符号文件是否完整")
        log_info("  3. 符号文件是否与 crash 版本匹配")
        return 1

    log_success("解析完成")

    # 如果有输出目录，显示结果位置
    if output_dir and is_file:
        log_info(f"结果已保存到: {output_dir}")

        # 列出输出文件
        output_path = Path(output_dir)
        if output_path.exists():
            log_info("输出文件:")
            for file in sorted(output_path.iterdir()):
                if file.is_file():
                    print(f"  - {file.name}")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="解析 HarmonyOS/OpenHarmony 应用崩溃堆栈",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -f crash.txt                           # 解析 crash 文件
  %(prog)s -f crash/                              # 解析 crash 目录
  %(prog)s -c "at i (entry|entry|1.0.0|...)"      # 解析堆栈内容
  %(prog)s -f crash.txt --dir /path/to/project    # 指定项目目录
        """
    )

    parser.add_argument(
        "-f", "--file",
        help="crash 文件或目录"
    )

    parser.add_argument(
        "-c", "--content",
        help="直接指定堆栈内容"
    )

    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="项目根目录 (默认: 当前目录)"
    )

    parser.add_argument(
        "-m", "--module",
        default="entry",
        help="模块名称 (默认: entry)"
    )

    parser.add_argument(
        "--mode",
        default="release",
        choices=["debug", "release"],
        help="编译模式 (默认: release)"
    )

    parser.add_argument(
        "-o", "--output",
        help="输出目录"
    )

    args = parser.parse_args()

    # 验证参数
    if not args.file and not args.content:
        parser.error("请提供 -f crash文件 或 -c 堆栈内容")

    return parse_crash(args.file, args.content, args.dir,
                      args.module, args.mode, args.output)


if __name__ == "__main__":
    sys.exit(main())
