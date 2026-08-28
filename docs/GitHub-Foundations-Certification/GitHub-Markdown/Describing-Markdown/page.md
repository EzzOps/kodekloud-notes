# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

Headings structure content for both readers and search engines—use them to improve readability and SEO by including concise, descriptive phrases.

## Blockquotes

Use the greater-than symbol (`>`) to make quoted blocks:

```markdown theme={null}
> This is a quoted block. It will be indented and usually has a vertical line on the left.
```

Blockquotes are great for highlighting notes, quotes, or important callouts inside regular text.

## Emphasis and inline code

Use emphasis and inline code to call out terms, filenames, or commands:

* Italic: `*italic*` or `_italic_`
* Bold: `**bold**` or `__bold__`
* Inline code: use backticks `` `like this` ``

Example:

```markdown theme={null}
This is *italic* and this is **bold**. Use `inline code` for commands or filenames.
```

Tip: prefer inline code for short commands, filenames, or placeholders.

## Horizontal rule / divider

Separate sections with a horizontal rule. Any of these work:

```markdown theme={null}
---
***
___
```

Horizontal rules visually break longer README files into logical parts.

## Lists

Use unordered (bulleted) or ordered (numbered) lists for steps, features, or itemized details.

Unordered:

```markdown theme={null}
- Item A
- Item B
```

Ordered:

```markdown theme={null}
1. First item
2. Second item
```

Lists improve scanability and accessibility of README content.

## Task lists (checkboxes)

GitHub-Flavored Markdown supports task lists to show progress or checklist items:

```markdown theme={null}
- [x] Master HTML5, CSS & responsive design
- [x] Learn vanilla JavaScript
- [ ] Build and deploy a personal portfolio website
- [ ] Master Git and GitHub workflows
```

Task lists render as interactive checkboxes on GitHub and are useful for contributing guides or project roadmaps.

## Tables

Create tables with pipes (`|`) and separate the header row with dashes (`-`). Example:

```markdown theme={null}
| Category | Tools / Technologies |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| Backend | Node.js, Express |
| Database | MongoDB, PostgreSQL |
| Tools | Git, VS Code, Figma |
| OS | Ubuntu, Windows |
```

Tables are ideal for comparing tools, listing features, or showing compatibility. Keep table rows concise for best readability.

## Links and featured projects

Create hyperlinks using square brackets for text and parentheses for the URL. Combine links with inline code formatting when you want to highlight technologies:

```markdown theme={null}
1. [My profile website](https://example.com)
2. [Project Repository](https://github.com/username/repo) — built with `HTML5`, `CSS`, `JavaScript`
```

These appear as clickable items in the rendered README.

***

Once you add these elements to your README and commit the changes (for example, committing directly to the `main` branch), GitHub will render headings, blockquotes, lists, task checkboxes, tables, and links—making your profile or project README easier to scan and more informative.

## Links and References

* [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/)
* [GitHub README rendering](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
* [Markdown Guide](https://www.markdownguide.org/)
* [MDX documentation](https://mdxjs.com/)

Use these references for advanced MDX/Markdown features and best practices.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/42c15655-2217-4c66-8d0a-2472a3b15e43/lesson/285a86eb-3540-4e21-aa4d-8f3cee3820fe" />
</CardGroup>


# Describing Markdown

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Markdown/Describing-Markdown/page

Overview of Markdown explaining purpose, benefits, syntax examples, tables, and common uses for documentation, README files, blogs, and quick notes

## What is Markdown language?

Markdown is a lightweight markup language designed for writing documentation, README files, and web content with minimal syntax. It converts plain-text formatting into structured HTML while remaining highly readable in its raw form. Markdown is widely supported across platforms such as GitHub, GitLab, and many static site generators.

Key uses:

* README files and project documentation
* Quick notes and knowledge bases
* Blog posts and static websites

<Callout icon="lightbulb">
  Markdown is ideal for README files, quick notes, and simple documentation because it balances formatting power with readability.
</Callout>

## Benefits (at a glance)

| Benefit              | Why it matters                                | Example use                                            |
| -------------------- | --------------------------------------------- | ------------------------------------------------------ |
| Faster than HTML     | Minimal syntax speeds authoring               | Write `**bold**` instead of `<strong>`                 |
| Readable in raw form | Easier to review and edit in plain text       | Collaborators can understand content without rendering |
| Portable & supported | Many platforms and converters accept Markdown | GitHub, GitLab, static site generators                 |

## This lesson

In this article we demonstrate a simple Markdown example that includes headings and tables. Use the sample below as a template for documenting small features, game elements, or product details.

## Example Markdown

```markdown theme={null}
Here are the details for each power-up that can drop from a destroyed brick.

| Icon         | Name         | Duration    | Effect                                         |
|--------------|--------------|-------------|------------------------------------------------|
| 🏓           | Multi-Ball   | 10 seconds  | Doubles the number of balls on the screen.     |
| 🛡️           | Mega Paddle  | 10 seconds  | Increases the width of your paddle.            |
| 🚀           | Auto-Bullets | 10 seconds  | The paddle automatically fires bullets upwards.|
```

## Quick Markdown Reference

| Element      | Syntax                        | Rendered example            |
| ------------ | ----------------------------- | --------------------------- |
| Heading      | `# H1`, `## H2`               | # H1                        |
| Bold         | `**bold**` or `__bold__`      | **bold**                    |
| Italic       | `*italic*` or `_italic_`      | *italic*                    |
| List (ul)    | `- item` or `* item`          | - item                      |
| Ordered list | `1. First`                    | 1. First                    |
| Code inline  | `` `code` ``                  | `code`                      |
| Code block   | triple backticks \`\`\`       | `code`                      |
| Link         | `[text](https://example.com)` | [text](https://example.com) |
| Image        | `![alt](path/to/image.png)`   | <img alt="alt" />           |
| Table        | Pipes and dashes              | See example above           |

<Callout icon="warning">
  Markdown dialects (CommonMark, GitHub Flavored Markdown, etc.) vary slightly — tables, task lists, and some extensions may behave differently depending on the renderer. Test on your target platform.
</Callout>

## Notes

* Markdown keeps documentation focused on content rather than verbose tags.
* Use emojis or inline images in tables when icons are needed; ensure image files exist in the repository if you reference them.
* For complex layouts, combine Markdown with HTML only if your renderer allows it.

## Links and References

* [CommonMark Spec](https://spec.commonmark.org/)
* [GitHub Flavored Markdown](https://github.github.com/gfm/)
* [The Markdown Guide](https://www.markdownguide.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/42c15655-2217-4c66-8d0a-2472a3b15e43/lesson/c5dd836f-505a-4343-a2d3-7fb56d339206" />
</CardGroup>
