# Create a Docker Action

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Custom-Actions/Create-a-Docker-Action/page

Build a Docker Action that posts Giphy comments on pull requests using the GitHub REST API.

In this tutorial, you’ll build a custom Docker Action that:

1. Triggers when a pull request is opened.
2. Fetches a random “thank you” GIF from Giphy.
3. Posts a comment with the GIF on the PR using the GitHub REST API.

This pattern can be adapted to any third-party API integration.

***

## External APIs

We rely on two REST APIs:

| API                                | Endpoint                                                                                        | Purpose                        |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------ |
| Giphy API                          | `https://api.giphy.com/v1/gifs/random?api_key=YOUR_GIPHY_API_KEY&tag=thank%20you&rating=g`      | Get a random “thank you” GIF   |
| GitHub REST API for Issue Comments | [Create an Issue Comment](https://docs.github.com/rest/issues/comments#create-an-issue-comment) | Post comments on PRs or issues |

### Giphy API: Random GIF Endpoint

Request URL:

```text theme={null}
https://api.giphy.com/v1/gifs/random?api_key=YOUR_GIPHY_API_KEY&tag=thank%20you&rating=g
```

Sample response:

```json theme={null}
{
  "data": {
    "type": "gif",
    "id": "l119IDMNbVskgyf5u",
    "images": {
      "original": { "url": "https://media1.giphy.com/media/l119IDMNbVskgyf5u/giphy.gif" },
      "downsized": { "url": "https://media1.giphy.com/media/l119IDMNbVskgyf5u/200.gif" }
    },
    "title": "sci-fi comedy GIF by Ghosted"
  }
}
```

<Frame>
  ![The image shows the GIPHY Developers API Explorer interface, where users can input sample queries to test the API. It includes options to choose an app/API key, resource, endpoint, and parameters like tag and rating.](https://kodekloud.com/kk-media/image/upload/v1752876566/notes-assets/images/GitHub-Actions-Create-a-Docker-Action/giphy-developers-api-explorer-interface.jpg)
</Frame>

### GitHub REST API: Post a Comment

Use the Issues API to add a comment:

```bash theme={null}
curl -s -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{"body":"![GIF](GIF_URL)\nThank you for this contribution!"}' \
  https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments
```

<Frame>
  ![The image shows a GitHub documentation page for the REST API, specifically focusing on managing issues, with links to various related actions like creating, updating, and locking issues.](https://kodekloud.com/kk-media/image/upload/v1752876567/notes-assets/images/GitHub-Actions-Create-a-Docker-Action/github-rest-api-managing-issues.jpg)
</Frame>

***

## 1. Create the Repository

1. On GitHub, create a new public repo named `docker-action-pr-giphy-comment`.
2. Initialize with a `README.md`.

<Frame>
  ![The image shows a GitHub page for creating a new repository, with fields for the repository name, description, and visibility options.](https://kodekloud.com/kk-media/image/upload/v1752876568/notes-assets/images/GitHub-Actions-Create-a-Docker-Action/github-new-repository-creation-page.jpg)
</Frame>

After creation, you’ll see the default commit:

<Frame>
  ![The image shows a GitHub repository page titled "docker-action-pr-giphy-comment" with an initial commit and a README file. The repository has no stars, forks, or releases.](https://kodekloud.com/kk-media/image/upload/v1752876570/notes-assets/images/GitHub-Actions-Create-a-Docker-Action/github-repo-docker-action-readme.jpg)
</Frame>

### Add Giphy API Key as a Secret

1. Go to **Settings → Secrets and variables → Actions**.
2. Add a new secret `GIPHY_API_KEY` with your Giphy API key.

<Callout icon="lightbulb">
  Keep your secrets safe. Never hard-code API keys in your code or Docker image.
</Callout>

<Frame>
  ![The image shows a GitHub repository settings page where a new secret is being added under "Actions secrets." The secret is named "GIPHY\_API\_KEY."](https://kodekloud.com/kk-media/image/upload/v1752876570/notes-assets/images/GitHub-Actions-Create-a-Docker-Action/github-repo-settings-actions-secret-giphy-api-key.jpg)
</Frame>

Once saved, the secret appears in the list:

<Frame>
  ![The image shows a GitHub repository settings page, specifically the "Secrets and variables" section, with a repository secret named "GIPHY\_API\_KEY" listed.](https://kodekloud.com/kk-media/image/upload/v1752876572/notes-assets/images/GitHub-Actions-Create-a-Docker-Action/github-repo-settings-secrets-giphy-api-key.jpg)
</Frame>

***

## 2. Define the Action Structure

In your repo root, create:

* `Dockerfile`
* `entrypoint.sh`
* `action.yml`

### Dockerfile

```dockerfile theme={null}
FROM alpine:3.10
