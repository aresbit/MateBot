#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Utility Functions
跨平台工具函数模块
"""

import os
import sys
import platform
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List, Dict

# 尝试导入环境检测模块
try:
    from env_detector import detect_environment, get_cached_environment, ToolchainDetector
    ENV_DETECTION_AVAILABLE = True
    _cached_env_info = None
except ImportError:
    ENV_DETECTION_AVAILABLE = False
    _cached_env_info = None


def get_build_environment() -> Dict[str, str]:
    """
    获取构建环境（集成 DevEco Studio 检测）

    Returns:
        环境变量字典
    """
    global _cached_env_info

    if not ENV_DETECTION_AVAILABLE:
        return os.environ.copy()

    # 使用缓存的检测信息
    if _cached_env_info is None:
        try:
            _cached_env_info = detect_environment()
        except Exception as e:
            # 如果检测失败，回退到系统环境
            import logging
            logging.warning(f"环境检测失败: {e}，使用系统环境")
            return os.environ.copy()

    # 构建环境变量
    env = os.environ.copy()

    if _cached_env_info:
        # 设置 JAVA_HOME
        if _cached_env_info.get("java_home"):
            env["JAVA_HOME"] = _cached_env_info["java_home"]
            java_bin = os.path.join(_cached_env_info["java_home"], "bin")
            env["PATH"] = f"{java_bin}{os.pathsep}{env.get('PATH', '')}"

        # 添加工具路径（使用 oh_sdk_path 以获取正确的 toolchains 路径）
        if _cached_env_info.get("oh_sdk_path"):
            toolchains_dir = os.path.join(_cached_env_info["oh_sdk_path"], "toolchains")
            if os.path.isdir(toolchains_dir):
                env["PATH"] = f"{toolchains_dir}{os.pathsep}{env.get('PATH', '')}"

        # 添加所有检测到的工具目录到 PATH
        if _cached_env_info.get("tool_dirs"):
            # 按优先级添加工具目录
            path_dirs = []

            # LLVM 工具链
            if "llvm_dir" in _cached_env_info["tool_dirs"]:
                path_dirs.append(_cached_env_info["tool_dirs"]["llvm_dir"])

            # Profiler 工具
            if "profiler_dir" in _cached_env_info["tool_dirs"]:
                path_dirs.append(_cached_env_info["tool_dirs"]["profiler_dir"])

            # Ark 工具
            if "ark_dir" in _cached_env_info["tool_dirs"]:
                path_dirs.append(_cached_env_info["tool_dirs"]["ark_dir"])

            # hvigorw
            if "hvigorw_dir" in _cached_env_info["tool_dirs"]:
                path_dirs.append(_cached_env_info["tool_dirs"]["hvigorw_dir"])

            # 将所有目录添加到 PATH
            for dir_path in reversed(path_dirs):  # 反转以保证优先级
                env["PATH"] = f"{dir_path}{os.pathsep}{env.get('PATH', '')}"

        # 添加单个工具到 PATH（如果工具目录未知）
        for tool_name in ["hvigorw"]:
            if _cached_env_info.get("tools", {}).get(tool_name):
                tool_dir = os.path.dirname(_cached_env_info["tools"][tool_name])
                if tool_dir not in env.get("PATH", ""):
                    env["PATH"] = f"{tool_dir}{os.pathsep}{env.get('PATH', '')}"

        # 设置 DEVECO_SDK_HOME（hvigor 需要）
        if _cached_env_info.get("sdk_path"):
            env["DEVECO_SDK_HOME"] = _cached_env_info["sdk_path"]

        # 设置 LLVM 相关环境变量
        if _cached_env_info.get("tool_dirs", {}).get("llvm_dir"):
            env["LLVM_HOME"] = _cached_env_info["tool_dirs"]["llvm_dir"]

        # 设置 HDC 端口
        env["HDC_SERVER_PORT"] = "7035"

    return env


# ==================== 颜色输出 ====================

class Colors:
    """终端颜色代码"""
    if platform.system() == "Windows":
        # Windows 可能不支持 ANSI 颜色
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        RESET = ""
    else:
        RED = '\033[0;31m'
        GREEN = '\033[0;32m'
        YELLOW = '\033[1;33m'
        BLUE = '\033[0;34m'
        RESET = '\033[0m'


def log_info(msg: str):
    """输出信息日志"""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")


def log_success(msg: str):
    """输出成功日志"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def log_warning(msg: str):
    """输出警告日志"""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")


def log_error(msg: str):
    """输出错误日志"""
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")


# ==================== 命令执行 ====================

