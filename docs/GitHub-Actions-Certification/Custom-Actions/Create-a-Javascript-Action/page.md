# Install HTTP client and JSON parser
RUN apk update && apk add --no-cache curl jq

# Copy and set entrypoint script permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

***

## 7. Entrypoint Script

The `entrypoint.sh` script orchestrates:

1. Reading the PR number from the GitHub event payload
2. Fetching a random “thank you” GIF
3. Parsing the GIF URL
4. Posting a comment on the PR

```bash theme={null}
#!/bin/sh

GITHUB_TOKEN=$1
GIPHY_API_KEY=$2

# Get PR number
pr_number=$(jq --raw-output .pull_request.number "$GITHUB_EVENT_PATH")
echo "PR Number: $pr_number"

# Fetch GIF from Giphy
giphy_response=$(curl -s \
  "https://api.giphy.com/v1/gifs/random?api_key=$GIPHY_API_KEY&tag=thank%20you&rating=g")
echo "Giphy Response: $giphy_response"

# Extract GIF URL
gif_url=$(echo "$giphy_response" | jq --raw-output .data.images.downsized.url)
echo "GIF URL: $gif_url"

# Post comment
response=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{\"body\": \"Thank you for your contribution! 🎉\n![GIF]($gif_url)\"}" \
  "https://api.github.com/repos/$GITHUB_REPOSITORY/issues/$pr_number/comments")
echo "Comment posted: $(echo "$response" | jq --raw-output .html_url)"
```

***

## 8. Action Metadata (`action.yml`)

Define inputs and Docker run settings:

```yaml theme={null}
name: 'Giphy PR Comment'
description: 'Automatically add a thank-you Giphy GIF to pull requests.'
inputs:
  github-token:
    description: 'Token for GitHub API authentication'
    required: true
  giphy-api-key:
    description: 'Secret key for Giphy API'
    required: true
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.github-token }}
    - ${{ inputs.giphy-api-key }}
```

***

## 9. Test Workflow Setup

Configure `.github/workflows/test.yml` to trigger on PR opens:

```yaml theme={null}
on:
  pull_request:
    types: [opened]

jobs:
  test-giphy-action:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Invoke Giphy PR Comment Action
        uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          giphy-api-key: ${{ secrets.GIPHY_API_KEY }}
```

***

## 10. Opening a Pull Request

Make a small update (e.g., edit `README.md`) in a feature branch to trigger the workflow:

