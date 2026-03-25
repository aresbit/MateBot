---
name: podwise
description: "Podcast knowledge workflows powered by Podwise CLI: search podcasts and episodes by keyword, monitor followed shows for new releases, find popular episodes, ask questions and extract insights from transcript content, process Podwise episode URLs, YouTube videos, Xiaoyuzhou links, and local audio or video files to retrieve transcripts, summaries, chapters, Q&A, mind maps, highlights, and keywords — plus catch up on your backlog, refine your listening taste, generate weekly recaps, export episode notes to PKM tools, research topics across podcasts, debate episode ideas, and generate language learning cards. Use when the user wants to find, summarize, transcribe, or extract insights from any podcast or audio content, or manage their listening library."
version: 0.1.0
homepage: https://podwise.ai
metadata:
  clawdbot:
    emoji: "🎧"
---

# Podwise

Podwise skills help you get more out of every podcast you listen to.

## References

Load these files when needed — do not load all of them upfront:

- [references/cli.md](references/cli.md) — full CLI command reference. Load before running any `podwise` command or looking up flags and syntax.
- [references/installation.md](references/installation.md) — installation and API key setup. Load if `podwise` is not installed or not configured.
- [references/taste.md](references/taste.md) — the user's listener profile. Load at the start of any workflow that benefits from personalisation.

## Environment Check

Before running any workflow, verify the CLI is available:

```bash
podwise --help
podwise config show
```

If `podwise` is not installed or the API key is missing, load [references/installation.md](references/installation.md) and stop until setup is complete.

## CLI Reference

Before running any `podwise` command, load [references/cli.md](references/cli.md) as the source of truth for exact flags, subcommands, and examples. Do not guess command syntax from memory.

## First-Time Setup

If [references/taste.md](references/taste.md) does not exist, suggest running the `refine-taste` workflow before any other workflow. Other workflows will still run without it, but their outputs will not be personalised.

## Workflow Routing

---

**`workflows/refine-taste.md`**
- "Set up my Podwise profile"
- "Tell me about my listening habits"
- "I want to personalise my recommendations"
- "Refine my taste profile"
- Running any other workflow for the first time and `references/taste.md` does not exist

---

**`workflows/catch-up.md`**
- "I haven't listened in a while, catch me up"
- "What did I miss this week?" / "What's new from my podcasts?"
- "Help me clear my backlog" / "Too many unheard episodes"
- "Show me what's new from the shows I follow"
- "Triage my podcast queue"

---

**`workflows/weekly-recap.md`**
- "Give me a recap of this week's listening"
- "What did I listen to this week?" / "Summarise my week in podcasts"
- "Send me a weekly digest" / "What were the highlights from this week?"
- "I want a summary of what I've been listening to lately"

---

**`workflows/episode-notes.md`**
- "Save notes for this episode" / "Export this episode to Notion / Obsidian / Logseq"
- "Turn this episode into a note" / "I want to keep notes on this episode"
- "Export the summary and highlights from this episode to my PKM"
- "Create a note from this podcast" — followed by a URL or episode title

---

**`workflows/topic-research.md`**
- "What do podcasts say about [topic]?"
- "Research [topic] across my podcasts" / "Synthesise what I've heard about [topic]"
- "Find everything related to [topic] across episodes"
- "I want a deep dive into [topic] from podcast content"
- "Compile insights on [topic] from multiple episodes"

---

**`workflows/episode-debate.md`**
- "Challenge the ideas in this episode" / "Debate this episode with me"
- "I want to stress-test what [speaker] said"
- "Push back on the claims in this episode"
- "Play devil's advocate on this podcast"
- "Help me think critically about this episode"

---

**`workflows/language-learning.md`**
- "Make flashcards from this episode" / "Generate Anki cards from this transcript"
- "I want to learn vocabulary from this podcast"
- "Extract phrases for language learning from this episode"
- "Help me study English / Japanese / [language] using this podcast"
- "Turn this transcript into study cards"

---

**`workflows/discover.md`**
- "Recommend new podcasts for me" / "Find me something new to listen to"
- "What shows should I subscribe to?" / "Discover podcasts based on my taste"
- "I want to find podcasts similar to [show]"
- "What else would I like based on what I already follow?"
- "Suggest new episodes outside my subscriptions"

---

Once you identify the right workflow, load that file and follow its instructions exactly.

If the user's intent matches more than one workflow, ask one clarifying question before routing. If it matches none, ask what they are trying to accomplish. Do not guess.

Some requests can be handled directly with the CLI without loading a workflow. Load [references/cli.md](references/cli.md) and execute directly when the user's intent is a single, self-contained CLI operation:

- Follow or unfollow a podcast — `podwise follow / unfollow`
- Search for an episode or podcast by name — `podwise search`
- Check what's trending — `podwise popular`
- Browse listening or reading history — `podwise history`
- Fetch a specific artifact from an episode — `podwise get`
- Ask a one-off question from transcripts — `podwise ask`
