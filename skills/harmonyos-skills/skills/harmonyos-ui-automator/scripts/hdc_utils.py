#!/usr/bin/env python3
"""
Shared helpers for locating hdc and resolving connected HarmonyOS devices.
"""

import glob
import os
import subprocess
from typing import List, Optional


class DeviceResolutionError(RuntimeError):
    """Raised when target device cannot be resolved safely."""


def _candidate_hdc_paths() -> List[str]:
    candidates: List[str] = []

    sdk_root = os.path.expanduser("~/Library/OpenHarmony/Sdk")
    for path in sorted(glob.glob(os.path.join(sdk_root, "*/toolchains/hdc")), reverse=True):
        candidates.append(path)

    candidates.append("/Applications/DevEco-Studio.app/Contents/sdk/default/openharmony/toolchains/hdc")
    candidates.append("hdc")
    return candidates


def find_hdc() -> str:
    """Find an available hdc binary path."""
    for path in _candidate_hdc_paths():
        if path != "hdc" and not os.path.exists(path):
            continue
        try:
            result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return path
        except Exception:
            continue
    return "hdc"


def get_devices(hdc_path: str) -> List[str]:
    """Get list of connected devices via hdc list targets."""
    try:
        result = subprocess.run([hdc_path, "list", "targets"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return [d.strip() for d in result.stdout.strip().split("\n") if d.strip()]
    except Exception:
        pass
    return []


def resolve_device(
    hdc_path: str,
    preferred_device: Optional[str] = None,
    strict_multi: bool = True,
) -> Optional[str]:
    """Resolve active device.

    If strict_multi is True and multiple devices are connected, raise an
    explicit error and require caller to pass --device.
    """
    if preferred_device:
        return preferred_device
    devices = get_devices(hdc_path)
    if not devices:
        return None
    if len(devices) > 1 and strict_multi:
        raise DeviceResolutionError(
            f"Multiple devices found: {devices}. Please pass --device explicitly."
        )
    return devices[0]
