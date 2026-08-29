# Tips Tricks

Source: https://notes.kodekloud.com/docs/Prep-Course-Istio-Certified-Associate-ICA-Certification/Troubleshooting/Tips-Tricks/page

Practical tips and strategies to pass the Istio Certified Associate hands on exam including documentation navigation, Vim editing, istioctl analyze, SSH workflow, Kubernetes troubleshooting, partial credit and time management

All right — practical tips and techniques to help you pass the Istio Certified Associate (ICA) hands‑on exam. These notes complement the [Istio Service Mesh](https://learn.kodekloud.com/user/courses/istio-service-mesh) course and focus on exam strategy, tools, and troubleshooting patterns.

This certification is widely regarded as a challenging, hands‑on exam — in my experience, it felt more difficult than many CKA-style tasks. Below are focused recommendations to maximize your score and efficiency.

## 1) Know the documentation and how to navigate it

You don't need to memorize every API field (for example, a complete VirtualService spec). What you must master is how to quickly find the relevant docs and examples. The ICA interface often includes direct links to the relevant [Istio docs](https://istio.io/latest/docs/) for the resource referenced in a task (for example, VirtualService). Use those links as your starting point — they provide resource definitions and examples, but rarely contain the exact YAML you need for the task.

> **lightbulb** Familiarize yourself with the structure of the [Istio documentation](https://istio.io/latest/docs/) (resources, examples, and diagnostics). Knowing where to look saves significant time under exam pressure.

## 2) Use a sufficiently large screen when possible

If allowed, use a larger display (27" or similar). The exam UI typically splits the problem panel, countdown/proctor windows, and the remote session (terminal + browser). On a small laptop screen you'll waste time switching panes and making edits. Check proctor requirements carefully before the exam.

> **warning** Proctors often disallow additional monitors. You may be required to disconnect extra displays and demonstrate your setup. Verify the exam rules before you start.

## 3) Practical editing — know Vim (or be very efficient with your editor)

You will edit a lot of YAML. Vim provides rapid navigation and editing for multi-line files and bulk substitutions. Nano works, but is slower for repetitive edits.

Example — a typical nginx Deployment you may need to edit:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

<Frame>
  <img alt="The image is a cheat sheet summarizing various commands and shortcuts for using the Vim text editor, organized into sections such as Text Manipulation, Visual Mode, and Save & Exit." />
</Frame>

Tips for editor efficiency:

* Learn basic motions (h/j/k/l), word jumps (`w`, `b`), line edits (`^`, `$`), visual select (`v`), and substitutions (`:%s/old/new/g`).
* Use yank/paste registers when copying blocks of YAML.
* Use `:set number` and `:set paste` as needed to ease editing multi-line content pasted from the browser.

## 4) Run istioctl analyze after applying resources

`istioctl analyze` quickly surfaces common configuration issues (mismatched ports, bad hosts, invalid fields). Always run it immediately after `kubectl apply` to catch errors before you do other debugging.

Example workflow:

```bash theme={null}
$ mkdir 1.1
$ cd 1.1
$ vim virtual_svc.yaml
$ kubectl apply -f virtual_svc.yaml
$ istioctl analyze -n <namespace>
No validation issues found when analyzing namespace: <namespace>
```

Replace the backticked placeholder with the actual namespace in the command above: `istioctl analyze -n \`\<namespace>\`\`.

> **lightbulb** Run `istioctl analyze` right after applying resources to detect issues such as a VirtualService pointing to a non-existent service/port or invalid spec fields.

## 5) SSH workflow per question — exit when finished

Each ICA question runs on a separate remote host. You must SSH into the host for the current question, perform the task there, then exit. If you forget to exit a session and reuse it for the next question, you risk applying resources to the wrong environment and losing points.

Example SSH flow:

```bash theme={null}
$ ssh 000v3021
