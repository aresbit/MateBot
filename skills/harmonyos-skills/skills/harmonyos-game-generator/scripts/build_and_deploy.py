#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HarmonyOS 游戏构建部署脚本
自动编译、安装到模拟器、启动应用
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def find_dev_tools():
    """查找 DevEco Studio 工具链"""
    # 常见路径
    possible_paths = [
        '/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains',
        os.path.expanduser('~/DevEco/sdk/default/openharmony/toolchains'),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def find_hvigorw(project_path):
    """查找 hvigorw 脚本"""
    # macOS/Linux
    hvigorw = os.path.join(project_path, 'hvigorw')
    if os.path.exists(hvigorw):
        return hvigorw

    # Windows
    hvigorw_bat = os.path.join(project_path, 'hvigorw.bat')
    if os.path.exists(hvigorw_bat):
        return hvigorw_bat

    return None


def build_project(project_path: str) -> tuple:
    """构建项目，返回 (success, hap_path)"""
    print("🔨 编译项目...")

    hvigorw = find_hvigorw(project_path)
    if not hvigorw:
        print("❌ 找不到 hvigorw 脚本")
        return False, None

    # 设置环境变量
    env = os.environ.copy()
    toolchains = find_dev_tools()
    if toolchains:
        env['PATH'] = f"{toolchains}{os.pathsep}{env.get('PATH', '')}"

    # 执行编译
    cmd = [hvigorw, 'assembleHap', '--mode', 'module', '-p', 'module=entry@default', '-p', 'product=default']

    try:
        result = subprocess.run(
            cmd,
            cwd=project_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode != 0:
            print(f"❌ 编译失败:")
            print(result.stderr)
            return False, None

        # 查找 HAP 文件
        hap_patterns = [
            'entry/build/default/outputs/default/entry-default-unsigned.hap',
            'entry/build/default/outputs/default/entry-default-signed.hap',
        ]

        for pattern in hap_patterns:
            hap_path = os.path.join(project_path, pattern)
            if os.path.exists(hap_path):
                print(f"✅ 编译成功: {hap_path}")
                return True, hap_path

        print("❌ 找不到编译产物")
        return False, None

    except subprocess.TimeoutExpired:
        print("❌ 编译超时")
        return False, None
    except Exception as e:
        print(f"❌ 编译异常: {e}")
        return False, None


def get_connected_devices(toolchains_path: str) -> list:
    """获取已连接设备列表"""
    hdc = os.path.join(toolchains_path, 'hdc')
    if not os.path.exists(hdc):
        return []

    try:
        result = subprocess.run(
            [hdc, 'list', 'targets'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            devices = [d.strip() for d in result.stdout.strip().split('\n') if d.strip()]
            return devices
    except:
        pass

    return []


def install_to_device(toolchains_path: str, hap_path: str, device: str) -> bool:
    """安装 HAP 到设备"""
    hdc = os.path.join(toolchains_path, 'hdc')
    print(f"📦 安装到设备: {device}")

    try:
        # 先连接设备（如果是网络设备）
        if ':' in device:
            subprocess.run([hdc, 'tconn', device], capture_output=True, timeout=10)

        # 安装 HAP
        result = subprocess.run(
            [hdc, '-t', device, 'install', '-r', hap_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if 'success' in result.stdout.lower() or result.returncode == 0:
            print(f"✅ 安装成功")
            return True
        else:
            print(f"❌ 安装失败: {result.stdout}")
            return False

    except Exception as e:
        print(f"❌ 安装异常: {e}")
        return False


def launch_app(toolchains_path: str, device: str, bundle_name: str) -> bool:
    """启动应用"""
    hdc = os.path.join(toolchains_path, 'hdc')
    print(f"🚀 启动应用...")

    try:
        result = subprocess.run(
            [hdc, '-t', device, 'shell', 'aa', 'start', '-a', 'EntryAbility', '-b', bundle_name],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print(f"✅ 启动成功")
            return True
        else:
            print(f"⚠️ 启动可能失败: {result.stdout}")
            return False

    except Exception as e:
        print(f"❌ 启动异常: {e}")
        return False


def get_bundle_name(project_path: str) -> str:
    """从项目配置获取包名"""
    build_profile = os.path.join(project_path, 'entry/build-profile.json5')
    if os.path.exists(build_profile):
        try:
            import json5
            with open(build_profile, 'r') as f:
                content = f.read()
                # 简单解析
                import re
                match = re.search(r'"bundleName"\s*:\s*"([^"]+)"', content)
                if match:
                    return match.group(1)
        except:
            pass

    # 尝试从 app.json5 获取
    app_json5 = os.path.join(project_path, 'AppScope/app.json5')
    if os.path.exists(app_json5):
        try:
            with open(app_json5, 'r') as f:
                content = f.read()
                import re
                match = re.search(r'"bundleName"\s*:\s*"([^"]+)"', content)
                if match:
                    return match.group(1)
        except:
            pass

    return ''


def main():
    parser = argparse.ArgumentParser(description='HarmonyOS 游戏构建部署工具')
    parser.add_argument('project_path', help='项目路径')
    parser.add_argument('--device', '-d', help='指定设备 (默认使用模拟器)')
    parser.add_argument('--no-launch', action='store_true', help='不自动启动应用')
    args = parser.parse_args()

    print("\n🎮 HarmonyOS 游戏构建部署工具\n")

    # 查找工具链
    toolchains = find_dev_tools()
    if not toolchains:
        print("❌ 找不到 DevEco Studio 工具链")
        print("   请确保 DevEco Studio 已安装")
        return 1

    print(f"✓ 工具链: {toolchains}")

    # 构建项目
    success, hap_path = build_project(args.project_path)
    if not success:
        return 1

    # 获取设备列表
    devices = get_connected_devices(toolchains)
    if not devices:
        print("❌ 没有找到已连接的设备")
        return 1

    print(f"✓ 已连接设备: {', '.join(devices)}")

    # 选择设备
    target_device = args.device
    if not target_device:
        # 优先选择模拟器 (127.0.0.1)
        for d in devices:
            if d.startswith('127.0.0.1') or 'emulator' in d.lower():
                target_device = d
                break
        if not target_device:
            target_device = devices[0]

    print(f"✓ 目标设备: {target_device}")

    # 安装
    if not install_to_device(toolchains, hap_path, target_device):
        return 1

    # 启动
    if not args.no_launch:
        bundle_name = get_bundle_name(args.project_path)
        if bundle_name:
            launch_app(toolchains, target_device, bundle_name)

    print("\n✅ 部署完成!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
