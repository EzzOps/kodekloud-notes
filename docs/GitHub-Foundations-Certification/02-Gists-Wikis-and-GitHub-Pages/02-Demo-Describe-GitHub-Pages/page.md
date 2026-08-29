# Clone a gist to your local machine (replace <username> and <gist-id> with actual values)
git clone https://gist.github.com/<username>/<gist-id>.git
```

When to use a Gist

Gists are excellent for focused, small-scale sharing:

<Frame>
  <img alt="The image presents four use cases for a software tool, each with an icon and a brief description: Code Documentation, System Configuration, Diagnostic Logs, and Interactive Feedback." />
</Frame>

| Use case                              | Why a Gist is a good fit                                                     |
| ------------------------------------- | ---------------------------------------------------------------------------- |
| Code examples & snippets              | Quick sharing without creating a full repo; easy to embed in blogs or forums |
| Dotfiles or single config files       | Track changes to a single config file and share across machines              |
| Diagnostic logs / short error outputs | Share trimmed logs for troubleshooting and lightweight peer review           |
| Documentation examples                | Combine Markdown and code to illustrate a single behavior or API usage       |

Limitations and best practices

<Callout icon="warning">
  Never store sensitive data such as API keys, passwords, or tokens in a gist. Secret gists are not secure storage — anyone with the URL can access the content.
</Callout>

<Frame>
  <img alt="The image outlines two limitations: &#x22;Credential Safety,&#x22; advising against storing sensitive data in Gists, and &#x22;Scope Limitation,&#x22; suggesting using repositories for large or complex projects." />
</Frame>

* Credential safety: Do not store secrets or credentials in any gist. Use dedicated secret management (e.g., vaults, environment variables, or GitHub Secrets) for sensitive information.
* Scope limitation: If your work requires multiple directories, complex branching, CI/CD, fine-grained access controls, or extensive collaboration, create a full GitHub repository instead of a Gist.

Quick checklist before creating a Gist

* Is the content small and self-contained? If yes, a Gist is appropriate.
* Will the content contain secrets? If yes, do not use a Gist.
* Do you need CI, multiple branches, or complex permissions? If yes, use a repository.

Further reading and references

* [GitHub Gist documentation](https://docs.github.com/en/get-started/writing-on-github/creating-gists)
* [Embedding gists in web pages](https://docs.github.com/en/get-started/writing-on-github/including-references-to-files-in-your-repository)
* [Managing secrets on GitHub](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

This guide introduced what Gists are, how they differ from full repositories, practical use cases, how to clone and work locally, and the key safety and scope considerations to keep your code sharing secure and effective.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/276e82b4-df95-4d98-ace5-3bf4e5889b26/lesson/5095fd2c-0048-411d-b042-0432d92f3063" />
</CardGroup>


# Demo Describe GitHub Pages

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Gists-Wikis-and-GitHub-Pages/Demo-Describe-GitHub-Pages/page

Guide to publishing a static website with GitHub Pages using a Block Buster game demo

GitHub Pages lets you publish a static website directly from a GitHub repository without needing separate hosting. If your repo contains standard web assets such as `index.html`, `style.css`, and `script.js`, GitHub Pages can serve them so visitors can open a URL and run your site or web app in any browser.

In this repository, `index.html`, `style.css`, and `script.js` combine to make the Block Buster game playable in the browser without downloading files.

<Frame>
  <img alt="The image shows a GitHub repository page for a project called &#x22;block-buster,&#x22; which is an enhanced version of the Block Buster Brick Breaker game. The project includes several files such as .gitignore, README.md, index.html, script.js, and style.css." />
</Frame>

## How to enable GitHub Pages for your repository

Follow these steps to publish the repository as a static site:

1. Open the repository on GitHub and select **Settings**.
2. In the left sidebar, choose **Pages** under the “Code and automation” section.
3. Under **Build and deployment**, choose a source for your site:
   * Deploy from a branch — quick and simple for static project pages.
   * Use GitHub Actions — useful when you need a build pipeline (for example, bundling, minification, or static site generators).
4. If you choose **Deploy from a branch**, select the branch (e.g., `main`) and pick the folder to publish:
   * Root (`/`) — use when `index.html` is in the repository root.
   * `/docs` — use if you maintain site files inside a `docs` directory.
5. Save your settings. GitHub Pages will start building the site; this can take a few minutes.

<Frame>
  <img alt="The image shows the GitHub Pages settings interface, where options for build and deployment using branches or GitHub Actions are available. It includes sections for access, code automation, and security features related to a GitHub repository." />
</Frame>

### Quick reference: source options

| Source option       | When to use it                                        | Notes                                                |
| ------------------- | ----------------------------------------------------- | ---------------------------------------------------- |
| `Branch > root (/)` | Simple sites where `index.html` is at repository root | Recommended for single-page projects and small demos |
| `Branch > /docs`    | Repo contains docs or site assets under `docs/`       | Keeps site files separate from repo root             |
| `GitHub Actions`    | Use a build step (e.g., Jekyll, Hugo, Webpack)        | Provides CI/CD control and custom build steps        |

## Accessing your published site

After a successful build, GitHub Pages supplies the public URL for your site. For project pages the URL format is:

```text theme={null}
https://<username>.github.io/<repository-name>/
```

Example:

```text theme={null}
https://sid-dh900.github.io/blog-post-course/
```

Copy the provided URL from the Pages settings and open it in a browser tab. If the build is still running, wait a few minutes and refresh the page. If you see a 404, double-check that `index.html` is in the selected publish folder (`/` or `/docs`) and that the build completed successfully.

<Callout icon="lightbulb">
  Ensure `index.html` exists in the folder you selected to publish (root or `docs`). Without a valid `index.html`, GitHub Pages has no default file to serve and the site will return a 404.
</Callout>

A few minutes after enabling Pages and once the build finishes, the Block Buster game in this repo is served publicly and can be played directly from the GitHub Pages URL.

<Frame>
  <img alt="The image shows the start screen of a web-based game called &#x22;Block Buster,&#x22; featuring options to start the game or reset the score, with various game attributes like dynamic brick breaker and power-ups listed." />
</Frame>

Anyone with the URL can open and play the game in their browser.

<Frame>
  <img alt="The image shows a browser-based game called &#x22;Block Buster,&#x22; which includes colorful blocks and a ball that the player controls to break them. The game interface displays scores, lives, bricks, and balls, along with options to pause or exit the game." />
</Frame>

## Additional configuration and troubleshooting

* Custom domain: Configure a custom domain from the Pages settings if you own a domain. GitHub provides DNS instructions and will create a `CNAME` file for you.
* Themes: For content sites, you can apply a theme (Jekyll themes are available) via the repository settings or a static site generator.
* Common issues:
  * 404 after build: Verify `index.html` location and successful build logs.
  * Changes not visible: Clear browser cache or force-refresh (Ctrl/⌘+Shift+R).
  * HTTPS not enabled: Pages provides HTTPS by default; verify the certificate is active in Pages settings.

## Links and references

* [GitHub Pages documentation](https://docs.github.com/en/pages)
* [GitHub Actions documentation](https://docs.github.com/en/actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/276e82b4-df95-4d98-ace5-3bf4e5889b26/lesson/42562a8d-5de0-41fb-ac65-21b358be5c34" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/276e82b4-df95-4d98-ace5-3bf4e5889b26/lesson/cac3eb8d-a7c8-4b08-b8da-012516646b2c" />
</CardGroup>
