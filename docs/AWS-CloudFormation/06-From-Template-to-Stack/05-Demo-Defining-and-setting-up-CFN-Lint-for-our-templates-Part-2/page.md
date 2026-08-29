# Ensure pip is up-to-date
python3 -m pip install --upgrade pip

# Install the core linter
python3 -m pip install cfn-lint

# Optional extras for additional features
python3 -m pip install "cfn-lint[full]"
python3 -m pip install "cfn-lint[graph]"
python3 -m pip install "cfn-lint[junit]"
python3 -m pip install "cfn-lint[sarif]"
```

Alternative: macOS Homebrew

```bash theme={null}
brew install cfn-lint
```

Alternative: Build or run from source with Docker

```bash theme={null}
git clone https://github.com/aws-cloudformation/cfn-lint.git
cd cfn-lint
docker build --tag cfn-lint:latest .
# or use the repository's instructions to run the container directly
```

For detailed platform-specific instructions and the latest release, see the cfn-lint repository on GitHub.

<Frame>
  <img alt="A dark-mode Google search results page in a browser for &#x22;cfn lint github,&#x22; showing GitHub links to aws-cloudformation/cfn-lint and cfn-lint-visual-studio-code. The screenshot also shows browser tabs at the top and a Windows taskbar across the bottom." />
</Frame>

Quick reference: installation options

| Method          | Platform                         | Install command                 | Notes                                                                  |
| --------------- | -------------------------------- | ------------------------------- | ---------------------------------------------------------------------- |
| pip             | Linux / macOS / Windows (Python) | python3 -m pip install cfn-lint | Use extras for full feature set (graph, junit, sarif).                 |
| Homebrew        | macOS                            | brew install cfn-lint           | Simple macOS install; kept up-to-date via brew.                        |
| Docker / Source | Any (with Docker)                | docker build . (from repo)      | Useful in environments where installing Python packages is restricted. |

> **lightbulb** After installing Python and cfn-lint, restart VS Code so the extension can detect the installed cfn-lint executable. If VS Code still cannot find the executable, set the path to the cfn-lint binary in the extension settings or ensure the binary is on your system PATH.

4. Run cfn-lint from the command line
   Once installed, verify the linter from your terminal:

```bash theme={null}
# Lint a single template
cfn-lint template.yaml
```

You will see any warnings or errors with file/line references. Use this output to update your template and re-run the linter.

Troubleshooting tips

* If the extension does not detect the cfn-lint executable:
  * Confirm the CLI runs from your terminal (run `cfn-lint --version`).
  * Ensure the terminal shell used by VS Code has the same PATH as your interactive shell.
  * Configure the extension setting for the cfn-lint executable path if necessary.
* If you need dependency isolation, install cfn-lint in a virtual environment (venv) and point VS Code to that venv’s binary.

Links and references

* cfn-lint GitHub repository: [https://github.com/aws-cloudformation/cfn-lint](https://github.com/aws-cloudformation/cfn-lint)
* VS Code CloudFormation linter extension: search "vscode-cfn-lint" in the Extensions Marketplace
* AWS CloudFormation docs: [https://docs.aws.amazon.com/cloudformation/](https://docs.aws.amazon.com/cloudformation/)

Next steps
In the next demo we'll run cfn-lint against several real templates, interpret common rule violations, and apply fixes to meet best-practice guidance. Follow along and you’ll have a reproducible linting workflow for every CloudFormation template you create.

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/d0ac0bcf-be2c-4c53-a2f7-8f59a760e9de/lesson/e0932d32-0ba5-477a-938c-5a45c9bbd839)


# Demo Defining and setting up CFN Lint for our templates Part 2

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/From-Template-to-Stack/Demo-Defining-and-setting-up-CFN-Lint-for-our-templates-Part-2/page

Guide to installing and using cfn-lint to validate AWS CloudFormation YAML templates, detect common errors like indentation and misspelled keys, and integrate linting into development workflows

This lesson continues the walkthrough for applying cfn-lint to AWS CloudFormation templates. By now you should have Python installed on your machine. We’ll install cfn-lint, run it against a minimal template, and review common errors it detects so you can fix templates before deployment.

## Example minimal CloudFormation template (s3-bucket.yaml)

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
```

## Install cfn-lint

* Open Visual Studio Code and open the integrated terminal (View → Terminal or the toggle panel icon).
* Install cfn-lint using pip:

