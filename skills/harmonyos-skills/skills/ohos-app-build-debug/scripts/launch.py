#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Launch Script
启动 HarmonyOS/OpenHarmony 应用
"""

import sys
import time
import argparse
from pathlib import Path

# 添加工具函数路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from ohos_utils import (
    log_info, log_success, log_error, log_warning,
    run_command, check_hdc, check_device,
    get_bundle_name, get_ability_name,
    check_app_installed, get_app_pid
)


def launch_app(bundle_name: str = None, ability_name: str = "EntryAbility",
               device_id: str = None, project_dir: str = ".",
               module_name: str = "entry") -> int:
    """
    启动应用

    Args:
        bundle_name: 应用包名
        ability_name: Ability 名称
        device_id: 设备 ID
        project_dir: 项目根目录
        module_name: 模块名称

    Returns:
        0 成功, 非0 失败
    """
    log_info("启动应用...")
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

    # 3. 获取 bundleName
    if not bundle_name:
        bundle_name = get_bundle_name(project_dir)
        if not bundle_name:
            log_error("无法获取 bundleName")
            return 1

    # 4. 获取 Ability 名称
    if ability_name == "EntryAbility":
        ability_name = get_ability_name(project_dir, module_name)

    # 5. 检查应用是否已安装
    log_info("检查应用是否已安装...")
    if not check_app_installed(bundle_name, target_device):
        log_error(f"应用未安装: {bundle_name}")
        log_info("请先执行安装")
        return 1
    log_success("应用已安装")
    print()

    # 6. 显示启动信息
    log_info("启动信息:")
    print(f"  包名: {bundle_name}")
    print(f"  Ability: {ability_name}")
    print(f"  设备 ID: {target_device}")
    print()

    # 7. 执行启动命令
    log_info("启动应用...")
    print("```bash")

    launch_cmd = [
        "hdc", "-t", target_device, "shell",
        "aa", "start", "-a", ability_name, "-b", bundle_name
    ]

    print(" ".join(launch_cmd))
    print("```")
    print()

    code, stdout, stderr = run_command(launch_cmd, check=False)

    if code != 0:
        log_error("启动失败")
        log_info("常见原因:")
        log_info("  1. 应用未安装 - 先执行安装")
        log_info("  2. Ability 名称错误 - 检查 module.json5")
        log_info("  3. 包名错误 - 检查 AppScope/app.json5")
        log_info("  4. 设备兼容性问题 - 检查 API 级别")
        if stderr:
            print(stderr)
        return 1

    # 8. 等待应用启动
    log_info("等待应用启动...")
    time.sleep(2)
    print()

    # 9. 获取应用进程 ID
    log_info("查询应用进程...")
    app_pid = get_app_pid(bundle_name, target_device)

    if app_pid:
        log_success("应用已启动")
        log_success(f"进程 ID: {app_pid}")
        print()

        # 显示进程信息
        info_cmd = ["hdc", "-t", target_device, "shell", "ps", "-ef"]
        code, stdout, _ = run_command(info_cmd, check=False)
        if code == 0:
            for line in stdout.split('\n'):
                if app_pid in line:
                    print(line)
    else:
        log_warning("未检测到应用进程")
        log_info("应用可能已启动但未在进程中显示")

    print()
    log_success("启动完成")

    # 输出 PID 供后续使用
    if app_pid:
        print(app_pid)

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="启动 HarmonyOS/OpenHarmony 应用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --dir .                        # 从项目目录自动读取配置并启动
  %(prog)s -b com.example.app             # 指定包名启动
  %(prog)s -b com.example.app -a MainAbility  # 指定 Ability
        """
    )

    parser.add_argument(
        "-b", "--bundle",
        help="应用包名 (如果不指定，从项目目录读取)"
    )

    parser.add_argument(
        "-a", "--ability",
        default="EntryAbility",
        help="Ability 名称 (默认: EntryAbility)"
    )

    parser.add_argument(
        "-d", "--device",
        help="设备 ID (可选)"
    )

    parser.add_argument(
        "-m", "--module",
        default="entry",
        help="模块名称 (默认: entry)"
    )

    parser.add_argument(
        "--dir",
        default=".",
        help="项目根目录 (用于自动读取配置)"
    )

    args = parser.parse_args()

    return launch_app(args.bundle, args.ability, args.device,
                     args.dir, args.module)


if __name__ == "__main__":
    sys.exit(main())
