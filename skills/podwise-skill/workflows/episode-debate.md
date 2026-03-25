# Podwise Episode Debate

Use this skill to turn passive listening into active thinking. It extracts the strongest claims from a podcast episode and then challenges them — probing assumptions, surfacing counterevidence, and forcing the user to engage rather than just nod along.

## Goals

1. Verify that `podwise` is installed and configured.
2. Identify and load the target episode's content.
3. Extract the episode's core claims and arguments.
4. Open a Socratic dialogue: present claims, challenge them, invite the user to respond.
5. Keep pushing until the user has formed or sharpened their own position.
6. Optionally produce a debate summary the user can save.

## Step 1: Check the Environment

```bash
podwise --help
podwise config show
```

If `podwise` is not installed or the API key is missing, stop and follow [references/installation.md](references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read the **Core Interest Areas** silently. Use this to calibrate the depth and angle of the debate — challenge claims harder in the user's areas of expertise, more gently in areas they are still exploring.
- If not found, proceed with default depth.

## Step 3: Identify the Target Episode

The user may provide the episode as:

- A Podwise episode URL: `https://podwise.ai/dashboard/episodes/{id}`
- A YouTube or Xiaoyuzhou URL
- An episode title or keyword — search first:

```bash
podwise search episode "{title or keyword}" --limit 5 --json
```

Present the results and ask the user to confirm which episode before continuing.

## Step 4: Load the Episode Content

Fetch the episode's AI artifacts to build a full picture of its arguments:

```bash
podwise get summary {episode-url}
podwise get highlights {episode-url}
podwise get qa {episode-url}
podwise get chapters {episode-url}
```

If any command fails because the episode is not yet processed, ask the user for confirmation before processing:

> "This episode hasn't been processed yet. Processing will use one credit from your Podwise quota. Proceed?"

Only run `process` after explicit confirmation:

```bash
podwise process {episode-url}
```

Once processed, re-run the `get` commands.

Do not begin the debate until at least `get summary` and `get highlights` succeed — these are the minimum needed to identify the episode's claims.

Optionally, if the episode's speaker attribution in highlights is ambiguous, fetch the transcript to confirm who made which claim:

```bash
podwise get transcript {episode-url}
```

Use the transcript only to disambiguate speaker attribution — do not read it in full for claim extraction. Skip this step if attribution is already clear from the other artifacts.

## Step 5: Extract the Core Claims

Read the summary, highlights, Q&A, and chapters. Before extracting claims, assess whether the material is actually suitable for debate:

- If the summary and highlights contain no assertion that meets the criteria below, stop and tell the user: *"This episode appears to be primarily factual or instructional rather than argumentative — there may not be enough debatable claims for a rich debate. Would you like to try a different episode?"*
- If the material looks viable, proceed to extract 3–5 claims.

A good claim for debate has these properties:
- It makes a specific assertion (not just an observation)
- It is falsifiable or at least challengeable
- It has real-world implications if true or false
- A reasonable person could disagree with it

Weak claims (trivial facts, obvious statements, pure personal anecdotes) are not worth debating. Discard them silently.

Do not share the full extraction step with the user — only the resulting claim count (see Step 6).

## Step 6: Run the Socratic Dialogue

After extracting claims, open with a brief framing message that gives the user choice:

> Based on my analysis of *{Episode Title}* by {Podcast Name}, I've identified **{N} claims** worth examining. I'll start with the one I think is strongest — but let me know if you'd like to tackle a different one first.
>
> **Claim 1**: {State the claim clearly in 1–2 sentences, attributing it to the speaker if possible.}
>
> **Challenge**: {1–2 sentences questioning an assumption, citing a counterexample, or probing the scope of the claim. Do not demolish it — open a question.}
>
> What's your reaction?

**Dialogue rules:**

- Ask one focused question at a time. Never ask multiple questions in a single message.
- When the user responds:
  - If they defend the claim with strength and specificity: accept the point, acknowledge it, and move to the next claim.
  - If their defence has gaps or weaknesses: push on exactly that weak point — do not accept or move on prematurely.
  - If they fully concede: acknowledge it cleanly and move to the next claim.
  - If they introduce a new claim not from the episode: note it, add it to the end of the claim list, and return to the current thread.
- Introduce counterarguments from the real world, not just logic — cite named researchers, known events, or competing frameworks when relevant.
- Never let the dialogue become a lecture. The user's responses should shape where the debate goes.
- **Minimum exchange rule**: you may only move to the next claim after at least 2 full exchange rounds on the current one. Do not skip this to shorten the session.
- Stop when all extracted claims have been discussed, or when the user signals they are done early.

**After each claim is resolved**, silently record a brief note (not shown to the user) with:
- The claim text
- The challenge raised
- The user's final position on this claim

These notes are used only to populate Step 7's summary if the user requests it.

**Closing the session:**

When the debate feels complete (or the user signals they are done), close with a 3–4 sentence synthesis:

> Here's where I think you landed: {summary of the user's apparent position after the dialogue}. The strongest argument for the episode's view was {X}. The weakest was {Y}. The question worth sitting with is: {one open question that the debate did not fully resolve}.

Then ask: *"Does this feel accurate to you?"* — do not extend the debate from the answer. If the user corrects something, note it for the summary, then ask: *"Want me to save a summary of this debate?"*

## Step 7: Optionally Save a Debate Summary

If the user confirms, write a summary file named: `episode-debate-{episode-slug}-{YYYY-MM-DD}.md`

Use this template:

```markdown
# Episode Debate: {Episode Title}

**Podcast**: {Podcast Name}
**Episode**: {episode-url}
**Debated**: {date}

---

## Claims Examined

### Claim 1: {claim}
**Challenge raised**: {the challenge}
**User's position**: {summary of where the user landed}

### Claim 2: {claim}
**Challenge raised**: {the challenge}
**User's position**: {summary of where the user landed}

{repeat for each claim discussed}

---

## Overall Position After Debate

{2–3 sentences on where the user landed by the end of the session.}

## Open Question

{The one question the debate did not fully resolve.}

---

_Generated by podwise-episode-debate · {date}_
_Source: {episode-url}_
```

Write the file to the current working directory and confirm the path.

## Common Failure Cases

- If the episode's content is entirely factual and non-argumentative (e.g. a news recap or a how-to episode), tell the user this episode may not yield a rich debate. Offer to either proceed with what is available or switch to a different episode.
- If the user gives one-word responses and is not engaging, try reframing the challenge or offering the opposing position directly to provoke a reaction: *"Let me put it differently — what if {speaker} is completely wrong about this?"*
- If the user asks for the debate to be faster, compress to 2–3 key claims instead of 5 and skip the nuanced follow-ups.
- If the user wants to debate a claim that requires information beyond the episode, acknowledge the limit: *"That's a fair challenge, though it's outside what this episode covers — let me bring it back to what {speaker} actually argued."*

## Output Contract

The debate is a live dialogue, not a document. Do not produce a structured output mid-session.

The closing synthesis is always delivered verbally at the end of the session.

A written debate summary file is produced only if the user requests it.

Exactly one claim is active at a time. Never stack multiple challenges.

At least 2 full exchange rounds must occur before moving off any claim — no exceptions.
