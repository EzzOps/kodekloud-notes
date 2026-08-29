# (Example log output for a 5-second time window)
I0419 15:56:11.117300  57 logs_generator.go:67] 521 POST /api/v1/namespaces/kube-system/pods/cs3 395
I0419 15:56:11.117287  57 logs_generator.go:67] 522 POST /api/v1/namespaces/kube-system/pods/rs 498
I0419 15:56:11.117273  57 logs_generator.go:67] 523 GET /api/v1/namespaces/default/pods/ijb 435
I0419 15:56:11.117292  57 logs_generator.go:67] 524 POST /api/v1/namespaces/default/pods/678 453
I0419 15:56:14.117276  57 logs_generator.go:67] 525 GET /api/v1/namespaces/kube-system/pods/xppk 375
I0419 15:56:16.117263  57 logs_generator.go:67] 526 POST /api/v1/namespaces/default/pods/xrtc 325
I0419 15:56:16.117268  57 logs_generator.go:67] 527 GET /api/v1/namespaces/default/pods/p2j 435
I0419 15:56:17.117292  57 logs_generator.go:67] 528 POST /api/v1/namespaces/kube-system/pods/4dic 337
I0419 15:56:17.117298  57 logs_generator.go:67] 529 GET /api/v1/namespaces/default/pods/qy9l 268
I0419 15:56:18.117281  57 logs_generator.go:67] 530 GET /api/v1/namespaces/ns/pods/sxn 302
I0419 15:56:18.117291  57 logs_generator.go:67] 531 PUT /api/v1/namespaces/ns/pods/ken 406
I0419 15:56:18.117290  57 logs_generator.go:67] 532 GET /api/v1/namespaces/ns/pods/kan3 415
I0419 15:56:19.117287  57 logs_generator.go:67] 533 GET /api/v1/namespaces/kube-system/pods/ks1 536
I0419 15:56:19.117275  57 logs_generator.go:67] 534 POST /api/v1/namespaces/default/pods/ijf 411
I0419 15:56:20.117280  57 logs_generator.go:67] 536 GET /api/v1/namespaces/default/pods/vbs 358
I0419 15:56:20.117276  57 logs_generator.go:67] 537 POST /api/v1/namespaces/kube-system/pods/05h3 415
I0419 15:56:20.117268  57 logs_generator.go:67] 538 GET /api/v1/namespaces/ns/pods/k61 231
I0419 15:56:21.117259  57 logs_generator.go:67] 539 GET /api/v1/namespaces/ns/pods/bcr1 536
I0419 15:56:21.117274  57 logs_generator.go:67] 540 PUT /api/v1/namespaces/default/pods/qk2 406
I0419 15:56:24.117279  57 logs_generator.go:67] 541 GET /api/v1/namespaces/kube-system/pods/h7k 583
I0419 15:56:34.117288  57 logs_generator.go:67] 542 POST /api/v1/namespaces/ns/pods/nk9 399
I0419 15:56:34.117285  57 logs_generator.go:67] 543 GET /api/v1/namespaces/kube-system/pods/q3nk 343
I0419 15:56:35.117296  57 logs_generator.go:67] 544 POST /api/v1/namespaces/default/pods/rrn9 272
I0419 15:56:35.117276  57 logs_generator.go:67] 545 PUT /api/v1/namespaces/ns/pods/v2n 364
I0419 15:56:35.117275  57 logs_generator.go:67] 546 GET /api
```

You can easily extend the time window as necessary. To capture logs from the past 10 seconds (or even up to 1 hour), adjust the value provided to the `--since` flag accordingly. Below is an example capturing logs over a longer period:

```bash theme={null}
# (Example log output for an extended time window)
I0419 15:56:17.117300  57 logs_generator.go:67] 531 PUT /api/v1/namespaces/default/pods/clbg 268
I0419 15:56:18.117278  57 logs_generator.go:67] 532 GET /api/v1/namespaces/ns/pods/o3l 436
I0419 15:56:18.117279  57 logs_generator.go:67] 533 POST /api/v1/namespaces/ns/pods/sxwn 302
I0419 15:56:18.117286  57 logs_generator.go:67] 534 PUT /api/v1/namespaces/default/pods/6nk 406
I0419 15:56:19.117282  57 logs_generator.go:67] 535 POST /api/v1/namespaces/default/pods/qq8 241
I0419 15:56:20.117276  57 logs_generator.go:67] 536 PUT /api/v1/namespaces/default/pods/oh5a 415
I0419 15:56:21.117265  57 logs_generator.go:67] 537 GET /api/v1/namespaces/ns/pods/k6l 231
I0419 15:56:21.117270  57 logs_generator.go:67] 538 POST /api/v1/namespaces/kube-system/pods/bcr1 536
I0419 15:56:23.117292  57 logs_generator.go:67] 539 GET /api/v1/namespaces/default/pods/ijf 411
I0419 15:56:24.117279  57 logs_generator.go:67] 540 GET /api/v1/namespaces/pods/hdv 583
I0419 15:56:25.117260  57 logs_generator.go:67] 541 GET /api/v1/namespaces/kube-system/pods/nk9 399
I0419 15:56:25.117264  57 logs_generator.go:67] 542 GET /api/v1/namespaces/default/pods/h38 229
I0419 15:56:25.117268  57 logs_generator.go:67] 543 POST /api/v1/namespaces/kube-system/pods/qhk 343
I0419 15:56:26.117262  57 logs_generator.go:67] 544 PUT /api/v1/namespaces/ns/pods/gqh 255
I0419 15:56:26.117277  57 logs_generator.go:67] 545 GET /api/v1/namespaces/ns/pods/q3nk 272
I0419 15:56:26.117285  57 logs_generator.go:67] 546 PUT /api/v1/namespaces/default/pods/908j 338
I0419 15:56:26.117291  57 logs_generator.go:67] 547 GET /api/v1/namespaces/ns/pods/q3nk 343
I0419 15:56:27.117300  57 logs_generator.go:67] 548 POST /api/v1/namespaces/kube-system/pods/lobp 375
I0419 15:56:27.117285  57 logs_generator.go:67] 549 PUT /api/v1/namespaces/default/pods/hmkd 438
I0419 15:56:27.117292  57 logs_generator.go:67] 550 GET /api/v1/namespaces/kube-system/pods/n8bz 513
I0419 15:56:32.117271  57 logs_generator.go:67] 551 POST /api/v1/namespaces/kube-system/pods/c4f 345
I0419 15:56:32.117281  57 logs_generator.go:67] 552 PUT /api/v1/namespaces/default/pods/52b5 513
I0419 15:56:35.117280  57 logs_generator.go:67] 553 GET /api/v1/namespaces/kube-system/pods/rFw4 529
I0419 15:56:35.117284  57 logs_generator.go:67] 554 GET /api/v1/namespaces/ns/pods/rg94 488
I0419 15:56:36.117276  57 logs_generator.go:67] 555 GET /api/v1/n
```

Adjusting the `--since` flag allows you to tailor the log output to the exact timeframe you need for effective troubleshooting.

***

## Summary

By adding the `--timestamps` flag to your kubectl logs command, you enrich your log data with temporal context, which is essential for diagnosing issues in real time. Additionally, leveraging the `--since` flag lets you filter logs to a specific duration, simplifying the process of pinpointing errors or warnings.

For more detailed information on Kubernetes log management and best practices, refer to the [Kubernetes Documentation](https://kubernetes.io/docs/).

> **lightbulb** Both flags are crucial in environments with high logging volumes where pinpointing the exact moment of an issue can lead to faster resolutions.

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-troubleshooting-for-application-developers/module/09c2c8a6-ba29-4d55-bea1-cd8584be9107/lesson/8c0130ec-31e4-4e87-b996-8d8e1fb27fad)


# kubectl logs

Source: https://notes.kodekloud.com/docs/Kubernetes-Troubleshooting-for-Application-Developers/Prerequisites/kubectl-logs/page

This guide explores the `kubectl logs` command for retrieving logs from Kubernetes pods to aid in troubleshooting applications.

In this guide, we explore one of the fundamental Kubernetes troubleshooting commands: `kubectl logs`. Retrieving logs is often the first step when debugging issues with applications running in Kubernetes pods.

## Basic Log Retrieval

To view the logs for a specific pod, use the following command:

```bash theme={null}
kubectl logs
```

Typically, you will specify the namespace (if needed) and the pod's name. For instance, consider a pod named `notes-app-deployment-d4fcc5ccd-5fl7z` running in the `uat` namespace. Execute the following command to retrieve its logs:

```bash theme={null}
controlplane ~ ➜ k logs -n uat notes-app-deployment-d4fcc5ccd-5fl7z
> notes-app@1.0.0 start /app
> node app.js
App is running on port 3000
controlplane ~ ➜
```

The output above shows the log messages produced during the startup of the application.

> **lightbulb** For a complete list of `kubectl logs` options and other Kubernetes commands, check out the [Kubernetes Documentation](https://kubernetes.io/docs/).

## Viewing Logs in Multicontainer Pods

In more advanced scenarios, a pod may run multiple containers (e.g., an init container, a sidecar container, and the main application container). When you need to retrieve logs from all containers simultaneously, use the `--all-containers` flag:

```bash theme={null}
controlplane ~ → k logs -n uat notes-app-deployment-d4fcc5ccd-5fl7z
> notes-app@1.0.0 start /app
> node app.js

