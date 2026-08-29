# GitHub Wiki Pages

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Gists-Wikis-and-GitHub-Pages/GitHub-Wiki-Pages/page

Guide to using GitHub repository wikis, covering enabling, editing, cloning, permissions, and when to use wikis versus README or docs for project documentation.

GitHub repositories can include a dedicated wiki for hosting long-form project documentation. While the repository README gives a quick start and overview, the wiki is ideal for detailed guides such as user manuals, architecture notes, and project philosophies. The screenshot below shows a sample repository wiki page with sidebar navigation.

<Frame>
  <img alt="The image shows a webpage titled &#x22;Wiki&#x22; used for project documentation, with a depiction of the solar system and navigation options on the side." />
</Frame>

## Enable the wiki for a repository

1. Open the repository on GitHub.
2. Go to **Settings → Features**.
3. Check the **Wikis** option to enable the wiki for that repository.

## Create and edit wiki pages

* Click the **Wiki** tab in the repository UI to create and edit pages directly in the browser.
* Pages support Markdown (and other formats) and can include headings, links, images, and internal navigation.
* Add special files like `_Sidebar.md` and `_Footer.md` to customize the sidebar and footer that appear across all wiki pages.

> **warning** If your repository is public, be aware that the wiki can be edited by contributors depending on repository settings. Use the "Restrict editing to users with push access" option to limit who can update the wiki.

## Work with the wiki as a Git repository

Each wiki is a separate Git repository. Clone it locally, edit Markdown files, and push changes like any other repository:

```bash theme={null}
