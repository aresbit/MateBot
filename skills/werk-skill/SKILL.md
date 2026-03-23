---
name: werk-skill
description: SPCL (Skill Composition Language) toolkit usage including werk command for skill composition and spcl interpreter for skill merging. Use when working with SPCL skills, composing multiple skills with werk, converting SKILL.md to SKILL.spcl format, or building/installing SPCL from source.
---

# Werk Skill

Werk is the German Red Dot aesthetic command for SPCL skill composition.

## Installation
if werk --help ok do not install repo, then goto Quick Reference.

### From Source

```bash
# Clone repository
git clone https://github.com/aresbit/spcl.git
cd spcl

# Build
make clean && make all

# Install
sudo make uninstall  # Remove old version if exists
sudo make install
```

This installs:
- `spcl` - SPCL interpreter
- `cclq` - CLI query tool
- `werk` - Skill composition command
- `llskill2spcl` - SKILL.md to SKILL.spcl converter

### Verify Installation

```bash
which werk
werk --help
spcl --help
```

## Quick Reference

```bash
# Compose two skills
werk skill1 skill2

# Compose with options
werk --source-dir ~/.claude/skills --work-dir ./skills skill1 skill2

# Mock mode (skip LLM)
werk --mock-llm skill1
```

## Core Concepts

### SPCL Language

SPCL (Skill Composition Language) is a configuration language for skill composition:

- **Hierarchical structure**: Indentation-based tree format
- **Key-value pairs**: `key = value`
- **Lists**: Multiple `= value` lines under a key
- **Nesting**: Deeper indentation = nested structure

Example:
```spcl
meta =
  name = my-skill
  version = 1

skill =
  name = my-skill
  description = A useful skill
  entry = SKILL.spcl
  refs =
    = reference/*.md
```

### Werk Command

Werk performs skill composition through these steps:

1. **Normalize**: Convert each `SKILL.md` → `SKILL.spcl` via LLM
2. **Manifest**: Generate compose manifest
3. **Compose**: Call `spcl compose` to merge skills
4. **Assemble**: Collect references and output final skill

Output structure:
```
trick/<skill1>-and-then-<skill2>/
├── SKILL.md              # Combined skill documentation
├── SKILL.spcl            # Combined skill configuration
├── source-skills/        # Normalized individual skills
│   ├── skill1/SKILL.spcl
│   └── skill2/SKILL.spcl
└── reference/            # Merged reference files
```

## Environment Variables

### For llskill2spcl (used by werk)

```bash
LLM_API_KEY            # API key for LLM service
LLM_API_URL            # API endpoint (default: https://api.deepseek.com/chat/completions)
LLM_MODEL              # Model name (default: deepseek-chat)
LLM_MAX_TOKENS         # Max output tokens (default: 8192)
LLM_TEMPERATURE        # Sampling temperature (default: 0)
```

### For werk

```bash
SPCL_INTERPRETER       # Path to spcl interpreter
SPCL_LLSKILL2SPCL      # Path to llskill2spcl script
```

## Command Reference

### werk [OPTIONS] SKILL [SKILL ...]

Compose multiple skills into a combined skill.

Options:
- `--source-dir DIR` - Fallback source directory (default: ~/.claude/skills)
- `--work-dir DIR` - Local work directory (default: ./skills)
- `--out-dir DIR` - Output directory (default: ./trick)
- `--interpreter PATH` - Spcl interpreter path
- `--refresh-copy` - Re-copy skills from source before run
- `--mock-llm` - Generate deterministic mock output (no API call)

### spcl compose MANIFEST --skills DIR --out DIR

Low-level composition command invoked by werk.

Example:
```bash
spcl compose manifest.spcl --skills ./skills --out ./output
```

## Advanced Usage

### Adding Custom References

References from source skills are automatically merged:
- `reference/` or `references/` directories
- `script/` or `scripts/` directories (preserved at top level)
- Other files (placed in `reference/`)

### Creating Composable Skills

To make a skill composable:

1. Include proper frontmatter in `SKILL.md`:
   ```yaml
   ---
   name: my-skill
   description: What this skill does
   ---
   ```

2. Add SPCL metadata in `SKILL.md`:
   ```markdown
   <!-- SPCL:BEGIN -->
   skill =
     name = my-skill
     description = Detailed description
     entry = SKILL.md
     refs =
       = reference/*.md
   <!-- SPCL:END -->
   ```

3. Place reference files in `reference/` directory

## Scripts

See `scripts/` directory for helper utilities:

- `install_spcl.sh` - Full installation from source
