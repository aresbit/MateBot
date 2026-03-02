#!/usr/bin/env python3
"""
Execute UI interactions on HarmonyOS device via hdc.
Usage: python3 interact.py <command> [arguments]

Commands:
  click <x> <y>                    - Click at coordinates
  double-click <x> <y>             - Double click at coordinates
  long-click <x> <y>               - Long click (press and hold) at coordinates
  swipe <x1> <y1> <x2> <y2> [speed] - Swipe from (x1,y1) to (x2,y2)
  drag <x1> <y1> <x2> <y2> [speed] - Drag from (x1,y1) to (x2,y2)
  fling <x1> <y1> <x2> <y2> [speed] [step] - Fling (fast swipe)
  key-event <key>                  - Send key event (Back, Home, Power, or key ID)
  input-text <x> <y> <text>        - Tap at (x,y) then input text
  type <text>                      - Type text at current focus

  click-component [options]        - Click component by search criteria
  long-click-component [options]   - Long click component by search criteria
"""

import argparse
import json
import os
import subprocess
import sys
import time
from typing import Optional, Tuple

# Import find_component functionality
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from hdc_utils import DeviceResolutionError, find_hdc, resolve_device


class UIInteractor:
    def __init__(self, device_id=None):
        self.hdc_path = find_hdc()
        try:
            self.device_id = resolve_device(self.hdc_path, device_id, strict_multi=True)
        except DeviceResolutionError as exc:
            raise RuntimeError(str(exc))

        if not self.device_id:
            raise RuntimeError("No connected device found. Use hdc list targets and pass --device.")

    def _run_uitest(self, args):
        """Run uitest command via hdc."""
        cmd = [self.hdc_path]
        if self.device_id:
            cmd.extend(["-t", self.device_id])
        cmd.extend(["shell", "uitest"] + args)

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timeout"
        except Exception as e:
            return -1, "", str(e)

    def click(self, x: int, y: int) -> bool:
        """Click at coordinates."""
        code, out, err = self._run_uitest(["uiInput", "click", str(x), str(y)])
        if code == 0:
            print(f"Clicked at ({x}, {y})")
            return True
        else:
            print(f"Click failed: {err}", file=sys.stderr)
            return False

    def double_click(self, x: int, y: int) -> bool:
        """Double click at coordinates."""
        code, out, err = self._run_uitest(["uiInput", "doubleClick", str(x), str(y)])
        if code == 0:
            print(f"Double clicked at ({x}, {y})")
            return True
        else:
            print(f"Double click failed: {err}", file=sys.stderr)
            return False

    def long_click(self, x: int, y: int) -> bool:
        """Long click at coordinates."""
        code, out, err = self._run_uitest(["uiInput", "longClick", str(x), str(y)])
        if code == 0:
            print(f"Long clicked at ({x}, {y})")
            return True
        else:
            print(f"Long click failed: {err}", file=sys.stderr)
            return False

    def swipe(self, x1: int, y1: int, x2: int, y2: int, velocity: int = 600) -> bool:
        """Swipe from (x1,y1) to (x2,y2)."""
        code, out, err = self._run_uitest(["uiInput", "swipe", str(x1), str(y1), str(x2), str(y2), str(velocity)])
        if code == 0:
            print(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")
            return True
        else:
            print(f"Swipe failed: {err}", file=sys.stderr)
            return False

    def drag(self, x1: int, y1: int, x2: int, y2: int, velocity: int = 600) -> bool:
        """Drag from (x1,y1) to (x2,y2)."""
        code, out, err = self._run_uitest(["uiInput", "drag", str(x1), str(y1), str(x2), str(y2), str(velocity)])
        if code == 0:
            print(f"Dragged from ({x1}, {y1}) to ({x2}, {y2})")
            return True
        else:
            print(f"Drag failed: {err}", file=sys.stderr)
            return False

    def fling(self, x1: int, y1: int, x2: int, y2: int, velocity: int = 600, step: int = 50) -> bool:
        """Fling (fast swipe) from (x1,y1) to (x2,y2)."""
        code, out, err = self._run_uitest(["uiInput", "fling", str(x1), str(y1), str(x2), str(y2), str(velocity), str(step)])
        if code == 0:
            print(f"Flinged from ({x1}, {y1}) to ({x2}, {y2})")
            return True
        else:
            print(f"Fling failed: {err}", file=sys.stderr)
            return False

    def dirc_fling(self, direction: int, velocity: int = 600, step: int = 50) -> bool:
        """Direction fling. Direction: 0=left, 1=right, 2=up, 3=down."""
        code, out, err = self._run_uitest(["uiInput", "dircFling", str(direction), str(velocity), str(step)])
        direction_names = ["left", "right", "up", "down"]
        if code == 0:
            print(f"Flinged {direction_names[direction] if direction < 4 else direction}")
            return True
        else:
            print(f"Direction fling failed: {err}", file=sys.stderr)
            return False

    def key_event(self, key: str) -> bool:
        """Send key event. Key can be: Back, Home, Power, or numeric key ID."""
        code, out, err = self._run_uitest(["uiInput", "keyEvent", key])
        if code == 0:
            print(f"Sent key event: {key}")
            return True
        else:
            print(f"Key event failed: {err}", file=sys.stderr)
            return False

    def input_text(self, x: int, y: int, text: str) -> bool:
        """Input text at coordinates."""
        # First tap to focus, then input
        self.click(x, y)
        time.sleep(0.3)

        code, out, err = self._run_uitest(["uiInput", "inputText", str(x), str(y), text])
        if code == 0:
            print(f"Input text '{text}' at ({x}, {y})")
            return True
        else:
            print(f"Input text failed: {err}", file=sys.stderr)
            return False

    def type_text(self, text: str) -> bool:
        """Type text at current focus."""
        code, out, err = self._run_uitest(["uiInput", "text", text])
        if code == 0:
            print(f"Typed text: {text}")
            return True
        else:
            print(f"Type text failed: {err}", file=sys.stderr)
            return False

    def screenshot(self, output_path: str = None) -> Optional[str]:
        """Take screenshot."""
        if output_path is None:
            output_path = f"/tmp/harmonyos_screen_{int(time.time())}.png"

        code, out, err = self._run_uitest(["screenCap", "-p", output_path])
        if code == 0:
            print(f"Screenshot saved to: {output_path}")
            return output_path
        else:
            print(f"Screenshot failed: {err}", file=sys.stderr)
            return None


def parse_bounds(bounds_str) -> Optional[Tuple[int, int, int, int]]:
    """Parse bounds string to tuple."""
    try:
        bounds_str = bounds_str.replace("[", " ").replace("]", " ").strip()
        parts = bounds_str.split()
        if len(parts) == 4:
            return tuple(map(int, parts))
    except:
        pass
    return None


def find_component_center(criteria: dict) -> Optional[Tuple[int, int]]:
    """Find component and return its center coordinates."""
    from find_component import extract_all_components, find_components

    # Find layout file
    tmp_dir = "/tmp"
    layout_files = [f for f in os.listdir(tmp_dir) if f.startswith("harmonyos_layout")]

    if not layout_files:
        print("Error: No layout file found. Run dump_layout.py first.", file=sys.stderr)
        return None

    # Prefer components file
    components_file = None
    layout_file = None

    for f in sorted(layout_files, key=lambda x: os.path.getmtime(os.path.join(tmp_dir, x)), reverse=True):
        if "_components" in f:
            components_file = os.path.join(tmp_dir, f)
            break

    if not components_file:
        for f in sorted(layout_files, key=lambda x: os.path.getmtime(os.path.join(tmp_dir, x)), reverse=True):
            if not "_components" in f:
                layout_file = os.path.join(tmp_dir, f)
                break

    # Load and search
    if components_file:
        with open(components_file, 'r', encoding='utf-8') as f:
            components = json.load(f)
    elif layout_file:
        with open(layout_file, 'r', encoding='utf-8') as f:
            layout_data = json.load(f)
        components = extract_all_components(layout_data)
    else:
        return None

    # Avoid accidental taps: component operations must always be constrained
    # to interactive and actionable nodes.
    safe_criteria = dict(criteria)
    safe_criteria.setdefault("clickable", "true")
    safe_criteria.setdefault("enabled", "true")
    safe_criteria.setdefault("visible", "true")

    results = find_components(components, safe_criteria)
    if results:
        return results[0].get("center")
    return None


def main():
    parser = argparse.ArgumentParser(description="HarmonyOS UI Interaction Tool")
    parser.add_argument("--device", "-d", help="Device ID")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # click
    click_parser = subparsers.add_parser("click", help="Click at coordinates")
    click_parser.add_argument("x", type=int, help="X coordinate")
    click_parser.add_argument("y", type=int, help="Y coordinate")

    # double-click
    dc_parser = subparsers.add_parser("double-click", help="Double click")
    dc_parser.add_argument("x", type=int)
    dc_parser.add_argument("y", type=int)

    # long-click
    lc_parser = subparsers.add_parser("long-click", help="Long click")
    lc_parser.add_argument("x", type=int)
    lc_parser.add_argument("y", type=int)

    # swipe
    swipe_parser = subparsers.add_parser("swipe", help="Swipe")
    swipe_parser.add_argument("x1", type=int)
    swipe_parser.add_argument("y1", type=int)
    swipe_parser.add_argument("x2", type=int)
    swipe_parser.add_argument("y2", type=int)
    swipe_parser.add_argument("--velocity", "-v", type=int, default=600)

    # drag
    drag_parser = subparsers.add_parser("drag", help="Drag")
    drag_parser.add_argument("x1", type=int)
    drag_parser.add_argument("y1", type=int)
    drag_parser.add_argument("x2", type=int)
    drag_parser.add_argument("y2", type=int)
    drag_parser.add_argument("--velocity", "-v", type=int, default=600)

    # fling
    fling_parser = subparsers.add_parser("fling", help="Fling")
    fling_parser.add_argument("x1", type=int)
    fling_parser.add_argument("y1", type=int)
    fling_parser.add_argument("x2", type=int)
    fling_parser.add_argument("y2", type=int)
    fling_parser.add_argument("--velocity", "-v", type=int, default=600)
    fling_parser.add_argument("--step", "-s", type=int, default=50)

    # dirc-fling
    dfling_parser = subparsers.add_parser("dirc-fling", help="Direction fling (0=left,1=right,2=up,3=down)")
    dfling_parser.add_argument("direction", type=int, choices=[0, 1, 2, 3])
    dfling_parser.add_argument("--velocity", "-v", type=int, default=600)
    dfling_parser.add_argument("--step", "-s", type=int, default=50)

    # key-event
    key_parser = subparsers.add_parser("key-event", help="Send key event")
    key_parser.add_argument("key", help="Key name (Back, Home, Power) or key ID")

    # input-text
    it_parser = subparsers.add_parser("input-text", help="Input text at coordinates")
    it_parser.add_argument("x", type=int)
    it_parser.add_argument("y", type=int)
    it_parser.add_argument("text", help="Text to input")

    # type
    type_parser = subparsers.add_parser("type", help="Type text at current focus")
    type_parser.add_argument("text", help="Text to type")

    # screenshot
    ss_parser = subparsers.add_parser("screenshot", help="Take screenshot")
    ss_parser.add_argument("--output", "-o", help="Output file path")

    # click-component
    cc_parser = subparsers.add_parser("click-component", help="Click component by search criteria")
    cc_parser.add_argument("--text", "-t", help="Search by text")
    cc_parser.add_argument("--id", "-i", help="Search by ID")
    cc_parser.add_argument("--type", help="Search by type")
    cc_parser.add_argument("--regex", "-r", help="Regex pattern")

    # long-click-component
    lcc_parser = subparsers.add_parser("long-click-component", help="Long click component by search criteria")
    lcc_parser.add_argument("--text", "-t", help="Search by text")
    lcc_parser.add_argument("--id", "-i", help="Search by ID")
    lcc_parser.add_argument("--type", help="Search by type")
    lcc_parser.add_argument("--regex", "-r", help="Regex pattern")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        interactor = UIInteractor(args.device)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    if args.command == "click":
        success = interactor.click(args.x, args.y)
        sys.exit(0 if success else 1)

    elif args.command == "double-click":
        success = interactor.double_click(args.x, args.y)
        sys.exit(0 if success else 1)

    elif args.command == "long-click":
        success = interactor.long_click(args.x, args.y)
        sys.exit(0 if success else 1)

    elif args.command == "swipe":
        success = interactor.swipe(args.x1, args.y1, args.x2, args.y2, args.velocity)
        sys.exit(0 if success else 1)

    elif args.command == "drag":
        success = interactor.drag(args.x1, args.y1, args.x2, args.y2, args.velocity)
        sys.exit(0 if success else 1)

    elif args.command == "fling":
        success = interactor.fling(args.x1, args.y1, args.x2, args.y2, args.velocity, args.step)
        sys.exit(0 if success else 1)

    elif args.command == "dirc-fling":
        success = interactor.dirc_fling(args.direction, args.velocity, args.step)
        sys.exit(0 if success else 1)

    elif args.command == "key-event":
        success = interactor.key_event(args.key)
        sys.exit(0 if success else 1)

    elif args.command == "input-text":
        success = interactor.input_text(args.x, args.y, args.text)
        sys.exit(0 if success else 1)

    elif args.command == "type":
        success = interactor.type_text(args.text)
        sys.exit(0 if success else 1)

    elif args.command == "screenshot":
        result = interactor.screenshot(args.output)
        sys.exit(0 if result else 1)

    elif args.command == "click-component":
        criteria = {}
        if args.text:
            criteria["text"] = args.text
        if args.id:
            criteria["id"] = args.id
        if args.type:
            criteria["type"] = args.type
        if args.regex:
            criteria["regex"] = args.regex

        if not criteria:
            print("Error: click-component requires at least one selector (--text/--id/--type/--regex).", file=sys.stderr)
            sys.exit(1)

        center = find_component_center(criteria)
        if center:
            success = interactor.click(center[0], center[1])
            sys.exit(0 if success else 1)
        else:
            print("Component not found", file=sys.stderr)
            sys.exit(1)

    elif args.command == "long-click-component":
        criteria = {}
        if args.text:
            criteria["text"] = args.text
        if args.id:
            criteria["id"] = args.id
        if args.type:
            criteria["type"] = args.type
        if args.regex:
            criteria["regex"] = args.regex

        if not criteria:
            print("Error: long-click-component requires at least one selector (--text/--id/--type/--regex).", file=sys.stderr)
            sys.exit(1)

        center = find_component_center(criteria)
        if center:
            success = interactor.long_click(center[0], center[1])
            sys.exit(0 if success else 1)
        else:
            print("Component not found", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
