# Expected Output
NAME                        STATUS   ROLES   AGE    VERSION
aks-agentpool-14693408-0    Ready    agent   15m    v1.11.5
```

Additionally, you might encounter a snippet in a Kubernetes configuration file like:

```yaml theme={null}
apiVersion: apps/v1
```

Scroll to the bottom of the documentation (if referenced) for further instructions on connecting to your cluster. The Azure Cloud Shell comes pre-installed with the kubectl client, so you can quickly grant access to your cluster.

![The image shows a Microsoft Azure documentation page about connecting to a Kubernetes cluster using the Azure portal, featuring a screenshot of the Azure interface.](https://kodekloud.com/kk-media/image/upload/v1752884937/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-Azure-AKS/frame_210.jpg)

### Configuring kubectl in Cloud Shell

In the Cloud Shell window, execute the following command to configure kubectl. Replace "myResourceGroup" and "myAKSCluster" with your actual resource group and cluster names:

```bash theme={null}
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
```

After running the command, you will see messages similar to:

```bash theme={null}
Your cloud drive has been created in:
Subscription ID: a9415065-9776-4bf1-9708-80832eb4365d
Resource group: cloud-shell-storage-eus
Storage account: cs21032002001aa74
File share: cs-vpalazhica-gmail-com-10032002001aa74

Initializing your account for Cloud Shell...
Requesting a Cloud Shell...Succeeded.
Connecting terminal...

Welcome to Azure Cloud Shell
Type "az" to use Azure CLI
Type "help" to learn about Cloud Shell

