# Mitigating Script Injection Attack

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Security-Guide/Mitigating-Script-Injection-Attack/page

This guide shows how to mitigate script injection attacks in GitHub Actions workflows by using environment variables for untrusted input.

Script injection occurs when untrusted input is interpolated directly into shell commands, allowing attackers to execute arbitrary code. In GitHub Actions workflows, inline shell scripts are especially susceptible if values like issue titles or user inputs are expanded before execution. This guide shows how to move untrusted data into environment variables, ensuring it’s parsed at runtime rather than baked into your script.

## Insecure Example

> **triangle-alert** Interpolating untrusted input inside the `run` block lets attackers inject arbitrary commands.\
  Never build shell scripts by concatenating or expanding variables directly in the script body.

```yaml theme={null}
name: Label Issues (Script Injection)

on:
  issues:
    types: [opened]

jobs:
  assign-label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4.1.1
      - name: Add a Label
        env:
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Unsafe: github.event.issue.title is expanded into the script
          issue_title="{{ github.event.issue.title }}"
          if [[ "$issue_title" == *"bug"* ]]; then
            echo "Issue is about a bug!"
            echo "Assigning Label - BUG.........."
          else
            echo "Not a bug"
          fi
```

## Secure Approach

By passing untrusted input via the `env` block, the value is provided to the shell at execution time rather than expanded when the workflow is generated.

> **lightbulb** Defining `issue_title` as an environment variable prevents any injected payload from being interpreted as part of the script.\
  The shell will see it only as data.

```yaml theme={null}
name: Label Issues (Script Injection)

on:
  issues:
    types: [opened]

jobs:
  assign-label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4.1.1

      - name: Add a Label
        env:
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          issue_title: '${{ github.event.issue.title }}'
        run: |
          # Safe: issue_title is injected at runtime
          if [[ "$issue_title" == *"bug"* ]]; then
            echo "Issue is about a bug!"
            echo "Assigning Label - BUG .................."
          else
            echo "Not a bug"
          fi
```

## Insecure vs. Secure Comparison

| Aspect             | Insecure Workflow                                | Secure Workflow                                  |
| ------------------ | ------------------------------------------------ | ------------------------------------------------ |
| Expansion point    | Inline script (`run` block)                      | Environment variable (`env` block)               |
| Vulnerability      | Shell interprets injected characters as commands | Shell treats the entire value as a string        |
| Example assignment | `issue_title="{{ github.event.issue.title }}"`   | `issue_title: '${{ github.event.issue.title }}'` |

## Demonstration of Attack Mitigation

Simulate an issue title containing a malicious payload:

```yaml theme={null}
