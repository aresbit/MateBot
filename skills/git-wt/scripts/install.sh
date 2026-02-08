#!/bin/bash

# Git-wt Installation Script
# This script installs git-wt to your system

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_WT_SCRIPT="$SCRIPT_DIR/git-wt"

# Installation directories (in order of preference)
INSTALL_DIRS=(
    "$HOME/.local/bin"
    "$HOME/bin"
    "/usr/local/bin"
)

echo -e "${GREEN}Installing git-wt...${NC}"

# Check if git-wt script exists
if [[ ! -f "$GIT_WT_SCRIPT" ]]; then
    echo -e "${RED}Error: git-wt script not found at $GIT_WT_SCRIPT${NC}"
    exit 1
fi

# Find suitable installation directory
INSTALL_DIR=""
for dir in "${INSTALL_DIRS[@]}"; do
    # Check if directory exists and is writable, or can be created
    if [[ -d "$dir" ]] && [[ -w "$dir" ]]; then
        INSTALL_DIR="$dir"
        break
    elif [[ ! -d "$dir" ]] && mkdir -p "$dir" 2>/dev/null; then
        INSTALL_DIR="$dir"
        break
    fi
done

# If no suitable directory found, use ~/.local/bin as default
if [[ -z "$INSTALL_DIR" ]]; then
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

# Check if directory is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH${NC}"
    echo -e "${YELLOW}Add this to your shell profile (.bashrc, .zshrc, etc.):${NC}"
    echo -e "${YELLOW}  export PATH=\"$INSTALL_DIR:\$PATH\"${NC}"
    echo ""
fi

# Install the script
cp "$GIT_WT_SCRIPT" "$INSTALL_DIR/git-wt"
chmod +x "$INSTALL_DIR/git-wt"

echo -e "${GREEN}✓ Installed git-wt to $INSTALL_DIR/git-wt${NC}"

# Check for fzf
if ! command -v fzf &> /dev/null; then
    echo -e "${YELLOW}⚠ fzf not found. Install it for interactive features:${NC}"
    echo -e "${YELLOW}  brew install fzf    # macOS${NC}"
    echo -e "${YELLOW}  apt install fzf     # Ubuntu/Debian${NC}"
    echo ""
fi

# Check git version
GIT_VERSION=$(git --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
REQUIRED_VERSION="2.7"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$GIT_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]]; then
    echo -e "${YELLOW}⚠ Git version $GIT_VERSION found. git-wt requires Git 2.7+${NC}"
    echo ""
fi

# Verify installation
if command -v git-wt &> /dev/null || [[ -x "$INSTALL_DIR/git-wt" ]]; then
    echo -e "${GREEN}✓ Installation successful!${NC}"
    echo ""
    echo "Quick start:"
    echo "  git wt clone <url>     # Clone a repo with worktree structure"
    echo "  git wt add             # Create new worktree (interactive)"
    echo "  git wt switch          # Switch between worktrees"
    echo "  git wt --help          # Show all commands"
    echo ""
    echo "For more information:"
    echo "  cat /Users/mac/.claude/skills/git-wt/SKILL.md"
else
    echo -e "${YELLOW}⚠ Installation may have failed. Check your PATH.${NC}"
    echo -e "${YELLOW}  Try: $INSTALL_DIR/git-wt --help${NC}"
fi
