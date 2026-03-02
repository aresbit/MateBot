#!/usr/bin/env python3
"""
HarmonyOS system shortcuts and gestures.
Usage: python3 shortcut.py <command>

Commands:
  home              - Return to home screen (Home key)
  back              - Go back (Back key or swipe from edge)
  power             - Power button
  control-center    - Pull down control center (swipe from top)
  notification      - Pull down notification panel
  recent            - Open recent apps / multitasking
  screenshot        - Take screenshot
  swipe-up          - Swipe up from bottom
  swipe-down        - Swipe down from top
  swipe-left        - Swipe left
  swipe-right       - Swipe right
"""

import argparse
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from hdc_utils import DeviceResolutionError, find_hdc, resolve_device

# Screen dimensions (will be detected or use defaults)
SCREEN_WIDTH = 1320
SCREEN_HEIGHT = 2848


def detect_screen_size(hdc_path, device_id=None):
    """Best-effort screen size detection from device or latest layout dump."""
    base_cmd = [hdc_path]
    if device_id:
        base_cmd.extend(["-t", device_id])

    # Try device-level commands first.
    candidates = [
        ["shell", "hidumper", "-s", "RenderService", "-a", "screen"],
        ["shell", "hidumper", "-s", "RenderService", "-a", "display"],
    ]

    patterns = [
        re.compile(r"(\d{3,5})\s*[xX]\s*(\d{3,5})"),
        re.compile(r"width[^0-9]*(\d{3,5}).*height[^0-9]*(\d{3,5})", re.IGNORECASE | re.DOTALL),
    ]

    for tail in candidates:
        try:
            result = subprocess.run(base_cmd + tail, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                continue
            output = result.stdout or ""
            for pattern in patterns:
                match = pattern.search(output)
                if match:
                    w, h = int(match.group(1)), int(match.group(2))
                    if w > 0 and h > 0:
                        return w, h
        except Exception:
            continue

    # Fallback: use latest dumped layout bounds in /tmp.
    try:
        tmp_dir = "/tmp"
        layout_files = [
            os.path.join(tmp_dir, f)
            for f in os.listdir(tmp_dir)
            if f.startswith("harmonyos_layout_")
            and f.endswith(".json")
            and "_components" not in f
        ]
        if layout_files:
            latest = max(layout_files, key=os.path.getmtime)
            with open(latest, "r", encoding="utf-8") as f:
                layout = json.load(f)
            bounds = (layout.get("attributes") or {}).get("bounds", "")
            m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
            if m:
                left, top, right, bottom = map(int, m.groups())
                w, h = right - left, bottom - top
                if w > 0 and h > 0:
                    return w, h
    except Exception:
        pass

    return SCREEN_WIDTH, SCREEN_HEIGHT


class ShortcutExecutor:
    def __init__(self, device_id=None):
        self.hdc_path = find_hdc()
        try:
            self.device_id = resolve_device(self.hdc_path, device_id, strict_multi=True)
        except DeviceResolutionError as exc:
            raise RuntimeError(str(exc))

        if not self.device_id:
            raise RuntimeError("未检测到已连接设备，请先执行 hdc list targets 确认设备在线。")

        self.screen_width, self.screen_height = detect_screen_size(self.hdc_path, self.device_id)

    def _run_uitest(self, args):
        """Run uitest command."""
        cmd = [self.hdc_path]
        if self.device_id:
            cmd.extend(["-t", self.device_id])
        cmd.extend(["shell", "uitest"] + args)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except:
            return False

    def home(self):
        """Return to home screen."""
        success = self._run_uitest(["uiInput", "keyEvent", "Home"])
        print("返回桌面" if success else "操作失败")
        return success

    def back(self):
        """Go back using Back key."""
        success = self._run_uitest(["uiInput", "keyEvent", "Back"])
        print("返回" if success else "操作失败")
        return success

    def back_gesture(self):
        """Go back using swipe gesture from left edge."""
        # Swipe from left edge to right
        success = self._run_uitest([
            "uiInput", "swipe",
            "10", str(self.screen_height // 2),
            "200", str(self.screen_height // 2),
            "400"
        ])
        print("侧滑返回" if success else "操作失败")
        return success

    def power(self):
        """Press power button."""
        success = self._run_uitest(["uiInput", "keyEvent", "Power"])
        print("电源键" if success else "操作失败")
        return success

    def control_center(self):
        """Pull down control center from top right."""
        # Swipe down from top right area
        x = int(self.screen_width * 0.8)
        success = self._run_uitest([
            "uiInput", "swipe",
            str(x), "50",
            str(x), str(int(self.screen_height * 0.5)),
            "600"
        ])
        print("下拉控制中心" if success else "操作失败")
        return success

    def notification(self):
        """Pull down notification panel from top."""
        x = int(self.screen_width * 0.5)
        success = self._run_uitest([
            "uiInput", "swipe",
            str(x), "50",
            str(x), str(int(self.screen_height * 0.5)),
            "600"
        ])
        print("下拉通知栏" if success else "操作失败")
        return success

    def recent(self):
        """Open recent apps / multitasking view."""
        # Swipe up from bottom and hold
        x = int(self.screen_width * 0.5)
        y_bottom = self.screen_height - 50
        y_middle = int(self.screen_height * 0.6)

        # Method 1: Swipe up slowly (might trigger recent apps)
        success = self._run_uitest([
            "uiInput", "swipe",
            str(x), str(y_bottom),
            str(x), str(y_middle),
            "300"  # Slow swipe
        ])
        print("多任务中心" if success else "操作失败")
        return success

    def screenshot(self):
        """Take screenshot."""
        import time as t
        local_path = f"/tmp/harmonyos_screen_{int(t.time())}.png"
        success = self._run_uitest(["screenCap", "-p", local_path])
        if success:
            print(f"截图已保存: {local_path}")
        else:
            print("截图失败")
        return success

    def swipe_up(self):
        """Swipe up from bottom."""
        x = int(self.screen_width * 0.5)
        success = self._run_uitest([
            "uiInput", "swipe",
            str(x), str(self.screen_height - 100),
            str(x), "200",
            "600"
        ])
        print("上滑" if success else "操作失败")
        return success

    def swipe_down(self):
        """Swipe down from top."""
        x = int(self.screen_width * 0.5)
        success = self._run_uitest([
            "uiInput", "swipe",
            str(x), "100",
            str(x), str(self.screen_height - 200),
            "600"
        ])
        print("下滑" if success else "操作失败")
        return success

    def swipe_left(self):
        """Swipe left."""
        y = int(self.screen_height * 0.5)
        success = self._run_uitest([
            "uiInput", "swipe",
            str(self.screen_width - 100), str(y),
            "100", str(y),
            "600"
        ])
        print("左滑" if success else "操作失败")
        return success

    def swipe_right(self):
        """Swipe right."""
        y = int(self.screen_height * 0.5)
        success = self._run_uitest([
            "uiInput", "swipe",
            "100", str(y),
            str(self.screen_width - 100), str(y),
            "600"
        ])
        print("右滑" if success else "操作失败")
        return success


def main():
    parser = argparse.ArgumentParser(description="HarmonyOS 系统快捷操作")
    parser.add_argument("--device", "-d", help="设备 ID")

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 所有命令都不需要额外参数
    commands = [
        ("home", "返回桌面"),
        ("back", "返回 (按键)"),
        ("back-gesture", "侧滑返回"),
        ("power", "电源键"),
        ("control-center", "下拉控制中心"),
        ("notification", "下拉通知栏"),
        ("recent", "多任务中心"),
        ("screenshot", "截图"),
        ("swipe-up", "上滑"),
        ("swipe-down", "下滑"),
        ("swipe-left", "左滑"),
        ("swipe-right", "右滑"),
    ]

    for cmd, help_text in commands:
        subparsers.add_parser(cmd, help=help_text)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print("\n示例:")
        print("  python3 shortcut.py home          # 返回桌面")
        print("  python3 shortcut.py back          # 返回")
        print("  python3 shortcut.py control-center  # 下拉控制中心")
        sys.exit(1)

    try:
        executor = ShortcutExecutor(args.device)
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

    cmd_map = {
        "home": executor.home,
        "back": executor.back,
        "back-gesture": executor.back_gesture,
        "power": executor.power,
        "control-center": executor.control_center,
        "notification": executor.notification,
        "recent": executor.recent,
        "screenshot": executor.screenshot,
        "swipe-up": executor.swipe_up,
        "swipe-down": executor.swipe_down,
        "swipe-left": executor.swipe_left,
        "swipe-right": executor.swipe_right,
    }

    if args.command in cmd_map:
        success = cmd_map[args.command]()
        sys.exit(0 if success else 1)
    else:
        print(f"未知命令: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
