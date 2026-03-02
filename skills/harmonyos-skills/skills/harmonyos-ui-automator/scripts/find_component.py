#!/usr/bin/env python3
"""
Find components in HarmonyOS layout by various criteria.
Usage: python3 find_component.py [--text <text>] [--id <id>] [--type <type>] [--clickable <true/false>] [--layout <layout_file>]
"""

import argparse
import json
import os
import re
import sys
from typing import List, Dict, Optional


def parse_bounds(bounds_str):
    """Parse bounds string "[left,top][right,bottom]" to tuple."""
    try:
        if not bounds_str:
            return None
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


def extract_all_components(node, components=None, depth=0):
    """Extract all components from layout tree."""
    if components is None:
        components = []

    attrs = node.get("attributes", {})

    bounds = parse_bounds(attrs.get("bounds", ""))

    component = {
        "text": attrs.get("text", ""),
        "originalText": attrs.get("originalText", ""),
        "type": attrs.get("type", ""),
        "id": attrs.get("id", ""),
        "description": attrs.get("description", ""),
        "hint": attrs.get("hint", ""),
        "bounds": bounds,
        "center": get_center(bounds),
        "clickable": attrs.get("clickable", "false").lower() == "true",
        "longClickable": attrs.get("longClickable", "false").lower() == "true",
        "scrollable": attrs.get("scrollable", "false").lower() == "true",
        "checkable": attrs.get("checkable", "false").lower() == "true",
        "checked": attrs.get("checked", "false").lower() == "true",
        "enabled": attrs.get("enabled", "true").lower() == "true",
        "visible": attrs.get("visible", "true").lower() == "true",
        "depth": depth,
        "hierarchy": attrs.get("hierarchy", ""),
        "accessibilityId": attrs.get("accessibilityId", ""),
        "bundleName": attrs.get("bundleName", ""),
    }
    components.append(component)

    for child in node.get("children", []):
        extract_all_components(child, components, depth + 1)

    return components


def match_component(comp: Dict, criteria: Dict) -> bool:
    """Check if component matches all criteria."""
    for key, value in criteria.items():
        if value is None:
            continue

        comp_value = comp.get(key)

        if key == "text":
            # Fuzzy text matching
            if value.lower() not in str(comp_value).lower():
                return False
        elif key == "text_exact":
            if value != comp.get("text"):
                return False
        elif key == "id":
            if value.lower() not in str(comp.get("id", "")).lower():
                return False
        elif key == "type":
            if value.lower() not in str(comp.get("type", "")).lower():
                return False
        elif key in ["clickable", "longClickable", "scrollable", "enabled", "visible"]:
            if isinstance(value, str):
                expected = value.lower() == "true"
            else:
                expected = bool(value)
            if comp.get(key) != expected:
                return False
        elif key == "description":
            if value.lower() not in str(comp.get("description", "")).lower():
                return False
        elif key == "regex":
            # Regex match on text or id
            if not re.search(value, comp.get("text", "") or comp.get("id", "")):
                return False
        else:
            if comp_value != value:
                return False

    return True


def find_components(components: List[Dict], criteria: Dict) -> List[Dict]:
    """Find all components matching criteria."""
    results = []
    for comp in components:
        if match_component(comp, criteria):
            results.append(comp)
    return results


