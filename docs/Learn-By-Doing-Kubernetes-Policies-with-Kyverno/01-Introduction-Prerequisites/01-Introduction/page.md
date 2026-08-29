# Introduction

Source: https://notes.kodekloud.com/docs/Learn-By-Doing-Kubernetes-Policies-with-Kyverno/Introduction-Prerequisites/Introduction/page

Hands-on course teaching Kyverno for Kubernetes policies, including installation, validation and mutation policy authoring, testing, enforcement, advanced patterns, labs, and a final practical challenge.

Welcome to the Learn by Doing course: Kubernetes Policies with Kyverno.

Instructors: Vijin Palazhi and Srinivas.

This hands‑on course is built for DevOps engineers, system administrators, and cloud professionals who want practical experience creating, validating, and enforcing Kubernetes policies using Kyverno. You will deploy Kyverno in a Kubernetes cluster, author policies, test them, and apply best practices to improve cluster security and compliance.

By the end of this course you will be able to:

* Install and configure Kyverno in a Kubernetes cluster.
* Write validation and mutation policies.
* Test and iterate on policies safely.
* Apply advanced patterns and enforce organizational compliance.

<Frame>
  <img alt="The image shows the Kyverno logo for Kubernetes policies at the top, with icons and labels for &#x22;Efficient Policy Management,&#x22; &#x22;Validation,&#x22; and &#x22;Enforcement&#x22; below." />
</Frame>

This lesson uses short, focused labs with an Overview and step‑by‑step Tasks. Think of the Overview tab as the lesson content and the Tasks tab as your workbook. The Overview opens by default.

To work in each lab:

* Open the terminal using the terminal toggle icon in the lab UI. This provides an interactive shell connected to a live Kubernetes cluster.
* If you get stuck, use the Hint and Solution tabs.
* Use the Check button to validate task results and advance through exercises.

> **lightbulb** When using the default `nginx` image in examples, use `/bin/sh` for an interactive shell because `bash` may not be available.

> **warning** The examples in this course sometimes run containers as `root` for demonstration. Never run root containers in production—use least privilege and a proper `securityContext`.

Representative lab example — a pod running as root (for demonstration only). Save this as `root-pod.yaml` and apply it to inspect the container filesystem:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: root-pod
spec:
  containers:
    - name: root-container
      image: nginx
      securityContext:
        runAsUser: 0
```

Commands to apply and inspect:

```bash theme={null}
kubectl apply -f root-pod.yaml
kubectl exec -it root-pod -- /bin/sh
cat /etc/passwd
```

Course structure — topics are arranged to build skills progressively:

| Topic                       | What you'll learn                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------- |
| Why policies matter         | The role of policies in security, compliance, and guardrails for Kubernetes workloads |
| Installing Kyverno          | How to install and configure Kyverno in a cluster and why Kyverno is a strong choice  |
| Basic policies              | Validation and mutation examples to enforce simple rules                              |
| Advanced patterns           | Reusable patterns, policy composition, and performance considerations                 |
| Mutating resources          | Auto-injection and mutation strategies to enforce defaults and sidecars               |
| Policy testing & validation | Techniques and tools for testing policies safely                                      |
| Final challenge             | Apply everything in a real-world scenario to validate learning                        |

Finally, you will complete a Kyverno policy challenge that consolidates the lessons into a practical scenario.

<Frame>
  <img alt="The image is a course topics overview for a Kyverno and Kubernetes policy course, with six topics listed, including setting up Kyverno, creating policies, and validation." />
</Frame>

Ready to begin? Start with the first lab to install Kyverno and create your first policy.

Links and references

* Kyverno documentation: [https://kyverno.io/](https://kyverno.io/)
* Kubernetes documentation: [https://kubernetes.io/docs/](https://kubernetes.io/docs/)
* Getting started with Kyverno: [https://kyverno.io/docs/quickstart/](https://kyverno.io/docs/quickstart/)

- [Watch Video](https://learn.kodekloud.com/user/courses/learn-by-doing-kubernetes-policies-with-kyverno/module/a3370f08-e378-4285-9305-52025206031a/lesson/d3a737d3-eaee-4528-a90e-b04aebbdc633)
