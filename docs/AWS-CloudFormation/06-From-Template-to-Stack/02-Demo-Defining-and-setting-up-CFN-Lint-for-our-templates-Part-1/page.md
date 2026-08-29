# Demo Defining and setting up CFN Lint for our templates Part 1

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/From-Template-to-Stack/Demo-Defining-and-setting-up-CFN-Lint-for-our-templates-Part-1/page

Guide to install and configure cfn-lint and VS Code extension to lint AWS CloudFormation templates, verify CLI integration, and troubleshoot setup

Welcome — in this lesson we'll install and configure cfn-lint so Visual Studio Code can validate your AWS CloudFormation templates (YAML or JSON). cfn-lint detects syntax errors, invalid resource/property names, deprecated properties, and many best-practice suggestions so you catch problems before deploying stacks.

What you'll accomplish

1. Install the VS Code extension for CloudFormation linting.
2. Install the cfn-lint CLI (required by the extension).
3. Verify linting works from both VS Code and the command line.

Prerequisites

* Visual Studio Code
* Python 3.8+ (for the pip install method) or Homebrew / Docker (optional)
* Basic familiarity with CloudFormation templates

1. Install the CloudFormation Linter extension in VS Code

* Open Visual Studio Code and go to the Extensions view (use the sidebar icon or the three-dot/grid icon if your sidebar is narrow).
* Search for "CFN-Lint" or "CloudFormation Linter".
* Install the extension titled "CloudFormation Linter" (vscode-cfn-lint). When prompted, trust and install the publisher.

After installing the extension you should see it listed in the sidebar.

<Frame>
  <img alt="A screenshot of Visual Studio Code's Extensions view showing the &#x22;CloudFormation Linter&#x22; (vscode-cfn-lint) extension page, with install/disable buttons, ratings, version (v0.26.6) and download info. The left pane shows the extension listed in the sidebar." />
</Frame>

2. Open a template to test the extension
   Open any CloudFormation template (YAML or JSON) in VS Code. Example minimal YAML:

```yaml theme={null}
Resources:
  MyS3Bucket:
    Type: AWS::S3::Bucket
```

If the extension shows a warning or indicates `cfn-lint` is not found, that’s expected until you install the cfn-lint CLI. The VS Code extension uses the cfn-lint executable under the hood to perform checks.

3. Install the cfn-lint CLI
   The extension requires the Python-based cfn-lint executable. Below are common installation methods. Use the method that fits your platform and environment.

Recommended: pip (Python)

```bash theme={null}
