# =============================================================================
# MateBot - Modern Makefile
# =============================================================================
# A modern Makefile for installing MateBot scripts to system directories.
# Based on modern-c-makefile best practices.
#
# Usage:
#   make install       Install scripts to user directory (default: ~/.local)
#   make uninstall     Remove installed scripts
#   make clean         Clean generated files
#   make test          Run basic tests
#   make check         Check dependencies
#
# Variables:
#   PREFIX             Installation prefix (default: $(HOME)/.local)
#   DESTDIR            Destination directory (for packaging)
#   BINDIR             Binary directory (default: $(PREFIX)/bin)
#   LIBDIR             Library directory (default: $(PREFIX)/lib/matebot)
#   SHAREDIR           Share directory (default: $(PREFIX)/share/matebot)
#   DOCDIR             Documentation directory (default: $(PREFIX)/share/doc/matebot)
#
# Examples:
#   make install                           # Install to ~/.local (no sudo needed)
#   make install PREFIX=/opt/matebot       # Custom prefix
#   sudo make install PREFIX=/usr/local    # System-wide install (requires sudo)
# =============================================================================

# -----------------------------------------------------------------------------
# Project Configuration
# -----------------------------------------------------------------------------

# Project info
NAME        := MateBot
VERSION     := 1.0.0
DESCRIPTION := Claude Code Telegram Bridge

# Installation directories (default to user-local, no sudo needed)
PREFIX          := $(HOME)/.local
DESTDIR         :=
BINDIR          := $(DESTDIR)$(PREFIX)/bin
LIBDIR          := $(DESTDIR)$(PREFIX)/lib/matebot
SHAREDIR        := $(DESTDIR)$(PREFIX)/share/matebot
DOCDIR          := $(DESTDIR)$(PREFIX)/share/doc/matebot
CLAUDE_HOOKDIR  := $(HOME)/.claude/hooks
CLAUDE_SKILLDIR := $(HOME)/.claude/skills
CLAUDE_DISABLED_SKILLDIR := $(CLAUDE_SKILLDIR)/.disabled

# Source files
SCRIPT_SRCS := matecode.sh bridge_manager.sh start_bridge.sh stop_bridge.sh tmux-setup.sh
PY_MODULES  := bridge.py attention_manager.py external_memory.py memory.py failure_memory.py kv_cache.py

# -----------------------------------------------------------------------------
# Colors for Output
# -----------------------------------------------------------------------------

ifeq ($(TERM),dumb)
  NO_COLOR := 1
endif

ifdef NO_COLOR
  CYAN    :=
  GREEN   :=
  YELLOW  :=
  RED     :=
  RESET   :=