```bash theme={null}
pip install cfn-lint
```

The installer will fetch cfn-lint and its dependencies; this may take a minute. After installation, restart Visual Studio Code to ensure the editor picks up newly installed tools and any language extensions.

If you need to re-open your project folder in VS Code:

<Frame>
  <img alt="A dark-themed Visual Studio Code window with an &#x22;Open Folder&#x22; dialog open showing a Desktop folder named &#x22;cf-project.&#x22; The Windows taskbar and system tray are visible along the bottom of the screen." />
</Frame>

## Validate a template with cfn-lint

With your S3 template file open (s3-bucket.yaml), run cfn-lint from the terminal:

```powershell theme={null}
cfn-lint s3-bucket.yaml
```

* A successful run produces no error output — cfn-lint returns without printing errors or warnings.
* If it finds issues, cfn-lint prints descriptive error codes and locations so you can quickly correct the template.

## Common errors cfn-lint catches (examples and fixes)

Below are several typical mistakes and how cfn-lint helps identify them.

1. Indentation / YAML structure errors\
   Incorrect YAML indentation can cause the parser to miss required top-level keys such as `Resources`. Example malformed YAML (no indentation):

```yaml theme={null}
Resources:
MyS3Bucket:
Type: AWS::S3::Bucket
```

Running cfn-lint reports schema errors like:

```text theme={null}
E1001 'Resources' is a required property
s3-bucket.yaml:1:1

E3001 None is not of type 'object'
s3-bucket.yaml:1:1

E1001 Additional properties are not allowed ('MyS3Bucket' was unexpected)
s3-bucket.yaml:2:1

E1001 Additional properties are not allowed ('Type' was unexpected)
s3-bucket.yaml:3:1
```

Explanation: Because the nested resource names and Type values are not correctly indented under the `Resources` mapping, the linter interprets them as unexpected top-level properties. Correcting indentation to:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
```

resolves these errors.

2. Simple spelling / key name mistakes\
   Using an incorrect key such as `Resource` (singular) instead of `Resources` (plural) triggers clear messages:

Example incorrect key:

```yaml theme={null}
Resource:
  MyS3Bucket:
    Type: AWS::S3::Bucket
```

cfn-lint output may include:

```text theme={null}
E1001 Additional properties are not allowed ('Resource' was unexpected. Did you mean 'Resources'?)
s3-bucket.yaml:1:1

E1001 'Resources' is a required property
s3-bucket.yaml:1:1
```

Fixing the key to `Resources` and re-running cfn-lint returns no errors:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
```

> **lightbulb** Use cfn-lint on every CloudFormation template you author. It catches YAML formatting issues, schema problems, misspelled keys, and provides actionable error messages so templates are ready for deployment.

## Quick reference — Common lint error types

| Error type                                       | Symptom                                                | Typical fix                                                     |
| ------------------------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------- |
| Schema / required property errors (E1001, E3001) | Missing top-level keys or wrong YAML structure         | Fix YAML indentation and required key names (e.g., `Resources`) |
| Unknown resource property                        | Property name misspelled or not valid for the resource | Correct the property name or consult the resource schema        |
| Type mismatch                                    | Value type not expected (string vs object)             | Provide the correct data type in the template                   |
| Property validation                              | Property value out of allowed set or format            | Adjust value to match the CloudFormation resource specification |

## Best practices

* Run cfn-lint as part of your local development workflow and CI pipelines to catch issues early.
* Combine cfn-lint with template formatting tools (like `prettier` for YAML or an editor extension) to keep templates consistent.
* Refer to the CloudFormation resource specification when a property is unclear.

## Summary

* Install cfn-lint via pip in your development environment.
* Restart VS Code after installation if needed.
* Run cfn-lint against each template (example: `cfn-lint s3-bucket.yaml`).
* Fix indentation, spelling, and schema issues the linter reports.
* Repeat linting until the command completes without errors, indicating the template is valid and ready for CloudFormation.

## Links and References

* [AWS CloudFormation Concepts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* [cfn-lint GitHub Repository](https://github.com/aws-cloudformation/cfn-lint)
* [cfn-lint PyPI Package](https://pypi.org/project/cfn-lint/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/d0ac0bcf-be2c-4c53-a2f7-8f59a760e9de/lesson/d9ff7951-8d05-46a9-a01b-22263b0db9fd)