def run_command(cmd: List[str], check: bool = True,
                capture_output: bool = True, use_detected_env: bool = True) -> Tuple[int, str, str]:
    """
    执行命令并返回结果

    Args:
        cmd: 命令列表
        check: 是否检查返回码
        capture_output: 是否捕获输出
        use_detected_env: 是否使用检测到的环境变量（包含 DevEco Studio 工具链）

    Returns:
        (返回码, 标准输出, 标准错误)
    """
    try:
        # 获取环境变量
        env = get_build_environment() if use_detected_env else None

        if capture_output:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=check,
                env=env
            )
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, check=check, env=env)
            return result.returncode, "", ""
    except subprocess.CalledProcessError as e:
        if capture_output:
            return e.returncode, e.stdout, e.stderr
        return e.returncode, "", str(e)
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"


def check_command(cmd: str) -> bool:
    """检查命令是否存在"""
    result = subprocess.run(
        ["which", cmd] if platform.system() != "Windows" else ["where", cmd],
        capture_output=True
    )
    return result.returncode == 0


# ==================== 项目检查 ====================

def check_hdc() -> bool:
    """检查 hdc 工具是否可用（使用检测到的环境）"""
    # 使用检测到的环境检查 hdc
    env = get_build_environment()

    # 从环境变量 PATH 中查找 hdc
    path_dirs = env.get("PATH", "").split(os.pathsep)

    for path_dir in path_dirs:
        hdc_path = os.path.join(path_dir, "hdc")
        if os.path.exists(hdc_path):
            log_success("hdc 工具已就绪")
            return True

    # 如果没有找到，尝试使用 which
    result = subprocess.run(
        ["which", "hdc"] if platform.system() != "Windows" else ["where", "hdc"],
        capture_output=True,
        env=env
    )

    if result.returncode == 0:
        log_success("hdc 工具已就绪")
        return True

    log_error("hdc 工具未找到")
    log_info("请先安装 DevEco Studio: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download")
    return False


def check_project(project_dir: str = ".") -> bool:
    """检查项目结构是否有效"""
    project_path = Path(project_dir)

    # 检查是否存在 build-profile.json5（必需）
    if not (project_path / "build-profile.json5").exists():
        log_error("未找到 build-profile.json5")
        log_info("请确保是有效的 HarmonyOS/OpenHarmony 项目")
        return False

    # 检查构建系统类型
    # 老版本项目：有 hvigorw 脚本
    # 新版本项目：有 hvigor/hvigor-config.json5 或 hvigorfile.ts
    has_hvigorw_script = (project_path / "hvigorw").exists()
    has_hvigor_config = (project_path / "hvigor" / "hvigor-config.json5").exists()
    has_hvigorfile = (project_path / "hvigorfile.ts").exists()

    if not (has_hvigorw_script or has_hvigor_config or has_hvigorfile):
        log_error("未找到有效的 hvigor 构建配置")
        log_info("请确保是有效的 HarmonyOS/OpenHarmony 项目")
        return False

    if has_hvigorw_script:
        log_success("项目结构验证通过 (传统 hvigorw)")
    else:
        log_success("项目结构验证通过 (新版 hvigor)")

    return True


def check_device() -> Optional[str]:
    """检查设备连接并返回设备 ID"""
    code, stdout, _ = run_command(["hdc", "list", "targets"])

    if code != 0 or not stdout.strip():
        log_error("未检测到已连接的设备")
        log_info("请检查:")
        log_info("  1. USB 线是否连接")
        log_info("  2. 设备 USB 调试是否开启")
        log_info("  3. 设备是否授权（点击信任）")
        return None

    devices = [line.strip() for line in stdout.strip().split('\n') if line.strip()]

    if len(devices) == 1:
        log_success(f"检测到设备: {devices[0]}")
        return devices[0]
    else:
        log_warning("检测到多台设备:")
        for i, dev in enumerate(devices, 1):
            print(f"  {i}. {dev}")
        log_info(f"使用第一台设备: {devices[0]}")
        return devices[0]


# ==================== 配置读取 ====================