else
  CYAN    := \033[36m
  GREEN   := \033[32m
  YELLOW  := \033[33m
  RED     := \033[31m
  RESET   := \033[0m
endif

# -----------------------------------------------------------------------------
# Helper Macros
# -----------------------------------------------------------------------------

define print_info
	@printf "$(CYAN)==>$(RESET) %s\n" "$(1)"
endef

define print_success
	@printf "$(GREEN)✓$(RESET) %s\n" "$(1)"
endef

define print_warn
	@printf "$(YELLOW)!$(RESET) %s\n" "$(1)"
endef

define print_error
	@printf "$(RED)✗$(RESET) %s\n" "$(1)"
endef

# -----------------------------------------------------------------------------
# Default Target
# -----------------------------------------------------------------------------

.PHONY: all help install uninstall clean test check dry-run skill

all: help

# -----------------------------------------------------------------------------
# Help Target
# -----------------------------------------------------------------------------

help:
	@printf "$(CYAN)%s$(RESET) v%s - %s\n\n" "$(NAME)" "$(VERSION)" "$(DESCRIPTION)"
	@echo "Targets:"
	@echo "  $(GREEN)install$(RESET)      Install $(NAME) to system directories"
	@echo "  $(GREEN)uninstall$(RESET)    Remove $(NAME) from system directories"
	@echo "  $(GREEN)clean$(RESET)        Clean generated files"
	@echo "  $(GREEN)test$(RESET)         Run basic tests"
	@echo "  $(GREEN)check$(RESET)        Check dependencies"
	@echo "  $(GREEN)dry-run$(RESET)      Show what would be installed"
	@echo "  $(GREEN)skill$(RESET)        Install local skills to ~/.claude/skills (no overwrite)"
	@echo ""
	@echo "Variables:"
	@echo "  $(YELLOW)PREFIX$(RESET)       Installation prefix [$(HOME)/.local]"
	@echo "  $(YELLOW)DESTDIR$(RESET)      Destination directory (for packaging)"
	@echo "  $(YELLOW)BINDIR$(RESET)       Binary directory [$(BINDIR)]"
	@echo "  $(YELLOW)LIBDIR$(RESET)       Library directory [$(LIBDIR)]"
	@echo "  $(YELLOW)NO_COLOR$(RESET)     Disable colored output"
	@echo ""
	@echo "Examples:"
	@echo "  make install                           # User install, no sudo"
	@echo "  make install PREFIX=/opt/matebot       # Custom prefix"
	@echo "  sudo make install PREFIX=/usr/local    # System-wide install"

# -----------------------------------------------------------------------------
# Dependency Checks
# -----------------------------------------------------------------------------

check:
	$(call print_info,"Checking dependencies...")
	@command -v python3 >/dev/null 2>&1 || { $(call print_error,"python3 not found"); exit 1; }
	@command -v tmux >/dev/null 2>&1 || { $(call print_warn,"tmux not found - recommended for matecode"); }
	@$(call print_success,"All critical dependencies satisfied")

# -----------------------------------------------------------------------------
# Directory Creation
# -----------------------------------------------------------------------------

$(BINDIR) $(LIBDIR) $(SHAREDIR) $(DOCDIR) $(CLAUDE_HOOKDIR):
	@mkdir -p "$@"

# -----------------------------------------------------------------------------
# Install Target
# -----------------------------------------------------------------------------

install: check $(BINDIR) $(LIBDIR) $(SHAREDIR) $(DOCDIR) $(CLAUDE_HOOKDIR)
	$(call print_info,"Installing $(NAME) v$(VERSION)...")

	@$(call print_info,"Installing executables to $(BINDIR)...")
	@for script in $(SCRIPT_SRCS); do \
		base=$$(basename "$$script" .sh); \
		install -m 755 "$$script" "$(BINDIR)/$$base" && \
		printf "$(GREEN)✓$(RESET) Installed %s\n" "$$base"; \
	done

	@$(call print_info,"Installing Python modules to $(LIBDIR)...")
	@for file in $(PY_MODULES); do \
		if [ -f "$$file" ]; then \
			install -m 644 "$$file" "$(LIBDIR)/" && \
			printf "$(GREEN)✓$(RESET) Installed %s\n" "$$file"; \
		fi \
	done

	@$(call print_info,"Installing hooks to $(LIBDIR)/hooks...")
	@mkdir -p "$(LIBDIR)/hooks"
	@for hook in hooks/*.sh; do \
		if [ -f "$$hook" ]; then \
			install -m 755 "$$hook" "$(LIBDIR)/hooks/" && \
			printf "$(GREEN)✓$(RESET) Installed %s\n" "$$(basename $$hook)"; \
		fi \
	done

	@$(call print_info,"Installing Claude Code hooks to $(CLAUDE_HOOKDIR)...")
	@mkdir -p "$(CLAUDE_HOOKDIR)"
	@for hook in hooks/*.sh; do \
		if [ -f "$$hook" ]; then \
			base=$$(basename "$$hook" .sh); \
			install -m 755 "$$hook" "$(CLAUDE_HOOKDIR)/$$base" && \
			printf "$(GREEN)✓$(RESET) Installed %s\n" "$$base"; \
		fi \
	done

	@$(call print_info,"Installing skills to $(SHAREDIR)...")
	@cp -r skills "$(SHAREDIR)/" 2>/dev/null || true
	@find "$(SHAREDIR)/skills" -type f -name "*.sh" -exec chmod 755 {} \; 2>/dev/null || true
	@find "$(SHAREDIR)/skills" -type f -name "*.py" -exec chmod 644 {} \; 2>/dev/null || true
	@$(call print_success,"Installed skills")

	@$(call print_info,"Installing documentation to $(DOCDIR)...")
	@for doc in README.md CHANGELOG.md GUIDE.md TMUX_SETUP.md; do \
		if [ -f "$$doc" ]; then \
			install -m 644 "$$doc" "$(DOCDIR)/" && \
			printf "$(GREEN)✓$(RESET) Installed %s\n" "$$doc"; \
		fi \
	done

	@$(call print_info,"Creating wrapper script...")
	@echo '#!/bin/bash' > "$(BINDIR)/matebot"
	@echo '# $(NAME) v$(VERSION) - $(DESCRIPTION)' >> "$(BINDIR)/matebot"
	@echo '# Auto-generated wrapper script' >> "$(BINDIR)/matebot"
	@echo '' >> "$(BINDIR)/matebot"
	@echo 'export MATEBOT_HOME="$(LIBDIR)"' >> "$(BINDIR)/matebot"
	@echo 'export MATEBOT_SKILLS="$(SHAREDIR)/skills"' >> "$(BINDIR)/matebot"
	@echo 'export PYTHONPATH="$(LIBDIR):$$PYTHONPATH"' >> "$(BINDIR)/matebot"
	@echo '' >> "$(BINDIR)/matebot"
	@echo 'case "$$1" in' >> "$(BINDIR)/matebot"
	@echo '    start|stop|restart|status|logs)' >> "$(BINDIR)/matebot"
	@echo '        $(BINDIR)/matecode "$$@"' >> "$(BINDIR)/matebot"
	@echo '        ;;' >> "$(BINDIR)/matebot"
	@echo '    bridge)' >> "$(BINDIR)/matebot"
	@echo '        shift' >> "$(BINDIR)/matebot"
	@echo '        $(BINDIR)/bridge_manager "$$@"' >> "$(BINDIR)/matebot"
	@echo '        ;;' >> "$(BINDIR)/matebot"
	@echo '    *)' >> "$(BINDIR)/matebot"
	@echo '        echo "Usage: matebot {start|stop|restart|status|logs|bridge}"' >> "$(BINDIR)/matebot"
	@echo '        exit 1' >> "$(BINDIR)/matebot"
	@echo '        ;;' >> "$(BINDIR)/matebot"
	@echo 'esac' >> "$(BINDIR)/matebot"
	@chmod 755 "$(BINDIR)/matebot"
	@$(call print_success,"Created matebot wrapper")

	@echo ""
	@$(call print_success,"Installation complete!")
	@echo ""
	@echo "Usage:"
	@echo "  $(YELLOW)matebot start$(RESET)    - Start $(NAME) services"
	@echo "  $(YELLOW)matebot stop$(RESET)     - Stop $(NAME) services"
	@echo "  $(YELLOW)matebot status$(RESET)   - Check service status"
	@echo "  $(YELLOW)matebot bridge$(RESET)   - Manage bridge directly"
	@echo ""
	@echo "Note: Make sure $(BINDIR) is in your PATH"
	@echo "      and set TELEGRAM_BOT_TOKEN environment variable"

# -----------------------------------------------------------------------------
# Uninstall Target
# -----------------------------------------------------------------------------

uninstall:
	$(call print_info,"Uninstalling $(NAME)...")

	@$(call print_info,"Removing executables from $(BINDIR)...")
	@for script in matecode bridge_manager start_bridge stop_bridge tmux-setup matebot; do \
		if [ -f "$(BINDIR)/$$script" ]; then \
			rm -f "$(BINDIR)/$$script" && \
			printf "$(GREEN)✓$(RESET) Removed %s\n" "$$script"; \
		fi \
	done

	@$(call print_info,"Removing library files...")
	@if [ -d "$(LIBDIR)" ]; then \
		rm -rf "$(LIBDIR)" && \
		printf "$(GREEN)✓$(RESET) Removed %s\n" "$(LIBDIR)"; \
	fi

	@$(call print_info,"Removing share files...")
	@if [ -d "$(SHAREDIR)" ]; then \
		rm -rf "$(SHAREDIR)" && \
		printf "$(GREEN)✓$(RESET) Removed %s\n" "$(SHAREDIR)"; \
	fi

	@$(call print_info,"Removing documentation...")
	@if [ -d "$(DOCDIR)" ]; then \
		rm -rf "$(DOCDIR)" && \
		printf "$(GREEN)✓$(RESET) Removed %s\n" "$(DOCDIR)"; \
	fi

	@$(call print_info,"Removing Claude Code hooks...")
	@for hook in hooks/*.sh; do \
		if [ -f "$$hook" ]; then \
			base=$$(basename "$$hook" .sh); \
			if [ -f "$(CLAUDE_HOOKDIR)/$$base" ]; then \
				rm -f "$(CLAUDE_HOOKDIR)/$$base" && \
				printf "$(GREEN)✓$(RESET) Removed %s\n" "$$base"; \
			fi; \
		fi \
	done

	@$(call print_success,"Uninstall complete!")

# -----------------------------------------------------------------------------
# Clean Target
# -----------------------------------------------------------------------------

clean:
	$(call print_info,"Cleaning generated files...")
	@rm -f *.log *.pid
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@$(call print_success,"Clean complete")

# -----------------------------------------------------------------------------
# Test Target
# -----------------------------------------------------------------------------

test: check
	$(call print_info,"Running tests...")
	@echo "Testing script syntax..."
	@for script in $(SCRIPT_SRCS); do \
		bash -n "$$script" && \
		printf "$(GREEN)✓$(RESET) %s: syntax OK\n" "$$script"; \
	done
	@echo "Testing Python syntax..."
	@for py in $(PY_MODULES); do \
		if [ -f "$$py" ]; then \
			python3 -m py_compile "$$py" && \
			printf "$(GREEN)✓$(RESET) %s: syntax OK\n" "$$py"; \
		fi \
	done
	@$(call print_success,"All tests passed")

# -----------------------------------------------------------------------------
# Dry Run (for debugging)
# -----------------------------------------------------------------------------

dry-run:
	$(call print_info,"Dry run - would install to:")
	@echo "  BINDIR:         $(BINDIR)"
	@echo "  LIBDIR:         $(LIBDIR)"
	@echo "  SHAREDIR:       $(SHAREDIR)"
	@echo "  DOCDIR:         $(DOCDIR)"
	@echo "  CLAUDE_HOOKDIR: $(CLAUDE_HOOKDIR)"
	@echo ""
	@echo "Scripts to install:"
	@for script in $(SCRIPT_SRCS); do \
		base=$$(basename "$$script" .sh); \
		echo "  $$script -> $(BINDIR)/$$base"; \
	done
	@echo ""
	@echo "Claude hooks to install:"
	@for hook in hooks/*.sh; do \
		if [ -f "$$hook" ]; then \
			base=$$(basename "$$hook" .sh); \
			echo "  $$hook -> $(CLAUDE_HOOKDIR)/$$base"; \
		fi \
	done

# -----------------------------------------------------------------------------
# Install Skills to Claude Skill Directory (non-destructive)
# -----------------------------------------------------------------------------

skill:
	@printf "$(CYAN)==>$(RESET) %s\n" "Installing local skills to $(CLAUDE_SKILLDIR)..."
	@mkdir -p "$(CLAUDE_SKILLDIR)" "$(CLAUDE_DISABLED_SKILLDIR)"
	@installed=0; skipped_exists=0; skipped_tombstone=0; \
	for src in skills/*; do \
		[ -d "$$src" ] || continue; \
		name=$$(basename "$$src"); \
		dest="$(CLAUDE_SKILLDIR)/$$name"; \
		tombstone="$(CLAUDE_DISABLED_SKILLDIR)/$$name"; \
		if [ -e "$$tombstone" ]; then \
			printf "$(YELLOW)!$(RESET) Skipped %s (found tombstone in .disabled)\n" "$$name"; \
			skipped_tombstone=$$((skipped_tombstone + 1)); \
			continue; \
		fi; \
		if [ -e "$$dest" ]; then \
			printf "$(YELLOW)!$(RESET) Skipped %s (already exists)\n" "$$name"; \
			skipped_exists=$$((skipped_exists + 1)); \
			continue; \
		fi; \
		cp -R "$$src" "$$dest" && \
		printf "$(GREEN)✓$(RESET) Installed %s\n" "$$name" && \
		installed=$$((installed + 1)); \
	done; \
	printf "\nInstalled: %s, Skipped(existing): %s, Skipped(.disabled): %s\n" "$$installed" "$$skipped_exists" "$$skipped_tombstone"

# -----------------------------------------------------------------------------
# Individual Skill Installation (targets for each skill directory)
# -----------------------------------------------------------------------------
SKILLS := $(wildcard skills/*)
SKILL_NAMES := $(notdir $(SKILLS))

.PHONY: $(SKILL_NAMES)
$(SKILL_NAMES):
	@printf "$(CYAN)==>$(RESET) %s\n" "Installing skill $@ to $(CLAUDE_SKILLDIR)..."
	@mkdir -p "$(CLAUDE_SKILLDIR)" "$(CLAUDE_DISABLED_SKILLDIR)"
	@src="skills/$@"; \
	name="$@"; \
	dest="$(CLAUDE_SKILLDIR)/$$name"; \
	tombstone="$(CLAUDE_DISABLED_SKILLDIR)/$$name"; \
	if [ -e "$$tombstone" ]; then \
		printf "$(YELLOW)!$(RESET) Skipped %s (found tombstone in .disabled)\n" "$$name"; \
		exit 0; \
	fi; \
	if [ -e "$$dest" ]; then \
		printf "$(YELLOW)!$(RESET) Skipped %s (already exists)\n" "$$name"; \
		exit 0; \
	fi; \
	cp -R "$$src" "$$dest" && \
	printf "$(GREEN)✓$(RESET) Installed %s\n" "$$name";

# -----------------------------------------------------------------------------
# Default rule for unknown targets
# -----------------------------------------------------------------------------
%:
	@printf "$(RED)✗$(RESET) %s\n" "Unknown target '$@'. Try 'make help' for available targets."
	@exit 1
