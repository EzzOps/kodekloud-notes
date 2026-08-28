# Only CRITICAL and HIGH
trivy image --severity CRITICAL,HIGH nginx:1.18.0

# Skip vulnerabilities without available fixes
trivy image --ignore-unfixed nginx:1.18.0

# Scan a saved tar archive
docker save nginx:1.18.0 > nginx.tar
trivy image --input nginx.tar
```

<Callout icon="triangle-alert">
  Using `--ignore-unfixed` can hide critical risks if no patch is available. Always review the full report before deployment.
</Callout>

## Reduce Your Image’s Attack Surface

Smaller base images generally contain fewer vulnerabilities. Compare these scan results:

| Image                 | Total CVEs |
| --------------------- | ---------- |
| nginx:1.18.0 (debian) | 155        |
| nginx:1.18.0-alpine   | 0          |

Always prefer minimal, official base images.

<Frame>
  ![The image lists best practices for image scanning, including continuous rescanning, using Kubernetes Admission Controllers, maintaining a repository of pre-scanned images, and integrating scanning into the CI/CD pipeline.](https://kodekloud.com/kk-media/image/upload/v1752880920/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Supply-Chain-Security-Scan-images-for-known-vulnerabilities/image-scanning-best-practices.jpg)
</Frame>

## Image Scanning Best Practices

* Continuously re-scan images to catch newly disclosed CVEs
* Enforce admission controls to block or quarantine unscanned or unsafe images
* Maintain an internal registry of pre-scanned, approved images for rapid rollouts
* Integrate scanning into CI/CD pipelines so that every build is audited at source

***

## Links and References

* [CVE Database](https://cve.mitre.org/)
* [CVSS v3 Specification](https://www.first.org/cvss/specification-document)
* [Trivy GitHub Repository](https://github.com/aquasecurity/trivy)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/8f0d5517-7d43-4d97-871d-234bb4503f7f/lesson/119c1f94-b919-4aa9-a597-7e077869b89a" />
</CardGroup>


# Conclusion

Source: https://notes.kodekloud.com/docs/Kustomize/Capstone-Project/Conclusion/page

This article provides an overview of Kustomize for managing Kubernetes manifests, covering installation, syntax, transformers, overlays, and imperative commands.

## Conclusion

In this lesson, you’ve gained a solid understanding of Kustomize and its role in streamlining Kubernetes manifest management. We covered:

| Topic                   | Description                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| Rationale               | The motivation behind Kustomize and how it compares to Helm and other templating tools      |
| Installation & Syntax   | Installing Kustomize (standalone or via `kubectl`) and defining a `kustomization.yaml` file |
| Transformers & Overlays | Applying strategic merge patches, JSON 6902 patches, and composing overlays                 |
| Imperative Commands     | Using `kubectl kustomize` flags for on-the-fly customization without editing source files   |
| Generators              | Automatically creating Secrets and ConfigMaps from literals and files                       |

<Callout icon="lightbulb">
  Your feedback helps us improve! If there’s a topic you’d like us to explore in more depth—such as advanced patching strategies or multi-environment workflows—let us know.
</Callout>

## Further Reading

* [Kustomize Official Documentation](https://kubectl.docs.kubernetes.io/references/kustomize/)
* [Kubernetes Configuration Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)
* [Customization Patterns in Kubernetes](https://www.cncf.io/blog/2020/11/19/kustomize-building-and-maintaining-a-custom-kubernetes-configuration/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/kustomize/module/8ee78739-877b-4e11-a7a6-82ef7210468b/lesson/6b0f71b0-af8d-4394-bf24-0952d3f8f787" />
</CardGroup>