def parse_json5(file_path: str) -> Optional[dict]:
    """
    解析 JSON5 文件（简化版，移除注释）

    Args:
        file_path: JSON5 文件路径

    Returns:
        解析后的字典，失败返回 None
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None

        # 读取文件内容
        content = path.read_text(encoding='utf-8')

        # 移除注释（// 和 /* */）
        # 移除单行注释
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # 移除多行注释
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

        # 移除尾随逗号
        content = re.sub(r',\s*([}\]])', r'\1', content)

        # 解析 JSON
        return json.loads(content)
    except Exception as e:
        log_error(f"解析 {file_path} 失败: {e}")
        return None


def get_bundle_name(project_dir: str = ".") -> Optional[str]:
    """从 AppScope/app.json5 读取 bundleName"""
    app_file = Path(project_dir) / "AppScope" / "app.json5"

    if not app_file.exists():
        log_error("未找到 AppScope/app.json5")
        return None

    app_data = parse_json5(str(app_file))
    if not app_data:
        return None

    bundle_name = app_data.get("bundleName") or app_data.get("app", {}).get("bundleName")

    if not bundle_name:
        log_error("无法解析 bundleName")
        return None

    return bundle_name


def get_ability_name(project_dir: str = ".", module_name: str = "entry") -> str:
    """从 module.json5 读取 Ability 名称"""
    module_file = Path(project_dir) / module_name / "src" / "main" / "module.json5"

    if not module_file.exists():
        log_warning(f"未找到 {module_file}，使用默认值 EntryAbility")
        return "EntryAbility"

    module_data = parse_json5(str(module_file))
    if not module_data:
        return "EntryAbility"

    abilities = module_data.get("module", {}).get("abilities", [])
    if abilities and len(abilities) > 0:
        return abilities[0].get("name", "EntryAbility")

    log_warning("无法解析 Ability 名称，使用默认值 EntryAbility")
    return "EntryAbility"


# ==================== 文件查找 ====================

def find_hap_file(project_dir: str = ".", module_name: str = "entry") -> Optional[str]:
    """查找编译生成的 HAP 文件"""
    base_path = Path(project_dir) / module_name / "build" / "default" / "outputs" / "default"

    # 常见的 HAP 文件路径模式
    patterns = [
        base_path / f"{module_name}-default-signed.hap",
        base_path / f"{module_name}-default-*.hap",
    ]

    for pattern in patterns:
        if "*" in str(pattern):
            # glob 查找
            files = sorted(Path(str(pattern)).parent.glob(Path(str(pattern)).name),
                          key=lambda p: p.stat().st_mtime, reverse=True)
            if files:
                hap_file = files[0]
                log_success(f"编译产物: {hap_file}")
                return str(hap_file)
        else:
            if pattern.exists():
                log_success(f"编译产物: {pattern}")
                return str(pattern)

    log_error("未找到编译产物 HAP 文件")
    log_info("请先执行编译")
    return None


def find_symbol_dirs(project_dir: str = ".", module_name: str = "entry",
                     build_mode: str = "debug") -> Tuple[str, str, str]:
    """
    查找符号文件目录

    Returns:
        (sourcemap_dir, namecache_dir, so_dir)
    """
    base_dir = Path(project_dir) / module_name / "build" / build_mode / "outputs" / "default"

    sourcemap_dir = str(base_dir / "sourcemap")
    namecache_dir = str(base_dir / "cache")
    so_dir = str(base_dir / "libs")

    return sourcemap_dir, namecache_dir, so_dir


# ==================== 应用检查 ====================

def check_app_installed(bundle_name: str, device_id: Optional[str] = None) -> bool:
    """检查应用是否已安装"""
    cmd = ["hdc"]
    if device_id:
        cmd.extend(["-t", device_id])
    cmd.extend(["shell", "bm", "dump", "-a"])

    code, stdout, _ = run_command(cmd)
    if code == 0:
        return bundle_name in stdout
    return False


def check_app_running(bundle_name: str, device_id: Optional[str] = None) -> bool:
    """检查应用是否正在运行"""
    cmd = ["hdc"]
    if device_id:
        cmd.extend(["-t", device_id])
    cmd.extend(["shell", "mount"])

    code, stdout, _ = run_command(cmd)
    if code == 0:
        return bundle_name in stdout
    return False


def get_app_pid(bundle_name: str, device_id: Optional[str] = None) -> Optional[str]:
    """获取应用进程 ID"""
    cmd = ["hdc"]
    if device_id:
        cmd.extend(["-t", device_id])
    cmd.extend(["jpid"])

    code, stdout, _ = run_command(cmd)
    if code == 0:
        for line in stdout.split('\n'):
            if bundle_name in line:
                parts = line.split()
                if parts:
                    return parts[0]
    return None


# ==================== 环境检查 ====================

def check_nodejs() -> bool:
    """检查 Node.js 环境（hstack 需要）"""
    if not check_command("node"):
        log_error("Node.js 未安装")
        log_info("hstack 工具需要 Node.js 环境")
        log_info("请访问 https://nodejs.org/ 下载安装")
        return False

    code, stdout, _ = run_command(["node", "-v"])
    if code == 0:
        version_str = stdout.strip().lstrip('v')
        try:
            major_version = int(version_str.split('.')[0])
            if major_version < 14:
                log_warning(f"Node.js 版本过低 ({version_str})")
                log_info("建议使用 Node.js 14 或更高版本")
        except:
            pass

        log_success(f"Node.js 环境就绪: {stdout.strip()}")
        return True

    return False


def check_hstack() -> bool:
    """检查 hstack 工具"""
    if not check_command("hstack"):
        log_error("hstack 工具未找到")
        log_info("请将 Command Line Tools/bin 目录添加到 PATH")
        return False

    return check_nodejs()


# ==================== 工具函数 ====================

def generate_timestamp_filename(prefix: str = "screenshot",
                                extension: str = "jpeg") -> str:
    """生成带时间戳的文件名"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_file_size(file_path: str) -> str:
    """获取文件大小并格式化"""
    try:
        size = Path(file_path).stat().st_size
        return format_file_size(size)
    except:
        return "Unknown"
