# Demo Perform Dry run Migration of a Jenkins Job 2

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Automate-Migration-From-Jenkins-to-GitHub-Actions/Demo-Perform-Dry-run-Migration-of-a-Jenkins-Job-2/page

Demonstrates dry-run migration of a Jenkins Pipeline to GitHub Actions using gh actions-importer, showing converted workflows, placeholders for unsupported steps, and guidance on custom transformers and full migration.

This lesson demonstrates a dry-run migration of a Jenkins Pipeline job to GitHub Actions. It continues from the dry-run and production migration concepts typically used for Jenkins Freestyle projects and shows how the `gh actions-importer` tool translates pipeline stages and steps into a GitHub Actions workflow file.

<Frame>
  <img alt="A presentation slide with the title &#x22;Perform Dry-run Migration of a Jenkins Job - 2&#x22; centered on a blue-green gradient background. The bottom-left corner shows &#x22;© Copyright KodeKloud.&#x22;" />
</Frame>

## Source Jenkins Pipeline (pipeline portion of config.xml)

For this demo we used the Pipeline Project 2 located under `Folder One → Folder Two`. Below is the pipeline stage structure (scripted/declarative) from the job's `config.xml`:

```groovy theme={null}
stages {
    stage('First Stage') {
        steps {
            echo 'Starting the first stage...'
            sleep 5
            echo 'First stage completed.'
        }
    }

    stage('Second Stage') {
        steps {
            echo 'Starting the second stage...'
            sleep 2
            echo 'Second stage completed.'
        }
    }
}
```

## Dry-run vs Migrate

* Dry-run: translates and writes workflow files locally without modifying the target repository or creating pull requests.
* Migrate: performs a full migration and can push changes to a target repo or open PRs.

Use the `gh actions-importer` subcommands for both operations.

## Example: Full migration command

```bash theme={null}
gh actions-importer migrate jenkins \
  --target-url https://github.com/:owner/:repo \
  --output-dir tmp/migrate \
  --source-url my-jenkins-project
```

Replace `:owner` and `:repo` with your GitHub organization/user and repository.

## Example: Dry-run command used in this lesson

This dry-run writes translated workflows to `tmp/dry-run` without pushing anything:

```bash theme={null}
gh actions-importer dry-run jenkins \
  --source-url http://139.84.149.83:8080/job/folder-1/job/folder-2/job/pipeline-project-2 \
  --output-dir tmp/dry-run
```

## Actual dry-run invocation (console output)

The demo's console output shows the dry-run invocation and the generated output path:

```bash theme={null}
root@jenkins in /home
