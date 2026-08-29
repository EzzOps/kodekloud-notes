# Prerequisites

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Introduction/Prerequisites/page

Guidance on practical prerequisites and hands-on skills needed to prepare for the Istio Certified Associate exam, focusing on Kubernetes, kubectl, Linux, networking, Helm, and labs.

This lesson outlines the practical prerequisites you should meet before attempting the Istio Certified Associate (ICA) exam. Although the Linux Foundation lists “no prerequisites,” success on the ICA typically requires hands-on experience across several areas. Below are the core domains and specific skills to prioritize.

## Key areas to be comfortable with

* Kubernetes fundamentals (highest priority)
  * Understand what Kubernetes is, its primary architecture, and how workloads are scheduled.
  * Know core API objects and how to configure them: Pods, Deployments, ReplicaSets, DaemonSets, and Services. Because Istio operates at the service and mesh level, be especially comfortable with Services and service discovery.
  * Be able to create, edit, and debug these resources using `kubectl` and YAML manifests.

<Frame>
  <img alt="The image is a Kubernetes resources map diagram showing various components and their relationships within a Kubernetes environment. It uses icons and color-coded sections to illustrate how different resources interconnect and interact." />
</Frame>

If you are new to Kubernetes, consider taking a foundational course first. For example, KodeKloud’s [Kubernetes for the Absolute Beginners - Hands-on Tutorial](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial) is a practical starting point.

<Frame>
  <img alt="The image is a webpage from KodeKloud offering a &#x22;Kubernetes for the Absolute Beginners&#x22; online course, featuring a description, ratings, and an option to subscribe or try a free lab." />
</Frame>

* kubectl and imperative vs declarative operations
  * The ICA exam is performed from a Linux terminal and requires frequent use of the `kubectl` CLI.
  * Be fluent in both declarative workflows (`kubectl apply -f manifest.yaml`) and imperative commands (`kubectl create ...`). The exam may require creating or modifying resources using either approach.

<Frame>
  <img alt="The image depicts a graphic related to &#x22;kubectl&#x22; with buttons labeled &#x22;Apply,&#x22; &#x22;Remove,&#x22; &#x22;Edit,&#x22; &#x22;Investigate,&#x22; and &#x22;Monitor.&#x22; It includes the &#x22;Kubectl CLI&#x22; logo and references an &#x22;ICA Exam.&#x22;" />
</Frame>

<Callout icon="lightbulb">
  Imperative examples: `kubectl create deployment nginx --image=nginx`, or `kubectl expose deployment nginx --port=80 --target-port=80`. Declarative example: write a YAML manifest and run `kubectl apply -f my-deployment.yaml`.
</Callout>

* Linux CLI and terminal text editors
  * The exam environment is a shell—be fluent with essential Linux commands: `cat`, `cd`, `ls`, `mkdir`, `rm`, `curl`, `wget`, `ping`, etc.
  * Know how to edit files in the terminal. Vim is commonly available and powerful; Nano is acceptable. Don't depend on a graphical editor—be prepared to edit YAML in the terminal.

<Frame>
  <img alt="The image features the Linux penguin mascot and a list of Linux terminal commands: cat, cd, mkdir, and touch." />
</Frame>

* Networking basics
  * Have a working understanding of DNS, ports, and common protocols—HTTP, HTTPS, and TCP. Istio’s traffic routing, load balancing, and security features are built on these networking fundamentals.

<Frame>
  <img alt="The image displays the title &#x22;Networking Concepts&#x22; with an icon of a globe surrounded by four people, and lists terms: DNS, Ports, and HTTP/HTTPS/TCP." />
</Frame>

* Helm basics
  * Know what Helm is, how charts work, and basic chart lifecycle commands: `helm install`, `helm upgrade`, and `helm rollback`.
  * You don’t need to be a Helm expert, but you should understand chart values overrides, installing/upgrading components, and how to troubleshoot common Helm issues—especially during Istio install/upgrade tasks.

<Frame>
  <img alt="The image contains a blue Helm logo and three questions related to Helm: &#x22;What is Helm?&#x22;, &#x22;How does Helm work?&#x22;, and &#x22;How to apply Helm Charts?&#x22;." />
</Frame>

## Recommended hands-on experience

* Practical, hands-on experience with Kubernetes clusters and Istio configuration is highly valuable.
* Prior Kubernetes certifications (CKA, CKAD, or CKS) or experience preparing for them will help you succeed on the ICA.
* Use mock exams and time-limited labs to build speed and familiarity with the exam interface and tasks.

<Frame>
  <img alt="The image shows web page layouts for Kubernetes certifications offered by KodeKloud, including courses for Kubernetes Security Specialist, Administrator, and Application Developer." />
</Frame>

## Quick reference: Skills mapped to exam relevance

| Skill area                         | Why it matters for ICA                                                                 | Example tasks                                               |
| ---------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Kubernetes fundamentals            | Istio manages traffic between Kubernetes Services and depends on Kubernetes primitives | Create/Debug Deployments, Services, Pods                    |
| kubectl (imperative & declarative) | Exam tasks require efficient CLI operations                                            | `kubectl apply -f`, `kubectl create`                        |
| Linux CLI & editors                | The exam is performed in a terminal environment                                        | Edit YAML with `vim` or `nano`, use `curl` to test services |
| Networking basics                  | Istio configures routing, TLS, and policies over HTTP/TCP                              | Inspect DNS, ports, and service endpoints                   |
| Helm                               | Often used to install/upgrade Istio or add-ons                                         | `helm install istio <chart>`                                |

<Callout icon="warning">
  The ICA is a practical, time-limited exam performed entirely in a Linux shell. Do not rely on GUI tools—practice editing manifests and running `kubectl` commands under time pressure.
</Callout>

## Final recommendations

* Prioritize Kubernetes fundamentals and become fluent with `kubectl` and a terminal text editor.
* Practice creating and debugging Services and Deployments; try both imperative and declarative methods.
* Use hands-on labs and timed mock exams to build speed and confidence—real cluster experience with Istio is the best preparation.

If you feel ready, start practicing with real clusters and Istio configurations. Good luck!

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Istio Documentation](https://istio.io/latest/docs/)
* KodeKloud courses: [Kubernetes for the Absolute Beginners](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial), [CKA course](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator), [CKAD course](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad), [CKS course](https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/istio-certified-associate/module/da4579eb-7769-4ab9-a0e8-b81f70a12978/lesson/f3a181e2-ac9f-4a80-842a-2aaafb04aec5" />
</CardGroup>
