# only show IP address if it is not 192.168.1.1
```

After accepting the suggestion, the loop becomes:

```python theme={null}
for row in csv_reader:
    user_id, first_name, last_name, email, gender, ip_address = row

    # only show IP address if it is not 192.168.1.1
    if ip_address != '192.168.1.1':
        print(ip_address)

    print(f"Processing user {first_name} {last_name}")
```

Re-run the script to verify the change.

***

## 4. When to Use Each Mode

| Mode               | Shortcut             | Best For                                    |
| ------------------ | -------------------- | ------------------------------------------- |
| Generate New Code  | Command K / Ctrl + K | Creating new functions or large code blocks |
| Inline Chat        | Command L / Ctrl + L | Wrapping, refactoring, or multi-line edits  |
| Quick Inline Edits | Comments + Tab       | Small, one-line improvements                |

<Callout icon="triangle-alert">
  Avoid overusing auto-generated code without review—always test and validate generated snippets.
</Callout>

***

## 5. Controlling Context Scope

* **Inline Comments & Command K**\
  Scope is limited to the open file and surrounding lines.
* **Command L (Chat)**\
  Can reference the full project, additional files, or external sources (when enabled).

***

Intelligent code suggestions from **Cursor AI** can dramatically accelerate Python development by handling boilerplate and routine edits. Next, we’ll build a full project from scratch using these tools!

## Links and References

* [Cursor AI Official Site](https://cursor.so/)
* [Python `csv` Module](https://docs.python.org/3/library/csv.html)
* [Python Documentation](https://docs.python.org/3/)
* [Cursor AI Keyboard Shortcuts](/docs/shortcuts)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cursor-ai/module/e11e1c1e-9b6b-4c53-b14a-24babbd114a5/lesson/5cedd606-2303-420b-a7a6-374f28cbba56" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Cursor-AI/Mastering-Autocompletion/Introduction/page

Learn how to enhance your VS Code experience with Cursor's AI-driven autocompletion for efficient coding and real-time assistance.

Elevate your VS Code development experience with Cursor’s AI-driven autocompletion. In this lesson, you’ll discover how Cursor seamlessly integrates into your IDE, offering context-aware suggestions and interactive assistance to help you code more efficiently.

Throughout this tutorial, we’ll cover:

| Feature                      | Description                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| Intelligent Code Suggestions | Context-aware snippets and completions to speed up your workflow  |
| Composer Integration         | Quick setup and in-depth configuration options for AI completions |
| Automatic Imports            | Automatically insert missing imports as you code                  |
| Prompt Engineering           | Best practices to craft precise AI prompts                        |
| Ask Mode                     | On-demand, interactive AI chat for real-time guidance             |

By the end of this lesson, you’ll be able to:

* Configure Cursor Composer and tailor its settings
* Leverage automatic imports to maintain clean code
* Apply prompt engineering techniques for optimal suggestions
* Use Ask Mode to troubleshoot and refine your code

<Callout icon="lightbulb">
  Make sure you’re running VS Code version 1.60 or higher to ensure full compatibility with Cursor’s latest extensions.
</Callout>

***

## 1. Intelligent Code Suggestions

Cursor analyzes your open files and project context to provide accurate, relevant completions. As you type, Cursor offers:

* Real-time autocompletion for functions, classes, and variables
* Inline documentation and type hints
* Adaptive learning based on your coding patterns

```javascript theme={null}
// Example: Efficient React component skeleton
import React from 'react';

const MyComponent = ({ title, items }) => {
  return (
    <div>
      <h1>{title}</h1>
      <ul>
        {items.map((item) => (
          <li key={item.id}>{item.label}</li>
        ))}
      </ul>
    </div>
  );
};

export default MyComponent;
```

***

## 2. Getting Started with Composer

Composer is Cursor’s configuration hub, where you can:

1. Install the Cursor extension from the [Visual Studio Marketplace](https://marketplace.visualstudio.com/)
2. Open the Composer panel (`View > Command Palette > Cursor: Open Composer`)
3. Adjust settings such as model selection, response length, and suggestion triggers

<Callout icon="triangle-alert">
  Certain corporate firewalls may block AI model API requests. Ensure your network allows outbound HTTPS traffic to `api.cursor.dev`.
</Callout>

***

## 3. Automatic Imports & Customizable Settings

Cursor can detect missing imports and insert them automatically:

```python theme={null}
