# Example etcd service configuration
ExecStart=/usr/local/bin/etcd \
  --name ${ETCD_NAME} \
  --cert-file=/etc/etcd/kubernetes.pem \
  --key-file=/etc/etcd/kubernetes-key.pem \
  --peer-cert-file=/etc/etcd/kubernetes.pem \
  --peer-key-file=/etc/etcd/kubernetes-key.pem \
  --trusted-ca-file=/etc/etcd/ca.pem \
  --peer-trusted-ca-file=/etc/etcd/ca.pem \
  --peer-client-cert-auth \
  --client-cert-auth \
  --initial-advertise-peer-urls https://${INTERNAL_IP}:2380 \
  --listen-peer-urls https://${INTERNAL_IP}:2380 \
  --listen-client-urls https://${INTERNAL_IP}:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://${INTERNAL_IP}:2379 \
  --initial-cluster-token etcd-cluster-0 \
  --initial-cluster controller-0=https://${CONTROLLER0_IP}:2380,controller-1=https://${CONTROLLER1_IP}:2380 \
  --initial-cluster-state new \
  --data-dir=/var/lib/etcd
```

<Callout icon="lightbulb">
  For detailed information on configuring TLS certificates, refer to the Kubernetes documentation on [TLS Configuration](https://kubernetes.io/docs/concepts/cluster-administration/transport-layer-security/). Adjust certificate parameters according to your security requirements.
</Callout>

***

## High Availability Considerations

In a production Kubernetes environment, high availability (HA) is paramount. By running multiple master nodes with corresponding etcd instances, you ensure that your cluster remains resilient even if one node fails.

To enable HA, each etcd instance must know about its peers. This is achieved by configuring the `--initial-cluster` parameter with the details of each member in the cluster. For example:

```bash theme={null}
ExecStart=/usr/local/bin/etcd \
  --name ${ETCD_NAME} \
  --cert-file=/etc/etcd/kubernetes.pem \
  --key-file=/etc/etcd/kubernetes-key.pem \
  --peer-cert-file=/etc/etcd/kubernetes.pem \
  --peer-key-file=/etc/etcd/kubernetes-key.pem \
  --trusted-ca-file=/etc/etcd/ca.pem \
  --peer-trusted-ca-file=/etc/etcd/ca.pem \
  --peer-client-cert-auth \
  --client-cert-auth \
  --initial-advertise-peer-urls=https://${INTERNAL_IP}:2380 \
  --listen-peer-urls=https://${INTERNAL_IP}:2380 \
  --advertise-client-urls=https://${INTERNAL_IP}:2379 \
  --initial-cluster-token=etcd-cluster-0 \
  --initial-cluster controller-0=https://${CONTROLLER0_IP}:2380,controller-1=https://${CONTROLLER1_IP}:2380 \
  --initial-cluster-state=new \
  --data-dir=/var/lib/etcd
