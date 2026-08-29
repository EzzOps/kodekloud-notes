# Identifying Text Formatting Toolbar on Issue and Pull Request Comments

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Markdown/Identifying-Text-Formatting-Toolbar-on-Issue-and-Pull-Request-Comments/page

Guide to GitHub comment formatting toolbar showing buttons, Markdown insertions, keyboard shortcuts and GitHub behaviors like mentions, references, task lists, and emoji

This guide explains the text formatting toolbar available when composing comments on GitHub issues and pull requests. The toolbar helps you apply GitHub Flavored Markdown (GFM) and GitHub-specific features (mentions, issue/PR references, task lists) without memorizing markup. Use the "Write" and "Preview" tabs to switch between source and rendered output.

<Callout icon="lightbulb">
  The toolbar inserts Markdown for you. Toggle between the "Write" and "Preview" tabs to verify how your comment will render before posting.
</Callout>

Key toolbar buttons and what they insert

| Button             | Action                                           |     Markdown inserted (example) |
| ------------------ | ------------------------------------------------ | ------------------------------: |
| Bold               | Wraps selected text in bold                      |        `**bold**` or `__bold__` |
| Italic             | Wraps selected text in italic                    |        `*italic*` or `_italic_` |
| Strikethrough      | Applies strikethrough                            |             `~~strikethrough~~` |
| Inline code        | Marks inline code                                |                  `` `inline` `` |
| Code block         | Inserts fenced code block with optional language | ` ```python\nprint("hi")\n``` ` |
| Link               | Adds a hyperlink                                 |   `[text](https://example.com)` |
| Quote              | Makes a blockquote                               |                 `> quoted line` |
| Bulleted list      | Starts a bulleted list                           |                        `- item` |
| Numbered list      | Starts a numbered list                           |                       `1. item` |
| Task list          | Creates a checkbox item                          |    `- [ ] todo` or `- [x] done` |
| Mention            | Autocompletes users/teams                        |                     `@username` |
| Issue/PR reference | Autocompletes issues/PRs in the repo             |                          `#123` |
| Emoji              | Inserts emoji shortcodes                         |         `:rocket:` (becomes 🚀) |
| Insert image       | Adds image markdown or upload                    |      `` |
| Formatting help    | Opens Markdown help and shortcuts                |           Link to documentation |

Examples of Markdown the toolbar generates

Bold, italic and strikethrough

```markdown theme={null}
**bold text**
*italic text*
~~strikethrough~~
```

Inline code and a fenced code block

````markdown theme={null}
Here is `inline code`.

```python
def greet(name):
    return f"Hello, {name}!"
```You didn't include any text to analyze. Please paste the code, console output, or plain text you want identified.
````

Lists and task lists

```markdown theme={null}
- Bullet item 1
- Bullet item 2

1. Numbered item 1
2. Numbered item 2

- [ ] Todo item not done
- [x] Todo item done
```

Mentions, references, and emoji

```markdown theme={null}
Thanks @alice — please see #42 for details. :+1:
```

Keyboard shortcuts (commonly supported)

| Action               | Shortcut               |
| -------------------- | ---------------------- |
| Bold                 | Ctrl/Cmd + B           |
| Italic               | Ctrl/Cmd + I           |
| Inline code          | Ctrl/Cmd + \`          |
| Open formatting help | `?` (in some contexts) |

Note: exact shortcuts may vary by operating system and browser. The "Formatting help" link inside the comment editor lists the current shortcuts for your environment.

GitHub-specific behaviors to expect

* Mentions (`@username`) and issue/PR references (`#123`) autocomplete and render as links when posted.
* Fenced code blocks accept a language tag for syntax highlighting, for example ` ```javascript `.
* Task lists render interactive checkboxes in issue and PR conversations (they are clickable when the comment is part of the thread).
* Emoji shortcodes (e.g., `:rocket:`) convert to their emoji glyphs in the rendered comment.
* The toolbar is helpful for users unfamiliar with Markdown, but composing directly in Markdown remains faster once you know the syntax.

<Callout icon="lightbulb">
  Prefer keyboard-only editing? Learn a few Markdown basics and the keyboard shortcuts to compose rich comments faster than relying purely on mouse clicks. See the [Markdown help](https://docs.github.com/en/get-started/writing-on-github/basic-writing-and-formatting-syntax) and [keyboard shortcuts](https://docs.github.com/en/get-started/using-github/keyboard-shortcuts).
</Callout>

Links and references

* [GitHub: Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/basic-writing-and-formatting-syntax)
* [GitHub: Keyboard shortcuts](https://docs.github.com/en/get-started/using-github/keyboard-shortcuts)
* [GitHub: Working with mentions and references](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-mentions-and-references)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/42c15655-2217-4c66-8d0a-2472a3b15e43/lesson/bab1376b-51f5-4733-a885-09b5de1cb6e4" />
</CardGroup>
