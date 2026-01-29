#!/bin/bash
# =============================================================================
# MateBot Tmux Setup - Unified Configuration Script
# Simplified setup for open source project
# =============================================================================

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_info() { echo -e "${BLUE}[→]${NC} $1"; }

echo ""
echo "=========================================="
echo "   MateBot Tmux Setup"
echo "=========================================="
echo ""

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    print_error "tmux not found. Please install tmux first."
    echo ""
    echo "Installation:"
    echo "  Ubuntu/Debian: sudo apt-get install tmux"
    echo "  macOS:         brew install tmux"
    echo "  RHEL/CentOS:   sudo yum install tmux"
    exit 1
fi

# Install oh-my-tmux if not present
if [ ! -d "$HOME/.tmux" ]; then
    print_info "Installing oh-my-tmux..."
    git clone --depth 1 https://github.com/gpakosz/.tmux.git ~/.tmux
    ln -sf ~/.tmux/.tmux.conf ~/.tmux.conf
    print_success "oh-my-tmux installed"
else
    print_info "Updating oh-my-tmux..."
    cd ~/.tmux && git pull origin master
fi

# Copy MateBot configuration
PROJECT_DIR="/home/yangpt/yyscode/MateBot"
if [ -f "$PROJECT_DIR/.tmux.conf.local" ]; then
    print_info "Installing MateBot configuration..."
    cp "$PROJECT_DIR/.tmux.conf.local" ~/.tmux.conf.local
    print_success "Configuration installed"
    print_info "Copied from: $PROJECT_DIR/.tmux.conf.local"
    print_info "Copied to: $HOME/.tmux.conf.local"
else
    print_error "MateBot config not found at $PROJECT_DIR/.tmux.conf.local"
    exit 1
fi

# Verify installation
echo ""
print_info "Verifying installation..."

# Test configuration syntax
if tmux source-file ~/.tmux.conf.local 2>/dev/null; then
    print_success "Configuration syntax is valid"
else
    print_error "Configuration has syntax errors"
    exit 1
fi

# Check key settings
if grep -q "set -g mouse on" ~/.tmux.conf.local; then
    print_success "Mouse support configured"
fi

if grep -q "history-limit 50000" ~/.tmux.conf.local; then
    print_success "History limit set to 50000"
fi

echo ""
echo "=========================================="
echo "         Setup Complete"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  tmux new -s mysession"
echo ""
echo "Key features:"
echo "  ✓ Mouse support enabled"
echo "  ✓ 50000 line history limit"
echo "  ✓ Vi mode for copy/paste"
echo "  ✓ Quick window switch: Alt+1-5"
echo "  ✓ Status bar at top"
echo ""
echo "For help: Ctrl+b ?"
echo ""