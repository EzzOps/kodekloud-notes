# Choosing a License

Source: https://notes.kodekloud.com/docs/Open-Source-for-Beginners/Starting-Your-Open-Source-Project/Choosing-a-License/page

This guide helps you choose an open source license, outlining key considerations and categories to publish your project confidently.

Selecting an open source license is a pivotal step when launching a community-driven software project. It not only determines how others can use, modify, or distribute your code but also defines your project's governance model. With your idea validated and infrastructure ready, this guide will help you navigate the two main license categories and publish your project with confidence.

<Frame>
  ![The image shows four icons of documents with checkmarks, accompanied by the text "Let's Choose a License."](https://kodekloud.com/kk-media/image/upload/v1752882561/notes-assets/images/Open-Source-for-Beginners-Choosing-a-License/choose-license-documents-checkmarks-icons.jpg)
</Frame>

To streamline your decision:

* Identify your goals: community contributions, commercial adoption, or strict sharing.
* Compare license obligations: attribution, copyleft reciprocity, patent grants.
* Align with your project's mission and long-term vision.

<Callout icon="lightbulb">
  Always review the full legal text of any license and consider consulting a legal professional for complex projects.
</Callout>

## License Categories

| License Type | Key Feature                                | Common Examples               |
| ------------ | ------------------------------------------ | ----------------------------- |
| Copyleft     | Derivatives must carry the same license    | GPL, AGPL, LGPL               |
| Permissive   | Minimal restrictions; requires attribution | MIT, Apache 2.0, BSD-3-Clause |

### Copyleft Licenses

Copyleft licenses ensure that every modification or fork remains free and open by requiring derivative works to inherit the same terms as the original. This model fosters a collaborative ecosystem where improvements stay within the community.

<Frame>
  ![The image shows a diagram with the label "COPY LEFT" and icons representing a document with a checkmark and a hexagon with a keyhole.](https://kodekloud.com/kk-media/image/upload/v1752882562/notes-assets/images/Open-Source-for-Beginners-Choosing-a-License/copy-left-document-checkmark-hexagon-keyhole.jpg)
</Frame>

Key considerations:

* Enforces reciprocity for downstream users
* Protects community contributions from being closed-source
* May deter commercial adopters who need proprietary integration

### Permissive Licenses

Permissive licenses offer maximum flexibility by allowing your code to be used in both open source and proprietary projects. The only typical requirement is to retain the original copyright notice and license text.

<Frame>
  ![The image is a diagram with two sections, highlighting "Permissive" licenses with minimal restrictions.](https://kodekloud.com/kk-media/image/upload/v1752882562/notes-assets/images/Open-Source-for-Beginners-Choosing-a-License/permissive-licenses-minimal-restrictions-diagram.jpg)
</Frame>

Why choose permissive?

* Broad commercial adoption
* Fewer barriers for contributors
* Ideal for libraries or tools aiming for wide integration

## Publishing Your Project

Once you’ve chosen a license, make it official:

1. Add a `LICENSE` file at your repository root.
2. Reference the license in your `README.md`.
3. Tag your initial release to mark your project’s version history.

<Frame>
  ![The image features a network diagram with interconnected nodes and icons for GitHub and GitLab, suggesting a focus on version control or software development.](https://kodekloud.com/kk-media/image/upload/v1752882563/notes-assets/images/Open-Source-for-Beginners-Choosing-a-License/network-diagram-github-gitlab-icons.jpg)
</Frame>

Popular hosting platforms:

* [GitHub][github] – the largest development community
* [GitLab][gitlab] – built-in CI/CD pipelines and self-hosting options

<Callout icon="triangle-alert">
  Mismatched license files or missing attributions can lead to legal complications. Double-check that your repository includes the correct `LICENSE` and copyright notices.
</Callout>

## Links and References

* [Open Source Initiative](https://opensource.org/)
* [GitHub][github]
* [GitLab][gitlab]

[github]: https://github.com

[gitlab]: https://gitlab.com

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/open-source-for-beginners/module/767d06e2-2c02-403c-aa37-6e4a5549e6a6/lesson/287b0f0f-12e2-4763-a723-6316cc865b80" />
</CardGroup>
