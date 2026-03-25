# Podwise Weekly Recap

Use this skill to turn a week of scattered podcast listening into one coherent digest — what you heard, what you saved, and what was worth remembering. The output is ready to read as-is, forward to yourself by email, or drop into a PKM tool.

## Goals

1. Verify that `podwise` is installed and configured.
2. Load `taste.md` to determine the user's PKM tool and output format preference.
3. Fetch this week's episodes and highlights from the CLI.
4. Synthesize the material into a structured weekly recap.
5. Deliver the recap in the user's preferred format and offer to export it.

## Step 1: Check the Environment

```bash
podwise --help
podwise config show
```

If `podwise` is not installed or the API key is missing, stop and follow [references/installation.md](references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read it silently. Use the **PKM tool**, **Output Preferences**, and **Core Interest Areas** sections to shape the recap's format, length, and framing.
- If not found, proceed with default formatting (prose summary, medium length) and note at the top of the output: *"No taste.md found — run `refine-taste` to personalise recap format and export destination."*

## Step 3: Determine the Recap Window

If the user did not specify a time range, default to the past 7 days.

Confirm with the user if the window is ambiguous — for example if today is mid-week (Tuesday–Thursday), ask whether they want this week so far (Mon–today) or the last 7 days.

## Step 4: Fetch This Week's Listening

Fetch from two sources simultaneously:

```bash
# Actual listening behaviour this week
podwise history listened --json --limit 100

# Episodes the user read (viewed summaries/highlights but may not have listened fully)
podwise history read --json --limit 100
```

Parse each entry for: podcast name, episode title, publication date, and episode URL.

Then apply a secondary filter: keep only episodes whose publication date falls within the recap window (last 7 days). This ensures every entry in the recap represents something the user actually encountered this week, not just something new that was published.

**Fallback**: If the combined result after filtering is fewer than 5 episodes, supplement with:

```bash
podwise list episodes --json --date {window_start} --date {window_end}
```

Mark any supplement episodes as "not yet listened — published this week". If the total remains below 5 even after supplement, degrade to `podwise list episodes --latest 7` and note at the top of the recap: *"Based on your subscriptions this week — your listening history was thin for this window."*

## Step 5: Fetch AI Outputs for Each Episode

For each episode that made it through the Step 4 filter, fetch:

```bash
podwise get summary {episode-url}
podwise get highlights {episode-url}
```

Fetch `get keywords` optionally — only when the recap covers 5 or more episodes and the themes section may benefit from keyword context. Do not make it a required call.

If `get` fails for an episode because it has not been processed yet, include it in the recap with its podcast name, episode title, and a note: "not yet processed — [Open episode]({url})". This gives the user enough context to decide whether to process it manually.

**Silently record** every episode in the Step 4 history results that did not make it into the Part 1 recap (i.e., episodes beyond the top entries or from older weeks). These go into a "Also in your history this week" section at the bottom of the recap — title, podcast name, and date only, no `get` calls.

Do not run `podwise process` automatically during a recap.

## Step 6: Synthesize the Recap

Before writing, apply format preferences from the taste profile if loaded:

- If **Preferred format = bullet points**: write Part 1 summaries as bullet lists instead of prose
- If **Preferred summary length = short**: write 1–2 sentences per episode
- If **Preferred summary length = detailed**: retain 3–4 sentences per episode
- If **Preferred format = prose / mix**: keep the default prose format

Then synthesize in three parts:

### Part 1 — Episode by Episode

For each episode, produce a compact entry:

**▶ {Episode Title}** · {Podcast Name} · {date} *(listened)*  
or  
**👀 {Episode Title}** · {Podcast Name} · {date} *(read — viewed summary/highlights)*

{2–3 sentence summary}

Highlights:
- {highlight}
- {highlight}

[Open episode]({episode-url})

Order entries from most relevant to the user's **Core Interest Areas** down to least relevant, using the taste profile if loaded. Distinguish listened episodes (▶) from read-only episodes (👀) throughout.

### Part 2 — Themes of the Week

Look across all episodes and extract 2–4 recurring themes or ideas that appeared in multiple shows this week. Write 2–3 sentences on each theme, citing the 2–3 most relevant episodes per theme. This section transforms isolated episode content into a higher-level view of what the user's listening world was about this week.

If all episodes cover completely different topics with no overlap, skip this section and note: *"No recurring themes this week — your listening was varied."*

### Part 3 — Worth Revisiting

Pick highlights or ideas that stand out, in this priority order:
1. **Actionable** — anything with a clear next step or advice worth acting on
2. **Surprising** — ideas that challenge or reshape how you think
3. **Useful** — genuinely valuable knowledge that's worth remembering

Quantity rule (based on total episodes in Part 1):
- Fewer than 5 episodes → pick 1
- 5–10 episodes → pick 2
- More than 10 episodes → pick 3

Write one sentence per pick and link back to the source episode. This is the section the user is most likely to forward to a friend or paste into their notes.

## Step 7: Format and Deliver the Recap

Format the final output using this template:

---

## Weekly Podcast Recap — {week date range}

_{N} episodes · {M} shows · {week range}_

---

### This Week's Episodes

**▶ {Episode Title}** · {Podcast Name} · {date} *(listened)*
{2–3 sentence summary}

Highlights:
- {highlight}
- {highlight}

[Open episode]({episode-url})

---

{repeat for each episode (listened and read)}
{if any read-only episodes are included, tag them *(read)* instead of *(listened)*}

---

### Themes of the Week

**{Theme 1}**
{2–3 sentences. Mentioned in: {Episode A}, {Episode B}.}

**{Theme 2}**
{2–3 sentences. Mentioned in: {Episode C}.}

---

### Worth Revisiting

- **"{highlight or idea}"** — {Episode Title} · {one sentence on why it stands out}
- **"{highlight or idea}"** — {Episode Title} · {one sentence on why it stands out}

---

### Also in Your History This Week

*{N} additional episodes from your history that were outside the 7-day window or didn't make the recap cut:*

- **{Episode Title}** · {Podcast Name} · {date}
- **{Episode Title}** · {Podcast Name} · {date}

---

_Generated by podwise-weekly-recap · {date}_

---

After presenting the recap, ask the user:
*"Would you like to export this to {PKM tool from taste profile, or 'your PKM tool'}, share it, or save it as a plain text file?"*

## Step 8: Export the Recap

If the user confirms export, write the recap to a file named `weekly-recap-{YYYY-MM-DD}.md` in the current working directory.

If the user's taste profile specifies a PKM tool, remind them they can paste the file directly into:
- **Notion**: as a new page in their notes database
- **Obsidian**: as a new note in their vault
- **Logseq**: as a new journal page
- **Readwise**: via the Readwise import or daily highlights feature

Podwise does not push directly to PKM tools from the CLI at this step — the file is the handoff. Tell the user this clearly if they ask why it does not auto-sync.

## Common Failure Cases

- If all episodes in the window are unprocessed, there is nothing to synthesize. Offer to run `podwise-catch-up` first to process the week's episodes before generating the recap.
- If only one or two episodes are available, produce the recap as normal but skip the Themes section if there is insufficient material for cross-episode synthesis.
- If `taste.md` is missing, default formatting is fine — just note it at the top.
- If the user asks for a monthly recap instead, adjust the window to 30 days and update the output header accordingly.

## Output Contract

Produce exactly one recap document per run with three main sections: episodes, themes, and worth revisiting.

A fourth section ("Also in your history this week") is added whenever there are recorded history entries that did not make the episode list.

The themes section may be omitted only when there is genuinely no cross-episode material.

Always end with the export prompt. Always write the file if the user confirms export.
