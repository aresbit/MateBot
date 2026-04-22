#!/bin/bash
set -euo pipefail

# Package WSL Proxy Fix Skill for Claude Code
# Creates a ZIP file that can be imported into Claude Code

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="wsl-proxy-fix"
SKILL_DIR="$SCRIPT_DIR"
OUTPUT_DIR="$SCRIPT_DIR/../dist"
ZIP_FILE="$OUTPUT_DIR/${SKILL_NAME}-skill.zip"

echo "============================================"
echo "  Packaging WSL Proxy Fix Skill"
echo "============================================"

# Check required files
echo "Step 1: Validating skill files..."
if [[ ! -f "$SKILL_DIR/SKILL.md" ]]; then
    echo "❌ Error: Missing SKILL.md"
    exit 1
fi

if [[ ! -f "../../tools/wsl-proxy-fix.sh" ]]; then
    echo "❌ Error: Missing tools/wsl-proxy-fix.sh"
    exit 1
fi

echo "✅ SKILL.md found"
echo "✅ Script file found"

# Create output directory
echo "Step 2: Creating output directory..."
mkdir -p "$OUTPUT_DIR"
rm -f "$ZIP_FILE" 2>/dev/null || true

# Create temporary directory for packaging
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Step 3: Copying skill files..."
cp -r "$SKILL_DIR/SKILL.md" "$TEMP_DIR/"
cp "../../tools/wsl-proxy-fix.sh" "$TEMP_DIR/"

# Create a simple README
cat > "$TEMP_DIR/README.md" << 'EOF'
# WSL Proxy Fix Skill

This skill helps fix git proxy connection errors in WSL environments.

## Installation
1. Import this ZIP file into Claude Code
2. The skill will be available for Claude to reference

## Usage
Claude can now help you fix WSL git proxy issues by referencing this skill.

## Files
- `SKILL.md`: Main skill documentation
- `wsl-proxy-fix.sh`: Fix script (can be run manually)

## Manual Usage
```bash
# Make script executable
chmod +x wsl-proxy-fix.sh

# Diagnose issues
./wsl-proxy-fix.sh --diagnose

# Auto-fix
./wsl-proxy-fix.sh --auto
```

## Author
ericyangbit
EOF

# Create package info file
cat > "$TEMP_DIR/package.json" << EOF
{
  "name": "wsl-proxy-fix",
  "version": "1.0.0",
  "description": "Fix WSL git proxy connection errors",
  "author": "ericyangbit",
  "license": "MIT",
  "claude_code": {
    "skill": true,
    "category": "troubleshooting"
  }
}
EOF

echo "Step 4: Creating ZIP archive..."
cd "$TEMP_DIR"
zip -r "$ZIP_FILE" . > /dev/null

echo "Step 5: Verifying package..."
if [[ -f "$ZIP_FILE" ]]; then
    FILE_SIZE=$(du -h "$ZIP_FILE" | cut -f1)
    echo "✅ Package created: $ZIP_FILE ($FILE_SIZE)"
    echo "✅ Files included:"
    zipinfo -1 "$ZIP_FILE" | while read -r file; do
        echo "   - $file"
    done
else
    echo "❌ Error: Failed to create ZIP file"
    exit 1
fi

echo ""
echo "============================================"
echo "  Packaging Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Import into Claude Code:"
echo "   - Open Claude Code"
echo "   - Go to Skills section"
echo "   - Click 'Import Skill'"
echo "   - Select: $ZIP_FILE"
echo ""
echo "2. Or use with skill-seekers:"
echo "   skill-seekers package $SKILL_DIR --target claude"
echo ""
echo "3. Manual usage:"
echo "   cp $ZIP_FILE ~/.claude/skills/"
echo ""