App is running on port 3000

controlplane ~ → k logs -n uat notes-app-deployment-d4fcc5ccd-5fl7z --all-containers
> notes-app@1.0.0 start /app
> node app.js

App is running on port 3000

controlplane ~ → k get pods
NAME                READY   STATUS    RESTARTS   AGE
logs-generator      1/1     Running   1 (6m25s ago)   16m
multi-container-pod 2/2     Running   0          7m54s

controlplane ~ →
```

While this approach consolidates logs from every container in the pod, it may become challenging to determine the source container for each log entry.

> **triangle-alert** Avoid using `--all-containers` when you need to diagnose issues specific to a single container. Explicitly targeting a container clarifies the troubleshooting process.

## Retrieving Container-Specific Logs

To view logs for a particular container in a multicontainer pod, use the `-c` flag along with the container’s name. First, determine the container names from the pod specification using a JSONPath query:

```bash theme={null}
k get pod multi-container-pod -o jsonpath='{.spec.containers}'
```

For a more readable output, pipe the result to `jq`:

```bash theme={null}
k get pod multi-container-pod -o jsonpath='{.spec.containers}' | jq
```

This command will list containers such as `nginx-container` and `cron-logger`.

### Example: Viewing Logs for nginx-container

To see the logs from the `nginx-container`, run:

```bash theme={null}
controlplane ~ ➜ k logs multi-container-pod -c nginx-container
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/04/06 22:42:21 [notice] 1#1: using the "epoll" event method
2024/04/06 22:42:21 [notice] 1#1: nginx/1.25.4
2024/04/06 22:42:21 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2024/04/06 22:42:21 [notice] 1#1: OS: Linux 5.4.0-1106-gcp
2024/04/06 22:42:21 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/04/06 22:42:21 [notice] 1#1: start worker processes
2024/04/06 22:42:21 [notice] 1#1: start worker process 79
2024/04/06 22:42:21 [notice] 1#1: start worker process 80
2024/04/06 22:42:21 [notice] 1#1: start worker process 81
2024/04/06 22:42:21 [notice] 1#1: start worker process 83
2024/04/06 22:42:21 [notice] 1#1: start worker process 84
2024/04/06 22:42:21 [notice] 1#1: start worker process 86
2024/04/06 22:42:21 [notice] 1#1: start worker process 87
2024/04/06 22:42:21 [notice] 1#1: start worker process 89
2024/04/06 22:42:21 [notice] 1#1: start worker process 91
2024/04/06 22:42:21 [notice] 1#1: start worker process 92
2024/04/06 22:42:21 [notice] 1#1: start worker process 93
2024/04/06 22:42:21 [notice] 1#1: start worker process 94
controlplane ~ ➜
```

### Example: Viewing Logs for cron-logger

If you need logs for the `cron-logger` container, execute:

```bash theme={null}
controlplane ~ ✗ k logs multi-container-pod -c cron-logger
Cron logger started. Logging messages every 10 seconds.
Sat Apr  6 22:42:21 UTC 2024 - Regular log message.
Sat Apr  6 22:42:22 UTC 2024 - Regular log message.
Sat Apr  6 22:42:23 UTC 2024 - Regular log message.
Sat Apr  6 22:42:24 UTC 2024 - Regular log message.
Sat Apr  6 22:42:25 UTC 2024 - Regular log message.
Sat Apr  6 22:42:26 UTC 2024 - Regular log message.
Sat Apr  6 22:42:27 UTC 2024 - Regular log message.
Sat Apr  6 22:42:28 UTC 2024 - Regular log message.
```

By using the `-c` flag, you can accurately isolate logs for individual containers within a multicontainer pod. This separation is vital for efficient troubleshooting and gaining targeted insights into each container's behavior.

## Conclusion

Using `kubectl logs` is an integral part of managing and troubleshooting Kubernetes applications. Whether you are working with single-container pods or more complex multicontainer setups, understanding how to access and interpret logs will significantly enhance your ability to diagnose and resolve application issues.

For further details and advanced use cases, visit the official [Kubernetes Documentation](https://kubernetes.io/docs/).

Happy troubleshooting!

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-troubleshooting-for-application-developers/module/09c2c8a6-ba29-4d55-bea1-cd8584be9107/lesson/8d1b7b1f-3a2c-40f2-b5da-e979a842c9b8)
