# (edit `spec.type: ClusterIP` to `spec.type: NodePort`, save and exit)
```

* After saving the edit you should see:

```text theme={null}
service/argocd-server edited
```

* Verify the service now shows a NodePort mapping:

```bash theme={null}
kubectl -n argocd get svc argocd-server
```

Example result:

```text theme={null}
NAME             TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)
argocd-server    NodePort   10.107.64.168   <none>        80:30880/TCP,443:31428/TCP
```

> **warning** Exposing `argocd-server` via `NodePort` is convenient for demos but not recommended for production. For production use, prefer an Ingress with TLS termination or a cloud load balancer and secure RBAC. Ensure firewall rules restrict access as needed.

6. Access the Argo CD UI in your browser

* Open the server using the NodePort on the node IP (or `localhost` if running a local cluster that maps ports):

* Example URLs:
  * `http://localhost:<NODEPORT>` (HTTP)
  * `https://localhost:<NODEPORT>` (HTTPS — default uses a self-signed certificate)

* Expect a browser security warning when using the self-signed certificate — proceed after accepting the warning for demo/testing.

<Frame>
  <img alt="The image shows a browser security warning stating &#x22;Your connection is not private&#x22; with options to learn more, enhance security, or return to safety." />
</Frame>

7. Retrieve the initial admin password

* The initial admin password is stored in the `argocd-initial-admin-secret` secret. To list available secrets and decode the admin password:

```bash theme={null}
# List secrets in argocd namespace
kubectl -n argocd get secret

# Decode the initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 --decode; echo
```

* Login credentials:
  * Username: `admin`
  * Password: (decoded value from the command above)

> **lightbulb** After the first login, change the `admin` password or create RBAC-backed users/service accounts. Leaving default credentials in place is a security risk.

8. Update the admin password via the UI

* After logging in with the initial password, open User Info (top-right), update your password to a secure value, and re-authenticate. The UI typically logs you out after a password change — sign back in with the new password.

<Frame>
  <img alt="The image shows the Argo CD application dashboard with no applications listed. There is a prompt to create a new application to start managing resources in the cluster." />
</Frame>

9. What’s next

* With Argo CD running and accessible, you can:
  * Create Argo CD Applications that point to Git repositories to manage cluster state.
  * Configure repositories, RBAC, and SSO (OIDC) for production-ready setups.
  * Integrate Argo CD with CI pipelines and cluster observability tools.

Links and references

* Argo CD Getting Started: [https://argo-cd.readthedocs.io/en/stable/getting\_started/](https://argo-cd.readthedocs.io/en/stable/getting_started/)
* Argo CD GitHub manifests: [https://github.com/argoproj/argo-cd/tree/v3.0.5/manifests](https://github.com/argoproj/argo-cd/tree/v3.0.5/manifests)

That’s all for this installation walkthrough.

- [Watch Video](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/b21feba6-d9f9-4b88-998e-c7f7e9a148d1)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/gitops-certified-associate-cgoa/module/09e1d9df-2018-4278-805d-983bcf7b23d2/lesson/8a1cc650-22f4-4f2e-b250-5133f9999233)


# Demo Manual Reconciliation

Source: https://notes.kodekloud.com/docs/Prep-Course-GitOps-Certified-Associate-CGOA/GitOps-Principles/Demo-Manual-Reconciliation/page

Demonstrates Argo CD GitOps manual reconciliation, showing how in-cluster changes cause OutOfSync and how syncing from Git restores desired state.

In this lesson we perform a manual reconciliation of an Argo CD application to illustrate why making ad-hoc changes directly in the Kubernetes cluster results in an OutOfSync state. You will:

* Confirm cluster namespaces.
* Synchronize an Argo CD application from Git.
* Inspect the resulting live resources.
* Make an intentional manual change in-cluster to cause drift.
* Observe Argo CD detecting the OutOfSync state and restore the desired state by synchronizing from Git.

## 1. Confirm existing namespaces

First, verify which namespaces are present in the cluster:

```bash theme={null}
