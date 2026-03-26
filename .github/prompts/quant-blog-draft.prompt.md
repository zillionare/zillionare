---
name: quant-blog-draft
description: "Generate and save a quant blog draft with unified frontmatter under docs/_drafts. Use when you want a real markdown draft file, not just an outline."
argument-hint: "Topic, target reader, preferred angle, and whether to write full prose or scaffold"
agent: agent
---

Use the [quant blog writing skill](../skills/quant-blog-writing/SKILL.md) and follow [blog frontmatter rules](../instructions/blog-frontmatter.instructions.md).

Task:

Create a new markdown draft under `docs/_drafts/` for the requested blog topic.

Execution requirements:

1. Determine the strongest angle and a precise working title
2. Choose the appropriate `category`
3. Create a new file under `docs/_drafts/` with unified frontmatter
4. Unless the user asks for outline-only, include a substantial draft body
5. Do not overwrite an existing file; use a clear version suffix when needed

Required frontmatter:

- `title`
- `date`
- `excerpt`
- `category`
- `tags`
- `font`
- `addons`
- `aspectRatio`
- `canvasWidth`
- `img`
- `layout`

Placeholder rules:

- Use the repository's canonical XHS layout frontmatter template
- For early drafts, brace placeholders may remain for fields that should be finalized at publish time
- If the article is already concrete enough, it is acceptable to fill `title`, `excerpt`, `category`, and `tags` immediately
- Use the current date only when the user wants a publish-ready draft; otherwise `date` may remain a publish-time placeholder
- Generated frontmatter text values such as `title`, `excerpt`, and tag values must not contain `:` or `：`
- `excerpt` must be 120 characters or fewer, counting Chinese and English characters together and including punctuation

Body requirements:

- Open from a concrete tension, puzzle, or claim
- The first screen should identify the article's real bottleneck or operational constraint, not generic background throat-clearing
- If the article is mainly about a few concrete tools, datasets, APIs, or workflows, name those representative examples early in the opening instead of saving them for later
- Keep the article's 起承转合 visible: concrete pain point first, then concept/background framing, then mechanism or examples, then practical takeaway
- Keep the argument falsifiable and evidence-aware
- If facts or data are still missing, mark them in a short `待补充材料` section near the end instead of bluffing

Final response requirements:

- State the created file path
- Briefly summarize the chosen angle
- Briefly note how the opening is anchored to the core pain point or representative examples when that choice matters to the draft
- Call out any factual gaps or evidence still worth verifying
