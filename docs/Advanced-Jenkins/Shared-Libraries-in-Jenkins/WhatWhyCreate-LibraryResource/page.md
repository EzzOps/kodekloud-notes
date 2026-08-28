# WhatWhyCreate LibraryResource

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Shared-Libraries-in-Jenkins/WhatWhyCreate-LibraryResource/page

Explains using Jenkins Shared Library libraryResource to load a parameterized Trivy shell script, write and execute it from pipelines via a loader and Groovy wrapper.

What are `libraryResource`s?

`libraryResource` is a Jenkins Shared Library helper that loads non-Groovy static assets (for example, shell scripts, YAML, JSON) stored under a `resources` directory of the shared library. It returns the file contents as a string so your pipeline or library code can read those assets at runtime.

In this lesson we’ll demonstrate a real use case: packaging a parameterized Trivy scan script in the shared library and using `libraryResource` to persist and execute it from a pipeline.

## Problem statement

In our shared library we had a `trivyScan.groovy` method that hard-coded multiple [Trivy image](https://github.com/aquasecurity/trivy) commands for different severities and exit codes. That looked like this:

```groovy theme={null}
def vulnerability(String imageName) {
    sh """
        echo image - ${imageName}

        trivy image ${imageName} \
          --severity LOW,MEDIUM,HIGH \
          --exit-code 0 \
          --quiet \
          --format json -o trivy-image-MEDIUM-results.json

        trivy image ${imageName} \
          --severity CRITICAL \
          --exit-code 1 \
          --quiet \
          --format json -o trivy-image-CRITICAL-results.json
    """
}
```

Hard-coding every combination of severity and exit behavior makes maintenance difficult when requirements change. We want a reusable approach where pipeline authors can supply the image name, severity, and exit code at invocation time.

## Solution overview

1. Add a parameterized shell script to `resources/scripts/trivy.sh` inside the shared library.
2. Implement a small loader library (`loadScript`) that uses `libraryResource` to read the resource, writes it into the workspace, and sets executable permissions.
3. Add a Groovy wrapper (`trivyScanScript.groovy`) that calls the loader and executes the script with flexible parameters supplied via a `Map` (`config`).

This pattern keeps the script editable without changing compiled Groovy code and enables pipeline authors to control behavior via simple config.

## Create the parameterized shell script

Save this file at `resources/scripts/trivy.sh` in the shared library repository:

```bash theme={null}
#!/bin/bash

echo "imageName - $1"
echo "severity - $2"
echo "exitCode - $3"

trivy image "$1" \
  --severity "$2" \
  --exit-code "$3" \
  --format json -o "trivy-image-$2-results.json"
```

Notes about the script:

* It accepts three positional arguments: image name, severity, and exit code.
* The output filename is based on the severity so results for different severity scans are separated (e.g., `trivy-image-CRITICAL-results.json`).

## Loader library: `loadScript.groovy`

Create a loader in `vars/loadScript.groovy` that retrieves the script from `resources` using `libraryResource`, writes it to the workspace, and marks it executable:

```groovy theme={null}
def call(Map config = [:]) {
    def scriptData = libraryResource "scripts/${config.name}"
    writeFile file: "${config.name}", text: scriptData
    sh "chmod +x ./${config.name}"
}
```

Important:

* `libraryResource "scripts/${config.name}"` reads the file stored at `resources/scripts/${config.name}` in the shared library and returns its contents as a `String`.
* `writeFile` persists that string into the pipeline workspace; `chmod +x` makes the file executable so it can be run with `sh`.

<Callout icon="lightbulb">
  `libraryResource` loads the resource as a string. To execute a shell script you must write it to the workspace (e.g., using `writeFile`) and set executable permissions before running it.
</Callout>

## Trivy wrapper: `trivyScanScript.groovy`

Add a wrapper in `vars/trivyScanScript.groovy` that uses the loader and executes the script. Using a `Map` parameter lets callers pass named arguments rather than positional ones:

```groovy theme={null}
def vulnerability(Map config = [:]) {
    // config.name -> name of the script in resources/scripts, e.g. 'trivy.sh'
    // config.imageName, config.severity, config.exitCode -> arguments to the script

    loadScript(name: 'trivy.sh')
    sh "./trivy.sh ${config.imageName} ${config.severity} ${config.exitCode}"
}
```

Why use a `Map`?

* A `Map` (`config`) provides flexible key/value arguments so pipeline authors pass only the values they need and the wrapper can validate or apply defaults.
* Defaulting to `[:]` prevents null/argument errors if the caller omits the map; you can add validation and defaulting logic inside `vulnerability` as needed.

## How it works end-to-end

1. From your Jenkinsfile or another library caller you invoke `trivyScanScript.vulnerability(config)` with a `Map` (keys: `name`, `imageName`, `severity`, `exitCode`).
2. `trivyScanScript.vulnerability` calls `loadScript(name: 'trivy.sh')`.
3. `loadScript` uses `libraryResource "scripts/trivy.sh"` to fetch the script content as a string.
4. `loadScript` writes the script content into the workspace as `trivy.sh` and changes permissions to executable.
5. `vulnerability` runs `./trivy.sh` with the supplied arguments; the shell script executes `trivy image` with those parameters and writes a JSON report.

## Recap — roles of each file

| File path                     | Purpose                                                                      | Example / Notes                                                     |
| ----------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `resources/scripts/trivy.sh`  | Parameterized shell script stored in the shared library resources            | Accepts `imageName`, `severity`, `exitCode` as positional arguments |
| `vars/loadScript.groovy`      | Generic loader that reads a resource and writes it to the workspace          | Uses `libraryResource`, `writeFile`, and `sh chmod +x`              |
| `vars/trivyScanScript.groovy` | Groovy wrapper to call the loader and execute the script with a `Map` config | Provides a friendly API for pipeline authors                        |

## Example invocation from a Jenkinsfile

```groovy theme={null}
// Example usage in a Jenkinsfile
trivyScanScript.vulnerability(
  name: 'trivy.sh',
  imageName: 'myregistry/myimage:latest',
  severity: 'CRITICAL',
  exitCode: 1
)
```

This approach separates scan logic (in a shell script) from pipeline orchestration (Groovy wrapper), making maintenance and updates easier while letting pipelines control behavior through a simple configuration map.

## Appendix — reference snippets & links

* Jenkins Shared Library docs: [Jenkins Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
* Trivy project: [Aqua Security — Trivy](https://github.com/aquasecurity/trivy)

Example from the Jenkins docs showing `libraryResource` usage:

```groovy theme={null}
// Example: load resource into a variable (string)
def request = libraryResource 'com/mycorp/pipeline/somelib/request.json'
```

Use these references to extend the loader pattern for other static assets (YAML templates, JSON configs, helper scripts) that should live in your shared library’s `resources` directory.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/7e7be52f-69f5-496b-8a46-322d6b8df0ce/lesson/dd173275-f464-4683-8c25-25d686512181" />
</CardGroup>
