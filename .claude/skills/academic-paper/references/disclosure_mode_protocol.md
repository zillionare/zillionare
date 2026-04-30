# Disclosure Mode Protocol

**Status**: v3.2
**Parent skill**: `academic-paper`
**Mode name**: `disclosure`
**Purpose**: Generate a venue-specific AI-usage disclosure statement that complies with the target venue's current AI policy, placed in the venue's preferred section (Methods / Acknowledgements / cover letter / separate statement), in the venue's preferred voice.

---

## Why this mode exists

`academic-paper` already ships two generic AI disclosure templates in `journal_submission_guide.md` ("Minimal Disclosure" and "Detailed Disclosure"). Those templates are a good starting point but they are venue-agnostic: they don't know that Nature requires disclosure in the Methods section specifically, that ICLR requires it in the paper body with acknowledgement that "LLMs were used as general-purpose writing tools", or that ACL requires the disclosure in a dedicated "Use of AI Assistance" subsection.

Disclosure mode closes this gap. It takes the paper and a target venue, looks up the venue's current AI policy in the v1 policy database, and produces the disclosure text placed correctly.

---

## Inputs

1. **Paper draft**: current manuscript text (the mode needs to know what the AI actually did in order to describe it accurately).

2. **Target venue**: journal or conference name. If the venue is in the v1 database (ICLR, NeurIPS, Nature, Science, ACL, EMNLP), use the cached policy. If not, refuse to guess — prompt the user to paste the venue's current AI policy text from the venue's submission page.

3. **What ARS did**: the mode reads the paper's commit history / pipeline log (if using the full `academic-pipeline`) to identify which AI-assisted steps produced which parts of the paper. At minimum: research assistance, drafting assistance, revision assistance, citation checking, peer review simulation. If the pipeline log is not available, ask the user to confirm which categories apply.

---

## Process

### Phase 1: Intake + venue lookup

- If venue is in the v1 database → load policy from `venue_disclosure_policies.md`.
- If venue is unknown → halt. Print: "I do not have a cached policy for {venue}. Please paste the venue's current AI-usage / generative-AI policy text so I don't guess." Do NOT fabricate a policy.
- If the user pastes a policy for an unknown venue, use it for this session only. Do NOT auto-persist it to the database — policies drift, and the database needs curation.

### Phase 2: Categorize AI usage

Produce a categorized list of how AI was used in the manuscript:

| Category | Examples |
|---|---|
| Research assistance | Literature search, annotated bibliography, claim verification |
| Drafting assistance | Section drafting, paraphrasing, outline generation |
| Revision assistance | Reviewer response drafting, tracked changes, consistency checking |
| Editing assistance | Grammar, style, formatting, citation format conversion |
| Analysis assistance | Not applicable to pure writing flows; flag if the paper reports any analysis the AI did |
| Peer review simulation | `academic-paper-reviewer` was used on the draft pre-submission |

For each category, mark: USED / NOT USED / UNCERTAIN. UNCERTAIN items require user confirmation before the disclosure text is finalized.

### Phase 3: Match categories to the venue's required phrasing

Each venue in the policy database specifies (a) which categories are mandatory to disclose, (b) which are optional, (c) which are prohibited (e.g., analysis assistance may require separate disclosure at some venues). The mode matches the user's category list against the venue's requirements and flags any mismatch (e.g., "Venue requires disclosure of research assistance; your categorization marked it UNCERTAIN").

### Phase 4: Generate the disclosure text

Generate a single disclosure paragraph using:
- The venue's preferred voice (first person vs passive, past tense vs present)
- The venue's required phrasing elements (many venues require the phrase "The authors take full responsibility for the content" or equivalent)
- The specific tool name — "Claude (Anthropic) via Academic Research Skills pipeline" — not generic "AI tools"
- The specific categories marked USED

Example output for Nature (which requires disclosure in Methods):

```
## AI-assisted tools

The authors used Claude [MODEL_VERSION] (Anthropic), orchestrated via the
Academic Research Skills pipeline (Wu, 2026), during the preparation
of this manuscript. Specifically, the tool was used for literature
search assistance, citation verification, drafting of section outlines,
and internal peer-review simulation prior to submission. All
AI-assisted output was reviewed, edited, and verified by the authors,
who take full responsibility for the content of this article.
```

**Note**: Replace `[MODEL_VERSION]` with the actual model used in this run (e.g., `Opus 4.7`, `Sonnet 4.6`). Pull the identifier from session metadata rather than hard-coding a version, since Anthropic's lineup changes over time.

### Phase 5: Placement instructions

Output includes explicit placement instructions matching the venue's policy:

```
Placement: Methods section (Nature policy, accessed YYYY-MM-DD from
https://www.nature.com/.../policy-url). Include as the final
subsection of Methods, before Data Availability.
```

If the venue requires placement in multiple locations (e.g., Methods + cover letter + Acknowledgements), the mode generates tailored text for each location rather than a single paragraph.

---

## Failure cases this mode does NOT cover

- **Venues outside the v1 database**: the mode halts and asks the user. It does not guess.
- **Policies that have changed since the database snapshot**: the mode records the access date in the placement instructions. Users should verify against the current venue page before submission.
- **Analysis assistance**: if the AI actually ran computations or generated analysis results (not just writing), most venues require a separate disclosure in a Code Availability or Analysis section. This mode flags the case and produces a separate paragraph; the user must place it manually.
- **Co-authored AI**: as of the 2026 policy snapshot, no venue in the v1 database accepts AI as a listed author. The mode refuses to produce author-list text and instead produces authorship-rejection text plus the disclosure.

---

## Integration with existing journal_submission_guide.md

`journal_submission_guide.md` retains the two generic templates (Minimal / Detailed) as fallback for venues not in the v1 database. Disclosure mode's output supersedes those templates when the venue is known. The guide is updated to point to this mode for known venues.

---

## References

- `venue_disclosure_policies.md` — v1 policy database (ICLR, NeurIPS, Nature, Science, ACL, EMNLP)
- `journal_submission_guide.md` — existing generic templates (fallback)
- `credit_authorship_guide.md` — existing CRediT authorship best practices
- Lu et al. (2026). Towards end-to-end automation of AI research. *Nature* 651, 914-919 — the ethics statement for Lu 2026 was drafted in compliance with Nature's policy; their methodology is a worked example of what this mode should produce.
- ROADMAP_v3.2.md item 6 — design decisions (v1 venue set, unknown-venue halt, education/QA venues deferred to v2)
