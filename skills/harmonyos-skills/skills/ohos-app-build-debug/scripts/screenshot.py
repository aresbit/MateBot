#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Screenshot Script
截取 HarmonyOS/OpenHarmony 设备屏幕
"""

import sys
import os
import argparse
import time
from pathlib import Path

# 添加工具函数路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from ohos_utils import (
    log_info, log_success, log_error,
    run_command, check_hdc, check_device,
    generate_timestamp_filename, get_file_size
)


def take_screenshot(output_dir: str = "./", device_id: str = None,
                   filename_prefix: str = "screenshot") -> int:
    """
    截取设备屏幕

    Args:
        output_dir: 输出目录
        device_id: 设备 ID
        filename_prefix: 文件名前缀

    Returns:
        0 成功, 非0 失败
    """
    log_info("截取设备屏幕...")
    print()

    # 1. 检查 hdc 工具
    if not check_hdc():
        return 1
    print()

    # 2. 检查设备连接
    log_info("检查设备连接...")
    detected_device = check_device()
    if not detected_device:
        return 1

    # 使用指定的设备或检测到的设备
    target_device = device_id or detected_device
    print()

    # 3. 检查输出目录
    output_path = Path(output_dir)
    if not output_path.exists():
        log_info(f"创建输出目录: {output_dir}")
        output_path.mkdir(parents=True, exist_ok=True)

    # 4. 生成本地文件名
    local_filename = generate_timestamp_filename(filename_prefix, "jpeg")
    local_path = str(output_path / local_filename)

    # 设备端临时文件路径
    device_path = f"/data/local/tmp/screenshot_{int(time.time())}.jpeg"

    # 5. 截图
    log_info("执行截图...")
    print("```bash")
    print(f"hdc -t {target_device} shell snapshot_display -f {device_path}")
    print("```")
    print()

    snapshot_cmd = ["hdc", "-t", target_device, "shell",
                    "snapshot_display", "-f", device_path]

    code, _, stderr = run_command(snapshot_cmd, check=False)

    if code != 0:
        log_error("截图失败")
        log_info("请确认设备支持 snapshot_display 命令")
        if stderr:
            print(stderr)
        return 1

    log_success(f"截图已保存到设备: {device_path}")
    print()

    # 6. 传输到本地
    log_info("传输到本地...")
    print("```bash")
    print(f"hdc -t {target_device} file recv {device_path} \"{local_path}\"")
    print("```")
    print()

    recv_cmd = ["hdc", "-t", target_device, "file", "recv",
                device_path, local_path]

    code, _, stderr = run_command(recv_cmd, check=False)

    if code != 0:
        log_error("文件传输失败")
        # 清理设备端文件
        run_command(["hdc", "-t", target_device, "shell", "rm", "-f", device_path],
                   check=False)
        if stderr:
            print(stderr)
        return 1

    log_success("文件传输成功")
    print()

    # 7. 清理设备端临时文件
    log_info("清理临时文件...")
    run_command(["hdc", "-t", target_device, "shell", "rm", "-f", device_path],
               check=False)
    log_success("清理完成")
    print()

    # 8. 显示结果
    file_size = get_file_size(local_path)
    log_success("截图已保存")
    log_info(f"路径: {local_path}")
    log_info(f"大小: {file_size}")
    print()

    # 输出文件路径
    print(local_path)

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="截取 HarmonyOS/OpenHarmony 设备屏幕",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                           # 截图并保存到当前目录
  %(prog)s -o ./screenshots          # 保存到指定目录
  %(prog)s -p app_screen -d DEVICE   # 指定前缀和设备
        """
    )

    parser.add_argument(
        "-o", "--output",
        default="./",
        help="输出目录 (默认: 当前目录)"
    )

    parser.add_argument(
        "-d", "--device",
        help="设备 ID (可选)"
    )

    parser.add_argument(
        "-p", "--prefix",
        default="screenshot",
        help="文件名前缀 (默认: screenshot)"
    )

    args = parser.parse_args()

    return take_screenshot(args.output, args.device, args.prefix)


if __name__ == "__main__":
    sys.exit(main())
