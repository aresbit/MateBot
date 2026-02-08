#!/bin/bash

# Git Worktree Pattern - Detailed Reference

## What is the Bare Repo Pattern?

The bare repo pattern places all git data in a `.bare/` directory and creates worktrees as subdirectories. This solves the organization problems of native git worktrees.

## Comparison

### Traditional Clone
```
~/dev/
├── my-repo/              # main (has .git/)
├── my-repo-feature/      # worktree (outside, messy)
└── my-repo-hotfix/       # worktree (outside, messy)
```

### Bare Repo Pattern
```
~/dev/my-project/
├── .bare/            # All git data lives here
├── .git              # Just a pointer file
├── main/             # Worktree: main branch
└── feature/          # Worktree: feature branch
```

## Manual Setup (Without git-wt)

If you want to understand what's happening under the hood:

```bash
mkdir my-project && cd my-project
git clone --bare https://github.com/user/repo.git .bare

# Create pointer file (the magic)
echo "gitdir: ./.bare" > .git

# Configure for all branches
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"

# Make portable (can move folder)
git config worktree.useRelativePaths true

git fetch --all

# Create worktrees INSIDE the project
git worktree add main main
git worktree add feature origin/feature
```

## Key Configuration

### The .git file
A file (not directory) containing:
```
gitdir: ./.bare
```

This tells git: "The real repo data is in .bare/"

### Remote fetch configuration
```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
```

Bare clones don't fetch all branches by default. This fixes it.

### Relative paths
```bash
git config worktree.useRelativePaths true
```

Allows moving the entire project folder without breaking worktrees.

## Benefits

1. **Organization** - Everything in one folder
2. **No orphans** - Delete folder = clean removal
3. **Visibility** - `ls` shows your branches
4. **Project configs** - Store local configs at project root

## Use Cases

### AI Agent Isolation
Multiple agents working simultaneously:
```
project/
├── .bare/
├── main/
├── agent-refactor/
├── agent-add-tests/
└── agent-fix-types/
```

### Local Development Environment
```
project/
├── flake.nix         # Your nix setup
├── mise.toml         # Your runtime versions
├── .env              # Your secrets
├── .bare/
└── main/
```

### Personal Scratchpad
```
project/
├── _/                # Scripts, notes, prompts
├── .claude/          # Experimental prompts
├── .bare/
└── main/
```

## Shell Integration

### Jump to worktree
Add to `.bashrc` or `.zshrc`:
```bash
wt() {
    local dir
    dir=$(git wt switch)
    [[ -n "$dir" ]] && cd "$dir"
}
```

### Auto-complete
Git wt includes completions for bash, zsh, and fish when installed via Homebrew/Nix.

## Migration from Traditional Clone

The `git wt migrate` command handles:
1. Creating bare structure
2. Moving git data to `.bare/`
3. Preserving uncommitted changes (staged, unstaged, stashes)
4. Converting current directory to worktree

**What it preserves:**
- All branches (local and remote tracking)
- Staged files
- Unstaged changes
- Stashes
- Git config (remote URLs, etc.)

## References

- [Git Worktrees Done Right](https://gabri.me/blog/git-worktrees-done-right) - Original article
- [Git Documentation - git-worktree](https://git-scm.com/docs/git-worktree)
- [Git Documentation - --bare](https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---bare)
- [Anthropic Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices#c-use-git-worktrees)
- [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices#native-worktree-support)
