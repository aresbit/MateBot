#!/usr/bin/env python3
"""
Apply a binary patch to a target file.
Usage: apply_patch.py <patch.bin> <target> --offset 0x1139
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Apply binary patch to target file')
    parser.add_argument('patch', help='Patch file (binary)')
    parser.add_argument('target', help='Target file to patch')
    parser.add_argument('--offset', '-o', required=True, help='Offset to apply patch (hex or decimal)')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would be done')

    args = parser.parse_args()

    # Parse offset
    offset_str = args.offset
    if offset_str.startswith('0x') or offset_str.startswith('0X'):
        offset = int(offset_str, 16)
    else:
        offset = int(offset_str)

    # Read patch
    try:
        with open(args.patch, 'rb') as f:
            patch_data = f.read()
    except FileNotFoundError:
        print(f"Error: Patch file '{args.patch}' not found", file=sys.stderr)
        sys.exit(1)

    print(f"Patch size: {len(patch_data)} bytes")
    print(f"Target offset: 0x{offset:x} ({offset})")

    if args.dry_run:
        print(f"[DRY RUN] Would write {len(patch_data)} bytes to {args.target} at offset 0x{offset:x}")
        return

    # Apply patch
    try:
        with open(args.target, 'r+b') as f:
            f.seek(offset)
            f.write(patch_data)
        print(f"Successfully applied patch to {args.target}")
    except FileNotFoundError:
        print(f"Error: Target file '{args.target}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error applying patch: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
