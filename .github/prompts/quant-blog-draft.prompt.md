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

Body requirements:

- Open from a concrete tension, puzzle, or claim
- Keep the argument falsifiable and evidence-aware
- If facts or data are still missing, mark them in a short `待补充材料` section near the end instead of bluffing

Final response requirements:

- State the created file path
- Briefly summarize the chosen angle
- Call out any factual gaps or evidence still worth verifying
