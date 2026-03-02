# Git-wt Commands Reference

Complete reference for all `git wt` commands.

## Core Commands

### clone
Clone a repository with bare worktree structure.

```bash
git wt clone <url> [directory]
```

**Examples:**
```bash
git wt clone https://github.com/user/repo.git
git wt clone https://github.com/user/repo.git my-project
```

**Result:**
```
repo/
├── .bare/          # Git data (bare repository)
├── .git           # Points to .bare
└── main/          # Worktree for default branch
```

---

### migrate
Convert an existing repository to worktree structure.

```bash
cd existing-repo
git wt migrate
```

**⚠️ Warning:** Experimental command. Restructures your repository.

**Preserves:**
- All branches
- Staged/unstaged changes
- Stashes
- Git configuration

---

### add
Create a new worktree.

**Interactive mode** (requires fzf):
```bash
git wt add
```
Shows remote branches in fzf picker with commit preview.

**Direct mode:**
```bash
# From existing remote branch
git wt add <path> <branch>
git wt add feature origin/feature

# Create new branch
git wt add -b <branch> <path>
git wt add -b my-feature my-feature

# Detached HEAD
git wt add --detach hotfix HEAD~5

# Locked worktree
git wt add --lock -b wip wip-branch
```

**All `git worktree add` flags are supported.**

**Features:**
- Auto-fetches before creating
- Auto-configures upstream tracking

---

### remove
Remove worktree and local branch.

```bash
# Interactive multi-select (with fzf)
git wt remove

# Direct removal
git wt remove <worktree-name>

# Preview what would be removed
git wt remove --dry-run

# Remove multiple
git wt remove feature-a feature-b
```

**What it removes:**
- Worktree directory
- Local branch

**What it keeps:**
- Remote branch
- Git history

---

### destroy
Remove worktree and delete local + remote branches.

```bash
# Interactive with confirmation
git wt destroy

# Direct destruction
git wt destroy <worktree-name>

# Requires typing branch name to confirm
```

**⚠️ Destructive:** Removes local branch AND remote branch.

Shows exactly what will be deleted before confirming.

---

### switch
Interactive worktree selection.

```bash
# Print path to selected worktree
cd $(git wt switch)

# Use with shell function
wt() {
    local dir
    dir=$(git wt switch)
    [[ -n "$dir" ]] && cd "$dir"
}
```

Opens fzf picker showing all worktrees with preview.

---

### update
Fetch all remotes and update default branch.

```bash
git wt update
git wt u           # shorthand
```

**Does:**
1. Fetches all remotes
2. Fast-forwards default branch (main/master) if possible

Run periodically to keep worktrees current.

---

### list
List all worktrees.

```bash
git wt list
```

Passes through to `git worktree list`.

---

## Pass-through Commands

Native `git worktree` commands work directly:

```bash
git wt list              # List worktrees
git wt lock <name>       # Lock worktree
git wt unlock <name>     # Unlock worktree
git wt move <old> <new>  # Move worktree
git wt prune             # Remove stale worktrees
git wt repair            # Repair worktree administrative files
```

## Global Options

```bash
--dry-run       # Preview destructive operations
--quiet         # Suppress output
--verbose       # Verbose output
```

## Tips

### Work with multiple worktrees
```bash
# Create worktrees for parallel development
git wt add -b feature-a feature-a
git wt add -b feature-b feature-b
git wt add -b hotfix hotfix

# List all
git wt list

# Switch between them
cd $(git wt switch)
```

### Clean up after feature completion
```bash
# Remove worktree and local branch only
git wt remove feature-a

# Remove everything including remote branch
git wt destroy feature-b
```

### Batch operations
```bash
# Remove multiple at once
git wt remove feature-a feature-b feature-c

# Interactive multi-select (fzf)
git wt remove
# Then use tab to select multiple
```
