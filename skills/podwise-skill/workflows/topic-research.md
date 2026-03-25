# Podwise Topic Research

Use this skill to answer the question: *what do podcasts actually say about X?* It searches across Podwise's transcript corpus, synthesizes insights from multiple episodes and speakers, and produces a report that reads like research — not a playlist.

## Goals

1. Verify that `podwise` is installed and configured.
2. Clarify the research topic and scope with the user.
3. Use `ask` to retrieve transcript-grounded insights with cited episode URLs.
4. Fetch summaries and highlights from the cited episodes.
5. Synthesize a structured research report with multiple perspectives, key claims, and source links.
6. Write the report to a file and offer to export it.

## Step 1: Check the Environment

```bash
podwise --help
podwise config show
```

If `podwise` is not installed or the API key is missing, stop and follow [references/installation.md](references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read the **Core Interest Areas**, **PKM tool**, and **Output Preferences** fields silently. Use these to frame the report's angle and format.
- If not found, proceed with default formatting and note at the top of the report: *"No taste.md found — run `refine-taste` to personalise research output."*

## Step 3: Clarify the Research Topic

If the user has not already stated a clear topic, ask:

1. **Topic**: What specific topic, question, or theme do you want to research? The more specific, the better — e.g. "How do AI researchers think about consciousness?" beats "AI".
2. **Angle**: Are you looking for a broad overview, a specific angle, or contrarian takes?

If the user already provided both, skip the questions and proceed.

## Step 4: Run Ask

```bash
# Transcript-grounded synthesis — --sources appends cited episode URLs and excerpts
podwise ask "{topic}" --sources
```

`ask` searches transcript content and generates a synthesized answer — it may take up to 60 seconds. Do not cancel it early.

Parse the `ask` output to extract all cited episode URLs. These are the primary source episodes for Step 5.

## Step 5: Fetch Deep Artifacts from Cited Episodes

From the `ask --sources` output, identify all cited episode URLs. For each cited episode, run:

```bash
podwise get summary {episode-url}
podwise get highlights {episode-url}
podwise get keywords {episode-url}
```

**Handling cited episode count:**

- **3 or more cited episodes**: Proceed normally — fetch artifacts for all.
- **Fewer than 3 cited episodes**: Proceed with whatever episodes were cited. Add a note at the top of the report: *"Limited sources — this topic may be underrepresented in Podwise's corpus. Consider broadening your topic or angle."*
- **0 cited episodes**: This means `ask` succeeded but returned no source citations. Proceed using only the `ask` text output to write the report. Add a note at the top: *"No cited episodes available — this report is based on AI synthesis only, not traceable to specific episodes."*

If any `get` fails because an episode is not yet processed, skip that episode and note it in the report. Do not prompt for processing — do not let quota confirmation interrupt the research flow.

If the user explicitly asks to include an unprocessed episode, ask for confirmation once and then run:

```bash
podwise process {episode-url}
```

## Step 6: Synthesize the Research Report

With the `ask` output, episode summaries, highlights, and keywords in hand, write a structured research report in four parts.

### Part 1 — Overview

2–3 paragraphs summarising the state of the topic as represented across Podwise's podcast corpus. Draw primarily from the `ask` output. Be specific — name claims, name the kinds of speakers making them, and note any strong consensus.

### Part 2 — Key Perspectives

Identify 3–5 distinct perspectives, arguments, or schools of thought that appear across the source episodes. For each:

- Give the perspective a short label (e.g. "The optimist case", "The regulatory concern", "The practitioner view")
- Summarise it in 3–5 sentences
- Cite the episode(s) that best represent it with a link

This is the most important section. The goal is not to list what each episode said, but to map the *intellectual landscape* of the topic.

### Part 3 — Points of Tension

Where do speakers disagree? Identify 2–3 genuine tensions, contradictions, or unresolved debates found across the source material. Write 2–3 sentences on each tension and name the opposing positions. If all sources express substantially the same view, skip this section and note: *"The source material shows strong consensus on this topic — no significant tensions were found."*

### Part 4 — Source Episodes

A reference list of all episodes cited in the `ask` output and successfully fetched in Step 5:

- **{Episode Title}** · {Podcast Name} · {date} · [Open]({episode-url})
  > {one sentence on what this episode contributes to the topic}

---

## Step 7: Write the Report File

Name the file using the pattern: `topic-research-{topic-slug}-{YYYY-MM-DD}.md`

Example: `topic-research-ai-agents-2026-03-21.md`

Write the file to the current working directory unless the user specifies another path.

Use this document template:

```markdown
# Topic Research: {Topic}

**Research question**: {the user's original framing}
**Sources**: {N} episodes across {M} podcasts
**Generated**: {date}
{If limited sources or no citations: add the applicable note from Step 5}
{If no taste profile: "Note: run `refine-taste` for personalised output."}

---

## Overview

{Part 1 content}

---

## Key Perspectives

### {Perspective label}
{3–5 sentences. Source: [{Episode Title}]({url})}

### {Perspective label}
{3–5 sentences. Source: [{Episode Title}]({url})}

---

## Points of Tension

**{Tension label}**
{2–3 sentences describing the opposing positions.}

---

## Source Episodes

- **{Episode Title}** · {Podcast Name} · {date} · [Open]({url})
  > {one-sentence contribution note}

---

_Generated by podwise-topic-research · {date}_
```

After writing the file, confirm the path and ask:
*"Would you like me to go deeper on a specific perspective, fetch the full Q&A from an episode, or export this report to your PKM?"*

## Common Failure Cases

- If `podwise ask` times out or returns an error, report the error directly. Do not fabricate a synthesis — tell the user the research could not be completed and suggest retrying with a more specific topic.
- If the user's topic is very broad (e.g. "technology", "health"), ask them to narrow it before running — `ask` performs better on specific questions than general categories.
- If `get` fails for a cited episode because it is not yet processed, skip it and note it in the report. The `ask` synthesis remains the primary source.
- If all cited episodes fail to fetch artifacts, produce a lightweight report from the `ask` text output only and label it clearly as a "synthesis-only report".

## Output Contract

Produce exactly one report file per run.

The report must include at minimum: Overview, Key Perspectives, and Source Episodes.

Points of Tension may be omitted only when source material shows genuine consensus.

The `ask` output is the primary synthesis source. Episode summaries, highlights, and keywords are supplementary depth — use them to sharpen and cite the perspectives, not to replace the synthesis.

Always write the file and confirm the path. Always end with the follow-up prompt.
