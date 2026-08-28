# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

## Text and Line Breaks

Write paragraphs by separating text with blank lines. To force a line break within a paragraph, end a line with two spaces:

```markdown theme={null}
This is a paragraph describing how Markdown  
handles line breaks.

This is another paragraph.
```

## Emphasis and Lists

You can emphasize text and create different kinds of lists:

### Emphasis Types

| Style         | Syntax              | Rendered Output   |
| ------------- | ------------------- | ----------------- |
| Bold          | `**bold text**`     | **bold text**     |
| Italic        | `*italic text*`     | *italic text*     |
| Bold + Italic | `***bold italic***` | ***bold italic*** |

### Unordered Lists

Start lines with `-`, `*`, or `+`:

```markdown theme={null}
- Item 1
- Item 2
  - Nested item
```

### Ordered Lists

Use numbers followed by a period:

```markdown theme={null}
1. First item
2. Second item
```

### Task Lists (Checkboxes)

Great for tracking progress:

```markdown theme={null}
- [ ] Task not completed
- [x] Task completed
```

## Code Formatting

### Inline Code

Wrap code snippets in single backticks:

Use `inline code` to highlight commands or file names.

### Code Blocks

Fenced code blocks support syntax highlighting. Specify the language after the opening backticks:

<Callout icon="lightbulb">
  Always include the language identifier (e.g., `javascript`, `python`) for better readability.
</Callout>

```javascript theme={null}
console.log("Hello, world!");
```

```python theme={null}
print("Hello, world!")
```

## Links and Blockquotes

### Links

Create hyperlinks with the format `[link text](URL)`:

```markdown theme={null}
[Visit GitHub](https://github.com)
```

### Blockquotes

Use the greater-than sign (`>`) for quotations:

```markdown theme={null}
> This is a blockquote.
> It can span multiple lines.
```

***

Now that you’ve mastered Markdown basics, you’re ready to write clear, SEO-friendly documentation for your projects.

## Links and References

* [GitHub Markdown Guide](https://guides.github.com/features/mastering-markdown/)
* [CommonMark Spec](https://spec.commonmark.org/)
* [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/open-source-for-beginners/module/767d06e2-2c02-403c-aa37-6e4a5549e6a6/lesson/48c8da8d-edee-4c5b-afeb-fcc37a9a4256" />
</CardGroup>


# Documentation

Source: https://notes.kodekloud.com/docs/Open-Source-for-Beginners/Starting-Your-Open-Source-Project/Documentation/page

This article discusses best practices for creating clear and accessible documentation in open source projects to enhance collaboration and maintainability.

Open source success isn’t just about the code—it’s also built on clear, accessible documentation. Well-written docs:

* Empower maintainers to evolve the codebase over time
* Foster collaboration among contributors
* Serve as a centralized knowledge base for users and stakeholders

Documentation spans every phase of a project, from planning and design to user stories and final releases. While every project is unique, the community has standardized a few key files and conventions to help newcomers get started quickly.

## Why Clear Documentation Matters

| Benefit         | Description                                     | Example                             |
| --------------- | ----------------------------------------------- | ----------------------------------- |
| Maintainability | Easier code evolution and refactoring           | Documentation diagrams, design docs |
| Onboarding      | Faster ramp-up for new contributors             | Step-by-step setup guides           |
| Collaboration   | Central reference for discussions and decisions | Issue templates, meeting notes      |
| Consistency     | Uniform style and structure across the project  | Style guides, naming conventions    |

## Project Description (README.md)

At the entry point of most repositories sits the **README.md**. It typically covers:

* Project overview and goals
* Installation instructions
* Basic usage examples

<Frame>
  ![The image shows a dark interface with a central icon resembling a document and code symbol, accompanied by three buttons labeled "Project Details," "Set Guidelines," and "Core Working." On the left, there are three vertical icons in different colors.](https://kodekloud.com/kk-media/image/upload/v1752882564/notes-assets/images/Open-Source-for-Beginners-Documentation/dark-interface-document-code-icons.jpg)
</Frame>

### README Essentials

1. **Overview:** A concise description of what the project does and who it’s for.
2. **Quick Start:** `git clone`, installation prerequisites, and first steps.
3. **Usage Examples:** Code snippets or CLI examples demonstrating common tasks.

<Callout icon="lightbulb">
  Keep your README updated with each release. Link to deeper guides or reference documentation to avoid bloating the main file.
</Callout>

## Contribution Guidelines (CONTRIBUTING.md)

The **CONTRIBUTING.md** file tells potential contributors how to participate:

* Workflow for submitting pull requests
* Branch naming and commit message conventions
* Testing requirements and code style checks

<Callout icon="lightbulb">
  A clear CONTRIBUTING.md reduces friction and encourages first-time contributors. Include templates for issues and PRs where possible.
</Callout>

## Issue Tracking & Discussions

Most projects manage bugs and feature requests through platforms like [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues) or [GitLab Discussions](https://docs.gitlab.com/ee/user/discussions/). Your documentation should also provide:

* A **Code of Conduct** outlining expected community behavior
* Templates or instructions for creating new issue threads

| Platform           | Use Case                               | Link                                                                                         |
| ------------------ | -------------------------------------- | -------------------------------------------------------------------------------------------- |
| GitHub Issues      | Bug reports, feature requests          | [https://docs.github.com/en/issues](https://docs.github.com/en/issues)                       |
| GitLab Discussions | Community feedback, design discussions | [https://docs.gitlab.com/ee/user/discussions/](https://docs.gitlab.com/ee/user/discussions/) |

<Callout icon="triangle-alert">
  Always include a Code of Conduct and issue templates. This ensures contributors know the process and fosters a welcoming environment.
</Callout>

## Additional Resources

* [Open Source Guides](https://opensource.guide/)
* [Markdown Reference](https://www.markdownguide.org/basic-syntax/)
* [GitHub Docs](https://docs.github.com/)

By adopting these conventions and maintaining clear, structured documentation, you’ll streamline collaboration, improve onboarding, and help your project thrive.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/open-source-for-beginners/module/767d06e2-2c02-403c-aa37-6e4a5549e6a6/lesson/1c672a0a-ce32-452c-ae18-a7b072929c56" />
</CardGroup>
