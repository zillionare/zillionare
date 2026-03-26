---
name: quant-blog-outline
description: "Generate a strong angle and outline for a quant trading blog post. Use when you want a reusable blog idea package before writing the full draft."
argument-hint: "Topic, target reader, and constraints"
agent: agent
---

Use the [quant blog writing skill](../skills/quant-blog-writing/SKILL.md) and follow [blog frontmatter rules](../instructions/blog-frontmatter.instructions.md).

Task:

Create an outline-first package for a new quant-related blog post.

Required output:

1. Proposed title candidates
2. Core thesis
3. Target reader
4. Recommended `category`
5. A 4-8 section outline
6. Evidence and material checklist
7. Suggested draft path under `docs/_drafts/`
8. A frontmatter preview that follows the repository's canonical XHS layout template, using placeholders where publish-time values are still unstable

Rules:

- Do not write the full article unless the user explicitly asks for it
- Keep the angle concrete, defensible, and non-generic
- If the topic is broad, narrow it before outlining
- Design the opening around the article's real bottleneck or practical constraint rather than a generic industry statement
- If the article depends on a few representative tools, datasets, APIs, or workflows, surface them early in the outline and title logic instead of burying them mid-article
- Prefer an outline with visible 起承转合: concrete problem, concept framing, mechanism/examples, practical takeaway
- If a likely filename already exists, suggest a versioned alternative
- In any proposed frontmatter preview, generated text values such as `title`, `excerpt`, and tag values must not contain `:` or `：`
- Keep any generated `excerpt` within 120 characters total, counting Chinese and English characters together and including punctuation