aed2c8b3-0ba6-4e8f-b3b3-630db5d6Azure:~$
```

After configuring, verify connectivity by running:

```bash theme={null}
kubectl get nodes
```

For example, the output may appear as follows:

```bash theme={null}
NAME                            STATUS   ROLES   AGE     VERSION
aks-agentpool-29238863-vms00000   Ready    agent   6m12s   v1.16.10
```

## Deploying the Voting Application

With your single-node cluster up and running, it’s time to deploy the voting application. Follow these steps:

1. **Clone the Repository**: Clone the GitHub repository containing the application's YAML files.

   ```bash theme={null}
   git clone https://github.com/kodekloudhub/example-voting-app.git
   cd example-voting-app/k8s-specifications/
   ```

2. **Deploy the Application Components**: Execute the commands below in the order listed to deploy all necessary services and deployments:

   ```bash theme={null}
   kubectl create -f voting-app-deploy.yaml
   kubectl create -f voting-app-service.yaml
   kubectl create -f redis-deploy.yaml
   kubectl create -f redis-service.yaml
   kubectl create -f postgres-deploy.yaml
   kubectl create -f postgres-service.yaml
   kubectl create -f result-app-deploy.yaml   # Deploys the result app if provided.
   ```

3. **Verify Deployments**: Check the status of your deployments and services using:

   ```bash theme={null}
   kubectl get deployments,svc
   ```

   A typical output might be:

   ```bash theme={null}
   NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
   deployment.apps/postgres-deploy   1/1     1            1           96s
   deployment.apps/redis-deploy      1/1     1            1           104s
   deployment.apps/result-app-deploy 1/1     1            1           83s
   deployment.apps/voting-app-deploy 1/1     1            1           112s
   deployment.apps/worker-app-deploy 1/1     1            1           88s

   NAME                     TYPE         CLUSTER-IP      EXTERNAL-IP      PORT(S)           AGE
   service/db               ClusterIP    10.0.43.213     <none>           5432/TCP          93s
   service/kubernetes       ClusterIP    10.0.0.1        <none>           443/TCP           11m
   service/redis            ClusterIP    10.0.180.53     <none>           6379/TCP          101s
   service/result-service   LoadBalancer 10.1.1.176      52.152.245.94    80:30219/TCP       79s
   service/voting-service   LoadBalancer 10.0.100.120    52.152.240.186   80:32245/TCP       109s
   ```

> **lightbulb** In some cases, the result app service may initially show a pending state while the load balancer is being provisioned. Give it a few minutes to complete this process.

## Testing Your Deployment

Once all deployments are confirmed (each showing one out of one pod ready) and the load balancers for both the voting and result services have been provisioned, you can test the applications:

* Open your browser in a new tab to access the voting application using the external IP provided for the "voting-service".
* Similarly, open another tab to access the results application using the external IP of the "result-service".

![The image shows a split screen with equal blue and teal sections, labeled "CATS 50.0%" and "DOGS 50.0%".](https://kodekloud.com/kk-media/image/upload/v1752884938/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-Azure-AKS/frame_370.jpg)

Vote on the application and watch the result update in real time. This confirms that the applications are functioning correctly.

## Clean Up

After finishing your demonstration and learning session, remember to delete the cluster and clean up your resources to prevent any unexpected charges.

That concludes this Kubernetes on Azure AKS tutorial. Happy learning, and see you in the next guide!

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/2f291cbc-acc2-4250-b96c-2094daff556d/lesson/87c36f17-1717-4060-9d0a-a02377d17196)


# Kubernetes on GCP GKE

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/Kubernetes-on-the-Cloud/Kubernetes-on-GCP-GKE/page

Learn to deploy applications on Google Kubernetes Engine within Google

In this article, you will learn how to deploy your application on Google Kubernetes Engine (GKE) within the Google Cloud Platform (GCP). Before getting started, ensure you have access to a Google Cloud account. Google offers a 12-month free trial with a \$300 credit, which is sufficient for following along with this guide.

![The image describes Google Cloud's Free Tier, offering a 12-month trial with \$300 credit and limited free access to resources.](https://kodekloud.com/kk-media/image/upload/v1752884939/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_10.jpg)

A basic understanding of the GCP console and shell usage is essential, as you will configure the prerequisites directly in the cloud console.

> **lightbulb** Ensure you have:

  * A valid Google Cloud account.
  * Familiarity with GCP Console and basic terminal commands.

***

## Creating the Cluster

After logging into the GCP console, locate your project. In this example, we will use the project named "Example Voting App". Follow these steps to begin configuring GKE:

1. Click the navigation menu at the top left corner.
2. Under the **Compute** section, select **Kubernetes Engine**.
3. In the Kubernetes Engine section, click **Create Cluster**.

This action opens the Kubernetes cluster creation interface:

![The image shows the Google Cloud Platform interface, specifically the Kubernetes Engine section, with options to create a cluster, deploy a container, or take a quickstart.](https://kodekloud.com/kk-media/image/upload/v1752884940/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_60.jpg)

### Cluster Settings

* Rename the cluster to "Example Voting App".
* Use the default values for location type and zone.
* For the master version, you can either select a static version or a release channel for automatic upgrades. For this demonstration, leave it at the default setting.

Additional options are available for worker nodes, such as configuring the VM type or size; however, the default settings will suffice for this tutorial.

![The image shows a Google Kubernetes Engine (GKE) cluster setup interface, detailing options for naming, location type, zone, and master version selection.](https://kodekloud.com/kk-media/image/upload/v1752884941/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_90.jpg)

![The image shows a Google Cloud Platform interface for setting up a Kubernetes cluster, with options for naming, location type, and version selection.](https://kodekloud.com/kk-media/image/upload/v1752884943/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_110.jpg)

Once your configuration is complete, click **Create** to begin provision the cluster. Note that this process typically takes between 5 to 10 minutes. You can monitor the progress by clicking the Refresh button:

![The image shows the Google Cloud Platform interface for creating a Kubernetes cluster, with options for cluster basics, location, and master version settings.](https://kodekloud.com/kk-media/image/upload/v1752884944/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_130.jpg)

When the cluster setup is complete, you'll see a green check mark next to the cluster name.

***

## Connecting to Your Cluster

The simplest method to connect to your cluster is by clicking the **Connect** button:

![The image shows a Kubernetes clusters dashboard with one running cluster, displaying details like location, size, cores, and memory.](https://kodekloud.com/kk-media/image/upload/v1752884945/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_150.jpg)

Click **Connect** to display the command needed to configure `kubectl` using Cloud Shell. Once the Cloud Shell opens (you can maximize the window for convenience), run the provided command:

```bash theme={null}
gcloud container clusters get-credentials example-voting-app --zone us-central1-c --project example-voting-app-283506
```

This command updates your `kubectl` configuration, allowing you to interact with your GKE cluster. To verify the connection, run:

```bash theme={null}
kubectl get nodes
```

The output should look similar to this:

```bash theme={null}
NAME                                                  STATUS   ROLES    AGE   VERSION
gke-example-voting-app-default-pool-e388a8c8-46b0       Ready    <none>   86s   v1.14.10-gke.36
gke-example-voting-app-default-pool-e388a8c8-bjx4       Ready    <none>   95s   v1.14.10-gke.36
gke-example-voting-app-default-pool-e388a8c8-rp73       Ready    <none>   94s   v1.14.10-gke.36
```

***

## Deploying the Application

Now that your cluster is connected, you can deploy the YAML files for the various Deployments and Services that make up the voting application. These files are available in a GitHub repository. Follow the steps below in your Cloud Shell:

### Step 1. Clone the Repository

Execute the following commands to clone the repository and navigate into the project directory:

```bash theme={null}
git clone <repository-url>
cd example-voting-app
```

### Step 2. Navigate to the Kubernetes Specifications Directory

Change into the directory containing the deployment and service definitions:

```bash theme={null}
cd k8s-specifications
ls
```

You should see files similar to:

```bash theme={null}
postgres-deploy.yaml   redis-deploy.yaml   result-app-deploy.yaml   voting-app-deploy.yaml   worker-app-deploy.yaml
postgres-service.yaml  redis-service.yaml  result-app-service.yaml  voting-app-service.yaml
```

### Updating Service Definitions

To ensure the application works seamlessly in a cloud environment, a minor modification was made to the service definitions. For example, the voting service YAML now uses a LoadBalancer instead of a NodePort:

```yaml theme={null}
apiVersion: v1
kind: Service
metadata:
  name: voting-service
  labels:
    name: voting-service
    app: demo-voting-app
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 80
  selector:
    name: voting-app-pod
    app: demo-voting-app
