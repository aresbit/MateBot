#!/bin/bash
# install-skill.sh - Install a single skill to ~/.claude/skills without overwriting
#
# Usage: ./install-skill.sh <skill-name>
#        make <skill-name>   # via Makefile pattern rule

set -e

# Colors for output
if [ -t 1 ]; then
    CYAN='\033[36m'
    GREEN='\033[32m'
    YELLOW='\033[33m'
    RED='\033[31m'
    RESET='\033[0m'
else
    CYAN=''
    GREEN=''
    YELLOW=''
    RED=''
    RESET=''
fi

print_info() {
    printf "${CYAN}==>${RESET} %s\n" "$1"
}

print_success() {
    printf "${GREEN}✓${RESET} %s\n" "$1"
}

print_warn() {
    printf "${YELLOW}!${RESET} %s\n" "$1"
}

print_error() {
    printf "${RED}✗${RESET} %s\n" "$1"
}

# Configuration
CLAUDE_SKILLDIR="${HOME}/.claude/skills"
CLAUDE_DISABLED_SKILLDIR="${CLAUDE_SKILLDIR}/.disabled"

if [ $# -ne 1 ]; then
    print_error "Usage: $0 <skill-name>"
    exit 1
fi

SKILL_NAME="$1"
SRC_DIR="skills/${SKILL_NAME}"
DEST_DIR="${CLAUDE_SKILLDIR}/${SKILL_NAME}"
TOMBSTONE="${CLAUDE_DISABLED_SKILLDIR}/${SKILL_NAME}"

# Validate source
if [ ! -d "${SRC_DIR}" ]; then
    print_error "Skill '${SKILL_NAME}' not found in skills/"
    exit 1
fi

# Create destination directories
mkdir -p "${CLAUDE_SKILLDIR}" "${CLAUDE_DISABLED_SKILLDIR}"

# Check for tombstone (disabled skill)
if [ -e "${TOMBSTONE}" ]; then
    print_warn "Skipped ${SKILL_NAME} (found tombstone in .disabled)"
    exit 0
fi

# Check if already exists
if [ -e "${DEST_DIR}" ]; then
    print_warn "Skipped ${SKILL_NAME} (already exists)"
    exit 0
fi

# Install skill
print_info "Installing skill ${SKILL_NAME} to ${CLAUDE_SKILLDIR}..."
cp -R "${SRC_DIR}" "${DEST_DIR}"
print_success "Installed ${SKILL_NAME}"