def format_component(comp: Dict, verbose: bool = False) -> str:
    """Format component for display."""
    lines = []

    # Basic info
    text = comp.get("text", "") or comp.get("originalText", "") or "(no text)"
    comp_type = comp.get("type", "Unknown")
    comp_id = comp.get("id", "")
    center = comp.get("center")

    lines.append(f"  Text: \"{text}\"")
    lines.append(f"  Type: {comp_type}")
    if comp_id:
        lines.append(f"  ID: {comp_id}")
    if center:
        lines.append(f"  Center: ({center[0]}, {center[1]})")

    if verbose:
        bounds = comp.get("bounds")
        if bounds:
            lines.append(f"  Bounds: {bounds}")
        lines.append(f"  Clickable: {comp.get('clickable')}")
        lines.append(f"  Long Clickable: {comp.get('longClickable')}")
        lines.append(f"  Scrollable: {comp.get('scrollable')}")
        lines.append(f"  Enabled: {comp.get('enabled')}")
        lines.append(f"  Visible: {comp.get('visible')}")
        desc = comp.get("description", "")
        if desc:
            lines.append(f"  Description: {desc}")
        hint = comp.get("hint", "")
        if hint:
            lines.append(f"  Hint: {hint}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find components in HarmonyOS layout")
    parser.add_argument("--text", "-t", help="Find by text (fuzzy match)")
    parser.add_argument("--text-exact", help="Find by exact text match")
    parser.add_argument("--id", "-i", help="Find by ID (fuzzy match)")
    parser.add_argument("--type", help="Find by type (fuzzy match)")
    parser.add_argument("--description", help="Find by description")
    parser.add_argument("--clickable", choices=["true", "false"], help="Filter by clickable")
    parser.add_argument("--long-clickable", choices=["true", "false"], help="Filter by longClickable")
    parser.add_argument("--scrollable", choices=["true", "false"], help="Filter by scrollable")
    parser.add_argument("--enabled", choices=["true", "false"], help="Filter by enabled")
    parser.add_argument("--visible", choices=["true", "false"], help="Filter by visible")
    parser.add_argument("--regex", "-r", help="Regex pattern to match text or id")
    parser.add_argument("--layout", "-l", help="Path to layout JSON file")
    parser.add_argument("--components", "-c", help="Path to components JSON file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--first", "-f", action="store_true", help="Return only first match")
    parser.add_argument("--center-only", action="store_true", help="Output only center coordinates")
    args = parser.parse_args()

    # Build criteria
    criteria = {}
    if args.text:
        criteria["text"] = args.text
    if args.text_exact:
        criteria["text_exact"] = args.text_exact
    if args.id:
        criteria["id"] = args.id
    if args.type:
        criteria["type"] = args.type
    if args.description:
        criteria["description"] = args.description
    if args.clickable:
        criteria["clickable"] = args.clickable
    if args.long_clickable:
        criteria["longClickable"] = args.long_clickable
    if args.scrollable:
        criteria["scrollable"] = args.scrollable
    if args.enabled:
        criteria["enabled"] = args.enabled
    if args.visible:
        criteria["visible"] = args.visible
    if args.regex:
        criteria["regex"] = args.regex

    if not criteria:
        print("Error: No search criteria provided", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Find layout file
    layout_file = args.layout
    components_file = args.components

    if not layout_file and not components_file:
        # Try to find the most recent layout file
        tmp_dir = "/tmp"
        layout_files = [f for f in os.listdir(tmp_dir) if f.startswith("harmonyos_layout") and f.endswith(".json")]
        if layout_files:
            # Sort by modification time, prefer _components.json
            layout_files.sort(key=lambda f: os.path.getmtime(os.path.join(tmp_dir, f)), reverse=True)
            for f in layout_files:
                if "_components" in f:
                    components_file = os.path.join(tmp_dir, f)
                    break
            if not components_file:
                # Use the most recent layout file
                layout_file = os.path.join(tmp_dir, layout_files[0])

    # Load data
    components = None

    if components_file and os.path.exists(components_file):
        with open(components_file, 'r', encoding='utf-8') as f:
            components = json.load(f)
    elif layout_file and os.path.exists(layout_file):
        with open(layout_file, 'r', encoding='utf-8') as f:
            layout_data = json.load(f)
        components = extract_all_components(layout_data)
    else:
        print("Error: No layout file found. Run dump_layout.py first.", file=sys.stderr)
        sys.exit(1)

    # Search
    results = find_components(components, criteria)

    if not results:
        print("No matching components found", file=sys.stderr)
        sys.exit(1)

    if args.first:
        results = results[:1]

    # Output
    if args.center_only:
        for comp in results:
            center = comp.get("center")
            if center:
                print(f"{center[0]} {center[1]}")
    elif args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"Found {len(results)} component(s):\n")
        for i, comp in enumerate(results, 1):
            print(f"[{i}]")
            print(format_component(comp, args.verbose))
            print()


if __name__ == "__main__":
    main()
