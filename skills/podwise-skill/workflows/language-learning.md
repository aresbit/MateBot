# Podwise Language Learning

Use this skill to mine a podcast transcript for language learning material. It pulls real phrases from real conversations — not textbook examples — and turns them into flashcards the user can study immediately or import into Anki.

## Goals

1. Verify that `podwise` is installed and configured.
2. Identify the target episode and fetch its transcript.
3. Ask the user to specify their learning language and level.
4. Extract relevant vocabulary and phrases from the transcript.
5. Format them as flashcards with context sentences, translations, and usage notes.
6. Deliver as an inline review, an Anki-importable file, or a CSV.

## Step 1: Check the Environment

```bash
podwise --help
podwise config show
```

If `podwise` is not installed or the API key is missing, stop and follow [references/installation.md](references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read the **Languages** field silently. Use the learning language and native language to pre-fill Step 4 questions and skip any that are already known.
- If found, also read **Output Preferences** to shape the default delivery format recommendation in Step 8.
- If not found, ask all setup questions in full.

## Step 3: Identify the Target Episode

The user may provide the episode as:

- A Podwise episode URL: `https://podwise.ai/dashboard/episodes/{id}`
- A YouTube or Xiaoyuzhou URL
- A local audio or video file path
- An episode title or keyword — search first:

```bash
podwise search episode "{title or keyword}" --limit 5 --json
```

Present the results and ask the user to confirm which episode before continuing.

If the user provided a YouTube URL, Xiaoyuzhou URL, or local file path, run `podwise process <url>` before Step 5 to obtain a valid Podwise episode URL. Ask for confirmation before processing:

> "This episode hasn't been processed yet. Processing will use one credit from your Podwise quota. Proceed?"

Only run `process` after explicit confirmation. Once processed, re-run the search to obtain the resolved Podwise episode URL, then proceed to Step 4.

## Step 4: Set Up the Learning Context

If any information is not already in the taste profile, ask the following questions — all at once, not one by one:

1. **Learning language**: Which language are you studying in this episode? (e.g. English, Japanese, Mandarin) — skip if already known from taste.md
2. **Native language**: What is your native language? (Cards will be translated into this language.) — skip if already known from taste.md
3. **Level**: How would you rate your level in the learning language? (Beginner / Intermediate / Advanced)
4. **Focus**: What type of material do you want to prioritise?
   - Everyday vocabulary (common words used in natural conversation)
   - Topic-specific terminology (domain words relevant to this episode's subject)
   - Idiomatic expressions and collocations (phrases that are hard to guess from individual words)
   - All of the above
5. **Card count**: How many cards do you want? (Suggested: 10–20 for a focused session, up to 40 for a deep mine)

Use the answers to calibrate extraction in Step 6.

## Step 5: Fetch the Transcript

```bash
podwise get transcript {episode-url}
```

If the episode is not yet processed, ask the user for confirmation before processing:

> "This episode hasn't been processed yet. Processing will use one credit from your Podwise quota. Proceed?"

Only run `process` after explicit confirmation:

```bash
podwise process {episode-url}
```

Once processed, fetch the transcript again.

The transcript is the primary source for card extraction.

## Step 6: Extract Cards from the Transcript

Read the transcript and identify phrases that match the user's level and focus. Apply these extraction rules:

**For Beginner level:**
Target high-frequency vocabulary that appears in the episode but may be unfamiliar to a new learner. Avoid rare or overly academic terms. Prefer words that are genuinely useful in everyday speech.

**For Intermediate level:**
Target phrases, collocations, and multi-word expressions that a learner at this stage would not yet produce naturally — things like "take that with a grain of salt", "push back on", or domain compound nouns. Skip isolated single words that are easy to look up.

**For Advanced level:**
Target idiomatic expressions, register-specific vocabulary, discourse markers, and subtle word-choice distinctions that are only learnable from authentic input. Skip anything below B2 level.

**Universal rules:**
- Always extract the phrase in its full context sentence from the transcript — do not strip it down to a single word.
- Prioritise phrases that appear in natural spoken dialogue, not in a prepared script read aloud.
- Never fabricate a phrase. Every card must trace back to a specific line in the transcript.
- Respect the card count limit the user set. Stop extracting once the limit is reached.

## Step 7: Format the Cards

For each extracted phrase, produce a card with these fields:

| Field | Content |
|---|---|
| **Front** | The phrase or vocabulary item in the learning language |
| **Back** | Translation into the user's native language (as specified in Step 4 or taste.md) |
| **Context** | The full sentence from the transcript where this phrase appeared |
| **Note** | One sentence explaining usage, register, or a common mistake to avoid |
| **Source** | Episode title + podcast name (for reference) |

Example card:

> **Front**: take that with a grain of salt
> **Back**: 对此保持怀疑 / 不要全信
> **Context**: "The data looks promising, but I'd take that with a grain of salt until we see the full study."
> **Note**: Used when you want to acknowledge a claim while signalling scepticism. Tone is polite and common in professional speech.
> **Source**: Lex Fridman Podcast · "The Science of Longevity"

## Step 8: Deliver the Cards

Based on your output preferences, I've recommended a format for you — but you're free to choose any of the three:

1. **Inline review** — show the cards one by one in chat for an immediate study session
2. **Anki import file** — produce a `.txt` file in Anki's tab-separated format, ready to import via `File → Import`
3. **CSV file** — produce a `.csv` with column headers: Front, Back, Context, Note, Source

**Default recommendation order** (shaped by Output Preferences):
- If `Preferred format = bullet points` or `Preferred summary length = short` → recommend **CSV** first
- If `Preferred format = prose / mix` → recommend **inline review** first
- Anki is always available as a third option

**For inline review**, show cards one at a time:
> Here's card 1 of {N}:
> **{phrase}**
> Ready to see the translation and context? (Reply anything to continue.)

**For Anki import**, write the file as `language-cards-{episode-slug}.txt` using this format:
```
#separator:tab
#html:false
#notetype:Basic
#deck:{Podcast Name} — {Episode Title}
{Front}\t{Back}\t{Context}\t{Note}
```

**For CSV**, write the file as `language-cards-{episode-slug}.csv` with a header row:
```
Front,Back,Context,Note,Source
```

Write files to the current working directory and confirm the path.

## Common Failure Cases

- If `get transcript` fails because the episode is not processed and the user declines to process it, the skill cannot run. Stop and suggest the user choose a different episode or process this one later.
- If the transcript is in a different language than the user's specified learning language, tell them immediately — do not extract cards from the wrong language.
- If the episode transcript is very short (under 1,000 words), warn the user that card yield will be low and offer to proceed anyway or switch to a longer episode.
- If the user's level is Beginner but the episode is highly technical, note this mismatch and suggest that the card quality may be lower for this episode — very few phrases will be at a beginner-appropriate level.
- If the user asks for more than 40 cards, cap at 40 and explain that quality drops with larger extraction windows from a single episode.
- If the transcript yields fewer cards than the user's requested count, extract all available phrases and tell the user: "I found {N} phrases at your level — fewer than your target of {M}. These are the best matches from this episode."
- If the user sends multiple confirmation words in a row during inline review (e.g. 'ok ok yes continue'), treat any reply as confirmation of the current card and advance to the next. Do not parse the content of the reply — any non-empty reply advances the session.

## Output Contract

Every card must be grounded in an actual transcript sentence — never invented.

Inline review delivers cards one at a time, waiting for the user to advance.

Anki and CSV files are written to disk and the path confirmed.

The card count never exceeds the user's stated limit or 40, whichever is lower.
