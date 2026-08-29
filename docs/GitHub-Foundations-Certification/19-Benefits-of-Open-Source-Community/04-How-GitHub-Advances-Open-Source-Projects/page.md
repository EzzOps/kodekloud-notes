# Supported funding model platforms (example values)
github:            # Replace with up to 4 GitHub Sponsors-enabled usernames, e.g. [user1, user2]
  - [alice, bob]
patreon:           # Replace with a single Patreon username, e.g. 'project-patron'
  - project-patron
open_collective:   # Replace with a single Open Collective slug, e.g. 'my-collective'
  - my-collective
ko_fi:             # Replace with a single Ko-fi username, e.g. 'my_kofi'
  - my_kofi
tidelift:          # Replace with a single Tidelift package identifier, e.g. 'npm/babel'
  - npm/babel
community_bridge:  # Replace with a single Community Bridge project slug, e.g. 'cloud-foundry'
  - cloud-foundry
liberapay:         # Replace with a single Liberapay username, e.g. 'myname'
  - myname
issuehunt:         # Replace with a single Issuehunt username or project
  - project-issuehunt
lfx_crowdfunding:  # Replace with a single LFX Crowdfunding project slug
  - cloud-foundry
polar:             # Replace with a single Polar username
  - polar-user
buy_me_a_coffee:   # Replace with a single Buy Me a Coffee username
  - buyme-user
thanks_dev:        # Replace with a single thanks.dev username
  - thanks-user
custom:            # Replace with up to 4 custom sponsorship URLs, e.g. ['https://example.com/donate']
  - ['https://example.com/donate']
```

Supported platforms at a glance

| Platform                           | What to include in your funding file              | Example                                         |
| ---------------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| GitHub Sponsors                    | Up to 4 GitHub usernames or organization accounts | `- [alice, bob]`                                |
| Patreon                            | Single Patreon username or project                | `- project-patron`                              |
| Open Collective                    | Single collective slug                            | `- my-collective`                               |
| Ko-fi                              | Ko-fi username                                    | `- my_kofi`                                     |
| Tidelift                           | Package identifier (ecosystem/package)            | `- npm/babel`                                   |
| Community Bridge                   | Project slug                                      | `- cloud-foundry`                               |
| Liberapay                          | Username                                          | `- myname`                                      |
| Issuehunt                          | Username or project identifier                    | `- project-issuehunt`                           |
| LFX Crowdfunding                   | Project slug                                      | `- cloud-foundry`                               |
| Polar, Buy Me a Coffee, thanks.dev | Respective usernames                              | `- polar-user`, `- buyme-user`, `- thanks-user` |
| Custom                             | Any custom sponsorship URL(s)                     | `- ['https://example.com/donate']`              |

How does GitHub Sponsors work?

1. Direct support

* Sponsors can back individual maintainers (via their GitHub profile) or entire organizations (via an organization Sponsors page).
* Payments may be set up as monthly recurring contributions or one-time donations depending on recipient configuration.

2. Flexible tiers

* Maintainers and organizations can define multiple sponsorship tiers with specified monthly amounts and optional perks (examples: early access, private support channels, or public recognition).
* Prospective sponsors choose the tier that best matches their desired level of support.

3. Zero-platform fees (for individual sponsorships)

* GitHub currently charges zero platform fees for individual-sponsored contributions so more of the pledge reaches the recipient.
* Note that payment processing fees from third-party payment providers may still apply.

<Callout icon="lightbulb">
  Payment processing fees may still apply, and GitHub Sponsors availability varies by country and region. Always verify the latest regional availability and fee details in the official GitHub Sponsors documentation: [https://docs.github.com/en/sponsors/setting-up-sponsorships-for-your-organization/about-github-sponsors](https://docs.github.com/en/sponsors/setting-up-sponsorships-for-your-organization/about-github-sponsors)
</Callout>

4. Corporate sponsorship and budgets

* Companies can create corporate sponsorships, allocate budgets, and distribute funds to maintainers and projects.
* Organization-level sponsorships may require additional configuration, legal agreements, or enterprise features depending on the plan.

Summary

* GitHub Sponsors centralizes open-source funding by enabling direct sponsorship, configurable tiers, and organizational sponsorship controls.
* Use the funding file example above to list the platforms you accept for contributions, and replace placeholder values with your actual usernames, slugs, or URLs.
* Confirm current fee policies and geographic availability on the official GitHub Sponsors documentation.

Links and references

* GitHub Sponsors documentation: [https://docs.github.com/en/sponsors/setting-up-sponsorships-for-your-organization/about-github-sponsors](https://docs.github.com/en/sponsors/setting-up-sponsorships-for-your-organization/about-github-sponsors)
* Funding file guidance: [https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-funding-files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-funding-files)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c969426b-f74f-4ca3-8269-a63dff90fbc2/lesson/8d282c62-b3e2-460c-bb53-1552c0dae65c" />
</CardGroup>


# How GitHub Advances Open Source Projects

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Benefits-of-Open-Source-Community/How-GitHub-Advances-Open-Source-Projects/page

GitHub supports and sustains open source projects by providing free infrastructure, standardized workflows, automated security, discoverability, funding, and long term preservation.

GitHub is more than a code host — it provides the platform, tools, and community patterns that help open source projects scale, stay secure, and remain sustainable over time. Below we break down the core ways GitHub supports open source, with practical examples and links to relevant features.

<Callout icon="lightbulb">
  This article highlights the core ways GitHub supports open source: free infrastructure, standardized workflows, automated security, discoverability and growth, financial support, and long-term preservation.
</Callout>

## Key pillars GitHub provides

| Pillar                 | What GitHub provides                                                        | Example / Benefit                                                                                              |
| ---------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Free infrastructure    | Free hosting and build minutes for public repos; CI/CD via `GitHub Actions` | Solo maintainers can run the same pipelines as large organizations using `https://github.com/features/actions` |
| Standardized workflows | Pull requests, issues, code review, templates, labels                       | Contributors from anywhere can follow a common workflow, lowering friction for contributions                   |
| Automated security     | Dependabot, CodeQL, secret scanning, security advisories                    | Automatically detect and often remediate vulnerable dependencies or code issues                                |
| Discovery & growth     | Explore, Trending, stars, social signals                                    | Projects gain visibility and attract contributors and users globally                                           |
| Financial support      | GitHub Sponsors and integrated funding tools                                | Enables maintainers to get paid and reduces burnout                                                            |
| Preservation           | GitHub Archive Program, Arctic Code Vault                                   | Protects open source code for long-term access and historical record                                           |

