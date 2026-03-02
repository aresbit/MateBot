#!/usr/bin/env python3
"""
HarmonyOS 测试用例执行脚本
支持通过组件文本/ID定位，自动适配不同屏幕尺寸
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import time
from typing import Dict, List, Optional, Tuple

# 获取技能目录
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_AUTOMATOR_SKILL = os.path.join(os.path.dirname(SKILL_DIR), "harmonyos-ui-automator")
TESTCASES_DIR = os.path.join(SKILL_DIR, "testcases")
DEFAULT_TIMEOUT = 30


class TestRunner:
    def __init__(self, device: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT):
        self.device = device
        self.timeout = timeout
        self.runtime: Dict[str, int] = {}
        self.hdc_path = self._find_hdc()
        self.dump_script = os.path.join(UI_AUTOMATOR_SKILL, "scripts", "dump_layout.py")
        self.find_script = os.path.join(UI_AUTOMATOR_SKILL, "scripts", "find_component.py")
        self.interact_script = os.path.join(UI_AUTOMATOR_SKILL, "scripts", "interact.py")

    def _find_hdc(self) -> str:
        sdk_root = os.path.expanduser("~/Library/OpenHarmony/Sdk")
        for path in sorted(glob.glob(os.path.join(sdk_root, "*/toolchains/hdc")), reverse=True):
            if os.path.exists(path):
                return path
        return "hdc"

    def _run(self, argv: List[str], timeout: Optional[int] = None) -> Tuple[str, str, int]:
        try:
            result = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=timeout if timeout is not None else self.timeout,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", f"Command timeout after {timeout or self.timeout}s: {' '.join(argv)}", 124

    def _python(self, script: str, args: List[str], timeout: Optional[int] = None) -> Tuple[str, str, int]:
        return self._run(["python3", script] + args, timeout=timeout)

    def _with_device(self, args: List[str]) -> List[str]:
        if self.device:
            return ["--device", self.device] + args
        return args

    def dump_layout(self) -> Optional[str]:
        stdout, stderr, code = self._python(self.dump_script, self._with_device([]))
        if code != 0:
            print(f"    ❌ dump layout 失败: {stderr.strip() or stdout.strip()}", file=sys.stderr)
            return None
        for line in stdout.splitlines():
            if "Layout saved to:" in line:
                return line.split("Layout saved to:", 1)[1].strip()
        return None

    def find_component(self, locator: Dict) -> Optional[Tuple[int, int]]:
        locator_type = locator.get("type", "text")
        locator_value = str(locator.get("value", "")).strip()
        if not locator_value:
            print("    ❌ 定位器缺少 value", file=sys.stderr)
            return None
        if locator_type not in {"text", "id", "type", "regex", "description"}:
            print(f"    ❌ 不支持的定位器类型: {locator_type}", file=sys.stderr)
            return None

        layout_path = self.dump_layout()
        if not layout_path:
            return None

        args = [f"--{locator_type}", locator_value, "--first", "--center-only", "--layout", layout_path]
        stdout, stderr, code = self._python(self.find_script, args)
        if code != 0:
            print(f"    ❌ 查找组件失败: {stderr.strip() or stdout.strip()}", file=sys.stderr)
            return None

        line = (stdout.strip().splitlines() or [""])[0].strip()
        if not line:
            return None
        parts = line.split()
        if len(parts) != 2:
            print(f"    ❌ 解析坐标失败: {line}", file=sys.stderr)
            return None

    def find_component_with_retries(self, locator: Dict, back_retries: int = 0) -> Optional[Tuple[int, int]]:
        retries = max(0, int(back_retries))
        for i in range(retries + 1):
            coords = self.find_component(locator)
            if coords:
                return coords
            if i < retries:
                self.key_event("Back")
                time.sleep(0.3)
        return None
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            print(f"    ❌ 解析坐标失败: {line}", file=sys.stderr)
            return None

    def count_components(self, locator: Dict) -> Optional[int]:
        locator_type = locator.get("type", "text")
        locator_value = str(locator.get("value", "")).strip()
        if not locator_value:
            print("    ❌ 计数定位器缺少 value", file=sys.stderr)
            return None
        if locator_type not in {"text", "id", "type", "regex", "description"}:
            print(f"    ❌ 不支持的计数定位器类型: {locator_type}", file=sys.stderr)
            return None

        layout_path = self.dump_layout()
        if not layout_path:
            return None

        args = [f"--{locator_type}", locator_value, "--json", "--layout", layout_path]
        stdout, stderr, code = self._python(self.find_script, args)
        if code != 0:
            msg = (stderr or stdout).strip()
            if "No matching components found" in msg:
                return 0
            print(f"    ❌ 计数组件失败: {msg}", file=sys.stderr)
            return None

        try:
            data = json.loads(stdout)
            if isinstance(data, list):
                return len(data)
        except json.JSONDecodeError:
            pass
        print("    ❌ 计数组件失败: 输出不是有效 JSON 列表", file=sys.stderr)
        return None

    def click(self, x: int, y: int) -> bool:
        _, stderr, code = self._python(self.interact_script, self._with_device(["click", str(x), str(y)]))
        if code != 0:
            print(f"    ❌ 点击失败: {stderr.strip()}", file=sys.stderr)
            return False
        return True

    def key_event(self, key: str) -> bool:
        _, stderr, code = self._python(self.interact_script, self._with_device(["key-event", key]))
        if code != 0:
            print(f"    ❌ 按键失败: {stderr.strip()}", file=sys.stderr)
            return False
        return True

    def swipe(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        _, stderr, code = self._python(
            self.interact_script,
            self._with_device(["swipe", str(x1), str(y1), str(x2), str(y2)]),
        )
        if code != 0:
            print(f"    ❌ 滑动失败: {stderr.strip()}", file=sys.stderr)
            return False
        return True

    def start_app(self, bundle: str, ability: Optional[str] = None) -> bool:
        return self._start_or_stop_app(bundle, ability, start=True)

    def force_stop_app(self, bundle: str) -> bool:
        return self._start_or_stop_app(bundle, None, start=False)

    def _start_or_stop_app(self, bundle: str, ability: Optional[str], start: bool) -> bool:
        if start:
            cmd = ["aa", "start", "-b", bundle]
            if ability:
                cmd.extend(["-a", ability])
        else:
            cmd = ["aa", "force-stop", bundle]
        hdc_cmd = [self.hdc_path]
        if self.device:
            hdc_cmd.extend(["-t", self.device])
        hdc_cmd.extend(["shell"] + cmd)
        stdout, stderr, code = self._run(hdc_cmd)
        msg = (stderr or stdout).strip()
        if code != 0:
            action = "启动应用" if start else "停止应用"
            print(f"    ❌ {action}失败: {msg}", file=sys.stderr)
            return False
        if start:
            out = (stdout + "\n" + stderr).lower()
            if "start ability successfully" not in out:
                print(f"    ❌ 启动应用失败: {msg}", file=sys.stderr)
                return False
        return True

    def execute_step(self, step: Dict) -> bool:
        action = step.get("action")
        params = step.get("params", {})
        description = step.get("description", "")
        print(f"  执行: {description}")

        if action == "launch_app":
            bundle = str(params.get("bundle", "")).strip()
            ability = str(params.get("ability", "")).strip()
            if bundle:
                if params.get("force_stop", True):
                    self.force_stop_app(bundle)
                    time.sleep(float(params.get("force_stop_wait", 0.5)))
                return self.start_app(bundle, ability or None)
            locator = params.get("locator", {})
            coords = self.find_component_with_retries(locator, params.get("back_retries", 0))
            if not coords:
                print(f"    ❌ 未找到组件: {locator}")
                return False
            return self.click(coords[0], coords[1])

        if action == "click":
            back_retries = params.get("back_retries", 0)
            if "coords" in params:
                coords = params["coords"]
                if len(coords) != 2:
                    print(f"    ❌ click coords 参数非法: {coords}")
                    return False
                return self.click(int(coords[0]), int(coords[1]))
            locator = params.get("locator", {})
            coords = self.find_component_with_retries(locator, back_retries)
            if not coords and params.get("relaunch_bundle"):
                bundle = str(params.get("relaunch_bundle", "")).strip()
                ability = str(params.get("relaunch_ability", "")).strip()
                if bundle:
                    self.start_app(bundle, ability or None)
                    time.sleep(float(params.get("relaunch_wait", 1.0)))
                    coords = self.find_component_with_retries(locator, back_retries)
            if not coords:
                print(f"    ❌ 未找到组件: {locator}")
                return False
            return self.click(coords[0], coords[1])

        if action == "wait":
            duration = float(params.get("duration", 1))
            time.sleep(max(0.0, duration))
            return True

        if action == "key_event":
            key = str(params.get("value", "Back"))
            return self.key_event(key)

        if action == "swipe":
            if "start_locator" in params and "end_locator" in params:
                start = self.find_component(params["start_locator"])
                end = self.find_component(params["end_locator"])
                if start and end:
                    return self.swipe(start[0], start[1], end[0], end[1])
                print("    ❌ 滑动起止组件定位失败")
                return False
            if "coords" in params:
                coords = params["coords"]
                if len(coords) != 4:
                    print(f"    ❌ swipe coords 参数非法: {coords}")
                    return False
                return self.swipe(int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3]))
            print("    ❌ swipe 缺少参数，需提供 coords 或 start_locator/end_locator")
            return False

        if action == "verify":
            locator = params.get("locator", {})
            if not locator:
                print("    ❌ verify 缺少 locator")
                return False
            coords = self.find_component(locator)
            if coords:
                print(f"    ✓ 验证通过: {step.get('expected', '')}")
                return True
            print(f"    ❌ 验证失败: {step.get('expected', '')}")
            return False

        if action == "capture_count":
            key = str(params.get("key", "")).strip()
            locator = params.get("locator", {})
            if not key:
                print("    ❌ capture_count 缺少 key")
                return False
            count = self.count_components(locator)
            if count is None:
                return False
            self.runtime[key] = count
            print(f"    ✓ 已记录 {key}={count}")
            return True

        if action == "verify_count_delta":
            key = str(params.get("key", "")).strip()
            locator = params.get("locator", {})
            allowed = params.get("allowed_deltas", [-1, 1])
            if not key:
                print("    ❌ verify_count_delta 缺少 key")
                return False
            if key not in self.runtime:
                print(f"    ❌ verify_count_delta 找不到基线计数: {key}")
                return False
            current = self.count_components(locator)
            if current is None:
                return False
            before = self.runtime[key]
            delta = current - before
            print(f"    计数变化: before={before}, after={current}, delta={delta}")
            if delta in allowed:
                print(f"    ✓ 验证通过: {step.get('expected', '')}")
                return True
            print(
                f"    ❌ 验证失败: 变化量 {delta} 不在允许集合 {allowed}. {step.get('expected', '')}"
            )
            return False

        print(f"    ❌ 不支持的 action: {action}")
        return False


def list_testcases() -> int:
    if not os.path.isdir(TESTCASES_DIR):
        print(f"错误: 测试目录不存在: {TESTCASES_DIR}")
        return 1

    print("可用测试用例:")
    found = False
    for filename in sorted(os.listdir(TESTCASES_DIR)):
        if not filename.endswith(".json"):
            continue
        found = True
        path = os.path.join(TESTCASES_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                tc = json.load(f)
            print(f"  - {filename[:-5]}: {tc.get('name', 'Unknown')}")
        except Exception as exc:
            print(f"  - {filename}: 解析失败 ({exc})")
    if not found:
        print("  (空)")
    return 0


def resolve_testcase_path(test_case: str) -> Optional[str]:
    if os.path.exists(test_case):
        return test_case
    candidate = os.path.join(TESTCASES_DIR, test_case)
    if not candidate.endswith(".json"):
        candidate += ".json"
    if os.path.exists(candidate):
        return candidate
    return None


def run_test(test_file: str, runner: TestRunner, step_delay: float = 0.2, fail_fast: bool = False) -> bool:
    with open(test_file, "r", encoding="utf-8") as f:
        test_case = json.load(f)

    print(f"\n{'=' * 50}")
    print(f"测试用例: {test_case.get('name', 'Unknown')}")
    print(f"描述: {test_case.get('description', '')}")
    print(f"{'=' * 50}\n")

    steps = test_case.get("steps", [])
    if not isinstance(steps, list) or not steps:
        print("错误: 测试用例缺少 steps 或 steps 为空")
        return False

    print("[准备工作] 返回主屏幕...")
    if not runner.key_event("Home"):
        print("  ❌ 无法发送 Home 键，终止测试")
        return False
    time.sleep(0.5)
    if not runner.key_event("Home"):
        print("  ❌ 无法发送第二次 Home 键，终止测试")
        return False
    time.sleep(0.8)

    results = []
    for step in steps:
        step_num = step.get("step", len(results) + 1)
        print(f"[步骤 {step_num}]")

        success = runner.execute_step(step)
        results.append(
            {
                "step": step_num,
                "description": step.get("description", ""),
                "success": success,
            }
        )

        if fail_fast and not success:
            print("  ⚠️ fail-fast: 遇到失败步骤，提前终止。")
            break
        time.sleep(max(0.0, step_delay))

    teardown_steps = test_case.get("teardown_steps", [])
    if isinstance(teardown_steps, list) and teardown_steps:
        print("\n[清理步骤]")
        for step in teardown_steps:
            runner.execute_step(step)
            time.sleep(max(0.0, step_delay))

    print(f"\n{'=' * 50}")
    print("测试结果:")
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    print(f"  通过: {passed}/{total}")
    for r in results:
        status = "✓" if r["success"] else "❌"
        print(f"  {status} 步骤{r['step']}: {r['description']}")
    return passed == total


def main() -> None:
    parser = argparse.ArgumentParser(description="HarmonyOS 测试用例执行工具")
    parser.add_argument("test_case", nargs="?", help="测试用例 JSON 文件路径或用例 ID")
    parser.add_argument("--list", action="store_true", help="列出所有可用测试用例")
    parser.add_argument("--device", "-d", help="设备 ID（多设备时建议显式指定）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="子命令超时（秒）")
    parser.add_argument("--step-delay", type=float, default=0.2, help="步骤间隔（秒）")
    parser.add_argument("--fail-fast", action="store_true", help="遇到失败步骤立即终止")
    args = parser.parse_args()

    if args.list:
        sys.exit(list_testcases())

    if not args.test_case:
        parser.error("the following arguments are required: test_case (unless --list is used)")

    test_path = resolve_testcase_path(args.test_case)
    if not test_path:
        print(f"错误: 测试用例文件不存在: {args.test_case}")
        sys.exit(1)

    runner = TestRunner(device=args.device, timeout=max(1, args.timeout))
    success = run_test(
        test_path,
        runner,
        step_delay=max(0.0, args.step_delay),
        fail_fast=args.fail_fast,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
