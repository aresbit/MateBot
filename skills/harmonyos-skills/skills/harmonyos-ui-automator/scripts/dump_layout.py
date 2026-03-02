#!/usr/bin/env python3
"""
Dump ArkUI layout tree from HarmonyOS device.
Usage: python3 dump_layout.py [--device <device_id>] [--output <output_file>]
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from hdc_utils import DeviceResolutionError, find_hdc, get_devices, resolve_device


def dump_layout(hdc_path, device_id=None, output_path=None):
    """Dump layout from device and return local file path."""
    # Build command
    cmd = [hdc_path]
    if device_id:
        cmd.extend(["-t", device_id])
    cmd.extend(["shell", "uitest", "dumpLayout"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"Dump failed: {result.stderr}", file=sys.stderr)
            return None

        # Parse output to get remote file path
        # Output format: "DumpLayout saved to:/data/local/tmp/layout_xxx.json"
        output = result.stdout.strip()
        if "DumpLayout saved to:" in output:
            remote_path = output.split("DumpLayout saved to:")[1].strip()

            # Generate local path
            if output_path:
                local_path = str(Path(output_path).expanduser())
                Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            else:
                local_path = f"/tmp/harmonyos_layout_{int(time.time())}.json"

            # Pull file from device
            pull_cmd = [hdc_path]
            if device_id:
                pull_cmd.extend(["-t", device_id])
            pull_cmd.extend(["file", "recv", remote_path, local_path])

            pull_result = subprocess.run(pull_cmd, capture_output=True, text=True, timeout=30)

            if pull_result.returncode == 0 and os.path.exists(local_path):
                return local_path
            else:
                print(f"Failed to pull layout file: {pull_result.stderr}", file=sys.stderr)

        return None

    except subprocess.TimeoutExpired:
        print("Timeout while dumping layout", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error dumping layout: {e}", file=sys.stderr)
        return None


def parse_bounds(bounds_str):
    """Parse bounds string "[left,top][right,bottom]" to tuple."""
    try:
        if not bounds_str:
            return None
        # Format: "[left,top][right,bottom]"
        import re
        match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
        if match:
            left, top, right, bottom = map(int, match.groups())
            return (left, top, right, bottom)
    except:
        pass
    return None


def get_center(bounds):
    """Get center point of bounds."""
    if bounds:
        left, top, right, bottom = bounds
        return ((left + right) // 2, (top + bottom) // 2)
    return None


def extract_interactive_components(node, components=None, depth=0):
    """Extract all interactive components from layout tree."""
    if components is None:
        components = []

    attrs = node.get("attributes", {})

    # Check if component is interactive
    is_clickable = attrs.get("clickable", "false").lower() == "true"
    is_long_clickable = attrs.get("longClickable", "false").lower() == "true"
    is_scrollable = attrs.get("scrollable", "false").lower() == "true"
    is_enabled = attrs.get("enabled", "true").lower() == "true"
    is_visible = attrs.get("visible", "true").lower() == "true"
    has_text = bool(attrs.get("text", "").strip())
    has_id = bool(attrs.get("id", "").strip())

    # Include component if it's interactive or has meaningful content
    if (is_clickable or is_long_clickable or is_scrollable or has_text) and is_enabled and is_visible:
        bounds = parse_bounds(attrs.get("bounds", ""))
        center = get_center(bounds)

        component = {
            "text": attrs.get("text", ""),
            "originalText": attrs.get("originalText", ""),
            "type": attrs.get("type", ""),
            "id": attrs.get("id", ""),
            "description": attrs.get("description", ""),
            "bounds": bounds,
            "center": center,
            "clickable": is_clickable,
            "longClickable": is_long_clickable,
            "scrollable": is_scrollable,
            "depth": depth,
            "hierarchy": attrs.get("hierarchy", ""),
            "accessibilityId": attrs.get("accessibilityId", ""),
        }
        components.append(component)

    # Recursively process children
    for child in node.get("children", []):
        extract_interactive_components(child, components, depth + 1)

    return components


def summarize_layout(layout_data):
    """Generate a summary of the layout."""
    components = extract_interactive_components(layout_data)

    # Group by type
    type_counts = {}
    for comp in components:
        t = comp["type"] or "Unknown"
        type_counts[t] = type_counts.get(t, 0) + 1

    # Get clickable items with text
    clickable_items = [
        comp for comp in components
        if comp["clickable"] and (comp["text"] or comp["id"])
    ]

    summary = {
        "total_components": len(components),
        "clickable_count": len([c for c in components if c["clickable"]]),
        "type_distribution": type_counts,
        "clickable_items": [
            {
                "text": c["text"] or c["id"],
                "type": c["type"],
                "center": c["center"],
            }
            for c in clickable_items[:20]  # Limit output
        ]
    }

    return summary, components


def main():
    parser = argparse.ArgumentParser(description="Dump ArkUI layout from HarmonyOS device")
    parser.add_argument("--device", "-d", help="Device ID (e.g., 127.0.0.1:5555)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--summary", "-s", action="store_true", help="Print summary only")
    args = parser.parse_args()

    hdc_path = find_hdc()

    # Get device
    devices = get_devices(hdc_path)
    if not devices:
        print("No devices found. Please connect a device via hdc.", file=sys.stderr)
        sys.exit(1)

    try:
        device_id = resolve_device(hdc_path, args.device, strict_multi=True)
    except DeviceResolutionError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    print(f"Using device: {device_id}", file=sys.stderr)

    # Dump layout
    layout_path = dump_layout(hdc_path, device_id, args.output)
    if not layout_path:
        print("Failed to dump layout", file=sys.stderr)
        sys.exit(1)

    print(f"Layout saved to: {layout_path}")

    # Load and summarize
    with open(layout_path, 'r', encoding='utf-8') as f:
        layout_data = json.load(f)

    summary, components = summarize_layout(layout_data)

    if args.summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        # Output summary info
        print(f"\n=== Layout Summary ===")
        print(f"Total interactive components: {summary['total_components']}")
        print(f"Clickable components: {summary['clickable_count']}")

        print(f"\n=== Clickable Items ===")
        for item in summary['clickable_items']:
            text = item['text']
            ctype = item['type']
            center = item['center']
            print(f"  [{ctype}] \"{text}\" at {center}")

        print(f"\n=== Type Distribution ===")
        for t, count in sorted(summary['type_distribution'].items(), key=lambda x: -x[1]):
            print(f"  {t}: {count}")

        print(f"\nLayout file: {layout_path}")

    # Save components to separate file for easy access
    components_path = layout_path.replace('.json', '_components.json')
    with open(components_path, 'w', encoding='utf-8') as f:
        json.dump(components, f, ensure_ascii=False, indent=2)
    print(f"Components file: {components_path}")

    return layout_path


if __name__ == "__main__":
    main()
