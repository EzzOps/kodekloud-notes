# Demo ICA Overview

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Introduction/Demo-ICA-Overview/page

Overview of the updated Istio Certified Associate exam including format changes, logistics, exam domains, proctoring, supported Istio version 1.26, and study and preparation tips.

All right — let's review the Istio Certified Associate (ICA) exam: what to expect, how it's changed recently, and how to prepare efficiently.

## Exam cost and retake

The ICA is a paid exam: the registration fee is \$250 USD and includes one free retake. That retake was commonly used by candidates in previous versions, and it's still included with the exam purchase.

## Passing score, duration, and validity

You can confirm up-to-date exam logistics on the official FAQ page.

<Frame>
  <img alt="The image shows a webpage displaying frequently asked questions about the Istio Certified Associate (ICA) exam, including details on exam duration, passing score, language, validity, and renewal process." />
</Frame>

* Passing score: 68% (previously 75%)
* Exam length: 2 hours (hands-on, performance-based tasks)
* Validity: 2 years for certifications issued after April 2024 (previously 3 years)

Note: If you earned a certification under the older rules, it may still carry the older validity period (for example, certificates issued before April 2024 could be valid for three years).

## Proctoring and system requirements

The ICA is proctored remotely through PSI. During the exam you will be monitored via webcam, microphone, and screen sharing. Expect to show your surroundings and keep audio/video enabled for the entire session.

> **warning** Remote proctoring requires your camera and microphone to remain on. You may be asked to show your workspace, and certain behaviors (e.g., covering your mouth, looking away frequently, or having another person present) can cause interruptions or disqualification. Review PSI's system requirements before your exam.

<Frame>
  <img alt="The image shows a webpage detailing information about how exams are proctored and the system requirements for taking an exam, including notes on remote proctoring through video, audio, and screen sharing." />
</Frame>

Recommended resources:

* PSI test center and remote proctoring info: [https://www.psionline.com](https://www.psionline.com)
* Check hardware and browser compatibility well before your appointment

## Open-book exam — know the documentation

The exam is open-book: you can use Istio's official documentation during the test. That makes familiarity with the docs and fast navigation essential.

> **lightbulb** Being able to quickly locate documentation pages and configuration references is as important as hands-on practice. Practice searching the Istio docs for APIs such as VirtualService, DestinationRule, Gateway, and Authentication policies so you can look up details during the exam.

<Frame>
  <img alt="The image shows a webpage from Istio's documentation site with navigation links on the left and various documentation categories and resources displayed on the right." />
</Frame>

Good news for the new exam format: some tasks include direct links to the relevant documentation pages. Instead of searching the entire docs tree, the task description may open a relevant doc page for you.

When a task asks you to create a resource such as a VirtualService, the documentation and examples are available directly. For example:

<Frame>
  <img alt="The image shows a webpage from Istio's documentation site focused on &#x22;Traffic Management,&#x22; listing various configuration options like Destination Rule, ProxyConfig, and Virtual Service." />
</Frame>

Example VirtualService skeleton:

```yaml theme={null}
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
    - reviews.prod.vs.cluster.local
  http:
    - name: "reviews-v2-routes"
      # add route/configuration here (e.g., match, route, rewrite)
```

Practice using the docs to find field names, API versions, and example manifests so you can build or edit YAML quickly in the exam environment.

## Supported Istio version for the exam

The ICA was updated to target a more recent Istio release. At the time this overview was created:

* Latest Istio upstream release: 1.27
* ICA exam version target: 1.26 (this course and exam content are based on Istio 1.26)

Most of the configuration and patterns you knew from 1.18 still apply, but pay attention to new features and changes introduced between those versions (for instance, ambient mode and in-place canary upgrades).

## Exam domains and weighting

The exam domains are similar to prior versions but have adjusted weights. Below is a concise breakdown of the major domains and approximate weightings:

| Domain                                                      | Weight / Focus                                                                      |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Installation, Upgrading, Configuration                      | 25% — installation modes, ambient mode, and in-place canary upgrades                |
| Traffic Management (including resiliency & fault injection) | 25% — VirtualService, DestinationRule, routing, retries, timeouts, circuit breakers |
| Securing Workloads                                          | 25% — mTLS, authentication/authorization policies, service identities               |
| Advanced / Troubleshooting                                  | 20% — mesh troubleshooting, observability, policy enforcement                       |

These weights reflect the newer exam layout (note: weights are approximate and subject to change—check the official exam page for definitive details).

## What changed in the new ICA exam format

Key improvements in the latest exam version:

* Fewer tasks: reduced from \~20–22 hands-on tasks to 16 hands-on tasks
* Multiple-choice removed: prior multiple-choice questions have been eliminated
* Passing score reduced from 75% to 68%
* You get time to review your answers before submission (the new format allows some time to verify work)
* The exam remains 2 hours long and is still hands-on and performance-based

These changes make the exam more focused and, for many candidates, easier to complete within the allotted time.

## Preparation tips

* Practice common Istio resources: VirtualService, DestinationRule, Gateway, PeerAuthentication, AuthorizationPolicy, and ServiceEntry.
* Get hands-on with ambient mode (sidecar-less) scenarios and in-place upgrade patterns.
* Timebox practice exams to 2 hours and practice reviewing your answers at the end.
* Learn to navigate the Istio docs quickly (table of contents, search, and resource examples).
* Validate YAML in a local cluster (Kind / KinD + Istio) and practice debugging with istioctl and kubectl.

## Useful links and references

* Official Istio documentation: [https://istio.io](https://istio.io)
* ICA exam FAQ and policies: (refer to the exam FAQ image above or the official certification page)
* PSI remote proctoring: [https://www.psionline.com](https://www.psionline.com)

If you want, I can provide a focused study plan, sample hands-on tasks, or a practice checklist tailored to the ICA 1.26 objectives. Which would help you most right now?

- [Watch Video](https://learn.kodekloud.com/user/courses/istio-certified-associate/module/da4579eb-7769-4ab9-a0e8-b81f70a12978/lesson/86992247-ae84-4fc0-8081-2db5f994f998)
