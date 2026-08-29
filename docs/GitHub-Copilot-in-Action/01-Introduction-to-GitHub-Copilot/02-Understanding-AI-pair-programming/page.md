# print each username
for username in usernames:
    print(username)
```

Run it to verify output:

```bash theme={null}
jeremy@Jeremys-Mac-Studio fakedatagenerator % python3 main.py
Michael
Sanjeev
Jeremy
jeremy@Jeremys-Mac-Studio fakedatagenerator %
```

Copilot speeds up repetitive patterns by completing common idioms like this.

## 5) Gracefully handle missing files with try/except

When interacting with files, Copilot often suggests handling `FileNotFoundError` explicitly. Example:

```python theme={null}
try:
    with open("data.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    data = "No data available"

print(data)
```

If you prefer broader error coverage, Copilot can also suggest a general exception handler:

```python theme={null}
try:
    with open("data.txt", "r") as f:
        data = f.read()
except Exception as e:
    print(e)
    data = "default data"

print(data)
```

Recommendation: choose the more specific exception when you know which errors to expect; use general handlers only when necessary.

## 6) Using requests and fixing an AttributeError

If you import `requests` but forget to install it, your editor may offer a quick fix to install the package. Example pip installation:

```bash theme={null}
(venv) jeremy@Jeremys-Mac-Studio fakedatagenerator % pip install requests
Collecting requests
  Downloading requests-2.32.3-py3-none-any.whl (64 kB)
Installing collected packages: requests
Successfully installed requests-2.32.3
(venv) jeremy@Jeremys-Mac-Studio fakedatagenerator %
```

A common mistake is calling a non-existent method (e.g., `requests.test`), which raises an AttributeError:

```python theme={null}
import requests

response = requests.test("https://api.github.com")  # incorrect
print(response.status_code)
```

Traceback example:

```bash theme={null}
(venv) jeremy@Jeremys-Mac-Studio fakedatagenerator % python3 main.py
Traceback (most recent call last):
  File "/Users/jeremy/Projects/fakedatagenerator/main.py", line 3, in <module>
    response = requests.test("https://api.github.com")
                   ^^^^^^^^^^^
AttributeError: module 'requests' has no attribute 'test'
(venv) jeremy@Jeremys-Mac-Studio fakedatagenerator %
```

Copilot typically suggests replacing the incorrect call with `requests.get` and adding a safe network exception handler:

```python theme={null}
import requests

try:
    response = requests.get("https://api.github.com")
    print(response.status_code)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
```

This both corrects the method and adds robust handling for network-related errors.

<Frame>
  <img alt="Screenshot of a GitHub Copilot menu overlaid on a code editor, with &#x22;Status: Ready&#x22; highlighted and a hand cursor pointing at &#x22;GitHub Copilot Chat.&#x22; The menu shows options like Open Completion Panel, Disable Completions, Edit Settings, and View Copilot Documentation." />
</Frame>

## 7) Using Copilot Chat to diagnose issues

Open Copilot Chat, paste the error message and the relevant code, and Copilot Chat will usually return a diagnosis and suggested edits. When applying suggestions, you typically have three options:

* Apply in Editor — Copilot modifies the file directly.
* Insert at Cursor — Copilot inserts the suggestion at the current cursor location.
* Copy — copy the suggestion and paste it manually.

> **warning** Be cautious when using "Apply in Editor" — in some cases Copilot may change more than you expect. Review diffs before accepting changes.

For the `requests.test` error above, Copilot Chat commonly suggests switching to `requests.get` and wrapping the call in a `try/except` for `requests.exceptions.RequestException`, as shown earlier.

## Reference table: patterns and Copilot behavior

| Pattern                    | What Copilot suggests                              | Example                                                          |
| -------------------------- | -------------------------------------------------- | ---------------------------------------------------------------- |
| Boilerplate / entry point  | Complete `main()` and `if __name__ == "__main__":` | `def main(): ...`                                                |
| Docstring + type hints     | Implementation inferred from description           | `def factorial(n: int) -> int:`                                  |
| Collection transformations | Full list comprehension or generator               | `usernames = [user["name"] for user in users]`                   |
| File handling              | Specific exceptions like `FileNotFoundError`       | `except FileNotFoundError:`                                      |
| Network calls              | Correct HTTP method + `requests` exceptions        | `requests.get(...); except requests.exceptions.RequestException` |

## Summary

* GitHub Copilot quickly completes common code patterns (Hello World, factorial, comprehensions).
* Docstrings and clear type hints improve suggestion accuracy.
* Copilot recommends specific exceptions (e.g., `FileNotFoundError`) and practical error-handling idioms.
* Use Copilot Chat for diagnosing runtime errors, but always review suggested edits before applying them.
* When an edit is overly broad, copy and paste the suggested change manually to retain control.

By practicing with small examples like these, you'll learn how Copilot streamlines repetitive tasks and helps diagnose issues without relinquishing control of your code.

## Links and further reading

* [GitHub Copilot docs](https://docs.github.com/en/copilot)
* [Copilot Chat docs](https://docs.github.com/en/copilot/copilot-chat)
* [Python requests](https://docs.python-requests.org/en/latest/)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/fb848134-d908-42a6-b195-1ea9c9cd1ffe/lesson/73b6deac-6b87-4d73-9321-85cf364cb833)


# Understanding AI pair programming

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-in-Action/Introduction-to-GitHub-Copilot/Understanding-AI-pair-programming/page

Explains AI pair programming with GitHub Copilot, its benefits, workflow changes, use cases, risks, and best practices for combining AI suggestions with human oversight.

Welcome. In this lesson we explore an important evolution in software development: AI pair programming with [GitHub Copilot](https://github.com/features/copilot). This approach combines human creativity and judgment with AI assistance to boost productivity, reduce repetitive work, and keep learning inside the editor.

What you’ll learn:

* What pair programming is and how AI pair programming differs
* The benefits of GitHub Copilot
* How developer workflows change before and after Copilot
* Best practices: when to use Copilot and when to exercise caution

<Frame>
  <img alt="A presentation agenda slide showing four numbered items about pair programming and AI (introduction, comparison with traditional pair programming, benefits with Copilot, and workflow transformation). A dark left column displays the word &#x22;Agenda&#x22; with blue numbered markers next to each item." />
</Frame>

## What is pair programming?

Pair programming is a collaborative development practice where two people work together at the same workstation:

* Driver: writes the code
* Navigator: reviews the code, thinks ahead, spots edge cases, and suggests improvements

This model provides immediate feedback, encourages knowledge transfer, and often improves design decisions.

## What is AI pair programming?

AI pair programming replaces—or augments—the human navigator with an AI partner. GitHub Copilot provides context-aware, inline suggestions based on the file you’re editing, the surrounding project, and patterns learned from large public codebases. Key differences from human partners:

* Available 24/7
* Scales across teams without scheduling
* Produces suggestions but does not make final decisions—you accept, modify, or reject outputs

<Frame>
  <img alt="A presentation slide titled &#x22;AI Pair Programming&#x22; showing the GitHub Copilot mascot on the left and three feature highlights on the right. The highlights state real-time code suggestions, learning your coding style and patterns, and 24/7 availability that scales across teams." />
</Frame>

## Traditional vs AI pair programming — a comparison

Traditional pair programming and AI pair programming share the same goals (knowledge sharing, immediate feedback, error catching) but achieve them differently.

| Focus             | Traditional Pair Programming               | AI Pair Programming (Copilot)                    |
| ----------------- | ------------------------------------------ | ------------------------------------------------ |
| Feedback model    | Human-driven, conversational               | Automated, inline suggestions                    |
| Availability      | Dependent on people and schedules          | Always available in the editor                   |
| Knowledge sources | Individual experience and team knowledge   | Large public codebases + project context         |
| Best for          | Deep architectural decisions, mentorship   | Repetitive tasks, scaffolding, quick prototyping |
| Control           | Human decides architecture and correctness | Human reviews and accepts AI suggestions         |

Benefits of combining both:

* Humans: creativity, intuition, architectural reasoning, mentorship
* Copilot: fast access to patterns, consistent style, scaffolded tests and docs, faster prototyping

## How workflows change

### Before Copilot

Typical pre-Copilot workflow:

* Write code
* Consult documentation
* Search Stack Overflow or examples
* Review, refactor, and test

These steps introduce context switches that slow iteration.

<Frame>
  <img alt="A slide titled &#x22;Workflow: Before Copilot&#x22; showing a simple flowchart: write code, then check documentation, then search Stack Overflow. The steps are displayed as connected rounded rectangles on a pale background." />
</Frame>

### After Copilot

Copilot moves learning and discovery into the editor:

* You write code and receive inline suggestions in real time
* Accept, modify, or reject suggestions instantly
* Contextual documentation and examples appear without leaving the editor
* AI can assist with quick reviews, refactors, and test generation

This reduces context switching and shortens iteration cycles.

<Frame>
  <img alt="A slide showing a flowchart titled &#x22;Workflow: After Copilot&#x22; with steps: &#x22;Write code + Receive suggestions&#x22; → &#x22;Accept/Modify/Reject in real time&#x22; → &#x22;Documentation appears as you code&#x22; → &#x22;Review and refactor with AI assistance.&#x22; The left side has a dark panel with the heading &#x22;Workflow: After Copilot.&#x22;" />
</Frame>

## Practical use cases: when Copilot excels

Copilot is particularly effective for tasks that are routine, pattern-based, or require fast scaffolding:

| Use Case                        | Why Copilot helps                                       |
| ------------------------------- | ------------------------------------------------------- |
| Repetitive tasks & boilerplate  | Generates standard code quickly                         |
| Common API integration patterns | Suggests idiomatic examples based on project context    |
| Test generation & scaffolding   | Creates unit tests and test harnesses faster            |
| Documentation & README content  | Produces structured docs from code/comments             |
| Converting comments to code     | Transforms natural-language intent into implementations |

<Frame>
  <img alt="A presentation slide titled &#x22;When to Use Copilot&#x22; showing five colored panels that list use cases: repetitive tasks and boilerplate code, API integration patterns, test case generation, documentation writing, and converting comments to code. Each panel includes an icon and a number (01–05)." />
</Frame>

## When to be cautious — human oversight needed

There are scenarios where AI suggestions require careful review and expert validation:

| Risk Area                       | Why human review is essential                              |
| ------------------------------- | ---------------------------------------------------------- |
| Security-critical code          | Vulnerabilities and threat modeling need expert assessment |
| Complex domain-specific logic   | Domain knowledge and business rules may be missed          |
| Performance-critical sections   | Profiling and low-level optimizations require experience   |
| Licensed/proprietary algorithms | Licensing, IP, and copyright concerns must be evaluated    |

<Frame>
  <img alt="A presentation slide titled &#x22;When to Be Cautious&#x22; showing four colorful circular icons labeled: Security-critical code, Complex business logic, Performance-critical sections, and Licensed/Proprietary algorithms. The icons sit above a dark band across the bottom of the slide." />
</Frame>

> **warning** Always review AI-generated code for correctness, security, licensing, and performance. Copilot helps accelerate work, but does not replace expert validation.

## Best practices for adopting Copilot

* Start small: try Copilot on low-risk tasks such as boilerplate, tests, and docs.
* Learn from suggestions: use prompts and edits as a way to discover APIs and idioms.
* Establish team norms: share examples and review AI output as a team to standardize usage.
* Iterate and measure: adjust how you use Copilot over time and measure outcomes (e.g., time saved, defect rates).
* Keep responsibility clear: humans remain accountable for architecture, security, and legal compliance.

> **lightbulb** Treat Copilot as a force multiplier: it speeds routine work and surfaces possibilities, while humans retain responsibility for design, security, and correctness.

## Conclusion — AI + Human collaboration

GitHub Copilot is a powerful assistant that complements developer expertise. When used thoughtfully, AI pair programming:

* Accelerates routine work and scaffolding
* Keeps learning and discovery inside the editor
* Improves consistency and speed of prototyping

But it is not a replacement for human judgment on architecture, security, performance, or licensing. Adopt Copilot incrementally, validate outputs, and combine AI assistance with code review and expert oversight to get the best results.

<Frame>
  <img alt="A presentation slide titled &#x22;Conclusion&#x22; showing five numbered takeaways about AI pair programming. The points include: AI pair programming is a tool not a replacement, start small and expand, learn from suggestions, share experiences, and keep experimenting." />
</Frame>

## Links and references

* [GitHub Copilot](https://github.com/features/copilot) — product page and documentation
* [Stack Overflow](https://stackoverflow.com) — community Q\&A and examples

Further reading:

* [GitHub Copilot docs](https://docs.github.com/en/copilot)
* [Responsible AI guidelines](https://www.microsoft.com/en-us/ai/responsible-ai)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-copilot-in-action/module/fb848134-d908-42a6-b195-1ea9c9cd1ffe/lesson/d8ebd8eb-6d55-4c72-9974-4f447b238780)
