#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Install Script
安装 HAP 文件到设备
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
    run_command, check_hdc, check_device,
    get_bundle_name, get_file_size, check_app_installed
)


def install_hap(hap_file: str, device_id: str = None,
                reinstall: bool = True, user_id: str = None) -> int:
    """
    安装 HAP 文件到设备

    Args:
        hap_file: HAP 文件路径
        device_id: 设备 ID
        reinstall: 是否覆盖安装
        user_id: 用户 ID

    Returns:
        0 成功, 非0 失败
    """
    # 检查文件是否存在
    if not Path(hap_file).exists():
        log_error(f"HAP 文件不存在: {hap_file}")
        return 1

    log_info("安装应用到设备...")
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

    # 3. 显示安装信息
    file_size = get_file_size(hap_file)
    log_info("安装信息:")
    print(f"  HAP 文件: {hap_file}")
    print(f"  设备 ID: {target_device}")
    print(f"  文件大小: {file_size}")
    print()

    # 4. 执行安装
    log_info("安装到设备...")
    print("```bash")

    install_cmd = ["hdc", "-t", target_device, "install"]

    if reinstall:
        install_cmd.append("-r")

    if user_id:
        install_cmd.extend(["-u", user_id])

    install_cmd.append(hap_file)

    print(" ".join(install_cmd))
    print("```")
    print()

    code, stdout, stderr = run_command(install_cmd, check=False)

    if code != 0:
        log_error("安装失败")
        log_info("常见原因:")
        log_info("  1. 签名不匹配 - 确认使用调试证书签名")
        log_info("  2. 版本冲突 - 先卸载旧版本")
        log_info("  3. 存储不足 - 清理设备空间")
        log_info("  4. 权限问题 - 检查应用权限配置")
        if stderr:
            print(stderr)
        return 1

    log_success("安装成功")
    print()

    # 5. 尝试读取 bundleName
    project_dir = Path.cwd()
    bundle_name = None

    if (project_dir / "AppScope" / "app.json5").exists():
        bundle_name = get_bundle_name(str(project_dir))
        if bundle_name:
            log_success(f"应用包名: {bundle_name}")
            print()

    log_success("安装完成")

    # 输出 bundleName 供后续使用
    if bundle_name:
        print(bundle_name)

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="安装 HAP 文件到 HarmonyOS/OpenHarmony 设备",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -f app.hap                    # 安装 HAP 文件
  %(prog)s -f app.hap -d DEVICE_ID      # 指定设备安装
  %(prog)s -f app.hap --no-reinstall     # 不覆盖安装
        """
    )

    parser.add_argument(
        "-f", "--file",
        required=True,
        help="HAP 文件路径 (必需)"
    )

    parser.add_argument(
        "-d", "--device",
        help="设备 ID (可选，默认使用第一台设备)"
    )

    parser.add_argument(
        "-r", "--reinstall",
        action="store_true",
        default=True,
        help="覆盖安装 (默认启用)"
    )

    parser.add_argument(
        "--no-reinstall",
        action="store_false",
        dest="reinstall",
        help="不覆盖安装"
    )

    parser.add_argument(
        "-u", "--user",
        help="用户 ID"
    )

    args = parser.parse_args()

    return install_hap(args.file, args.device, args.reinstall, args.user)


if __name__ == "__main__":
    sys.exit(main())
