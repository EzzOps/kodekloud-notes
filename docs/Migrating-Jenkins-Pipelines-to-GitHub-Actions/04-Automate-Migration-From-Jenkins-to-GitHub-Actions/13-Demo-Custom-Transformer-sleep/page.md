#  # This item has no matching transformer
# MONGO_DB_CREDS:
#  # This item has no matching transformer
# MONGO_USERNAME:
#  # This item has no matching transformer
# MONGO_PASSWORD:
jobs:
  Installing_Dependencies:
    name: Installing Dependencies
    runs-on:
      - self-hosted
      - us-west-1-ubuntu-22
    container:
      image: node:24
    steps:
      - name: checkout
        uses: actions/checkout@v4.1.0
      - name: sh
        shell: bash
        run: npm install --no-audit
```

Why some env vars were not transformed

* The importer converts SCM polling to a GitHub Actions cron schedule automatically.
* Credential references stored in Jenkins credential stores are typically not transformed by default. Those appear as commented placeholders with the message `# This item has no matching transformer`.
* Use a custom transformer to explicitly map these variables to literals or `secrets`.

Creating a custom transformer to handle environment variables
Create a transformer file (for example `ss-pipeline-transformer.rb`) and use `env` directives to add mappings, mark values as secrets, or remove variables.

Example transformer (Ruby DSL):

```ruby theme={null}
# ss-pipeline-transformer.rb
env "MONGO_USERNAME", "superuser"
env "MONGO_PASSWORD", secret("mongo_db_password")
env "MONGO_DB_CREDS", nil
```

* `secret("mongo_db_password")` indicates the importer should reference the GitHub Actions secret named `mongo_db_password`.
* Setting a variable to `nil` removes it from the generated workflow.

Run dry-run with the custom transformer
Re-run the importer specifying the transformer file:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/ci-pipeline-poll-scm/ \
  --output-dir tmp/dry-run \
  --custom-transformers ss-pipeline-transformer.rb
```

<Callout icon="warning">
  If you see a message such as:

  ```bash theme={null}
  [2025-05-22 12:58:53] No custom transformers found at path: /data/ss-pipeline-transformer.rb
  ```

  it usually means the transformer path is incorrect relative to your current working directory. Verify the file exists (for example `ls ss-pipeline-transformer.rb`) and either run the command from that directory or supply an absolute path to `--custom-transformers`.
</Callout>

Resulting transformed workflow (excerpt)
After applying the custom transformer, the `env` section reflects the mappings and secrets:

```yaml theme={null}
name: ci-pipeline-poll-scm
on:
  push:
    branches:
      - main
  schedule:
    - cron: "0 0 * * *"
env:
  MONGO_URI: mongodb+srv://supercluster.d83jj.mongodb.net/superData
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: "${{ secrets.mongo_db_password }}"
jobs:
  Installing_Dependencies:
    name: Installing Dependencies
    runs-on:
      - self-hosted
      - us-west-1-ubuntu-22
    container:
      image: node:14
    ...
```

Best practices and tips

<Callout icon="lightbulb">
  * Keep transformer files in your project repository and reference them with a relative or absolute path to avoid "not found" errors.
  * Prefer mapping credentials to GitHub Actions secrets rather than hard-coding sensitive values.
  * Use regular expressions cautiously to avoid accidentally removing environment variables you need.
</Callout>

Summary

* Use `env "NAME", "value"` to map literals, `env "NAME", secret("KEY")` to map to GitHub Actions secrets, and `env "NAME", nil` to remove variables from the generated workflow.
* If the importer cannot find your custom transformer, verify the path and working directory or use an absolute path.
* This article focuses on env var transformation; other Jenkins-specific constructs (e.g., complex credential bindings or specialized plugins) may require additional custom handling and are covered separately.

Links and references

* [GitHub Actions: Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
* [gh actions-importer — CLI repository / documentation](/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/migrating-jenkins-pipelines-to-github-actions/module/3b5e500f-482a-4860-9f2c-d5f9fbc95159/lesson/d9e086da-5595-4bd8-9f86-767774b8eb56" />
</CardGroup>


# Demo Custom Transformer sleep

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Custom-Transformer-sleep/page

Guide to build a Ruby custom transformer that converts Jenkins sleep steps into GitHub Actions sleep steps, extracting the time value and testing via gh actions-importer dry-run and migrate

In this lesson you'll create a custom transformer that converts a Jenkins `sleep` step into an equivalent GitHub Actions step. Instead of leaving the `sleep` step commented out in the generated workflow, the transformer will produce a step like:

```yaml theme={null}
- name: Sleep for 5 seconds
  run: sleep 5s
```

This guide walks through inspecting the Jenkins pipeline JSON, writing a helper transformer to verify the structure, and implementing the final transformer in Ruby. It also shows how to run `gh actions-importer` with your custom transformer for `dry-run` and `migrate`.

## Problem overview

When the importer doesn't have a built-in transformer for an identifier like `sleep`, it reports:

* "failed to locate transformer" for `sleep`
* the step is left commented out in the generated workflow

Example of a generated workflow where `sleep` was previously commented out:

```yaml theme={null}
name: Second Stage
runs-on: ubuntu-latest
needs: First_Stage
steps:
  - name: checkout
    uses: actions/checkout@v4.1.0
  - name: echo message
    run: echo Starting the second stage...
