# Demo Identify the Basic Formatting Syntax

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Markdown/Demo-Identify-the-Basic-Formatting-Syntax/page

Practical guide to Markdown and MDX formatting for README files with examples, tips, and best practices for headings, lists, tables, code blocks, and GitHub rendering.

This lesson shows how to apply common Markdown (and MDX) formatting to a README. It walks through practical examples you can paste directly into your README source to improve readability on GitHub and other Markdown renderers.

<Callout icon="lightbulb">
  A few MDX-specific tips for editing READMEs rendered as MDX:

  * Wrap snippets that include curly braces or angle-bracket placeholders in backticks, for example: `` `{{workflow.name}}` `` or `` `https://localhost:<PORT>` ``.
  * Avoid placing raw JSON or object literals inline; use fenced code blocks to ensure correct rendering and parsing.
</Callout>

<Callout icon="warning">
  When adding examples with placeholders (e.g., `<PORT>`, `<name>`) or template variables (e.g., `{{inputs.param}}`), always wrap them in backticks to prevent the MDX parser from interpreting them as JSX or template syntax.
</Callout>

## Quick reference

Use this short reference for common Markdown elements and how to use them in README files.

| Element         |                               Syntax | Example                                             |                              |
| --------------- | -----------------------------------: | --------------------------------------------------- | ---------------------------- |
| Heading         |                 `#` through `######` | `# Heading 1`                                       |                              |
| Blockquote      |                                  `>` | `> This is a quoted block.`                         |                              |
| Inline emphasis | `*italic*`, `**bold**`, `` `code` `` | `This is *italic* and **bold**. Use `inline code`.` |                              |
| Horizontal rule |                                `---` | `---`                                               |                              |
| Unordered list  |                           `-` or `*` | `- Item A`                                          |                              |
| Ordered list    |                                 `1.` | `1. First item`                                     |                              |
| Task list       |                    `- [ ]` / `- [x]` | `- [x] Complete step`                               |                              |
| Table           |                             Pipes \` | `and dashes`-\`                                     | See the Tables section below |
| Hidden comment  |                         HTML comment | `<!-- Hidden comment -->`                           |                              |

## Hiding lines with HTML comments

Use HTML-style comments in the README to keep content visible only in the source but hidden when rendered on GitHub:

```markdown theme={null}
<!--
This line is hidden when rendered.
This line is also hidden when rendered.
-->
```

These are useful for leaving notes, TODOs, or editing reminders inside your README file.

## Headings

Create headings with the hash (`#`) character. More hashes produce smaller headings:

```markdown theme={null}
