#!/bin/bash
# Install Python tools using uvx.sh
# Usage: ./install.sh <package> [version] [additional_args...]

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <package> [version] [additional_args...]"
    echo "Examples:"
    echo "  $0 ruff"
    echo "  $0 ruff 0.8.3"
    echo "  $0 ruff 0.8.3 --force"
    echo "  $0 cmake --index https://download.pytorch.org/whl/cpu"
    exit 1
fi

PACKAGE="$1"
shift

VERSION=""
EXTRA_ARGS=()

# Check if next argument looks like a version (starts with digit)
if [ $# -gt 0 ] && [[ "$1" =~ ^[0-9] ]]; then
    VERSION="$1"
    shift
fi

# Remaining arguments are extra args
if [ $# -gt 0 ]; then
    EXTRA_ARGS=("$@")
fi

# Build URL
if [ -n "$VERSION" ]; then
    URL="https://uvx.sh/${PACKAGE}/${VERSION}/install.sh"
else
    URL="https://uvx.sh/${PACKAGE}/install.sh"
fi

echo "Installing ${PACKAGE}${VERSION:+ version $VERSION}..."
echo "URL: $URL"

if [ ${#EXTRA_ARGS[@]} -gt 0 ]; then
    echo "Extra arguments: ${EXTRA_ARGS[*]}"
    curl -LsSf "$URL" | sh -s -- "${EXTRA_ARGS[@]}"
else
    curl -LsSf "$URL" | sh
fi

echo "Done."