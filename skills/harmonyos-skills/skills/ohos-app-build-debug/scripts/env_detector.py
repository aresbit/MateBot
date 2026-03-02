#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OHOS App Build & Debug - Environment Detector
自动检测 DevEco Studio 和工具链环境
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class DevEcoDetector:
    """DevEco Studio 检测器"""

    def __init__(self):
        self.platform = platform.system()
        self.deveco_paths = []
        self.sdk_info = {}

    def detect_all(self) -> Optional[Dict[str, Any]]:
        """
        执行完整的 DevEco Studio 检测

        Returns:
            DevEco 环境信息字典，如果未检测到返回 None
        """
        logger.info("检测 DevEco Studio...")

        # 1. 查找 DevEco Studio 安装
        if self.platform == "Windows":
            deveco_paths = self._find_deveco_windows()
        elif self.platform == "Darwin":
            deveco_paths = self._find_deveco_macos()
        else:  # Linux
            deveco_paths = self._find_deveco_linux()

        if not deveco_paths:
            logger.warning("未找到 DevEco Studio 安装")
            return None

        logger.info(f"找到 {len(deveco_paths)} 个候选安装")

        # 2. 验证并分析每个安装
        valid_installations = []
        for path in deveco_paths:
            info = self._analyze_installation(path)
            if info and info.get("valid"):
                valid_installations.append(info)

        if not valid_installations:
            logger.warning("未找到有效的 DevEco Studio 安装")
            return None

        # 3. 选择最佳安装
        return self._select_best_installation(valid_installations)

    def _find_deveco_windows(self) -> List[str]:
        """Windows 平台检测 DevEco Studio"""
        candidates = []

        # 1. 常见安装位置
        common_paths = [
            "C:/Program Files/Huawei/DevEco Studio",
            "C:/Program Files/DevEco Studio",
            "C:/Program Files (x86)/DevEco Studio",
            os.path.expandvars("%LOCALAPPDATA%/Huawei/DevEco Studio"),
            os.path.expandvars("%APPDATA%/Huawei/DevEco Studio"),
        ]

        # 2. 环境变量
        custom_path = os.environ.get("DEVECO_STUDIO_PATH")
        if custom_path:
            common_paths.insert(0, custom_path)

        # 3. 注册表查找（仅 Windows）
        try:
            import winreg
            reg_paths = [
                r"SOFTWARE\Huawei\DevEco Studio",
                r"SOFTWARE\WOW6432Node\Huawei\DevEco Studio",
            ]

            for reg_path in reg_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    path, _ = winreg.QueryValueEx(key, "InstallLocation")
                    candidates.append(path)
                    winreg.CloseKey(key)
                except:
                    pass

            # 检查用户注册表
            for reg_path in reg_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
                    path, _ = winreg.QueryValueEx(key, "InstallLocation")
                    candidates.append(path)
                    winreg.CloseKey(key)
                except:
                    pass
        except ImportError:
            pass

        # 4. 验证路径
        valid_paths = []
        for path in set(common_paths + candidates):
            if os.path.isdir(path) and self._is_deveco_installation(path):
                valid_paths.append(path)

        return valid_paths

    def _find_deveco_macos(self) -> List[str]:
        """macOS 平台检测 DevEco Studio"""
        candidates = []

        # 1. 标准 Applications 目录
        app_paths = [
            "/Applications",
            os.path.expanduser("~/Applications"),
        ]

        for base in app_paths:
            # 尝试不同的命名
            for app_name in ["DevEco-Studio.app", "DevEco Studio.app"]:
                app_path = os.path.join(base, app_name)
                if os.path.isdir(app_path):
                    candidates.append(app_path)

        # 2. 使用 mdfind 搜索
        try:
            result = subprocess.run(
                ["mdfind", "kMDItemDisplayName == 'DevEco-Studio.app'"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line and os.path.isdir(line):
                        candidates.append(line)
        except:
            pass

        # 3. 环境变量
        custom_path = os.environ.get("DEVECO_STUDIO_PATH")
        if custom_path and os.path.isdir(custom_path):
            candidates.append(custom_path)

        return list(set(candidates))

    def _find_deveco_linux(self) -> List[str]:
        """Linux 平台检测 DevEco Studio"""
        candidates = []

        # 1. 常见安装位置
        common_paths = [
            "/opt/deveco-studio",
            "/opt/DevEco-Studio",
            os.path.expanduser("~/deveco-studio"),
            os.path.expanduser("~/DevEco-Studio"),
            "/usr/local/DevEco-Studio",
            "/usr/local/deveco-studio",
        ]

        # 2. 环境变量
        custom_path = os.environ.get("DEVECO_STUDIO_PATH")
        if custom_path:
            common_paths.insert(0, custom_path)

        # 3. 从桌面文件查找
        desktop_dirs = [
            "/usr/share/applications",
            os.path.expanduser("~/.local/share/applications"),
        ]

        for dir_path in desktop_dirs:
            if not os.path.isdir(dir_path):
                continue
            try:
                for file in os.listdir(dir_path):
                    if "deveco" in file.lower() and file.endswith(".desktop"):
                        try:
                            with open(os.path.join(dir_path, file), 'r') as f:
                                for line in f:
                                    if line.startswith("Exec="):
                                        exec_path = line.split("=", 1)[1].strip().split()[0]
                                        exec_dir = os.path.dirname(os.path.dirname(exec_path))
                                        if os.path.isdir(exec_dir):
                                            candidates.append(exec_dir)
                                        break
                        except:
                            pass
            except:
                pass

        # 4. 验证并去重
        valid_paths = []
        for path in set(common_paths + candidates):
            if os.path.isdir(path) and self._is_deveco_installation(path):
                valid_paths.append(path)

        return valid_paths

    def _is_deveco_installation(self, path: str) -> bool:
        """验证路径是否为 DevEco Studio 安装"""
        # 检查关键文件/目录
        if self.platform == "Darwin":  # macOS
            contents_path = os.path.join(path, "Contents")
            if not os.path.isdir(contents_path):
                return False
            # 检查特征文件
            key_files = ["Info.plist", "MacOS/devecostudio"]
            for key_file in key_files:
                if os.path.exists(os.path.join(contents_path, key_file)):
                    return True
        else:  # Windows/Linux
            # 检查特征目录
            key_dirs = ["plugins", "lib", "bin"]
            matches = sum(1 for d in key_dirs if os.path.isdir(os.path.join(path, d)))
            if matches >= 2:
                return True

        return False

    def _analyze_installation(self, path: str) -> Optional[Dict[str, Any]]:
        """分析 DevEco 安装，提取工具路径"""
        # 根据平台确定内部路径
        if self.platform == "Darwin":  # macOS
            contents_path = os.path.join(path, "Contents")
        else:  # Windows/Linux
            contents_path = path

        info = {
            "installation_path": path,
            "platform": self.platform,
            "tools": {},
            "tool_dirs": {},  # 新增：存储工具目录
            "valid": False
        }

        # 1. 查找 SDK 目录
        sdk_path = os.path.join(contents_path, "sdk")
        if os.path.isdir(sdk_path):
            info["sdk_path"] = sdk_path

            # 查找 OpenHarmony SDK
            oh_sdk_paths = [
                os.path.join(sdk_path, "default", "openharmony"),
                os.path.join(sdk_path, "openharmony"),
            ]

            for oh_sdk_path in oh_sdk_paths:
                if os.path.isdir(oh_sdk_path):
                    info["oh_sdk_path"] = oh_sdk_path

                    # 扫描工具链目录中的所有工具
                    toolchains_dir = os.path.join(oh_sdk_path, "toolchains")
                    if os.path.isdir(toolchains_dir):
                        self._discover_toolchain_tools(toolchains_dir, info)

                    break

        # 2. 查找 DevEco Studio tools 目录下的工具
        tools_path = os.path.join(contents_path, "tools")
        if os.path.isdir(tools_path):
            self._discover_deveco_tools(tools_path, info)

        # 3. 查找 Java/JBR
        java_home = self._find_java_runtime(contents_path)
        if java_home:
            info["java_home"] = java_home
            java_exe = os.path.join(java_home, "bin", "java.exe" if self.platform == "Windows" else "java")
            if os.path.exists(java_exe):
                info["tools"]["java"] = java_exe

        # 4. 验证最小要求
        info["valid"] = (
            "sdk_path" in info and
            ("hdc" in info["tools"] or "java_home" in info)
        )

        return info if info["valid"] else None

    def _discover_toolchain_tools(self, toolchains_dir: str, info: Dict[str, Any]):
        """
        自动扫描并发现 toolchains 目录中的所有工具

        Args:
            toolchains_dir: toolchains 目录路径
            info: 安装信息字典（就地修改）
        """
        # 定义常见工具的检测规则
        # 格式: (工具名称, 相对于 toolchains 的路径, 可执行文件名)
        common_tools = [
            # 核心工具
            ("hdc", "", "hdc"),

            # LLVM 工具链
            ("llvm", "llvm", "bin"),
            ("clang", "llvm/bin", "clang"),
            ("clang++", "llvm/bin", "clang++"),
            ("lld", "llvm/bin", "lld"),
            ("llvm-ar", "llvm/bin", "llvm-ar"),
            ("llvm-nm", "llvm/bin", "llvm-nm"),
            ("llvm-objdump", "llvm/bin", "llvm-objdump"),
            ("llvm-strip", "llvm/bin", "llvm-strip"),
            ("llvm-objcopy", "llvm/bin", "llvm-objcopy"),

            # Profiler 工具
            ("profiler", "profiler", "bin"),
            ("hiprofiler", "profiler/bin", "hiprofiler"),
            ("hiperf", "profiler/bin", "hiperf"),

            # 堆栈解析工具
            ("hstack", "", "hstack"),

            # 包管理工具
            ("ohpm", "", "ohpm"),

            # 其他工具
            ("syscap", "", "syscap"),
            ("ark", "ark", "bin"),
        ]

        # 保存工具目录以便后续使用
        info["tool_dirs"]["toolchains"] = toolchains_dir

        # 逐个检测工具
        for tool_entry in common_tools:
            tool_name = tool_entry[0]
            rel_path = tool_entry[1]
            exe_name = tool_entry[2]

            # 构建工具路径
            if rel_path:
                tool_dir = os.path.join(toolchains_dir, rel_path)
            else:
                tool_dir = toolchains_dir

            # 添加平台特定的扩展名
            exe_suffix = ".exe" if self.platform == "Windows" else ""
            exe_path = os.path.join(tool_dir, f"{exe_name}{exe_suffix}")

            # 检查可执行文件是否存在
            if os.path.exists(exe_path):
                info["tools"][tool_name] = exe_path
                # 对于工具目录，也保存起来
                if os.path.isdir(tool_dir) and tool_name not in ["hdc", "hstack", "ohpm", "syscap"]:
                    info["tool_dirs"][f"{tool_name}_dir"] = tool_dir
            elif os.path.isdir(tool_dir):
                # 工具目录存在但可执行文件不在预期位置，保存目录
                if tool_name not in ["hdc", "hstack", "ohpm", "syscap"]:
                    info["tool_dirs"][f"{tool_name}_dir"] = tool_dir

        # 自动扫描 toolchains 目录下的所有可执行文件
        # 这样可以捕获未在列表中的工具
        # 非工具文件的扩展名黑名单
        non_tool_extensions = {'.txt', '.json', '.md', '.xml', '.properties', '.cfg', '.conf'}

        try:
            for item in os.listdir(toolchains_dir):
                item_path = os.path.join(toolchains_dir, item)

                # 跳过目录和已知的工具
                if os.path.isdir(item_path):
                    continue

                # 跳过非工具文件
                _, ext = os.path.splitext(item)
                if ext.lower() in non_tool_extensions:
                    continue

                # 跳过库文件和动态库
                if item.endswith('.so') or item.endswith('.dll') or item.endswith('.dylib') or item.endswith('.a'):
                    continue

                # 检查是否为可执行文件
                if os.access(item_path, os.X_OK):
                    # 跳过已检测的工具
                    if item not in info["tools"]:
                        info["tools"][item] = item_path
        except (PermissionError, OSError):
            pass

    def _discover_deveco_tools(self, tools_path: str, info: Dict[str, Any]):
        """
        发现 DevEco Studio tools 目录下的工具

        Args:
            tools_path: DevEco Studio tools 目录路径
            info: 安装信息字典（就地修改）
        """
        # 保存 tools 目录
        info["tool_dirs"]["deveco_tools"] = tools_path

        # hvigorw 构建工具
        hvigor_paths = [
            os.path.join(tools_path, "hvigor", "bin", "hvigorw"),
            os.path.join(tools_path, "hvigorw"),
        ]

        for hvigorw_path in hvigor_paths:
            if os.path.exists(hvigorw_path):
                info["tools"]["hvigorw"] = hvigorw_path
                info["tool_dirs"]["hvigorw_dir"] = os.path.dirname(hvigorw_path)
                break

    def _find_java_runtime(self, contents_path: str) -> Optional[str]:
        """
        查找 Java/JBR 运行时

        Args:
            contents_path: DevEco Studio Contents 目录路径

        Returns:
            JAVA_HOME 路径，如果未找到返回 None
        """
        jbr_paths = [
            os.path.join(contents_path, "jbr"),
            os.path.join(contents_path, "jre"),
        ]

        for jbr_path in jbr_paths:
            if os.path.isdir(jbr_path):
                # macOS 特殊处理
                if self.platform == "Darwin":
                    java_home = os.path.join(jbr_path, "Contents", "Home")
                else:
                    java_home = jbr_path

                if os.path.isdir(java_home):
                    java_bin = os.path.join(java_home, "bin")
                    if os.path.isdir(java_bin):
                        # 验证 java 命令
                        java_exe = os.path.join(java_bin, "java.exe" if self.platform == "Windows" else "java")
                        if os.path.exists(java_exe):
                            return java_home

        return None

    def _select_best_installation(self, installations: List[Dict]) -> Dict:
        """从多个安装中选择最佳的"""
        if len(installations) == 1:
            return installations[0]

        # 简单策略：优先选择包含 Java 的安装
        for info in installations:
            if "java_home" in info:
                logger.info(f"选择包含 Java 的安装: {info['installation_path']}")
                return info

        # 默认返回第一个
        logger.info(f"使用第一个安装: {installations[0]['installation_path']}")
        return installations[0]


class ToolchainDetector:
    """工具链检测器 - 仅支持 DevEco Studio"""

    def __init__(self, deveco_info: Optional[Dict] = None):
        self.deveco_info = deveco_info
        self.platform = platform.system()

    def detect_all(self) -> Dict[str, Any]:
        """
        检测工具链（仅从 DevEco Studio）

        Returns:
            工具链信息字典
        """
        toolchain_info = {
            "source": "unknown",
            "tools": {},
            "tool_dirs": {},
            "java_home": None,
            "sdk_path": None
        }

        # 检测 DevEco Studio
        if self.deveco_info:
            toolchain_info["source"] = "deveco"
            toolchain_info["installation_path"] = self.deveco_info.get("installation_path")
            toolchain_info["tools"] = self.deveco_info.get("tools", {})
            toolchain_info["tool_dirs"] = self.deveco_info.get("tool_dirs", {})
            toolchain_info["java_home"] = self.deveco_info.get("java_home")
            toolchain_info["sdk_path"] = self.deveco_info.get("sdk_path")
            toolchain_info["oh_sdk_path"] = self.deveco_info.get("oh_sdk_path")

            logger.info("✓ 使用 DevEco Studio 工具链")
            return toolchain_info

        # 未检测到 DevEco Studio
        logger.error("✗ 未检测到 DevEco Studio")
        logger.error("请先安装 DevEco Studio: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download")
        return toolchain_info

    def get_build_environment(self) -> Dict[str, str]:
        """获取构建环境变量（使用 DevEco Studio 工具链）"""
        env = os.environ.copy()

        toolchain_info = self.detect_all()

        # 如果未检测到 DevEco Studio，返回错误提示
        if toolchain_info["source"] == "unknown":
            logger.error("=" * 60)
            logger.error("未检测到 DevEco Studio！")
            logger.error("")
            logger.error("请先安装 DevEco Studio:")
            logger.error("1. 下载地址: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download")
            logger.error("2. 最低版本: DevEco Studio 3.1+ (推荐 4.0+)")
            logger.error("3. 安装后确保安装了 HarmonyOS/OpenHarmony SDK")
            logger.error("")
            logger.error("如已安装但仍无法检测，请设置环境变量:")
            logger.error("export DEVECO_STUDIO_PATH=\"/path/to/DevEco Studio\"")
            logger.error("=" * 60)
            return env

        # 配置 DevEco Studio 工具链环境
        # 1. 设置 JAVA_HOME
        if toolchain_info.get("java_home"):
            env["JAVA_HOME"] = toolchain_info["java_home"]
            java_bin = os.path.join(toolchain_info["java_home"], "bin")
            env["PATH"] = f"{java_bin}{os.pathsep}{env.get('PATH', '')}"

        # 2. 添加工具路径到 PATH
        # 2.1 添加 SDK toolchains 目录（包含 hdc）
        if toolchain_info.get("oh_sdk_path"):
            toolchains_dir = os.path.join(toolchain_info["oh_sdk_path"], "toolchains")
            if os.path.isdir(toolchains_dir):
                env["PATH"] = f"{toolchains_dir}{os.pathsep}{env.get('PATH', '')}"

        # 2.2 添加所有检测到的工具目录到 PATH
        if toolchain_info.get("tool_dirs"):
            # 按优先级添加工具目录
            path_dirs = []

            # LLVM 工具链
            if "llvm_dir" in toolchain_info["tool_dirs"]:
                path_dirs.append(toolchain_info["tool_dirs"]["llvm_dir"])

            # Profiler 工具
            if "profiler_dir" in toolchain_info["tool_dirs"]:
                path_dirs.append(toolchain_info["tool_dirs"]["profiler_dir"])

            # Ark 工具
            if "ark_dir" in toolchain_info["tool_dirs"]:
                path_dirs.append(toolchain_info["tool_dirs"]["ark_dir"])

            # hvigorw
            if "hvigorw_dir" in toolchain_info["tool_dirs"]:
                path_dirs.append(toolchain_info["tool_dirs"]["hvigorw_dir"])

            # 将所有目录添加到 PATH
            for dir_path in reversed(path_dirs):  # 反转以保证优先级
                env["PATH"] = f"{dir_path}{os.pathsep}{env.get('PATH', '')}"

        # 2.3 添加单个工具到 PATH（如果工具目录未知）
        for tool_name in ["hvigorw"]:
            if toolchain_info.get("tools", {}).get(tool_name):
                tool_dir = os.path.dirname(toolchain_info["tools"][tool_name])
                if tool_dir not in env.get("PATH", ""):
                    env["PATH"] = f"{tool_dir}{os.pathsep}{env.get('PATH', '')}"

        # 3. 设置 DEVECO_SDK_HOME（hvigor 需要）
        if toolchain_info.get("sdk_path"):
            env["DEVECO_SDK_HOME"] = toolchain_info["sdk_path"]

        # 4. 设置其他环境变量
        # LLVM 相关
        if toolchain_info.get("tool_dirs", {}).get("llvm_dir"):
            env["LLVM_HOME"] = toolchain_info["tool_dirs"]["llvm_dir"]

        # 5. 设置 HDC 端口
        env["HDC_SERVER_PORT"] = "7035"

        return env


def detect_environment(force_refresh: bool = False) -> Dict[str, Any]:
    """
    检测构建环境（公开接口）

    Args:
        force_refresh: 是否强制重新检测

    Returns:
        环境信息字典
    """
    # 尝试从缓存加载
    if not force_refresh:
        cache = get_cached_environment()
        if cache:
            logger.info("使用缓存的环境配置")
            return cache

    # 检测 DevEco Studio
    deveco_detector = DevEcoDetector()
    deveco_info = deveco_detector.detect_all()

    # 检测工具链
    toolchain_detector = ToolchainDetector(deveco_info)
    toolchain_info = toolchain_detector.detect_all()

    # 缓存结果
    cache_environment(toolchain_info)

    return toolchain_info


def get_cached_environment() -> Optional[Dict]:
    """获取缓存的环境配置"""
    cache_file = os.path.expanduser("~/.ohos_build_debug_cache.json")

    if not os.path.exists(cache_file):
        return None

    try:
        with open(cache_file) as f:
            cache = json.load(f)

        # 验证缓存
        if cache.get("version") == "1.0" and validate_cache(cache):
            return cache
    except:
        pass

    return None


def cache_environment(env_info: Dict):
    """缓存环境配置"""
    cache_file = os.path.expanduser("~/.ohos_build_debug_cache.json")

    from datetime import datetime

    cache_data = {
        **env_info,
        "version": "1.0",
        "cached_at": datetime.now().isoformat(),
        "platform": platform.system(),
        "hostname": platform.node()
    }

    try:
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    except:
        pass


def validate_cache(cache: Dict) -> bool:
    """验证缓存是否仍然有效"""
    # 检查关键路径是否存在
    if cache.get("installation_path"):
        if not os.path.isdir(cache["installation_path"]):
            return False

    if cache.get("sdk_path"):
        if not os.path.isdir(cache["sdk_path"]):
            return False

    if cache.get("java_home"):
        if not os.path.isdir(cache["java_home"]):
            return False

    # 检查缓存时间（24小时）
    try:
        from datetime import datetime
        cached_at = datetime.fromisoformat(cache["cached_at"])
        if (datetime.now() - cached_at).days > 1:
            return False
    except:
        return False

    return True


def print_detection_report(env_info: Dict):
    """打印检测报告"""
    print()
    print("=" * 60)
    print("环境检测结果")
    print("=" * 60)
    print()

    source = env_info.get("source", "unknown")

    if source == "deveco":
        print("✓ 检测源: DevEco Studio")
        print(f"  安装路径: {env_info.get('installation_path')}")
    elif source == "commandlinetools":
        print("✓ 检测源: Command Line Tools")
    else:
        print("✓ 检测源: 系统工具")

    print()

    if env_info.get("java_home"):
        print(f"✓ Java Home: {env_info['java_home']}")

    if env_info.get("sdk_path"):
        print(f"✓ SDK Path: {env_info['sdk_path']}")

    if env_info.get("oh_sdk_path"):
        print(f"✓ OpenHarmony SDK: {env_info['oh_sdk_path']}")

    if env_info.get("tools"):
        print()
        print("✓ 可用工具:")
        # 按类别分组显示工具
        core_tools = []
        llvm_tools = []
        profiler_tools = []
        other_tools = []

        for tool_name, tool_path in sorted(env_info["tools"].items()):
            if tool_name in ["hdc", "hvigorw", "java", "hstack", "ohpm", "syscap"]:
                core_tools.append((tool_name, tool_path))
            elif tool_name.startswith("llvm") or tool_name.startswith("clang") or tool_name.startswith("lld"):
                llvm_tools.append((tool_name, tool_path))
            elif "profiler" in tool_name or "hiperf" in tool_name:
                profiler_tools.append((tool_name, tool_path))
            else:
                other_tools.append((tool_name, tool_path))

        if core_tools:
            print("  核心工具:")
            for tool_name, tool_path in core_tools:
                print(f"    {tool_name}: {tool_path}")

        if llvm_tools:
            print()
            print("  LLVM 工具链:")
            for tool_name, tool_path in llvm_tools:
                print(f"    {tool_name}: {tool_path}")

        if profiler_tools:
            print()
            print("  性能分析工具:")
            for tool_name, tool_path in profiler_tools:
                print(f"    {tool_name}: {tool_path}")

        if other_tools:
            print()
            print("  其他工具:")
            for tool_name, tool_path in other_tools:
                print(f"    {tool_name}: {tool_path}")

    if env_info.get("tool_dirs"):
        print()
        print("✓ 工具目录:")
        for dir_name, dir_path in sorted(env_info["tool_dirs"].items()):
            print(f"    {dir_name}: {dir_path}")

    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    # 测试代码
    env_info = detect_environment(force_refresh=True)
    print_detection_report(env_info)
