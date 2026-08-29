# kubectl logs timestamps

Source: https://notes.kodekloud.com/docs/Kubernetes-Troubleshooting-for-Application-Developers/Prerequisites/kubectl-logs-timestamps/page

This article explains how to use timestamps with kubectl logs for better Kubernetes troubleshooting and filtering log output by time.

In this lesson, we explore how to enhance your Kubernetes troubleshooting by displaying timestamps with the kubectl logs command and filtering log output by time. By incorporating timestamps, you gain valuable insight into when each log entry was generated, making it easier to diagnose issues effectively.

***

## Displaying Timestamps with kubectl logs

To include timestamps in your pod logs, simply add the `--timestamps` flag. This flag appends the generation time to each log entry, providing vital context during troubleshooting.

```bash theme={null}
kubectl logs --timestamps
```

For instance, when examining logs from an NGINX Ingress controller pod, you will see timestamps displayed alongside the application logs.

> **lightbulb** Using timestamps along with log output is particularly useful for correlating log entries with system events or errors.

***

## Logs Without Timestamps

In some scenarios, your logging configuration might exclude timestamps. Consider the following example where log entries do not show timestamp information:

```bash theme={null}
controlplane ~ ➜  k logs -n ingress-nginx ingress-nginx-controller-647b798f59-ljfpt
NGINX Ingress controller
Release:         v1.1.3
Build:           9da328519a70452439c75b947e2189406565ab
Repository:      https://github.com/kubernetes/ingress-nginx
nginx version:   nginx/1.19.10
----------------------------------------------------
W0419 15:32:39.010550  57 client_config.go:615] Neither --kubeconfig nor --master was specified. Using the inClusterConfig. This might not work.
I0419 15:32:39.017167  57 main.go:223] "Creating API client" host="https://10.96.0.1:443"
I0419 15:32:39.207869  57 main.go:104] "SSL fake certificate created" file="/etc/ingress-controller/ssl/default-fake-certificate.pem"
I0419 15:32:39.227060  57 ssl.go:531] "loading tls certificate" path="/usr/local/certificates/cert" key="/usr/local/certificates/key"
I0419 15:32:39.268151  57 nginx.go:255] "Starting NGINX Ingress controller"
I0419 15:32:39.276038  57 event.go:282] Event(v1.ObjectReference{Kind:"ConfigMap", Namespace:"ingress-nginx", Name:"ingress-nginx-controller", UID:"9de694e8-400c-4843-8c0b-658dc430684", APIVersion:"v1", ResourceVersion:"1262", FieldPath:""}): type: 'Normal' reason: 'CREATE' ConfigMap ingress-nginx/ingress-nginx-controller
I0419 15:32:40.469435  57 nginx.go:298] "Starting NGINX process"
I0419 15:32:40.469674  57 leader_election.go:248] attempting to acquire leader lease ingress-nginx/ingress-controller-leader...
I0419 15:32:40.469993  57 nginx.go:318] "Starting validation webhook" address=":8443" certPath="/usr/local/certificates/key"
I0419 15:32:40.470219  57 controller.go:159] "Configuration changes detected, backend reload required"
I0419 15:32:40.479177  57 leader_election.go:258] successfully acquired lease ingress-nginx/ingress-controller-leader
I0419 15:32:40.487134  57 status.go:214] "POD is not ready" pod="ingress-nginx/ingress-nginx-controller-647b798f59-ljfpt" node="node01"
I0419 15:32:40.565735  57 controller.go:167] "Backend successfully reloaded"
I0419 15:32:40.566565  57 event.go:82] Event(v1.ObjectReference{Kind:"Pod", Namespace:"ingress-nginx", Name:"ingress-nginx-controller-647b798f59-ljfpt", UID:"84c80801-fc3d-4399-b1dc-80ab8411bcc1", APIVersion:"v1", ResourceVersion:"1307", FieldPath:""}): type: 'Normal' reason: 'RELOAD' NGINX reload triggered due to a change in configuration

controlplane ~ ➜
```

Even when log entries lack timestamps in the output, the container runtime retains the timestamp metadata. This metadata can be valuable for backend systems and further analysis.

A similar case arises with application logs from a Notes app:

```bash theme={null}
controlplane ~ ➜  k logs -n uat notes-app-deployment-d4fcc5ccd-n7nm8
> notes-app@1.0.0 start /app
> node app.js
App is running on port 3000
```

To integrate timestamps, re-run the command with the `--timestamps` flag.

***

## Filtering Logs by Relative Time

In addition to appending timestamps, you can filter log outputs based on a specific timeframe using the `--since` flag. This capability assists in narrowing down log entries to a relevant period, saving time during troubleshooting.

For example, if your pod generates logs every second and you need to inspect the logs from the past 5 seconds, you can run:

```bash theme={null}
kubectl logs --since=5s
```

Below is an example output for a 5-second window:

```bash theme={null}
