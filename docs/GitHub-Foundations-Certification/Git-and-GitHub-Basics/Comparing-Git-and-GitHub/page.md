# Clone the wiki repository (replace OWNER and REPO with your values)
git clone https://github.com/OWNER/REPO.wiki.git
cd REPO.wiki

# Create or edit pages as Markdown files, then commit and push
git add .
git commit -m "Update wiki pages"
# Push to the wiki repository's default branch (often 'main' or 'master')
git push origin HEAD
```

This workflow lets you use your favorite editor and local tools to manage wiki content.

## Permissions, workflows, and review considerations

* By default, wiki edits are made through the web UI by users with repository access.
* You can restrict editing to collaborators with push access via repository settings.
* Wikis do not use the same pull-request (PR) review model as the main repository. If you require PR-based reviews, CI checks, or stricter versioning for documentation, consider keeping docs in the main repository instead.

## When to use Wiki vs README vs docs/

Use the following guidance to choose the right place for documentation:

| Resource       |                                                                                      Best for | Typical example                                                     |
| -------------- | --------------------------------------------------------------------------------------------: | ------------------------------------------------------------------- |
| README         |                                        Short onboarding, quick start, and high-level overview | `README.md` with quick-start commands and examples                  |
| Wiki           |       Long-form, evolving, page-oriented documentation that benefits from a simple editing UI | How-to guides, architecture overviews, and tutorials                |
| `docs/` folder | Documentation that needs PR reviews, CI integration, or static-site publishing (GitHub Pages) | `docs/` published with a static site generator and reviewed via PRs |

## Links and references

* [GitHub Docs: About wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis)
* [GitHub Docs: Cloning a wiki locally](https://docs.github.com/en/communities/documenting-your-project-with-wikis/creating-and-editing-wiki-pages)
* [GitHub Pages](https://pages.github.com/)

<Callout icon="lightbulb">
  Wikis are great for collaborative, long-form documentation. If you need documentation that must be reviewed via pull requests or integrated with CI, prefer the repository `docs/` directory and GitHub Pages instead.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/276e82b4-df95-4d98-ace5-3bf4e5889b26/lesson/ea2087da-bfe4-4247-8a15-204e71004fd7" />
</CardGroup>


# Comparing Git and GitHub

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Comparing-Git-and-GitHub/page

Explains the difference between Git as a local version control system and GitHub as a cloud platform for collaboration, code review, automation, and security.

What is the difference between Git and GitHub?

Many people use these terms interchangeably, but they serve distinct roles in software development. A helpful analogy: Git is the engine that manages changes; GitHub is the collaborative garage where teams share, review, and automate work.

Git is a distributed version control system you install locally. It records every change to files, enables branching and merging, and lets you work offline. You do the heavy lifting on your machine and push changes to a remote host when ready.

GitHub is a cloud-based platform built on Git. It hosts repositories remotely and adds collaboration, code review, project planning, automation, and security features that go beyond Git alone.

<Frame>
  <img alt="The image illustrates a visual comparison between GitHub as a collaboration platform with features like Pull Requests and GitHub Actions, and Git as an engine with functions such as Command Line, Local Version Control, Tracks History, and Creates Branches." />
</Frame>

What Git provides

* Local version control with a complete history of changes
* Branch creation and merging workflows to develop features independently
* Command-line tools and local workflows that work offline

Common Git commands

```bash theme={null}
