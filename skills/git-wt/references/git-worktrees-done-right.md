
# Git Worktrees Done Right
The Context Switch Tax
Let’s be honest about why this matters.

Every time you stash and switch, you pay a tax:

Stash conflicts (your old changes fighting your new changes)
Forgotten stashes (check git stash list - how many ghosts live there?)
Mental context destruction (studies suggest 15-20 minutes to regain flow)
The naive fix? Clone the repo multiple times.

~/dev/
├── my-repo/           # main development
├── my-repo-hotfix/    # for fires
└── my-repo-review/    # for PR reviews
It works. But now you have three copies of the entire git history. Fetch in one? The others are stale. Five clones of a 2GB repo = 10GB of disk space for the same codebase.

There’s a better way.

Git Worktrees: Multiple Checkouts, One Repository
Worktrees have been in Git since 2015 (version 2.5). They let you check out multiple branches simultaneously in different directories - while sharing all the underlying git data.

One .git folder. Multiple working directories. Fetch once, updates everywhere.

Multiple Clones	Git Worktrees
Separate .git/ per clone	Single shared .git/
Fetch updates one clone only	Fetch updates all worktrees
Full disk cost per clone	Only working files are duplicated
No coordination	git worktree list shows all
Think of it as “multiple checkouts, single repository.”

The Catch (And Why Most People Give Up)
Here’s what happens when you try worktrees the “normal” way:

cd ~/dev/my-repo
git worktree add ../my-repo-feature feature-branch
Notice that ../? That’s where things get messy.

Your dev folder becomes chaos
~/dev/
├── my-repo/              # main (has .git/)
├── my-repo-feature/      # worktree
├── my-repo-hotfix/       # worktree
├── my-repo-experiment/   # worktree
├── other-project/        # actual clone
├── other-project-fix/    # worktree? clone? who knows
└── ...20 more directories
After a few months, you can’t tell worktrees from clones at a glance. You forget what’s linked to what.

Remote tracking is manual and forgettable
When you create a worktree from a remote branch, git creates a local branch but doesn’t automatically set up tracking. You have to remember to do it yourself every single time:

git worktree add ../feature origin/feature
cd ../feature
git push # "fatal: no upstream configured"
# Sigh...
git branch --set-upstream-to=origin/feature
Miss this step and your first push fails. Do it enough times and you start resenting the whole workflow.

Branches pile up like dirty dishes
git worktree remove ../feature
git branch
# * main
#   feature    <-- orphaned, still here
#   old-thing  <-- from last month
#   experiment <-- ???
You remove the worktree. The branch stays. Multiply by six months of work. git branch scrolls for pages.

The Bare Repo Pattern: Everything Changes
Here’s the trick that makes worktrees actually pleasant to use.

Instead of cloning normally and creating worktrees outside, you create a bare clone and put worktrees inside it.

my-project/
├── .bare/            # all git data lives here
├── .git              # just a pointer file
├── main/             # worktree: main branch
└── feature/          # worktree: feature branch
Everything for my-project lives in one folder. ls and you see your branches. Delete the folder? Everything’s gone - no orphans.

What’s a bare repo?
When you clone normally, you get a .git/ folder plus working files. A bare clone is just the .git/ contents - the database of commits and branches without any checked-out files.

Servers use bare repos. You can’t “work” in one - there’s nothing to edit. But you can create worktrees from it.

Setting it up manually
mkdir my-project && cd my-project
git clone --bare https://github.com/user/repo.git .bare

# This is the magic - a .git FILE that points to .bare
echo "gitdir: ./.bare" >.git

# Bare clones need this to fetch all branches
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"

# Make the setup portable (can move the folder)
git config worktree.useRelativePaths true

git fetch --all

# Now worktrees go INSIDE the project folder
git worktree add main main
git worktree add feature origin/feature
The .git file (not folder) is the clever bit. It tells git “the real repo data is over there in .bare”. Now you can create worktrees as subdirectories.

That’s 10+ commands to remember. Worth scripting if you do it often.

Why This Matters Now: AI Agents
Here’s where worktrees become essential rather than just nice-to-have.

AI coding agents - Claude Code, Cursor, Copilot - work best with isolation. They can touch dozens of files in one session. You don’t want that happening in your active work branch.

Worktrees give you:

Parallel execution: Three agents, three worktrees, no conflicts
Clean slate: Agent starts from pristine main, not your WIP
Safe experimentation: Your work is untouched
Easy review: git diff main...agent-branch
Quick rollback: Just delete the worktree
Both Anthropic and Cursor officially recommend this pattern.

The agent workflow
# You're working on feature-A
cd ~/dev/project/feature-A

# Spin up a worktree for the agent
git worktree add -b agent-refactor ../agent-refactor

# Point the agent at it
cd ~/dev/project/agent-refactor

# Agent goes wild. You keep working in feature-A.

# Later: review what it did
git diff main...agent-refactor

# Keep the good parts, toss the rest
Multi-agent parallelism
~/dev/project/
├── .bare/
├── main/                    # pristine reference
├── feature-auth/            # your work
├── agent-refactor-utils/    # Agent 1
├── agent-add-tests/         # Agent 2
└── agent-fix-types/         # Agent 3
Three agents running simultaneously. Each isolated. Review at your leisure.

The Hidden Superpower: Project-Level Customization
The bare repo pattern unlocks something else: a place for YOUR stuff that doesn’t touch the repo.

Agent configs outside version control
~/dev/project/
├── .claude/      # your experimental prompts, local context
├── .cursor/      # your cursor rules
├── .bare/
├── main/
└── feature/
The .claude/ folder sits at the project root, outside any worktree. Shared across all your branches. Not in git history. Fully yours.

Local dev environment
~/dev/project/
├── flake.nix     # your nix setup
├── mise.toml     # your runtime versions
├── .env          # your secrets
├── .bare/
├── main/
└── feature/
I don’t install runtimes globally. Each project is self-contained via flake.nix and direnv. But not everyone on the team uses these tools - so I keep them at the workspace root, outside the repo.

One-off scripts
~/dev/project/
├── _/            # scratchpad: scripts, prompts, notes
├── .bare/
├── main/
└── feature/
A dedicated junk drawer that doesn’t pollute the repo. Remember - it’s just folders.

Patterns That Work
Keep main/ pristine. Never work directly in it. It’s your clean reference for diffing and branching.

Name worktrees after branches. Directory = branch = no confusion.

One tmux window per worktree. Name windows after branches. Context is visual.

Use .bare/info/exclude for local ignores (if needed). With this structure: echo myfile >> ../.bare/info/exclude.

Keep 2-3 worktrees active. Each is a full checkout (shared git objects, but real files). Don’t go overboard.

Rough Edges
Worktrees aren’t new, but tooling support varies. Some IDEs handle them well. Some scripts assume single-clone structure. You might need workarounds.

That’s the tradeoff: you’re ahead of mainstream adoption. If more people use worktrees, tooling improves faster.

Try It
Pick one repo. Set up the bare pattern. Work like this for a week.

The mental overhead of “I need to save my context before switching” just vanishes. You stop paying the context switch tax. Your branches become directories you can see.

And when an AI agent needs to refactor half your codebase? You’ll be glad everything is isolated.