# Demo Enable Sponsors

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Benefits-of-Open-Source-Community/Demo-Enable-Sponsors/page

How to enable GitHub Sponsors for a repository using .github/FUNDING.yml, surface a Sponsor button, handle branch protection, and complete account onboarding to receive payouts

Sponsorships let the GitHub community financially support a user, a repository, or an organization. This guide shows how to enable sponsorship for a repository using a `.github/FUNDING.yml` file, how GitHub surfaces the Sponsor button, and what account owners must do to receive payouts.

Back in my BlogBuster repository, assume I want to enable sponsorship for this project. One way to do that is from the repository Settings.

<Frame>
  <img alt="This image shows a GitHub repository page for a project called &#x22;block-buster,&#x22; which is an enhanced version of a brick breaker game. The repository includes various files like .devcontainer, index.html, script.js, and others, with recent commit activity displayed." />
</Frame>

In the repository Settings, under the Features section, enable the “Sponsorship” option. Turning this on allows a Sponsor button to appear on the repository and lets you declare one or more funding providers that visitors can choose from.

<Frame>
  <img alt="The image shows a GitHub repository settings page with options related to features like issues, sponsorships, and discussions. Various settings are available for organizing and managing these features within the repository." />
</Frame>

How GitHub determines which funding options to show

* GitHub uses a configuration file named `FUNDING.yml` placed in the `.github` directory on the repository’s default branch (for example, `main`).
* That file declares supported providers and the account names or URLs to display when a visitor clicks the Sponsor button.

A template for supported platforms looks like this:

```yaml theme={null}
