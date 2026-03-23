#!/usr/bin/env bash
# Install SPCL toolkit from source
set -euo pipefail

REPO_URL="${SPCL_REPO_URL:-https://github.com/aresbit/spcl.git}"
INSTALL_PREFIX="${PREFIX:-/usr/local}"

echo "=== SPCL Installation ==="
echo "Repository: $REPO_URL"
echo "Prefix: $INSTALL_PREFIX"

# Check dependencies
echo "Checking dependencies..."
command -v git >/dev/null 2>&1 || { echo "Error: git required"; exit 1; }
command -v make >/dev/null 2>&1 || { echo "Error: make required"; exit 1; }
command -v cc >/dev/null 2>&1 || { echo "Error: C compiler required"; exit 1; }

# Clone or update
if [[ -d spcl ]]; then
    echo "Updating existing spcl directory..."
    cd spcl
    git pull
else
    echo "Cloning repository..."
    git clone "$REPO_URL"
    cd spcl
fi

# Build
echo "Building..."
make clean
make all

# Install
echo "Installing to $INSTALL_PREFIX (may require sudo)..."
if [[ -w "$INSTALL_PREFIX/bin" ]]; then
    make uninstall install PREFIX="$INSTALL_PREFIX"
else
    sudo make uninstall install PREFIX="$INSTALL_PREFIX"
fi

# Verify
echo ""
echo "=== Verification ==="
echo "Installed commands:"
command -v werk && echo "  ✓ werk"
command -v spcl && echo "  ✓ spcl"
command -v llskill2spcl && echo "  ✓ llskill2spcl"

echo ""
echo "Installation complete!"
