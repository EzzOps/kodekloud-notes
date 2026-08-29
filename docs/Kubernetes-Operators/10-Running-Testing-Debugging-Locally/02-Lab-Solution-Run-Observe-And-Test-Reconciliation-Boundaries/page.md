# Lab Solution Run Observe And Test Reconciliation Boundaries

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Running-Testing-Debugging-Locally/Lab-Solution-Run-Observe-And-Test-Reconciliation-Boundaries/page

Shows a Kubernetes controller that recreates missing child resources from a WebApp blueprint but does not repair in-place spec drift of existing child resources

This lesson demonstrates the reconciliation boundaries of a Kubernetes-style controller: it will recreate a missing child resource derived from a WebApp blueprint, but it does not automatically repair an existing child that has drifted from the blueprint. The steps below provide reproducible evidence for both behaviors by running the controller locally and performing targeted changes in the cluster.

Observe controller logs

* Start your local manager (for example, `make run` or your preferred controller run command).
* Keep the logs visible so you can observe reconcile events while you perform the changes below.

Step 1 — Apply the namespace and WebApp blueprint

* The WebApp resource is the blueprint. The controller should create the Deployment, Service, and ConfigMap from that spec.

```bash theme={null}