```

A similar update applies to the result app service.

### Creating Kubernetes Objects

Create the Kubernetes objects in the order below to ensure proper dependency management:

1. Deploy the voting application and its corresponding service.
2. Deploy Redis (both deployment and service).
3. Deploy PostgreSQL (both deployment and service).
4. Deploy the worker application.
5. Deploy the result application and its corresponding service.

You can create each object individually:

```bash theme={null}
kubectl create -f voting-app-deploy.yaml
kubectl create -f voting-app-service.yaml
kubectl create -f redis-deploy.yaml
kubectl create -f redis-service.yaml
kubectl create -f postgres-deploy.yaml
kubectl create -f postgres-service.yaml
kubectl create -f worker-app-deploy.yaml
kubectl create -f result-app-deploy.yaml
kubectl create -f result-app-service.yaml
```

Alternatively, create all objects at once with:

```bash theme={null}
kubectl create -f .
```

After executing the creation commands, verify that the deployments and services have been successfully created:

```bash theme={null}
kubectl get deployments,svc
```

The output should resemble:

```bash theme={null}
NAME                                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.extensions/postgres-deploy        1/1     1            1           34s
deployment.extensions/redis-deploy           1/1     1            1           43s
deployment.extensions/result-app-deploy      1/1     1            1           20s
deployment.extensions/voting-app-deploy      1/1     1            1           52s
deployment.extensions/worker-app-deploy      0/1     1            0           26s

NAME                        TYPE          CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
service/db                 ClusterIP     10.71.3.164    <none>        5432/TCP        30s
service/kubernetes         ClusterIP     10.71.0.1      <none>        443/TCP         5m58s
service/redis              ClusterIP     10.71.2.124    <none>        6379/TCP        39s
service/result-service     LoadBalancer  10.71.3.179    <pending>     80:30764/TCP    13s
service/voting-service     LoadBalancer  10.71.0.147    <pending>     80:31036/TCP    48s
```

> **lightbulb** Note that the external IP for load balancers might initially show as `<pending>`. Wait a few minutes and rerun the command to confirm that the IPs have been assigned.

***

## Verifying Load Balancer Configuration

Once all deployments are ready and pods are running, verify the load balancer settings in the GCP console. Navigate to **Services & Ingress** under the Kubernetes Engine section. Here, you'll see internal services (such as PostgreSQL and Redis) and front-end services that utilize the cloud provider’s native load balancer.

![The image shows the Google Cloud Platform Kubernetes Engine interface, displaying services and ingress details for an "example-voting-app" with various endpoints and statuses.](https://kodekloud.com/kk-media/image/upload/v1752884946/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_420.jpg)

Click on each service to view detailed information including ClusterIP, load balancer IP, and URL endpoints. Ensure that all statuses are marked as OK.

***

## Testing the Application

After the load balancers are assigned external IPs, open a new browser tab and navigate to the external IP associated with the voting service to load the voting application interface. Open another tab to view the results application.

![The image shows a webpage titled "Cats vs Dogs!" with buttons to vote for either "CATS" or "DOGS," processed by a container ID.](https://kodekloud.com/kk-media/image/upload/v1752884947/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_480.jpg)

Cast a vote and observe that the results update dynamically to reflect the percentage of votes. Further voting should continuously update the displayed results.

![The image shows a voting result with "CATS" at 100% and "DOGS" at 0% on a blue background.](https://kodekloud.com/kk-media/image/upload/v1752884948/notes-assets/images/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial-Kubernetes-on-GCP-GKE/frame_500.jpg)

***

This guide has demonstrated the process of deploying a Kubernetes cluster on GKE and launching a multi-component voting application. Happy deploying, and stay tuned for more advanced Kubernetes tutorials!

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-for-the-absolute-beginners-hands-on-tutorial/module/2f291cbc-acc2-4250-b96c-2094daff556d/lesson/94a543ce-89a9-48e9-aedb-77a8b6b43f30)
