# Patterns in the repository-level settings
config/**
*.secret.js
```

```javascript theme={null}
// src/App.js
import { useState } from 'react';
// This file is processed by Copilot since it's not excluded.
function App() {
  const [image, setImage] = useState(null);
  // ...
  return <div>App Component</div>;
}
```

<Callout icon="lightbulb">
  Use fnmatch patterns to fine-tune exclusions. For details, see the [fnmatch documentation](https://docs.python.org/3/library/fnmatch.html).
</Callout>

***

## Organization-Level Exclusion

Enforce rules across all repos and file paths in your organization:

1. Go to **Organization Settings** → **Copilot** → **Content Exclusion**.
2. Choose scope: Git repositories or file system.
3. Define fnmatch patterns and save.

<Frame>
  ![The image is a flowchart titled "Organization-Level Exclusion," detailing steps for accessing settings, defining scope, and applying patterns for file exclusion in Git repositories.](https://kodekloud.com/kk-media/image/upload/v1752876874/notes-assets/images/GitHub-Copilot-Certification-Data-Exclusion-Mechanisms/organization-level-exclusion-flowchart.jpg)
</Frame>

With this approach, privacy rules remain consistent organization-wide.

***

## Pattern-Matching Techniques

Use these common fnmatch-style patterns to exclude content:

| Pattern           | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `secrets.json`    | Excludes any file named exactly `secrets.json`.      |
| `*.cfg`           | Excludes all `.cfg` files.                           |
| `**/scripts/*.js` | Excludes every `.js` in a `scripts` folder anywhere. |
| `!allowed/*.cfg`  | Negates a previous pattern to allow specific files.  |

Combine patterns for granular control—exclude `.env` globally but allow `/.env.local`.

***

## Real-World Applications

1. Proprietary algorithms and secret business logic
2. Customer PII and personal data
3. API keys, tokens, and system credentials

***

## Limitations and Benefits

| Aspect      | Details                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------ |
| Limitations | IDEs might still index excluded files for semantic features; visual indicators only hint at exclusion. |
| Benefits    | Stronger data protection, regulatory compliance, and confidence in AI suggestions.                     |

***

## Exam Relevance

Mastering content exclusion is essential for GitHub Copilot certification. It demonstrates best practices for balancing productivity with security in modern development workflows.

<Frame>
  ![The image is a slide titled "Exam Relevance" with two points: the importance of GitHub Copilot certification and balancing productivity with security needs.](https://kodekloud.com/kk-media/image/upload/v1752876875/notes-assets/images/GitHub-Copilot-Certification-Data-Exclusion-Mechanisms/exam-relevance-github-copilot-productivity.jpg)
</Frame>

***

## Links and References

* [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
* [fnmatch — Unix filename pattern matching](https://docs.python.org/3/library/fnmatch.html)
* [GitHub Security Best Practices](https://docs.github.com/en/code-security)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-certification/module/f20687c1-eca3-4a6f-b075-5bee5f7cfbfb/lesson/f46472df-b090-48f2-83f1-f6f1983119a8" />
</CardGroup>


# Exploring GitHub Copilot Plans

Source: https://notes.kodekloud.com/docs/GitHub-Copilot-Certification/Management-of-GitHub-Copilot/Exploring-GitHub-Copilot-Plans/page

This guide compares GitHub Copilot subscription tiers, including Free, Pro, Business, and Enterprise plans, focusing on pricing, features, and ideal use cases.

Discover which GitHub Copilot subscription tier matches your workflow and budget. In this guide, we compare the Free, Pro, Business, and Enterprise plans—covering pricing, key features, and ideal use cases.

## Plan Comparison & Pricing

<Frame>
  ![The image shows a pricing table for GitHub Copilot plans, including Free, Pro (10/month), Business (19/user/month), and Enterprise (\$39/user/month) options.](https://kodekloud.com/kk-media/image/upload/v1752876877/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/github-copilot-pricing-table.jpg)
</Frame>

<Callout icon="lightbulb">
  Prices and feature sets may change over time. Always refer to the [official Copilot plans page](https://github.com/features/copilot) for the most up-to-date information.
</Callout>

| Plan       | Price (per user/month) | Key Features                                                      | Best For                                |
| ---------- | ---------------------: | ----------------------------------------------------------------- | --------------------------------------- |
| Free       |                    \$0 | 2,000 code completions, 50 chat requests per month                | Students, hobbyists, first-time users   |
| Pro        |                   \$10 | Unlimited completions & chat, latest AI models, 30-day free trial | Professional developers                 |
| Business   |                   \$19 | Policy & license management, IP indemnity, org-wide policies      | Teams & mid-sized organizations         |
| Enterprise |                   \$39 | Private AI models, codebase indexing, GitHub Chat integration     | Large enterprises with compliance needs |

***

## Free Plan

Ideal for developers who want to explore AI-assisted coding without cost.

* 2,000 AI-driven completions per month
* 50 Copilot Chat requests per month
* No subscription fee

<Frame>
  ![The image describes the GitHub Copilot Free Plan, highlighting target users, key limitations, cost, and availability. It is aimed at individual developers, offers 2,000 code completions and 50 chat requests per month, is free, and is accessible to developers not covered by other plans.](https://kodekloud.com/kk-media/image/upload/v1752876878/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/github-copilot-free-plan-overview.jpg)
</Frame>

This entry-level plan is perfect for students, occasional programmers, or anyone curious about AI-powered code suggestions.

***

## Pro Plan

Get unlimited AI assistance and early access to the latest model updates.

* Unlimited code completions and chat messages
* Access to cutting-edge Copilot AI models
* 30-day free trial

<Frame>
  ![The image is an advertisement for Copilot Pro, priced at \$10/month, highlighting its target users, special access for verified students and teachers, and key features like unlimited code completions and a 30-day free trial.](https://kodekloud.com/kk-media/image/upload/v1752876879/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/copilot-pro-advertisement-features.jpg)
</Frame>

<Callout icon="lightbulb">
  Verified students, teachers, and open-source maintainers receive Copilot Pro at no cost.
</Callout>

***

## Business Plan

Designed for growing teams that need centralized controls and compliance.

* Custom policy and license management
* IP indemnity protection
* Organization-wide AI completion settings

This tier ensures consistent coding standards and legal safeguards across your entire team.

***

## Enterprise Plan

The most comprehensive Copilot package for large enterprises.

* All Business features, plus:
  * Dedicated codebase indexing
  * GitHub Chat integration
  * Private AI models tuned to your repositories

<Frame>
  ![The image is an advertisement for "Copilot Enterprise" priced at \$39 per user per month, targeting large organizations requiring customization, with features like enterprise customization, codebase indexing, and GitHub chat integration.](https://kodekloud.com/kk-media/image/upload/v1752876881/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/copilot-enterprise-advertisement-39-dollars.jpg)
</Frame>

This plan caters to organizations with strict compliance, security, or customization requirements.

***

## Measurable Benefits

Organizations leveraging GitHub Copilot often see measurable improvements:

* 55% faster code completion in controlled studies
* 20% productivity gains during feature development
* 15% higher merge success rates
* 84% increase in successful builds

<Frame>
  ![The image presents a summary of benefits and impact, highlighting 55% faster code completion, 20% increased productivity, and a 15% improvement in pull request success.](https://kodekloud.com/kk-media/image/upload/v1752876882/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/code-completion-productivity-summary.jpg)
</Frame>

***

## Developer Experience

Beyond raw metrics, Copilot enhances day-to-day coding:

* 90% of users report increased job satisfaction
* 95% say coding feels more enjoyable
* 87% spend less mental energy on repetitive tasks

<Frame>
  ![The image highlights the benefits and impact of a developer tool, showing increased job satisfaction, coding enjoyment, and mental energy conservation among developers.](https://kodekloud.com/kk-media/image/upload/v1752876883/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/developer-tool-benefits-impact.jpg)
</Frame>

Copilot not only accelerates development but also makes it more engaging.

***

## IDE Support

Seamlessly integrate Copilot with your preferred editor:

* Visual Studio Code
* Visual Studio
* JetBrains IDEs
* Neovim
* Azure Data Studio
* Xcode

<Frame>
  ![The image lists various integrated development environments (IDEs) available on the platform, including VS Code, Visual Studio, JetBrains IDEs, Neovim, Azure Data Studio, and Xcode.](https://kodekloud.com/kk-media/image/upload/v1752876884/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/ides-available-on-platform.jpg)
</Frame>

***

## Platform Availability

Access GitHub Copilot wherever you work:

* GitHub.com
* Mobile applications (iOS & Android)
* Command-line interface tools

<Frame>
  ![The image shows a "Platform Availability" section with icons and labels for GitHub.com, Mobile Apps, and CLI Tools.](https://kodekloud.com/kk-media/image/upload/v1752876885/notes-assets/images/GitHub-Copilot-Certification-Exploring-GitHub-Copilot-Plans/platform-availability-github-mobile-cli.jpg)
</Frame>

***

For more details on features, trials, and pricing, visit the [official GitHub Copilot plans page](https://github.com/features/copilot). Understanding each tier will help you choose the best plan for your projects and certification goals.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-copilot-certification/module/f20687c1-eca3-4a6f-b075-5bee5f7cfbfb/lesson/8bcac0cc-2a37-40a8-bc2f-7ff00572d669" />
</CardGroup>
