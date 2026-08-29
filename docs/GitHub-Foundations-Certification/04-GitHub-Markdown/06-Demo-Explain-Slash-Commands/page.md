# H1: Project Documentation Header
## H2: Sub-Section Header
### H3: Feature Header
#### H4: Detail Header
##### H5: Minor Header
###### H6: Smallest Header
```

> **warning** Use only one `#` (H1) per document when possible and structure content with H2/H3 for accessibility and SEO.

## Emphasis

Use asterisks `*` or underscores `_` to emphasize text.

* One `*` or `_` for italic
* Two `**` or `__` for bold
* Three `***` or `___` for bold + italic

```markdown theme={null}
*italic*    _italic_
**bold**    __bold__
***bold italic***  ___bold italic___
```

To summarize these markers, here’s a quick reference:

| Effect        | Markup examples              |
| ------------- | ---------------------------- |
| Italic        | `*text*` or `_text_`         |
| Bold          | `**text**` or `__text__`     |
| Bold + Italic | `***text***` or `___text___` |

<Frame>
  <img alt="The image explains Markdown basic syntax for text emphasis, illustrating how to apply bold, italic, and bold-italic effects, along with escape characters for plain text." />
</Frame>

## Escaping Markdown Characters

If you need to show literal Markdown characters (for example, an asterisk) without rendering them, escape with a backslash `\`.

```markdown theme={null}
This is a literal asterisk: \*
This shows a backslash-escaped underscore: \_
```

## Links and Images

Links and images share a similar syntax. Put the link text in square brackets and the URL in parentheses; prefix with `!` to embed an image.

```markdown theme={null}
[Display text](https://example.com)
![Alt text](https://example.com/image.png)
```

Best practices:

* Use clear link text that describes the destination.
* Add descriptive alt text for images to improve accessibility and SEO.
* For local images in docs, use relative paths.

## Lists

Use unordered or ordered lists to break down steps or items. Unordered lists accept `-`, `*`, or `+`. For ordered lists, use numbers followed by a period. Indent to create nested lists (2–4 spaces is common).

```markdown theme={null}
- Item A
  - Nested item A.1
  - Nested item A.2
* Item B
+ Item C

1. First step
2. Second step
   1. Sub-step
   2. Sub-step
```

<Frame>
  <img alt="The image provides a comparison of unordered and ordered list syntax in Markdown, demonstrating basic list formatting." />
</Frame>

## Tables

Markdown tables use pipes `|` to separate columns and dashes `-` to separate headers from rows. Put inline code in backticks when table cells contain snippets or commands.

```markdown theme={null}
| Feature | Command        | Description        |
|---------|----------------|--------------------|
| Status  | `git status`   | Working tree state |
| Log     | `git log`      | Commit history     |
| Branch  | `git branch`   | Manage branches    |
```

When to use tables:

* To compare features or commands.
* To present structured data clearly for readers and search engines.

## Blockquotes

Blockquotes start with `>` and are useful for highlighting tips, notes, or quoted text.

```markdown theme={null}
> This is a blockquote about version control:
> Always commit with clear messages.
```

<Frame>
  <img alt="The image describes the basic syntax for using blockquotes in Markdown, with an example related to version control." />
</Frame>

## Inline Code and Fenced Code Blocks

Use single backticks for inline code and triple backticks for fenced code blocks. Specify the language immediately after the opening triple backticks to enable syntax highlighting.

Inline:

```markdown theme={null}
`print("hello")`
```

Fenced block with language:

```python theme={null}
# A larger code block with language specified
def greet(name):
    return f"Hello, {name}"

print(greet("World"))
```

> **lightbulb** Always specify the language after the opening triple backticks (for example, `python`) so renderers can apply proper syntax highlighting.

## Quick SEO & Accessibility Tips

* Use descriptive headings and alt text for images.
* Keep link text meaningful (avoid "click here").
* Use code fences and language tags for better indexing and readability.

That covers the core Markdown features you'll use most often when writing documentation and READMEs.

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/42c15655-2217-4c66-8d0a-2472a3b15e43/lesson/6671f083-263a-49bb-b7ef-999c7ea5ce1d)


# Demo Explain Slash Commands

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Markdown/Demo-Explain-Slash-Commands/page

Explains GitHub slash commands that insert alerts, code blocks, collapsible details, tables and templates to quickly compose rich Markdown in issues, pull requests, and discussions.

In this lesson you'll learn how GitHub's slash commands speed up composing rich Markdown content—such as alerts, code fences with syntax highlighting, collapsible details, and tables—without typing all the Markdown or HTML manually.

Slash commands are available where the editor accepts rich issue/PR/discussion content (issues, pull requests, and discussions). They are not available in static README editors.

> **lightbulb** Slash commands work in Issues, Pull Requests, and Discussions. They are not available in static README Markdown editors.

How to open the slash menu

* Create a new issue, a pull request body, or a discussion comment.
* Type a forward slash (`/`) to open the slash menu. The editor will display quick inserts such as Alerts, Code block, Details, Saved replies, Templates, and Table.
* Choose an item from the menu to insert a fully-formed snippet you can edit.

<Frame>
  <img alt="The image shows a GitHub interface where a new issue is being created with a title &#x22;exploring slash commands&#x22; and a description containing an alert message. There's a dropdown menu for slash commands with options like Alerts and Code block." />
</Frame>

Common slash-command inserts
Below is a concise overview of common slash-command inserts you’ll encounter and how to use them.

| Insert                    | What it does                                                                                | Example                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Alerts                    | Adds a visually prominent alert or callout to draw attention to warnings, notes, or tips.   | See the Alert example below.                                    |
| Code block                | Inserts a fenced code block and lets you pick a language for syntax highlighting.           | See the JavaScript example below.                               |
| Details (collapsible)     | Inserts an HTML `<details>` block so long content can be hidden behind a clickable summary. | See the Details example below.                                  |
| Table                     | Prompts for rows/columns and inserts a Markdown table skeleton.                             | See the 4×4 table example below.                                |
| Saved replies / Templates | Reuse or insert prewritten content such as issue templates or commonly used responses.      | Configure in repository settings (Saved replies and Templates). |

Examples

Alerts

* The Alerts insert creates a prominent message block. A portable Markdown pattern for a warning is a blockquote with bold text and an emoji:

```markdown theme={null}
> **⚠️ Warning**
> This action is irreversible. Make sure you understand the consequences before proceeding.
```

Code blocks

* The Code block insert produces a fenced code block with a language option so the editor can highlight syntax. Example JavaScript:

```javascript theme={null}
var a = -1;
console.log(a);
```

Details (collapsible content)

* The Details insert adds an HTML `<details>` block. This is supported in GitHub-flavored Markdown and is useful for hiding long sections until the reader expands them:

```html theme={null}
<details>
  <summary>Details</summary>
  <p>
    Long Paragraph Long Paragraph Long Paragraph Long Paragraph Long Paragraph
  </p>
</details>
```

Tables

* The Table insert prompts you for the number of columns and rows, then inserts a Markdown table skeleton. Replace headers and cells with your values. Example 4×4 table:

```markdown theme={null}
| Header | Header | Header | Header |
|--------|--------|--------|--------|
| Cell   | Cell   | Cell   | Cell   |
| Cell   | Cell   | Cell   | Cell   |
| Cell   | Cell   | Cell   | Cell   |
```

Other useful inserts

* Saved replies and Templates let you quickly reuse structured content across issues, PRs, and discussions—helpful for maintaining consistent responses and reducing repetitive typing.

Best practices and tips

* Use the slash menu to avoid manually typing fences, alignment pipes, or HTML tags.
* Combine inserts: for example, put a code block inside a Details block to hide long examples.
* Review and edit the inserted snippet—slash commands provide a starting point that you can tailor to your needs.

Links and references

* [GitHub Docs — Writing on GitHub](https://docs.github.com/en/get-started/writing-on-github)
* [GitHub Docs — Issue and pull request templates](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-issue-and-pull-request-templates)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/42c15655-2217-4c66-8d0a-2472a3b15e43/lesson/8bb1b5d3-d4a0-43f9-b107-7e06f57e3e78)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/github-foundation-certification/module/42c15655-2217-4c66-8d0a-2472a3b15e43/lesson/4d8c6375-8b77-452b-94ce-d6e03c474daa)
