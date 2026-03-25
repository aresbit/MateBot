# Podwise Catch-Up

Use this skill to process a backlog of new podcast episodes in one pass. It combines triage (deciding what's worth your time) with skimming (extracting the best from each episode) so the user can clear their queue efficiently.

## Goals

1. Verify that `podwise` is installed and configured.
2. Load `taste.md` if it exists, to personalize triage priority.
3. Fetch unlistened episodes from followed podcasts for the past 7 days.
4. Triage each episode: assign a priority tier based on the user's interests.
5. For Tier 1 episodes, fetch AI summaries and highlights automatically.
6. For Tier 2 and Tier 3 episodes, show just enough to let the user decide.
7. Present a clean, scannable catch-up digest and ask what the user wants to dive into.

## Step 1: Check the Environment

```bash
podwise --help
podwise config show
```

If `podwise` is not installed or the API key is missing, stop and follow [references/installation.md](references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read it silently. Use the **Core Interest Areas**, **Shows to Prioritize**, and **Shows to Deprioritize** sections to guide triage scoring in Step 4.
- If not found, proceed without personalization and note at the top of the output: *"No taste.md found — run `refine-taste` to get personalized triage."*

## Step 3: Fetch New Episodes

```bash
# Recent episodes from followed podcasts
podwise list episodes --json --latest 7
```

Parse each entry for: podcast name, episode title, publication date, episode URL, isRead status, and any available duration or category metadata.

**Filtering logic:**

1. From `list episodes`, filter to only episodes where `isRead == false`.
2. Sort by publication date (newest first).
3. Display all remaining episodes in the digest (no top-N limit).

If the user specified a different window, adjust `--latest N` accordingly.

## Step 4: Triage the Episodes

Score and sort every episode into three tiers. Do this silently — do not show the scoring process to the user, only the final sorted list.

**Tier 1 — Must Clear**
The episode comes from a show in the user's **Shows to Prioritize** list, or its title/podcast maps directly to one of the user's **Core Interest Areas**. Fetch AI outputs for these automatically in Step 5.

**Tier 2 — Consider Clearing**
The episode is from a show the user follows actively but did not prioritize, or the topic has partial overlap with their interests. Show the title, podcast name, and date; let the user decide.

**Tier 3 — Low Urgency**
The episode comes from a **Shows to Deprioritize** show, or the topic has no clear overlap with the user's interests. List these briefly at the bottom of the digest so the user can acknowledge and dismiss them.

If no `taste.md` is loaded, assign all episodes to Tier 2 and note that personalised triage is unavailable.

## Step 5: Fetch AI Outputs for Tier 1 Episodes

For each Tier 1 episode, run:

```bash
podwise get summary {episode-url}
podwise get highlights {episode-url}
```

If `get` fails because the episode is not yet processed, include it in the digest with its title, podcast name, and a note: "not yet processed — [Open episode]({url})". Ask the user whether they want to process it before fetching the summary.

## Step 6: Present the Catch-Up Digest

Format the output as a clean, scannable digest. Use this structure:

---

### Catch-Up — {date range}

_{N} episodes across {M} shows still in your backlog_

---

#### 🎯 Must Clear ({count})

**{Episode Title}** · {Podcast Name} · {date}
> {2–3 sentence summary derived from `get summary` output}

Key highlights:
- {highlight 1}
- {highlight 2}
- {highlight 3}

[Open episode]({episode-url})

---

#### 👀 Consider Clearing ({count})

- **{Episode Title}** · {Podcast Name} · {date} — {one sentence on why it might be relevant}
- **{Episode Title}** · {Podcast Name} · {date} — {one sentence on why it might be relevant}

---

#### ✓ Low Urgency ({count})

- **{Episode Title}** · {Podcast Name}
- **{Episode Title}** · {Podcast Name}

---

After the digest, ask: *"Would you like to go deeper on any of these, or save any episode's notes to your PKM?"*

## Step 7: Respond to Follow-Up Requests

**Go deeper on a specific episode:**

```bash
podwise get summary {episode-url}
podwise get highlights {episode-url}
```

**For full artifacts:**

```bash
podwise get qa {episode-url}
podwise get chapters {episode-url}
podwise get mindmap {episode-url}
podwise get keywords {episode-url}
```

**Transcript** (token-intensive — request only when you need a specific quote or full record):

```bash
podwise get transcript {episode-url}
```

**Save to PKM:** Guide the user to use `episode-notes` for the specific episode URL.

Always confirm before running `process`.

## Common Failure Cases

- If `podwise list episodes --latest 7` returns empty, tell the user their followed podcasts have no new episodes this week and suggest expanding the window to `--latest 14` if they want to check further back.
- If the combined result after filtering is fewer than 5 episodes, inform the user that their backlog is already clear — their followed podcasts have no unlistened episodes in this window.
- If `get summary` or `get highlights` fails because an episode is not processed, include it in the digest with its title, podcast name, and "not yet processed" — give the user the episode URL and ask if they want to process it before fetching the summary.
- If the user has no followed podcasts, stop and ask them to follow some shows in Podwise before running catch-up.
- If `taste.md` is missing, note at the top of the digest: *"Run `refine-taste` to get personalised triage."*

## Output Contract

Produce one catch-up digest per run with three clearly separated tiers.

Tier 1 entries always include an inline summary and highlights.
Tier 2 entries show title, show name, date, and one relevance note.
Tier 3 entries show title and show name only.

End every digest with the follow-up prompt, which must include both a "go deeper" option and a "save to PKM" option.
