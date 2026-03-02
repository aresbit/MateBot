# OHOS App Build & Debug - Command Reference

Complete reference for all scripts in the ohos-app-build-debug skill.

## build.py - Build Application

Compile HarmonyOS/OpenHarmony applications using hvigorw.

### Usage

```bash
python3 $SKILL_DIR/scripts/build.py [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-m, --mode` | Build mode (debug/release) | debug |
| `-d, --dir` | Project root directory | . |
| `--module` | Module name | entry |
| `--show-env` | Show environment detection info | false |

### Examples

```bash
# Build debug version (default)
python3 $SKILL_DIR/scripts/build.py

# Build release version
python3 $SKILL_DIR/scripts/build.py -m release

# Build specific project
python3 $SKILL_DIR/scripts/build.py --dir /path/to/project

# Build with environment info
python3 $SKILL_DIR/scripts/build.py --show-env

# Build specific module
python3 $SKILL_DIR/scripts/build.py --module entry
```

### Output

Returns path to compiled HAP file:
```
entry/build/default/outputs/default/entry-default-signed.hap
```

---

## install.py - Install HAP to Device

Install HAP files to connected HarmonyOS/OpenHarmony devices.

### Usage

```bash
python3 $SKILL_DIR/scripts/install.py -f <hap-file> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --file` | HAP file path (required) | - |
| `-d, --device` | Device ID | auto-detect |
| `-r, --reinstall` | Overwrite existing installation | true |
| `--no-reinstall` | Don't overwrite existing | - |
| `-u, --user` | User ID | - |

### Examples

```bash
# Install HAP file
python3 $SKILL_DIR/scripts/install.py -f app.hap

# Install to specific device
python3 $SKILL_DIR/scripts/install.py -f app.hap -d DEVICE_ID

# Install without overwriting
python3 $SKILL_DIR/scripts/install.py -f app.hap --no-reinstall

# Install for specific user
python3 $SKILL_DIR/scripts/install.py -f app.hap -u 100
```

### Output

Returns bundle name of installed app:
```
com.example.app
```

---

## launch.py - Launch Application

Launch installed HarmonyOS/OpenHarmony applications.

### Usage

```bash
python3 $SKILL_DIR/scripts/launch.py [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-b, --bundle` | Application bundle name | auto-detect from project |
| `-a, --ability` | Ability name | EntryAbility |
| `-d, --device` | Device ID | auto-detect |
| `-m, --module` | Module name | entry |
| `--dir` | Project root directory | . |

### Examples

```bash
# Auto-detect and launch from project directory
python3 $SKILL_DIR/scripts/launch.py --dir .

# Launch specific bundle
python3 $SKILL_DIR/scripts/launch.py -b com.example.app

# Launch with specific ability
python3 $SKILL_DIR/scripts/launch.py -b com.example.app -a MainAbility

# Launch on specific device
python3 $SKILL_DIR/scripts/launch.py -b com.example.app -d DEVICE_ID
```

### Output

Returns process ID if launch successful:
```
1234
```

---

## screenshot.py - Take Screenshot

Capture device screen screenshots.

### Usage

```bash
python3 $SKILL_DIR/scripts/screenshot.py [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output directory | ./screenshots |
| `-d, --device` | Device ID | auto-detect |

### Examples

```bash
# Take screenshot (saves to ./screenshots/)
python3 $SKILL_DIR/scripts/screenshot.py

# Save to specific directory
python3 $SKILL_DIR/scripts/screenshot.py -o ~/Desktop/screenshots

# Capture from specific device
python3 $SKILL_DIR/scripts/screenshot.py -d DEVICE_ID
```

### Output

Saved screenshot with timestamp:
```
screenshots/screenshot_20250209_143022.png
```

---

## parse_crash.py - Parse Crash Stack

Parse HarmonyOS/OpenHarmony crash stacks using hstack tool.

### Usage

```bash
python3 $SKILL_DIR/scripts/parse_crash.py (-f <file> | -c <content>)
```

### Options

| Option | Description |
|--------|-------------|
| `-f, --file` | Read crash stack from file |
| `-c, --content` | Parse crash stack from string |

### Examples

```bash
# Parse from file
python3 $SKILL_DIR/scripts/parse_crash.py -f crash.txt

# Parse from string
python3 $SKILL_DIR/scripts/parse_crash.py -c "Fatal Error 10 [package]..."
```

---

## env_detector.py - Environment Detection

Detect DevEco Studio installation and toolchain.

### Usage

```bash
python3 $SKILL_DIR/scripts/env_detector.py [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--refresh, -r` | Force refresh cache (bypass 24-hour cache) |

### Examples

```bash
# Show environment info
python3 $SKILL_DIR/scripts/env_detector.py

# Force refresh cache
python3 $SKILL_DIR/scripts/env_detector.py --refresh
```

### Output Example

```
============================================================
Environment Detection Result
============================================================

✓ Detection Source: DevEco Studio
  Installation: /Applications/DevEco-Studio.app

✓ Java Home: /Applications/DevEco-Studio.app/Contents/jbr/Contents/Home
✓ SDK Path: /Applications/DevEco-Studio.app/Contents/sdk
✓ Available Tools:
    hdc: .../toolchains/hdc
    hvigorw: .../tools/hvigor/bin/hvigorw
    java: .../jbr/Contents/Home/bin/java
    clang: .../llvm/bin/clang
    idl: .../toolchains/idl
    restool: .../toolchains/restool

============================================================
```

---

## Common Patterns

### Build Output Capture

Capture build output for use in install:

```bash
HAP_FILE=$(python3 $SKILL_DIR/scripts/build.py | tail -1)
python3 $SKILL_DIR/scripts/install.py -f "$HAP_FILE"
```

### Bundle Name Capture

Capture bundle name for use in launch:

```bash
BUNDLE_NAME=$(python3 $SKILL_DIR/scripts/install.py -f app.hap | tail -1)
python3 $SKILL_DIR/scripts/launch.py -b "$BUNDLE_NAME"
```

### Full Pipeline

```bash
# Set project directory
PROJECT_DIR="/path/to/project"

# Build
cd "$PROJECT_DIR"
HAP_FILE=$(python3 ~/.claude/skills/ohos-app-build-debug/scripts/build.py | tail -1)

# Install
BUNDLE_NAME=$(python3 ~/.claude/skills/ohos-app-build-debug/scripts/install.py -f "$HAP_FILE" | tail -1)

# Launch
python3 ~/.claude/skills/ohos-app-build-debug/scripts/launch.py -b "$BUNDLE_NAME"
```
