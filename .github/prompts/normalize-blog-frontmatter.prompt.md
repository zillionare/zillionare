---
name: normalize-blog-frontmatter
description: "Normalize metadata for an existing blog markdown file in this repository. Use when a post or draft has inconsistent frontmatter such as categories vs category, missing excerpt, or unordered metadata fields."
argument-hint: "Target file path or say current file"
agent: agent
---

Follow [blog frontmatter rules](../instructions/blog-frontmatter.instructions.md).

Task:

Normalize the frontmatter of the target markdown file.

Requirements:

1. Keep the article body intact unless a metadata fix requires a tiny wording change in the excerpt
2. Convert metadata to the canonical XHS layout key order when appropriate
3. Prefer `category` over `categories`
4. Preserve the fixed presentation fields required by the standard template: `font`, `addons`, `aspectRatio`, `canvasWidth`, and `layout`
5. For publish-ready files, replace brace placeholders with concrete values; for scaffolds, placeholders may remain when appropriate

Final response requirements:

- State which file was normalized
- List the metadata fields that changed
