# Demo Summary

Source: https://notes.kodekloud.com/docs/Cline/Core-Workflows-Prompt-Engineering/Demo-Summary/page

Practical prompt engineering and repository context management, using project ignore files to trim irrelevant files, reduce token usage, and improve LLM prompt relevance and performance.

This lesson covered practical prompt engineering techniques with a focus on context management and reducing noisy repository context to improve model outputs and token efficiency. Key takeaways:

* Prompt anatomy, context management, and practical checkpoints.
* How context window limits and prompt specificity affect results.
* How a project-level ignore file for Cline can trim irrelevant files, reduce token usage, and improve prompt relevance.

## Why an ignore file matters

A Cline project-level ignore file tells Cline which files and directories to exclude when analyzing your repository. Excluding large or irrelevant files (for example, `node_modules/`) prevents overloading the context you send with prompts. Benefits include:

* Lower token usage and cost when submitting context to a model.
* More focused analysis on the application code you care about.
* Faster scans and fewer false positives from generated or binary files.

### Quick strategy

* Exclude generated artifacts, dependency folders, large binary/data files, and local environment files.
* Keep source code, config, and migration/schema files if you want Cline to inspect them.
* Update the ignore file as the project evolves.

## Example: ignoring node modules

This is the standard way to tell Cline to ignore dependency folders:

```text theme={null}
