---
description: "Use when writing, drafting, or editing blog markdown files for this repository. Covers unified frontmatter, draft placement, category selection, filename rules, and metadata normalization for docs/_drafts and docs/blog/posts."
name: "Blog Frontmatter"
applyTo: "docs/_drafts/**/*.md,docs/blog/posts/**/*.md"
---

# Blog Frontmatter Rules

Use this instruction when creating or editing blog articles in this repository.

## Canonical Frontmatter

Unless the user explicitly asks for a special format, use this exact frontmatter structure and field order:

```yaml
---
title: {title}
date: {date}
excerpt: {excerpt}
category: {category}
tags: {[tags]}
font: "阿里巴巴普惠体-Regular"
addons:
	- quantide-palette
	- quantide-admonition
	- quantide-layout-xhs
aspectRatio: 3/4
canvasWidth: 600
img: {cats}
layout: cover-photo-down
---
```

## Required Fields

- `title`: concise, specific, not clickbait, and must not contain `:` or `：`
- `date`: fill with the current date when the article is prepared for publication, using `YYYY-MM-DD`
- `excerpt`: one compact summary derived from the article content, counting Chinese and English characters together, no more than 120 characters including punctuation, and must not contain `:` or `：`
- `category`: use singular `category`, not `categories`
- `tags`: a short list derived from the article content; individual tag values must not contain `:` or `：`
- `img`: this template uses the variable placeholder `{cats}` and should be resolved when the article is prepared for publication

## Metadata Safety Rules

- Generated frontmatter values such as `title`, `excerpt`, tag values, and other plain-text metadata should not contain `:` or `：`
- This is a hard constraint to avoid frontmatter parsing conflicts and accidental YAML breakage
- If a natural phrasing contains a colon, rewrite it rather than escaping it
- When counting the `excerpt` length, count Chinese and English characters together and keep the total at 120 characters or fewer, including punctuation

## Fixed Presentation Fields

These fields are part of the standard format and should be kept as shown unless the user explicitly requests another visual layout:

- `font: "阿里巴巴普惠体-Regular"`
- `addons` with the three `quantide-*` entries shown above
- `aspectRatio: 3/4`
- `canvasWidth: 600`
- `layout: cover-photo-down`

Do not remove or reorder these fixed presentation fields by default.

## Placeholders And Publish-Time Filling

The brace form means a variable placeholder.

- In scaffolds or early drafts, placeholders may remain in brace form when the final value is not yet stable
- When an article is being prepared for publication, replace placeholders using the current date and the finished article content
- `title`, `excerpt`, `category`, `tags`, and `img` should be inferred from the article itself at publish time if not already finalized
- Do not leave brace placeholders in a file that the user considers publish-ready

## Category Mapping

Choose the eventual category by topic, not by draft location:

- `algo`: strategy logic, data problems, backtests, execution, microstructure, implementation
- `papers`: paper reading, replication, critique, research commentary
- `others`: broader essays, weekly notes, adjacent technical commentary
- `career&figure`:人物、职业路径、机构故事、行业观察
- `coursea`: course-related content if the user explicitly asks for that column

When editing an existing published post, preserve its established section unless the user asks to move it.

## Draft Placement

- New articles should be created under `docs/_drafts/` first unless the user explicitly asks to publish directly
- Draft filenames should be human-readable and derived from the working title
- Prefer Chinese filenames when the article title is Chinese
- If the target filename already exists, append `-v2`, `-v3`, or another clear suffix instead of overwriting silently

## Normalization Rules

When normalizing frontmatter:

- convert `categories` to `category` unless the file clearly belongs to a different rendering system that requires `categories`
- convert ad hoc frontmatter layouts to the canonical field order above when the file is intended to use this XHS layout format
- preserve existing body content
- preserve intentional extra fields only if the user clearly wants them; otherwise prefer the canonical template without extras
- avoid changing the article’s meaning just to satisfy metadata consistency

## Writing Constraints

- Frontmatter should be followed by a blank line, then article body
- Do not fabricate unsupported claims in `excerpt`
- Do not generate frontmatter text values with `:` or `：`
- Keep `excerpt` within 120 characters total, counting Chinese and English characters together and including punctuation
- Do not insert placeholder text like `TODO` into published posts unless the user asks for a scaffold
- For drafts, brace placeholders are acceptable when the command explicitly creates a scaffold or the final metadata is not yet stable