<Frame>
  ![The image shows a GitHub repository interface where a user is editing the README.md file in a project named "docker-action-pr-giphy-comment."](https://kodekloud.com/kk-media/image/upload/v1752876042/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-repo-edit-readme-docker-action.jpg)
</Frame>

Create and submit the PR:

<Frame>
  ![The image shows a GitHub pull request page for updating a README.md file. It indicates that some checks are pending, and the branch has no conflicts with the base branch.](https://kodekloud.com/kk-media/image/upload/v1752876043/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-pull-request-readme-update.jpg)
</Frame>

***

## 11. Verifying the Workflow

Monitor the Action run under **Actions**. A successful run indicates:

<Frame>
  ![The image shows a GitHub Actions interface with a successful workflow run named "testing-action," detailing steps like setting up a job, checking out a repository, and posting a PR comment.](https://kodekloud.com/kk-media/image/upload/v1752876044/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-actions-successful-workflow-testing-action.jpg)
</Frame>

View detailed logs for build and script outputs:

<Frame>
  ![The image shows a GitHub Actions interface with a successful workflow run for "testing-action," displaying job setup details and steps like "Checkout Repository" and "Post PR Comment."](https://kodekloud.com/kk-media/image/upload/v1752876045/notes-assets/images/GitHub-Actions-Certification-Create-a-Docker-Action/github-actions-successful-workflow-testing-action-2.jpg)
</Frame>

***

## 12. Reviewing the Bot Comment

Your PR will now contain an automated comment with a thank-you message and a Giphy GIF. 🎉

***

## 13. Links and References

* [Giphy Random GIF Endpoint](https://developers.giphy.com/docs/api/endpoint#random)
* [GitHub Create an Issue Comment API](https://docs.github.com/rest/issues/comments#create-an-issue-comment)
* [jq Manual](https://stedolan.github.io/jq/)
* [GitHub Actions](https://docs.github.com/actions)

Congratulations! You have built a reusable Docker Action that integrates external APIs to enhance your pull request workflow. Consider publishing this action to the [GitHub Marketplace](https://docs.github.com/actions/creating-actions/publishing-actions-in-github-marketplace) next.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/428391ee-45d0-4e9c-9e06-78d0c5ff7657/lesson/6a13e90c-0182-4cdf-963b-fe5f7186b59b" />
</CardGroup>


# Create a Javascript Action

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Custom-Actions/Create-a-Javascript-Action/page

This tutorial guides you in building a JavaScript GitHub Action that posts a random thank you GIF from Giphy for new pull requests.

In this tutorial, you’ll build a JavaScript GitHub Action that posts a random “thank you” GIF from Giphy whenever a new pull request is opened. We’ll cover project setup, metadata definition, coding, bundling dependencies, and publishing to your GitHub repository.

<Frame>
  ![The image shows a GitHub documentation page titled "Creating a JavaScript action," which provides a guide on building a JavaScript action using the actions toolkit. The page includes an introduction and a sidebar with related topics.](https://kodekloud.com/kk-media/image/upload/v1752876046/notes-assets/images/GitHub-Actions-Certification-Create-a-Javascript-Action/github-documentation-javascript-action-guide.jpg)
</Frame>

## Prerequisites

Before you begin, verify that you have the following:

| Requirement    | Description                             |
| -------------- | --------------------------------------- |
| Node.js 20.x   | JavaScript runtime for your action      |
| npm            | Package manager to install dependencies |
| GitHub account | Host your repository and run workflows  |

<Frame>
  ![The image shows a GitHub documentation page about creating a JavaScript action, including prerequisites like downloading Node.js and creating a GitHub repository.](https://kodekloud.com/kk-media/image/upload/v1752876046/notes-assets/images/GitHub-Actions-Certification-Create-a-Javascript-Action/github-js-action-creation-guide.jpg)
</Frame>

## 1. Project Setup

Create a fresh directory and initialize npm. This scaffolds your package and creates essential files:

```bash theme={null}
mkdir js-action-pr-giphy-comment
cd js-action-pr-giphy-comment
npm init -y
touch README.md action.yml index.js
```

## 2. Define Action Metadata

The `action.yml` file tells GitHub how to run your action. Specify inputs and the entrypoint:

```yaml theme={null}
name: 'Giphy PR Comment'
description: 'Posts a Giphy GIF comment on new pull requests.'
inputs:
  github-token:
    description: 'GitHub token for authentication'
    required: true
  giphy-api-key:
    description: 'Your Giphy API key'
    required: true
runs:
  using: 'node20'
  main: 'dist/index.js'
```

<Callout icon="lightbulb">
  The `github-token` input is usually provided via `${{ secrets.GITHUB_TOKEN }}`.\
  Be sure to store your `giphy-api-key` in GitHub Secrets to keep it secure.
</Callout>

## 3. Install Dependencies

Install the GitHub Actions Toolkit and Giphy client:

```bash theme={null}
npm install @actions/core@1.10.0 \
            @actions/github@5.1.1 \
            @octokit/rest@20.0.1 \
            giphy-api@2.0.2
```

Here’s a quick reference of what each package does:

| Package         | Version | Purpose                                          |
| --------------- | ------- | ------------------------------------------------ |
| @actions/core   | ^1.10.0 | Read inputs, set outputs, and report failures    |
| @actions/github | ^5.1.1  | Access GitHub context and helpers                |
| @octokit/rest   | ^20.0.1 | Interact with the GitHub REST API                |
| giphy-api       | ^2.0.2  | Fetch random or search-based GIFs from Giphy API |

Check your `package.json` to confirm these are listed under `dependencies`.

## 4. Write the Action Code

In `index.js`, import the necessary modules, fetch a random “thank you” GIF, and post it as a comment on the pull request:

```javascript theme={null}
const core = require('@actions/core');
const github = require('@actions/github');
const { Octokit } = require('@octokit/rest');
const Giphy = require('giphy-api');

async function run() {
  try {
    const githubToken = core.getInput('github-token');
    const giphyApiKey = core.getInput('giphy-api-key');
    const octokit = new Octokit({ auth: githubToken });
    const giphy = Giphy(giphyApiKey);

    const { owner, repo, number: issue_number } = github.context.issue;
    const prComment = await giphy.random('thank you');

    await octokit.issues.createComment({
      owner,
      repo,
      issue_number,
      body: [
        '### 🎉 Thank you for your contribution!',
        '',
        `![Giphy](${prComment.data.images.downsized.url})`
      ].join('\n')
    });

    core.setOutput('comment-url', prComment.data.images.downsized.url);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
```

<Frame>
  ![The image shows a GitHub repository page for "docker-action-pr-giphy-comment," displaying files like Dockerfile, README.md, and action.yml, along with recent commit activity.](https://kodekloud.com/kk-media/image/upload/v1752876047/notes-assets/images/GitHub-Actions-Certification-Create-a-Javascript-Action/github-repo-docker-action-pr-giphy.jpg)
</Frame>

## 5. Bundle with ncc

To avoid committing `node_modules`, bundle your code and dependencies into a single file using [Vercel ncc][ncc]:

```bash theme={null}
npm install --save-dev @vercel/ncc@0.38.0
npx ncc build index.js -o dist
```

<Callout icon="lightbulb">
  `ncc` produces `dist/index.js` with your action logic and all dependencies. This simplifies deployment.
</Callout>

## 6. Ignore Unnecessary Files

Add a `.gitignore` to keep your repository clean:

```plaintext theme={null}
node_modules
dist/**/*.map
```

## 7. Publish to GitHub

Initialize and push your project:

```bash theme={null}
git init
git add .
git commit -m "Initial JavaScript action"
git branch -M main
git remote add origin https://github.com/<your-username>/js-action-pr-giphy-comment.git
git push -u origin main
```

<Frame>
  ![The image shows a GitHub interface for creating a new repository, with fields for the repository name, description, visibility options, and initialization settings.](https://kodekloud.com/kk-media/image/upload/v1752876048/notes-assets/images/GitHub-Actions-Certification-Create-a-Javascript-Action/github-new-repository-interface.jpg)
</Frame>

After pushing, your repository will look like this:

<Frame>
  ![The image shows a GitHub repository page titled "js-action-pr-giphy-comment," displaying files like .gitignore, README.md, and index.js. The repository is public with no stars or forks.](https://kodekloud.com/kk-media/image/upload/v1752876050/notes-assets/images/GitHub-Actions-Certification-Create-a-Javascript-Action/github-repo-js-action-giphy-comment.jpg)
</Frame>

***

You’ve now successfully created, bundled, and published a JavaScript GitHub Action. Next, tag a release and submit it to the [GitHub Marketplace][marketplace] so others can use it!

***

## Links and References

* [GitHub Actions Toolkit][toolkit]
* [Vercel ncc – Next.js Compiler][ncc]
* [GitHub Marketplace][marketplace]
* [GitHub Actions Documentation](https://docs.github.com/actions)
* [Giphy Developers](https://developers.giphy.com/)

[toolkit]: https://github.com/actions/toolkit

[ncc]: https://github.com/vercel/ncc

[marketplace]: https://github.com/marketplace/actions

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/428391ee-45d0-4e9c-9e06-78d0c5ff7657/lesson/d577dc08-becc-45c8-ac7b-77d45b70a673" />
</CardGroup>
