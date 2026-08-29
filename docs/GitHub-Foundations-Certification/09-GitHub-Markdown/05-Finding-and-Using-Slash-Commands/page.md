# Finding and Using Slash Commands

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Markdown/Finding-and-Using-Slash-Commands/page

How to use GitHub slash commands to insert Markdown components like code blocks, tables, task lists and templates, with examples and best practices for consistent issue and PR descriptions

Slash commands are quick shortcuts you can type inside any description or comment field on GitHub (issues, pull requests, and discussions) to insert structured Markdown components. They save time, reduce repetitive typing, and help keep comments consistently formatted and readable.

Why use slash commands

* Speed: Insert common Markdown fragments without manually typing the structure.
* Consistency: Enforce a consistent format for code blocks, tables, task lists, and more.
* Readability: Collapse large outputs or hide secondary details for cleaner threads.

Common slash commands and what they produce

| Slash Command    | Purpose                                                                                                               | Example output                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `/code`          | Inserts a Markdown code block and prompts for a language to enable syntax highlighting.                               | See the example code block below.      |
| `/details`       | Creates an expandable (collapsible) details section (HTML `<details>`). Useful for long logs or optional information. | See the details example below.         |
| `/table`         | Generates a Markdown table with a simple visual editor for rows/columns.                                              | See the table example below.           |
| `/saved-replies` | Inserts a pre-written reply from your saved replies for quick reuse.                                                  | N/A (inserts the saved reply content). |
| `/task-list`     | Generates a task-tracking list using GitHub task list syntax (available in issue descriptions only).                  | See the task list example below.       |
| `/template`      | Applies an available issue or pull request template from the repository to the current description.                   | N/A (applies selected template).       |

Code block example inserted by `/code`

````markdown theme={null}
```python
def hello():
    print("Hello, world!")
```text
````

Details (collapsible) example inserted by `/details`

```html theme={null}
<details>
<summary>Click to expand</summary>

Put long output or logs here.

</details>
```

Table example inserted by `/table`

```markdown theme={null}
| Name  | Role     | Status  |
|-------|----------|---------|
| Alice | Engineer | Active  |
| Bob   | Designer | Offline |
```

Task list example inserted by `/task-list`

```markdown theme={null}
- [ ] Design API endpoints
- [ ] Implement handlers
- [ ] Add tests
- [x] Write documentation
```

<Callout icon="lightbulb">
  The `/task-list` shortcut is restricted to the issue description. Use standard Markdown task lists (`- [ ]` / `- [x]`) in other comment fields if needed.
</Callout>

Tips and best practices

* Use `/code` when sharing code snippets to enable proper syntax highlighting (choose the language when prompted).
* Hide large logs or verbose output with `/details` so the main discussion stays focused.
* Use `/table` for data that benefits from a clear, tabular layout—this avoids manual pipe/dash formatting errors.
* Save frequently used replies with GitHub’s saved replies and insert them via `/saved-replies` to maintain a consistent voice across issues and PRs.
* Apply repository templates with `/template` to ensure all required sections are present when filing issues or PRs.

Quick links and references

* GitHub Docs: [https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
* GitHub Markdown guide: [https://docs.github.com/en/get-started/writing-on-github/basic-writing-and-formatting-syntax](https://docs.github.com/en/get-started/writing-on-github/basic-writing-and-formatting-syntax)

By incorporating slash commands into your workflow you can keep issue and PR descriptions concise, readable, and standardized—improving collaboration and the overall quality of your project documentation.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/42c15655-2217-4c66-8d0a-2472a3b15e43/lesson/c6708908-7f38-49b3-ad22-b98163d03113" />
</CardGroup>
