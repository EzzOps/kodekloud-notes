# or, if `python` points to Python 3:
# python read_members.py
```

This prints the first and last names from members.csv.

## Summary — Checklist

* Install Node.js 18+ (npm included)
* Install the Claude Code CLI globally:
  * npm install -g @anthropic-ai/claude-code
* Run the CLI: cloud
* Authenticate via Claude subscription or Anthropic Console (browser or copy-paste URL)
* Review generated code before running it
* Optionally integrate with Visual Studio Code for an in-IDE experience

## Links and references

* [Anthropic Console](https://console.anthropic.com)
* [Mockaroo — generate fake data](https://mockaroo.com)
* [Visual Studio Code](https://code.visualstudio.com)
* [Node.js downloads](https://nodejs.org)
* [Claude Code security docs](https://docs.anthropic.com/s/claude-code-security)

Now that your environment is set up, try asking Claude Code to inspect files, refactor code, generate tests, or create shell commands to streamline your workflow.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/0bd6d2b4-0fbf-4c4d-a348-af6c3321121c/lesson/88172a44-0447-4f86-b656-aecdb2786404)


# Demo Start Your First Session

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Introduction/Demo-Start-Your-First-Session/page

A demo showing how Claude Code initializes a repository, generates CLAUDE.md, and scaffolds a production-ready Python package from a simple CSV reader script with tests, tooling, and CI

All right — let's walk through starting your first Claude Code session, analyzing a repository, and scaffold­ing a production-ready Python package from a simple script.

<Frame>
  <img alt="A minimalist presentation slide that says &#x22;Start your First Session&#x22; on the left and a large &#x22;Demo&#x22; on a dark curved shape at right. A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left corner." />
</Frame>

Quick practical tips for a productive first session:

* Run `/init` to generate a CLAUDE.md file that guides Claude Code for repository-specific actions.
* Use Claude Code to analyze files, suggest edits, run bash commands, and help with git workflows.
* Be explicit in prompts — include expected behavior, sample inputs/outputs, and any constraints to get precise results.

> **lightbulb** Be explicit as you would be with another developer — include expected behavior, example inputs/outputs, constraints, and any style or tooling preferences (e.g., black, mypy).

## Example repository: simple CSV reader

The demo repository starts as a single-file Python script that reads member names from a CSV. It demonstrates basic error handling and flexible header parsing.

```python theme={null}
