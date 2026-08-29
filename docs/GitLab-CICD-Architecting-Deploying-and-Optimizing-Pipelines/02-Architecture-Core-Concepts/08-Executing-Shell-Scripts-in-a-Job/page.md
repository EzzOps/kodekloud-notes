# Executing Shell Scripts in a Job

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Architecture-Core-Concepts/Executing-Shell-Scripts-in-a-Job/page

Streamline GitLab CI/CD pipelines by using standalone shell scripts for improved readability, maintainability, and version control of build logic.

Streamline your GitLab CI/CD pipelines by extracting complex commands into standalone shell scripts. This approach improves readability, maintainability, and version control for your build logic.

## 1. Example Inline Job

Below is a simple `.gitlab-ci.yml` that installs the `cowsay` gem and runs commands directly:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

ascii_job:
  before_script:
    - gem install cowsay
  script:
    - echo "Generating ASCII Artwork using COWSAY Program"
    - cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt
    - grep -i "dragon" dragon.txt
    - cat dragon.txt
  after_script:
    - echo "Executed at the end, can be used for cleaning/removing content"
```

While this works, embedding multiple commands can quickly clutter your CI file.

> **lightbulb** Extract repetitive or lengthy command sequences into versioned scripts to keep your pipeline definitions clean and reusable.

## 2. Create a Dedicated Shell Script

1. Open the **GitLab Web IDE**.
2. Add a file named `ascii-script.sh` at your repository root:

```bash theme={null}
#!/bin/sh
echo "Generating ASCII Artwork using COWSAY Program"
cowsay -f dragon "Run for cover, I am a DRAGON....RAWR" >> dragon.txt
grep -i "dragon" dragon.txt
cat dragon.txt
ls -ltr
```

![The image shows the GitLab Web IDE interface with a welcome screen and options for connecting to a remote development environment. The left sidebar displays a file explorer with a project structure.](https://kodekloud.com/kk-media/image/upload/v1752876983/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Executing-Shell-Scripts-in-a-Job/gitlab-web-ide-welcome-screen.jpg)

Save and commit `ascii-script.sh` so it’s tracked by Git.

## 3. Update Your CI Configuration

Modify `.gitlab-ci.yml` to invoke the script instead of inline commands:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

ascii_job:
  before_script:
    - gem install cowsay
  script:
    - ./ascii-script.sh
  after_script:
    - echo "Executed at the end, can be used for cleaning/removing content"
```

Commit and push your changes. The pipeline will now call the external script.

## 4. Monitor Pipeline Status

Navigate to **CI/CD > Pipelines** in the GitLab UI to view your job status in real time.

![The image shows a GitLab interface displaying a list of CI/CD pipelines with their statuses, such as "Running," "Passed," "Failed," and "Canceled." The sidebar includes navigation options like "Issues," "Merge requests," and "Pipelines."](https://kodekloud.com/kk-media/image/upload/v1752876984/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Executing-Shell-Scripts-in-a-Job/gitlab-cicd-pipelines-status-interface.jpg)

You should see the `ascii_job` running under the “Generate ASCII Artwork” pipeline.

## 5. Handling Permission Errors

If your script isn’t executable, GitLab will report a permission denied error:

![The image shows a GitLab pipeline interface with a failed job named "ascii\_job" under the "Generate ASCII Artwork" project. The pipeline was created for a specific commit and has options to retry or delete.](https://kodekloud.com/kk-media/image/upload/v1752876985/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Executing-Shell-Scripts-in-a-Job/gitlab-pipeline-failed-job-ascii.jpg)

```bash theme={null}
$ gem install cowsay
Successfully installed cowsay-0.3.0
1 gem installed
$ ./ascii-script.sh
/usr/bin/bash: ./ascii-script.sh: Permission denied
ERROR: Job failed: exit code 1
```

> **triangle-alert** Always ensure your shell scripts have execute permissions. Without `chmod +x`, GitLab runners cannot run them.

## 6. Grant Execute Permissions

Add a `chmod` step in `before_script` to make the script executable:

```yaml theme={null}
workflow:
  name: Generate ASCII Artwork

ascii_job:
  before_script:
    - gem install cowsay
    - chmod +x ascii-script.sh
  script:
    - ./ascii-script.sh
  after_script:
    - echo "Executed at the end, can be used for cleaning/removing content"
```

Commit and push. The next pipeline run will apply the new permissions automatically.

## 7. Confirm Successful Execution

Once fixed, your job logs should show:

```bash theme={null}
$ chmod +x ascii-script.sh
$ ./ascii-script.sh
Generating ASCII Artwork using COWSAY Program
 |  Run for cover, I am a DRAGON....RAWR  |
total 32
-rwxrwxr-x 1 root root     185 Jan 25 19:32 ascii-script.sh
-rw-rw-r-- 1 root root    6181 Jan 25 19:32 README.md
-rw-rw-r-- 1 root root     270 Jan 25 19:32 .gitlab-ci.yml
-rw-r--r-- 1 root root     948 Jan 25 19:32 dragon.txt
Running after_script
Job succeeded
```

With this pattern, your `.gitlab-ci.yml` stays concise, and complex logic lives in maintainable, version-controlled scripts.

***

## Links and References

* [GitLab CI/CD pipelines](https://docs.gitlab.com/ee/ci/pipelines/)
* [GitLab Web IDE](https://docs.gitlab.com/ee/user/project/web_ide/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/fbf7cb8d-dcca-444e-a547-7bdb8b725634/lesson/eaa88615-2605-4fd3-9017-6c884918e492)