## 1. Free infrastructure

GitHub removes a major financial barrier by offering free hosting, bandwidth, and CI/CD features for public repositories. Combined with free GitHub Actions usage for public projects, maintainers can build, test, and deploy without additional infrastructure costs.

Benefits:

* Lowers cost to entry for individuals and small teams
* Makes reproducible CI/CD pipelines widely accessible
* Encourages experimentation and growth of early-stage projects

## 2. Standardized workflows

Features like pull requests, issues, review requests, and protected branches create a shared contribution model across millions of repositories. A common interface and process drastically reduce cultural and organizational friction when contributors move between projects.

<Frame>
  <img alt="The image shows a menu with various options like &#x22;Free Infrastructure&#x22; and &#x22;Automated Security,&#x22; with &#x22;Standardized Workflow&#x22; highlighted, detailing its components such as pull requests, issue tracking, and collaboration models." />
</Frame>

Why this matters:

* New contributors spend less time learning project-specific processes
* Maintainers can adopt templates and automation to scale contribution workflows
* Consistent workflows improve code quality and project governance

## 3. Automated security

GitHub integrates automated security tools that scan code and dependencies continuously. Services such as Dependabot and CodeQL surface vulnerabilities and offer automated fixes or guidance.

<Frame>
  <img alt="The image is a diagram highlighting &#x22;Automated Security&#x22; services, including Dependabot for dependency updates, CodeQL for vulnerability scanning, and continuous security monitoring. It is part of a list of features or services including free infrastructure, standardized workflow, discovery and growth, financial support, and project preservation." />
</Frame>

Typical outcomes:

* Faster detection of vulnerable dependencies
* Automated pull requests to update dependencies
* Continuous code analysis to find security issues early

## 4. Discovery and growth

Built-in discovery features like Explore, Trending, and repository stars surface projects to potential contributors and users, acting as lightweight popularity and quality signals.

<Frame>
  <img alt="The image contains a list of features related to &#x22;Discovery & Growth,&#x22; including visibility, popularity signals, and global contributor attraction, alongside other categories like infrastructure and security." />
</Frame>

How projects benefit:

* Improved visibility increases contributor and user acquisition
* Social signals (stars, forks) help newcomers assess project activity
* Discovery channels drive long-tail adoption across ecosystems

## 5. Financial support

GitHub Sponsors and integrated funding tools let individuals and organizations contribute directly to maintainers. This creates a pathway for sustainable funding that’s built into the same platform where the code lives.

<Frame>
  <img alt="The image is a diagram listing the benefits of &#x22;Financial Support&#x22; with options like &#x22;GitHub Sponsors for funding,&#x22; &#x22;Direct support to maintainers,&#x22; and &#x22;Enables sustainable open-source work.&#x22; It includes a menu with other options like &#x22;Free Infrastructure&#x22; and &#x22;Automated Security.&#x22;" />
</Frame>

Financial support implications:

* Helps retain maintainers and reduce burnout
* Enables paid work on critical infrastructure projects
* Lowers the risk of project abandonment

## 6. Project preservation

Long-term preservation initiatives like the GitHub Archive Program and the Arctic Code Vault ensure that today’s open source artifacts are preserved for future generations, protecting collective technical knowledge.

<Frame>
  <img alt="The image is a flowchart indicating aspects of project preservation, including GitHub Archive Program, Arctic Code Vault, and ensuring code longevity for future generations, with a sidebar listing features like free infrastructure and automated security." />
</Frame>

Preservation benefits:

* Acts as a historical and technical insurance policy
* Maintains access to code regardless of future platform changes
* Supports research, education, and restoration efforts

## Conclusion

By combining free infrastructure, standard workflows, automated security, discoverability, funding mechanisms, and preservation programs, GitHub turns code hosting into a holistic platform for sustaining open source. These pillars work together to lower barriers, improve safety, attract contributors, and protect our shared software heritage.

## Links and references

* GitHub Actions: [https://github.com/features/actions](https://github.com/features/actions)
* Dependabot: [https://github.com/dependabot](https://github.com/dependabot)
* CodeQL: [https://securitylab.github.com/tools/codeql](https://securitylab.github.com/tools/codeql)
* GitHub Explore: [https://github.com/explore](https://github.com/explore)
* GitHub Trending: [https://github.com/trending](https://github.com/trending)
* GitHub Sponsors: [https://github.com/sponsors](https://github.com/sponsors)
* GitHub Archive Program: [https://archiveprogram.github.com/](https://archiveprogram.github.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-foundation-certification/module/c969426b-f74f-4ca3-8269-a63dff90fbc2/lesson/b7ab3859-7b04-4ece-8d92-bbf4869ff2d3" />
</CardGroup>
