# Demo Enable and Disable Features

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/GitHub-Administration/Demo-Enable-and-Disable-Features/page

Guide for toggling GitHub repository features like Discussions, Projects, Wikis, and Issues to hide tabs, prevent new items, and align repository UI with team workflow

This guide shows how to enable or disable GitHub repository features (Discussions, Projects, Wikis, and Issues) so your repository UI matches your team's workflow. Follow the steps to hide unused tabs and prevent new items from being created for specific features.

Overview

* Disabling a feature hides its tab from the repository UI and prevents collaborators from creating new items for that feature.
* You can enable or disable the following features from the repository settings: Discussions, Projects, Wikis, and Issues.
* Consider the impact on contributors and automation before disabling a feature—Issues and pull requests are commonly used for day-to-day collaboration.

<Callout icon="lightbulb">
  Before making changes, review your team's workflow and inform collaborators. Disabling features will change how contributors interact with the repository.
</Callout>

What happens when you toggle a feature

| Feature     | Effect when disabled                                          | Notes / Considerations                                                                                      |
| ----------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Discussions | Tab is hidden and collaborators cannot create new discussions | Existing items may still be accessible via direct URLs depending on the feature; verify integrations first. |
| Projects    | Projects tab is hidden and new projects cannot be created     | Useful to avoid duplicated planning tools if you use external trackers.                                     |
| Wikis       | Wiki tab is hidden and new wiki pages cannot be created       | If your documentation is in the wiki, migrate it before disabling.                                          |
| Issues      | Issues tab is hidden and new issues cannot be opened          | Generally not recommended for active development; consider alternatives first.                              |

Step-by-step: Disable (or enable) repository features

1. Open your repository on GitHub.
2. Click the repository **Settings** tab.
3. In Settings, expand the **Options** (sometimes labeled "Features") section and scroll to the *Features* area.
4. Use the toggles to enable or disable features:
   * Discussions
   * Projects
   * Wikis
   * Issues
5. Your changes are typically applied automatically when you toggle an option.
6. To re-enable a feature later, return to the same toggles and switch them back on.

Quick checklist before toggling repository features

| Action                    | Why it matters                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Audit current usage       | Determine if contributors or CI/bots use the feature.                              |
| Export or migrate content | Move critical wiki pages, discussions, or projects to another system if needed.    |
| Notify contributors       | Announce the change and update contribution docs (e.g., `CONTRIBUTING.md`).        |
| Verify integrations       | Confirm CI, bots, and third-party tools will continue to work without the feature. |

Example flow

* To disable Wikis: go to Settings → Options → Features and flip off the "Wikis" toggle.
* To remove Discussions and Projects from the repository interface: toggle each off in the same Features area.
* After toggling, the corresponding tabs no longer appear in the repository header, so contributors will rely on the remaining features (for example, Issues and pull requests) for collaboration.

How to communicate the change

* Update repository README and `CONTRIBUTING.md` with the new preferred workflow.
* Create a pinned issue or send a team announcement explaining where to file bugs, feature requests, and design discussions after the change.
* Provide links to external trackers or documentation if you migrate content.

Links and references

* [GitHub Docs: Managing repository settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features)
* [GitHub Discussions](https://docs.github.com/en/discussions)
* [GitHub Issues](https://docs.github.com/en/issues)
* [GitHub Wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis)

<Callout icon="warning">
  Disabling features can impact existing workflows and automation. If you rely on integrations or bots that use a feature (for example, Discussions or Wikis), confirm compatibility before disabling it.
</Callout>

Recommendations

* Most teams keep Issues and Pull Requests enabled because they are central to code review and task tracking.
* Use the repository settings to tailor available features to your team's chosen processes.
* Communicate changes clearly so contributors know where to create and track work.

That's it — use Settings → Features toggles to enable or disable the UI features that best fit your workflow.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/e1fb240f-a163-45b7-ae70-61c1e162023f/lesson/adb39e5c-3c53-43ed-a368-1af4019c2dd6" />
</CardGroup>
