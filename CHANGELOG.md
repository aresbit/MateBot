# Changelog

All notable changes to the MateBot project.

## [Unreleased]

## [1.1.0] - 2025-02-01

### Changed
- **Fully automatic memory mode** - Every message now automatically includes auto-memory instructions
- Auto-memory instruction injected into every prompt via `_get_or_init_auto_memory_instruction()`
- **CCL-style memory format** - Migrated from XML tags to elegant key-value format
  - Format: `-- memory\nkey = value\n--` (inspired by [CCL](https://chshersh.com/blog/2025-01-06-the-most-elegant-configuration-language.html))
  - Replaced `<memory_update>` tags with `-- memory` blocks
  - Cleaner syntax, better readability, no XML escaping issues
  - Supports multi-line values via indentation
- `ResponseMonitor` extracts and saves memory updates to SQLite
- Updated documentation (README.md, GUIDE.md, SKILL.md files)

### Removed
- `/loop <prompt>` command - no longer needed
- `/meta_loop <prompt>` command - replaced by automatic memory
- `/metamem` command - functionality merged into `/recall`
- `ralph-loop` dependency - was never implemented

### Fixed
- **`_save_to_memory()` method** - Fixed bug where memory update saving depended on `recent_messages` entry
  - Now saves `memory_update` independently, even if conversation not from Telegram
- **`find_latest_transcript()`** - Fixed transcript file path detection
  - Now searches both `~/.claude/transcripts/` and `~/.claude/projects/*/` directories
  - Correctly finds Claude Code transcript files in project subdirectories
- **`clear_all()` and `delete()` methods** - Fixed FTS5 index deletion order bug
  - FTS5 records must be deleted BEFORE main table records (due to `content_rowid` constraint)
  - Previously deletion order was incorrect, causing FTS5 index to become out of sync

### Added
- **Self-referential meta-instruction storage** - Auto-memory instruction now stored in SQLite DB
- `_get_or_init_auto_memory_instruction()` method loads instruction from DB at startup
- Default instruction auto-initialized to DB on first run
- Instruction can be updated via `/remember` or auto-memory for iterative optimization
- Automatic memory extraction on every Telegram message

## [1.0.0] - 2025-01-31

### Core Features

#### Telegram Bot Bridge
- **Polling-based message handling** - Real-time message reception via Telegram Bot API
- **Command system** - 10 built-in commands for session management
- **Response monitoring** - Automatic detection and forwarding of Claude responses
- **Typing indicators** - Real-time feedback during processing

#### Session Management
| Command | Description |
|---------|-------------|
| `/clear` | Clear current conversation |
| `/continue_` | Continue most recent session |
| `/resume` | Interactive session picker with inline keyboard |
| `/stop` | Interrupt Claude (sends Escape) |
| `/status` | Check tmux and bridge status |

#### Local Memory System
- **Fully automatic** - Every message auto-extracts key info to memory (no command needed)
- **SQLite-based storage** - Local database at `~/.matecode/memory.db`
- **FTS5 full-text search** - Fast relevance-ranked memory retrieval
- **Auto-save conversations** - Every Q&A pair saved automatically
- **Memory injection** - Relevant memories auto-injected into context
- **Manual management** - `/remember`, `/recall`, `/forget` commands
- **Meta-update tracking** - Self-referential memories auto-saved via `-- memory` blocks
- **Self-referential instruction** - Meta-instruction stored in DB, iteratively improvable

#### tmux Integration
- **Session management** - Automatic tmux session creation and attachment
- **Claude Code wrapper** - Full tmux control via Telegram
- **Multi-window support** - Switch between Claude and shell
- **Automatic attachment** - `matecode.sh` auto-attaches after start/restart

### Skills System
25+ integrated skills for extended functionality:

| Category | Skills |
|----------|--------|
| **Development** | `coding-agent`, `skill-creator`, `vercel-react-best-practices`, `remotion-best-practices` |
| **AI/ML** | `openai-image-gen`, `openai-whisper`, `gemini`, `model-usage` |
| **Productivity** | `notion`, `obsidian`, `slack`, `discord`, `github` |
| **Media** | `video-frames`, `gifgrep`, `nano-pdf`, `summarize` |
| **Web** | `agent-browser`, `canvas`, `web-design-guidelines` |
| **Utilities** | `tmux`, `session-logs`, `blogwatcher`, `clawdhub` |
| **MateCode** | Self-management skill |

### Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Telegram Bot   │◄───►│  bridge.py   │◄───►│  Claude Code    │
│  (User Interface)│     │  (Bridge)    │     │  (tmux session) │
└─────────────────┘     └──────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  memory.py   │
                        │  (SQLite)    │
                        └──────────────┘
```

### File Structure
```
MateBot/
├── bridge.py              # Main bridge implementation
├── memory.py              # Local memory system
├── matecode.sh            # Management script (start/stop/status/attach)
├── bridge_manager.sh      # Process management
├── README.md              # English documentation
├── GUIDE.md               # Chinese guide
├── TMUX_SETUP.md          # tmux configuration guide
├── .tmux.conf.local       # Custom tmux config
├── hooks/
│   └── send-to-telegram.sh  # Response hook script
├── matecode/
│   └── SKILL.md           # Skill metadata
└── skills/                # 25+ integrated skills
```

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | - | Bot token (required) |
| `TMUX_SESSION` | `claude` | tmux session name |
| `MEMORY_ENABLED` | `true` | Enable memory system |
| `MEMORY_MAX_RESULTS` | `5` | Max memories per query |
| `MEMORY_MAX_CONTEXT` | `2000` | Context injection limit |

### Technical Highlights
- **Pure Python 3** - No external dependencies beyond standard library
- **Thread-safe** - Concurrent response monitoring and message handling
- **JSONL transcript parsing** - Efficient Claude output extraction
- **Hook-based integration** - Non-intrusive Claude Code extension
- **Polling architecture** - Reliable message delivery without webhooks
- **Automatic memory** - Every prompt includes auto-memory instruction, responses parsed for `-- memory` blocks

### Auto-Memory Flow
```
Startup → _get_or_init_auto_memory_instruction()
                    ↓
         [Load from DB or Initialize Default]
                    ↓
User Message → Bridge → _build_full_prompt()
                    ↓
         [DB-stored instruction prepended]
                    ↓
              Claude Response
                    ↓
         [Contains -- memory block]
                    ↓
         ResponseMonitor._save_to_memory()
                    ↓
              SQLite memory.db
                    ↓
    [Instruction itself can be updated via memory]
```

---

## Future Roadmap

- [ ] Webhook mode for lower latency
- [ ] Multi-user support with access control
- [ ] Conversation threading
- [ ] File upload/download support
- [ ] Voice message support
- [ ] Custom skill marketplace integration