```

<Callout icon="lightbulb">
  In some deployments, you may use separate certificate files for peer communications (e.g., `/etc/etcd/peer.pem` and `/etc/etcd/peer-key.pem`). Always tailor these settings to match your desired security posture.
</Callout>

***

## Deploying etcd with kubeadm

For many test environments and streamlined deployments, kubeadm automatically configures etcd. When you use kubeadm, the etcd server runs as a pod within the kube-system namespace, abstracting away the manual setup details.

To view all the pods running in the kube-system namespace, including etcd, run:

```bash theme={null}
kubectl get pods -n kube-system
```

Example output:

```text theme={null}
NAMESPACE     NAME                                 READY   STATUS      RESTARTS   AGE
kube-system   coredns-78fcdf6894-prwl              1/1     Running     0          1h
kube-system   coredns-78fcdf6894-vqd9w             1/1     Running     0          1h
kube-system   etcd-master                          1/1     Running     0          1h
kube-system   kube-apiserver-master                1/1     Running     0          1h
kube-system   kube-controller-manager-master       1/1     Running     0          1h
kube-system   kube-proxy-f6k26                     1/1     Running     0          1h
kube-system   kube-proxy-hnzw                      1/1     Running     0          1h
kube-system   kube-scheduler-master                1/1     Running     0          1h
kube-system   weave-net-924k8                      2/2     Running     1          1h
kube-system   weave-net-hzfcz                      2/2     Running     1          1h
```

To examine the keys stored in etcd (organized under the registry directory), use the following command:

```bash theme={null}
kubectl exec etcd-master -n kube-system -- etcdctl get / --prefix --keys-only
```

Sample output:

```text theme={null}
/registry/apiregistration.k8s.io/apiservices/v1
/registry/apiregistration.k8s.io/apiservices/v1.apps
/registry/apiregistration.k8s.io/apiservices/v1.authentication.k8s.io
/registry/apiregistration.k8s.io/apiservices/v1.authorization.k8s.io
/registry/apiregistration.k8s.io/apiservices/v1.autoscaling
/registry/apiregistration.k8s.io/apiservices/v1.batch
/registry/apiregistration.k8s.io/apiservices/v1.networking.k8s.io
/registry/apiregistration.k8s.io/apiservices/v1.rbac.authorization.k8s.io
/registry/apiregistration.k8s.io/apiservices/v1beta1.admissionregistration.k8s.io
```

The etcd root directory, organized as the registry, contains subdirectories for various Kubernetes components such as nodes, pods, ReplicaSets, and Deployments.

***

## Conclusion

In this article, we examined etcd’s essential role in Kubernetes by exploring both manual deployment and automated configuration with kubeadm. We also discussed best practices for configuring high availability in multi-master environments. As you advance, further exploration into HA configurations and enhanced security measures will help you operate a robust and resilient Kubernetes cluster.

For more in-depth resources, check out:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/c6d2ac7d-8192-4cff-aa54-e36d888c5bd9/lesson/a3ab7ad6-62ac-4205-86a5-e977443679e8" />
</CardGroup>


# Imperative vs Declarative

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Core-Concepts/Imperative-vs-Declarative/page

This article explores imperative and declarative approaches to managing Kubernetes objects, highlighting their benefits, drawbacks, and ideal use cases.

In this lesson, we explore the two core approaches used to manage Kubernetes objects: imperative and declarative. By understanding these methods and their respective benefits and drawbacks, you'll be better equipped to manage your clusters and prepare for Kubernetes certification exams.

So far, we have covered creating and managing Kubernetes objects either by directly issuing commands or by using configuration files. These approaches fall into two broad categories in the infrastructure-as-code domain: imperative and declarative.

## An Analogy

Imagine visiting a friend’s house. In the past, you might have taken a taxi and given the driver precise, step-by-step directions—for example, "Take a right onto Street B, then left onto Street C, another left onto Street D, and finally stop at the house." This sequence of detailed instructions illustrates the imperative approach.

<Frame>
  ![The image shows two navigation maps: one with imperative directions and another with declarative directions, illustrating different ways to guide someone to a destination.](https://kodekloud.com/kk-media/image/upload/v1752869717/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Imperative-vs-Declarative/frame_60.jpg)
</Frame>

Today, using an app like Uber, you simply enter your final destination. This is akin to the declarative approach where you specify the desired outcome—"Drive to Tom's house"—and the system figures out the best route.

<Frame>
  ![The image compares imperative and declarative directions using maps, showing step-by-step navigation versus a direct destination approach.](https://kodekloud.com/kk-media/image/upload/v1752869718/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Imperative-vs-Declarative/frame_90.jpg)
</Frame>

## Imperative vs Declarative: Kubernetes Perspective

### Imperative Approach

The imperative approach in Kubernetes involves executing specific commands to create, update, or delete objects. This method instructs Kubernetes on both what needs to be done and how it should be done. For example, you might run these commands:

```bash theme={null}
kubectl run --image=nginx nginx
kubectl create deployment --image=nginx nginx
kubectl expose deployment nginx --port 80
kubectl edit deployment nginx
kubectl scale deployment nginx --replicas=5
kubectl set image deployment nginx nginx=nginx:1.18
kubectl create -f nginx.yaml
kubectl replace -f nginx.yaml
kubectl delete -f nginx.yaml
```

While the imperative approach is effective for quick tasks, it comes with some limitations:

* If a command partially executes, running it again may require extra checks (e.g., verifying if a resource already exists).
* Updating resources—such as changing the image version—demands explicit re-execution with live adjustments.
* Commands executed interactively are often not persisted, making it challenging for teammates to trace the system’s original state.

In Kubernetes, imperative commands like `kubectl run`, `kubectl create deployment`, `kubectl expose`, and even editing commands such as `kubectl edit` or scaling commands are excellent for immediate changes but require careful tracking of the current state.

<Frame>
  ![The image compares imperative and declarative approaches in Infrastructure as Code, detailing steps for setting up an NGINX server on a virtual machine.](https://kodekloud.com/kk-media/image/upload/v1752869719/notes-assets/images/CKA-Certification-Course-Certified-Kubernetes-Administrator-Imperative-vs-Declarative/frame_240.jpg)
</Frame>

### Declarative Approach

The declarative approach enables you to specify the desired state of your infrastructure through configuration files (typically written in YAML). For example, defining a pod in a file (nginx.yaml) looks like this:

```yaml theme={null}
