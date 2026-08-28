# Perform behavioral analytics of syscall process

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/Monitoring-Logging-and-Runtime-Security/Perform-Behavioral-Analytics-of-Syscall-Process/page

This article discusses monitoring Kubernetes clusters for abnormal behavior using behavioral analytics on syscalls to enhance security and mitigate potential cyber threats.

In this article, we dive into monitoring Kubernetes clusters for abnormal behavior, potential cyberattacks, and security breaches. By leveraging advanced behavioral analytics on syscalls, you can significantly improve your cluster’s security posture and minimize damage in the event of an intrusion.

Various strategies exist to secure Kubernetes infrastructures—including hardening control plane components, implementing sandboxing techniques to limit container permissions, using mTLS for secure communications, and restricting network access to nodes. However, even with all these security measures in place,

<Frame>
  ![The image lists security measures: Securing Cluster, Sandboxing Techniques, Restricting Network Access, Minimizing Microservices Vulnerability, and MTLS Encryption.](https://kodekloud.com/kk-media/image/upload/v1752871685/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Perform-behavioral-analytics-of-syscall-process/frame_30.jpg)
</Frame>

there is no absolute guarantee against emerging threats. An attacker might always discover a new vulnerability, making it critical to prepare for potential container compromises.

<Callout icon="lightbulb">
  Early detection of suspicious activity can significantly mitigate the impact of a breach. By rapidly identifying irregularities, you can quickly contain any threat and prevent further damage.
</Callout>

<Frame>
  ![The image depicts a network diagram with three "controlplane" nodes and two "worker" nodes, connected in sequence, with an arrow pointing to a worker node from a figure.](https://kodekloud.com/kk-media/image/upload/v1752871688/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Perform-behavioral-analytics-of-syscall-process/frame_60.jpg)
</Frame>

To understand this concept better, consider an analogy with credit and debit card security. Modern smart chips and ATM authentication mechanisms have drastically improved card security, yet a card can still be physically stolen. If an unauthorized user learns your PIN, they can withdraw funds—even using contactless methods.

Before the advent of smartphones, fraudulent transactions might have gone unnoticed for days or weeks until you reviewed your bank statement. Today, instant smartphone notifications alert you immediately, allowing you to quickly report and reverse the transactions. Additionally, setting transaction limits can further restrict potential losses.

<Frame>
  ![The image shows a credit card icon with three features: Instant Notifications, Revert Transactions, and Transaction Limits.](https://kodekloud.com/kk-media/image/upload/v1752871689/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Perform-behavioral-analytics-of-syscall-process/frame_150.jpg)
</Frame>

This analogy holds true for compromised computer systems as well. Swift detection in the event of a breach is critical to containing damage and reducing the overall blast radius. Quickly identifying abnormal activities allows for rapid replacement of compromised nodes or pods

<Frame>
  ![The image depicts a network diagram with control plane and worker nodes, highlighting a security breach on a worker node with a warning symbol and an intruder icon.](https://kodekloud.com/kk-media/image/upload/v1752871690/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Perform-behavioral-analytics-of-syscall-process/frame_170.jpg)
</Frame>

and patching any exploited vulnerabilities to prevent future attacks.

## How to Identify Breaches in a Kubernetes Cluster

One effective tool for securing your Kubernetes environment is [Falco](https://falco.org) from Sysdig. Previously, deep dives into syscalls were performed using tools such as [strace](https://strace.io) and [AquaSec Tracee](https://github.com/aquasecurity/tracee) to analyze application behaviors within pods.

When hundreds of applications run across numerous pods, they generate thousands of syscalls—making simple monitoring insufficient:

<Frame>
  ![The image illustrates Falco monitoring system calls from containers interacting with the Linux kernel and hardware, listing specific syscalls like close and nanosleep.](https://kodekloud.com/kk-media/image/upload/v1752871692/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-Perform-behavioral-analytics-of-syscall-process/frame_210.jpg)
</Frame>

We need robust methods to analyze these syscalls and filter out suspicious events. For example, if an event involves accessing a container's bash shell or a program attempting to read the /etc/shadow file (which contains sensitive password data), it should be flagged for further investigation.

Consider this scenario: attackers often attempt to erase their trail from the system logs.

```bash theme={null}
kubectl exec -ti nginx-master -- bash
