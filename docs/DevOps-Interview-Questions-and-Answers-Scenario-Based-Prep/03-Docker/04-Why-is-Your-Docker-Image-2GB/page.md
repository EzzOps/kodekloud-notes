# Inspect the container's OOMKilled flag
$ docker inspect <container-id> | grep -i oom
"OOMKilled": true,

# Search kernel messages for OOM kills
$ dmesg | grep -i kill
Out of memory: Killed process 4127 (node)
anon-rss:1851232kB

$ journalctl -k | grep -i kill
kernel: Out of memory: Killed process 4127 (node)
```

If you see `OOMKilled: true` or an "Out of memory: Killed process" line in kernel logs, the OOM killer was responsible for the SIGKILL.

If there’s no OOM evidence, consider other common causes:

* Docker after `docker stop`: Docker sends SIGTERM, waits the stop timeout (default 10s), then escalates to SIGKILL.
* Orchestrator termination: Kubernetes/other orchestrators use SIGTERM then SIGKILL after the pod’s termination grace period.
* Manual intervention: someone executed `docker kill`.

To investigate non-OOM kills, check container events and orchestrator logs. Example:

```bash theme={null}
# Observe Docker events for the container over the last 10 minutes
$ docker events --filter 'container=<container-id>' --since '10m'
```

Related exit codes to be aware of

<Frame>
  <img alt="The image displays the text &#x22;Related Exit Codes&#x22; with a reference to exit code 143, labeled as SIGTERM, calculated as 128 + 15. The phrase &#x22;Confuse them, debug the wrong thing.&#x22; appears at the top." />
</Frame>

Use the following quick reference table to avoid debugging the wrong symptom:

| Exit Code | Calculation | Signal  | Typical Meaning                                                            |
| --------- | ----------- | ------- | -------------------------------------------------------------------------- |
| `137`     | `128 + 9`   | SIGKILL | Process was forcibly killed (often OOM killer or escalation after timeout) |
| `143`     | `128 + 15`  | SIGTERM | Graceful termination requested (shutdown path may still run)               |
| `139`     | `128 + 11`  | SIGSEGV | Process crashed with segmentation fault (invalid memory access)            |

Best-practice checklist when you see Exited (137)

1. docker inspect `<id>`: look for `"OOMKilled": true`.
2. Check kernel logs: `dmesg` or `journalctl -k` for OOM messages.
3. Examine Docker events: `docker events --filter 'container=<id>' --since '10m'`.
4. Review orchestrator logs (kubelet, controller manager, etc.) for stop/kill actions.
5. Confirm memory limits on the container and review memory metrics leading up to the failure.
6. If needed, reproduce the issue while collecting memory and process metrics to pinpoint the root cause.

<Callout icon="lightbulb">
  If you see `Exited (137)` but no `OOMKilled` flag and no kernel OOM messages, focus your investigation on orchestrator logs or manual actions (e.g., `docker kill`). Don’t assume OOM without confirming the kernel logs.
</Callout>

<Callout icon="warning">
  Avoid treating 137 as an application bug by default; it indicates an external kill. Only investigate application-level causes (crashes, segfaults) after ruling out external signals and resource limits.
</Callout>

Links and references

* [Docker Documentation](https://docs.docker.com/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Monitoring and troubleshooting kernel OOM killer](https://www.kernel.org/doc/html/latest/admin-guide/)

This guide should help you quickly identify why a container exited with code 137 and which next steps to take based on the evidence you find.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/1d3d5877-dbf7-4105-8bc2-2c619ac62421/lesson/0c4bed43-e0c1-41db-a7ca-6072ad266b82" />
</CardGroup>


# Why is Your Docker Image 2GB

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Docker/Why-is-Your-Docker-Image-2GB/page

How to reduce oversized Docker images using multi-stage builds, minimal base images, and .dockerignore to improve deploy time, autoscaling, security, and storage costs.

Let's start with another DevOps interview question.

A developer on your team builds a Docker image for a simple Node.js API. The image is two gigabytes.

They say, storage is cheap, who cares?

That response misses the real problems. A 2 GB image affects every stage of your deployment and runtime lifecycle:

* Every deploy pulls 2 GB across your network.
* Every new container on every host pulls 2 GB.
* During autoscaling, a traffic spike can cause many instances to pull 2 GB each.
* Cold redeploys and crash recoveries take longer because of the large image transfers.

A deploy that should take ten seconds can become minutes. In an outage, that delay can be critical.

<Frame>
  <img alt="The image highlights the importance of size, showing the 2 GB resource consumption for every deploy, container, server, and auto-scaling spike, emphasizing potential impacts on infrastructure." />
</Frame>

Why this matters (short reference)

| Impact area              | Why 2 GB hurts                                                             |
| ------------------------ | -------------------------------------------------------------------------- |
| Network & time-to-deploy | Slower pulls increase deploy time and recovery time                        |
| Autoscaling              | Concurrent pulls multiply network and I/O load                             |
| Storage & registry costs | Larger images use more disk and raise registry egress/storage fees         |
| Security                 | Extra tools enlarge the attack surface and increase vulnerability exposure |

It gets worse: fat images often contain build tools, compilers, and debug utilities that aren't needed at runtime. Each extra package increases attack surface and may introduce vulnerabilities. You're effectively shipping a toolbox an attacker could misuse.

<Frame>
  <img alt="The image warns about the risks of &#x22;fat images&#x22; in production environments containing unnecessary tools like build tools, compilers, and debug utilities, which can introduce potential vulnerabilities. It suggests that each unnecessary package included in a production image increases security risks." />
</Frame>

The right response: focus on three proven practices that dramatically reduce image size and risk.

1. Use multi-stage builds

* Do compilation and other build steps in a stage containing dev dependencies and build tools.
* Copy only the build artifacts and minimal runtime dependencies into the final image.
* This keeps compilers, package managers, and test tools out of production images.

Example Dockerfile for a Node.js + TypeScript app (multi-stage):

```dockerfile theme={null}
