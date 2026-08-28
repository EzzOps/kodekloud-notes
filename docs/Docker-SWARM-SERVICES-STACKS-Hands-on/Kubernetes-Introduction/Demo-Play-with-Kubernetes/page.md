# Demo Play with Kubernetes

Source: https://notes.kodekloud.com/docs/Docker-SWARM-SERVICES-STACKS-Hands-on/Kubernetes-Introduction/Demo-Play-with-Kubernetes/page

This article provides a step-by-step guide to setting up a Kubernetes test environment using PlayWithK8s.com for experimenting without infrastructure.

Welcome to this comprehensive lesson on setting up a Kubernetes test environment using PlayWithK8s.com. In this guide, you'll quickly learn how to experiment with Kubernetes without needing your own infrastructure or a public cloud account by following a step-by-step procedure similar to our previous demos, with environment-specific adjustments.

<Frame>
  ![The image is a slide titled "DEMO" outlining steps for setting up a Kubernetes test environment, creating pods, and services with ClusterIP and LoadBalancer.](https://kodekloud.com/kk-media/image/upload/v1752874109/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Play-with-Kubernetes/frame_10.jpg)
</Frame>

When you navigate to PlayWithK8s.com, you'll get free access to Kubernetes clusters with sessions lasting four hours. Simply click on "Add New Instance" to provision a cluster instance and begin your tests immediately.

<Frame>
  ![The image shows a Kubernetes login page with a reCAPTCHA verification, featuring the Kubernetes logo and branding by Google.](https://kodekloud.com/kk-media/image/upload/v1752874111/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Play-with-Kubernetes/frame_80.jpg)
</Frame>

Once logged in, you'll notice a session timer counting down from four hours. This environment is ideal for quick tests and experiments.

***

## Initializing the Kubernetes Cluster

Begin by initializing your Kubernetes cluster using the provided YAML definition files from previous demos. Execute the following commands on your provisioned instance:

```bash theme={null}
kubeadm init --apiserver-advertise-address $(hostname -i)

kubectl apply -n kube-system -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

curl -L -s https://raw.githubusercontent.com[AWS_SECRET_ACCESS_KEY]recommended/kubernetes-dashboard.yaml | sed 's/targetPort: 8443/targetPort: 8443\n  type: LoadBalancer/' | kubectl apply -f -
```

After executing these commands, you should see output similar to the snippet below:

```plaintext theme={null}
[apiclient] All control plane components are healthy after 36.501139 seconds
[token] Using token: 0f5aa8.4abec8c7a16185d
[apiconfig] Created RBAC rules
[addons] Applied essential addon: kube-proxy
[addons] Applied essential addon: kube-dns

Your Kubernetes master has initialized successfully!
To start using your cluster, you need to run (as a regular user):
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
http://kubernetes.io/docs/admin/addons/

You can now join any number of machines by running the following on each node as root:
kubeadm join --token 0f5aa8.4abec8c7a16185d 10.0.63.4:6443
```

The second command sets up the networking for your cluster. In this demo, we'll skip the optional deployment of the Kubernetes Dashboard. Once your master node is running and networking is configured, you are ready to deploy your application.

***

## Cloning the Application Repository

Next, clone our GitHub repository containing the Kubernetes YAML files for a sample voting application. First, ensure that Git is installed on your instance:

```bash theme={null}
yum install git
```

Clone the repository using:

```bash theme={null}
git clone https://github.com/mmumshad/kubernetes-example-voting-app.git
```

After cloning, verify the repository contents:

```bash theme={null}
ls
```

You should see files such as:

* postgres-pod.yml
* redis-pod.yml
* result-app-pod.yml
* voting-app-pod.yml
* worker-app-pod.yml
* postgres-service.yml
* redis-service.yml
* result-app-service.yml
* voting-app-service.yml

<Frame>
  ![The image shows a GitHub repository page for a Kubernetes example voting app, with options to clone or download the repository.](https://kodekloud.com/kk-media/image/upload/v1752874112/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Play-with-Kubernetes/frame_210.jpg)
</Frame>

***

## Deploying the Voting Application

Start by deploying the voting app pod, then expose it through a service. Create the voting app pod with:

```bash theme={null}
kubectl create -f voting-app-pod.yml
```

Check the pod status:

```bash theme={null}
kubectl get pods
```

If the pod shows as "Pending", inspect further details with:

```bash theme={null}
kubectl describe pods voting-app-pod
```

<Callout icon="lightbulb">
  If you see an error about no available nodes that match the scheduling predicates, it may be because the master node is tainted by default.
</Callout>

Allow scheduling on the master node by removing the taint (replace \<nodeName> with your actual node name, e.g., "node1"):

```bash theme={null}
kubectl taint nodes <nodeName> node-role.kubernetes.io/master:NoSchedule-
```

Once untainted, verify that the pod transitions to a Running state:

```bash theme={null}
kubectl get pods
```

After confirming, create the service to expose the voting app:

```bash theme={null}
kubectl create -f voting-app-service.yml
```

Check that the service is running:

```bash theme={null}
kubectl get services
```

Click the link provided by PlayWithK8s.com to open the voting app in your browser.

***

## Deploying the Remaining Application Components

Deploy additional components required by the voting app, including Redis, Postgres, the worker, and the result app pods, along with their corresponding services. Execute the following commands one after another:

```bash theme={null}
kubectl create -f redis-pod.yml
kubectl create -f redis-service.yml

kubectl create -f postgres-pod.yml
kubectl create -f postgres-service.yml

kubectl create -f worker-app-pod.yml

kubectl create -f result-app-pod.yml
kubectl create -f result-app-service.yml
```

Monitor the status of all pods:

```bash theme={null}
kubectl get pods
```

A typical output might look like:

```plaintext theme={null}
NAME               READY   STATUS              RESTARTS   AGE
postgres-pod       1/1     Running             0          32s
redis-pod          1/1     Running             0          48s
result-app-pod     0/1     ContainerCreating   0          13s
voting-app-pod     1/1     Running             0          5m
worker-app-pod     0/1     ContainerCreating   0          21s
```

Once all pods are Running, check that the services are created:

```bash theme={null}
kubectl get services
```

Access the voting application via the external link. The interface should display the current vote counts (initially 50-50, before any votes are cast). Casting a vote (e.g., selecting "CATS" or "DOGS") will update the results as the services communicate.

<Frame>
  ![A web page titled "Cats vs Dogs!" with buttons to vote for either "CATS" or "DOGS," processed by a container ID.](https://kodekloud.com/kk-media/image/upload/v1752874113/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Play-with-Kubernetes/frame_620.jpg)
</Frame>

<Frame>
  ![The image shows a voting result with "Cats" at 0.0% and "Dogs" at 100.0%, with a total of 1 vote.](https://kodekloud.com/kk-media/image/upload/v1752874114/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Play-with-Kubernetes/frame_630.jpg)
</Frame>

***

## Deploying All Components Simultaneously

Instead of deploying resources individually, you can deploy all YAML files from the repository at once. Execute the following command from within the repository directory:

```bash theme={null}
kubectl create -f .
```

This command initiates all pods and services. Verify the deployment using:

```bash theme={null}
kubectl get pods
kubectl get services
```

A sample pods output might be:

```plaintext theme={null}
NAME               READY   STATUS    RESTARTS   AGE
postgres-pod       1/1     Running   0          11s
redis-pod          1/1     Running   0          11s
result-app-pod     1/1     Running   0          10s
voting-app-pod     1/1     Running   0          10s
worker-app-pod     1/1     Running   0          10s
```

***

## Resetting Your Environment

After the demo, you can clean up by deleting all deployed resources simultaneously. Run the following command:

```bash theme={null}
kubectl delete -f .
```

This command removes all specified resources (pods, services, etc.). Confirm deletion with:

```bash theme={null}
kubectl get pods
kubectl get services
```

<Frame>
  ![The image features a dark background with hexagonal patterns and a central text box stating "Reset - Delete all at once" in white font.](https://kodekloud.com/kk-media/image/upload/v1752874115/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Play-with-Kubernetes/frame_700.jpg)
</Frame>

A typical deletion output might be:

```plaintext theme={null}
pod "postgres-pod" deleted
service "db" deleted
pod "redis-pod" deleted
service "redis" deleted
pod "result-app-pod" deleted
service "result-service" deleted
pod "voting-app-pod" deleted
service "voting-service" deleted
pod "worker-app-pod" deleted
```

***

Thank you for following this demo on deploying an application using PlayWithK8s.com. We hope you found this guide helpful, and we look forward to supporting your next Kubernetes adventure.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/9b8ffcd1-c5b0-45d0-968d-55a5146c3e39/lesson/4b5effe9-243d-43c7-928c-4316db4f91ec" />
</CardGroup>
