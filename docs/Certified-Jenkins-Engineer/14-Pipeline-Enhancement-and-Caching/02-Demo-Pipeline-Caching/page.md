# up-to-date (restored from cache)
```

### Cache Invalidation Details

```text theme={null}
17:06:30 cacheValidityDecidingFile(s) - actual file(s): /var/lib/jenkins/workspace/solar-system_feature_advanced-demo/package-lock.json
17:06:30 hash does not match - cache outdated
17:06:32 Creating cache...
17:06:32 got hash 5a1549c4b8a6882fddf4b8ef16c2 for cacheValidityDecidingFile
17:06:32 Cache created in 2179ms
```

![The image shows a console output from a Jenkins job, displaying logs related to caching and package installation processes. The word "cache" is highlighted multiple times throughout the text.](https://kodekloud.com/kk-media/image/upload/v1752870963/notes-assets/images/Certified-Jenkins-Engineer-Demo-Invalidate-Cache/jenkins-job-logs-cache-installation.jpg)

## 3. Cache Behavior Comparison

| Scenario                      | Cache Restored  | Action Taken                |
| ----------------------------- | --------------- | --------------------------- |
| `package-lock.json` unchanged | Yes (cache hit) | Skip install, restore cache |
| `package-lock.json` modified  | No (cache miss) | Reinstall & stash new cache |

## Conclusion

By configuring the Job Cache Plugin’s `cacheValidityDecidingFile` to point at `package-lock.json`, Jenkins automatically invalidates the cache whenever your dependencies change. This ensures that you always rebuild on the latest set of packages, while still benefiting from caching on subsequent runs.

## Links and References

* [Jenkins Job Cache Plugin](https://plugins.jenkins.io/job-cache/)
* [npm Documentation](https://docs.npmjs.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/49e48191-1afc-42bf-9ce5-b98f35b6a2fb/lesson/d728184e-6dd0-40b1-b396-3c4b00e33f18)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/49e48191-1afc-42bf-9ce5-b98f35b6a2fb/lesson/e7e56af6-d0f9-49e3-bc34-6649f60274b2)


# Demo Pipeline Caching

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Pipeline-Enhancement-and-Caching/Demo-Pipeline-Caching/page

This article explains how to use the Job Cacher plugin in Jenkins to cache dependencies and speed up CI build times.

Efficient dependency caching in a Jenkins Pipeline can dramatically reduce CI build times by reusing artifacts and installed modules across runs. In this guide, we’ll walk through installing and configuring the **Job Cacher** plugin to cache `node_modules` for an `npm`-based project.

## Why Cache Dependencies in Jenkins?

* Avoid repeated `npm install` on every build
* Save minutes or even hours for large dependency sets
* Ensure consistent environments by locking on `package-lock.json`

> **lightbulb** Caching works best when build agents start from a clean state (e.g., containers). The Job Cacher plugin handles archiving and restoring cache transparently.

***

## 1. Install the Job Cacher Plugin

1. Navigate to **Manage Jenkins › Manage Plugins › Available**.
2. Search for **Job Cacher** and install.

![The image shows a Jenkins interface displaying the "Available plugins" section, with the "Job Cacher" plugin selected for installation.](https://kodekloud.com/kk-media/image/upload/v1752870964/notes-assets/images/Certified-Jenkins-Engineer-Demo-Pipeline-Caching/jenkins-available-plugins-job-cacher.jpg)

3. After installation, perform a **Safe Restart** to activate the plugin:

![The image shows a Jenkins restart notification with a message indicating that the browser will reload automatically when Jenkins is ready. There is also an option for a "Safe Restart."](https://kodekloud.com/kk-media/image/upload/v1752870965/notes-assets/images/Certified-Jenkins-Engineer-Demo-Pipeline-Caching/jenkins-restart-notification-safe-restart.jpg)

***

## 2. Configure Cache via Snippet Generator

Open your Pipeline job configuration and click **Snippet Generator**. From the **Sample Step** dropdown, select **cache: Caches files from previous build to current build**.

| Field                        | Example Value          |
| ---------------------------- | ---------------------- |
| Cache name                   | `npm-dependency-cache` |
| Path                         | `node_modules`         |
| Includes                     | `**/*`                 |
| Excludes                     | (leave empty)          |
| Cache validity deciding file | `package-lock.json`    |
| Compression                  | `tar` or `zip`         |
| Max cache size (MB)          | `550`                  |

![The image shows a Jenkins interface with the "Snippet Generator" tool open, displaying options for generating pipeline scripts. A dropdown menu lists various sample steps, with "cache: Caches files from previous build to current build" selected.](https://kodekloud.com/kk-media/image/upload/v1752870966/notes-assets/images/Certified-Jenkins-Engineer-Demo-Pipeline-Caching/jenkins-snippet-generator-pipeline-scripts.jpg)

Click **Generate Pipeline Script** to preview the snippet:

![The image shows a Jenkins Pipeline Syntax configuration screen with options for includes, excludes, cache settings, and compression method. The "Generate Pipeline Script" button is visible at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752870967/notes-assets/images/Certified-Jenkins-Engineer-Demo-Pipeline-Caching/jenkins-pipeline-syntax-configuration.jpg)

```groovy theme={null}
cache(caches: [
    arbitraryFileCache(
        cacheName: 'npm-dependency-cache',
        cacheValidityDecidingFile: 'package-lock.json',
        includes: '**/*',
        excludes: '',
        path: 'node_modules'
    )
], defaultBranch: '', maxCacheSize: 550) {
    // your build steps here
}
```

### Advanced Settings

For additional tuning—such as custom includes/excludes or compression—you can tweak the advanced fields:

![The image shows a Jenkins Pipeline Syntax configuration screen with settings for caching, including fields for cache name, includes, excludes, and compression method.](https://kodekloud.com/kk-media/image/upload/v1752870968/notes-assets/images/Certified-Jenkins-Engineer-Demo-Pipeline-Caching/jenkins-pipeline-syntax-caching-settings.jpg)

***

## 3. Update Your Jenkinsfile

Embed the generated cache block in your `Jenkinsfile` to wrap the **Installing Dependencies** stage. Then use `stash` and `unstash` to share the cached folder across parallel and subsequent stages.

```groovy theme={null}
pipeline {
    agent any
    options { timestamps() }
    stages {
        stage('Installing Dependencies') {
            steps {
                cache(
                    maxCacheSize: 550,
                    caches: [
                        arbitraryFileCache(
                            cacheName: 'npm-dependency-cache',
                            cacheValidityDecidingFile: 'package-lock.json',
                            includes: ['**/*'],
                            path: 'node_modules'
                        )
                    ]
                ) {
                    sh 'node -v'
                    sh 'npm install --no-audit'
                    stash includes: 'node_modules/', name: 'solar-system-node-modules'
                }
            }
        }

        stage('Dependency Scanning') {
            steps {
                // security scan, linting, etc.
            }
        }

        stage('Unit Testing') {
            parallel {
                stage('NodeJS 18') {
                    options { retry(2) }
                    steps {
                        unstash 'solar-system-node-modules'
                        sh 'node -v'
                        sh 'npm test'
                    }
                }
                stage('NodeJS 19') {
                    options { retry(2) }
                    steps {
                        container('node-19') {
                            unstash 'solar-system-node-modules'
                            sh 'node -v'
                            sh 'npm test'
                        }
                    }
                }
            }
        }

        stage('Code Coverage') {
            steps {
                catchError(buildResult: 'SUCCESS', message: 'Coverage will be addressed later') {
                    unstash 'solar-system-node-modules'
                    sh 'node -v'
                    sh 'npm run coverage'
                }
            }
        }
    }
}
```

> **triangle-alert** Always commit your `package-lock.json` to source control. The cache validity hinges on this file’s checksum to detect changes.

***

## 4. Observe the First Build: Cache Miss

When you run the pipeline the first time, Jenkins will not find an existing cache, execute `npm install`, then create and store a new cache.

```bash theme={null}
Searching cache in job-specific caches...
Skip restoring cache as no up-to-date cache exists
+ node -v
v22.6.0
+ npm install --no-audit
up to date in 1s
Stashed 4993 file(s)
Creating cache...
got a47b9ef602dbc79d72ab6385105e0142 for cacheValidityDecidingFile(s)
cache created in 164ms
```

***

## 5. Subsequent Build: Cache Hit

On the next build, the plugin will detect that `package-lock.json` is unchanged, restore the `node_modules` folder, and skip reinstalling.

```bash theme={null}
Searching cache in job-specific caches...
Found cache for npm-dependency-cache with id 3ec03583f8eaec275cb2183db769ff47
Restoring cache...
+ npm install --no-audit
up to date in 1s
Stashed 4993 file(s)
Skip cache creation as the cache is up-to-date
```

***

## 6. Visualizing the Pipeline

Here’s a classic Jenkins Blue Ocean (or classic) view showing stages from **Installing Dependencies** through **Code Coverage**:

![The image shows a Jenkins dashboard displaying a pipeline for a project named "feature/advanced-demo," with various stages like "Checkout SCM," "Tool Install," and "Code Coverage." The pipeline includes multiple builds with their statuses indicated by checkmarks and warnings.](https://kodekloud.com/kk-media/image/upload/v1752870969/notes-assets/images/Certified-Jenkins-Engineer-Demo-Pipeline-Caching/jenkins-dashboard-pipeline-feature-advanced-demo.jpg)

***

By integrating Job Cacher into your Jenkins Pipeline, you’ll eliminate redundant dependency installs and accelerate your CI process. Next, try modifying `package-lock.json` to see cache invalidation in action!

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/49e48191-1afc-42bf-9ce5-b98f35b6a2fb/lesson/8bd40d19-3836-484c-97ec-516bde205634)
