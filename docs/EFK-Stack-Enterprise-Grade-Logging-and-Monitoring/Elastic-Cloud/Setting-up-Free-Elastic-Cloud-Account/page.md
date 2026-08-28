# For more information see: https://www.elastic.co/guide/en/fleet/current/running-on-kubernetes-managed-by-fleet.html
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: elastic-agent
  namespace: kube-system
  labels:
    app: elastic-agent
spec:
  selector:
    matchLabels:
      app: elastic-agent
  template:
    metadata:
```

Below is the command to deploy the Elastic Agent:

```bash theme={null}
kubectl apply -f elastic-agent-managed-kubernetes.yml
```

Next, copy the complete YAML content from the page into a new file (e.g., `elastic-agent-managed-kubernetes.yml`). Ensure that your YAML file includes the necessary specifications for proper scheduling, such as tolerations for control-plane nodes, to ensure that metrics from Kubernetes control components (scheduler, controller manager) are collected:

```yaml theme={null}
spec:
  selector:
    matchLabels:
      app: elastic-agent
  template:
    metadata:
      labels:
        app: elastic-agent
  spec:
    # Tolerations are needed to run Elastic Agent on Kubernetes control-plane nodes.
    # Agents running on control-plane nodes collect metrics from the control plane
    # components (scheduler, controller manager) of Kubernetes.
    tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
    serviceAccountName: elastic-agent
```

Apply the updated configuration with:

```bash theme={null}
kubectl apply -f elastic-agent-managed-kubernetes.yml
```

## Step 3: Verify the Deployment

Once the deployment process is complete, verify that the Elastic Agent pods are running. Execute the following command:

```bash theme={null}
kubectl get pods -n kube-system
```

You should see output similar to this:

```bash theme={null}
NAME                                      READY   STATUS              RESTARTS   AGE
coredns-64d57b6bd-6nfr4                   1/1     Running             0          8m37s
coredns-64d57b6bd-h8742                   1/1     Running             0          8m37s
elastic-agent-mxmx4                       0/1     ContainerCreating   0          17s
elastic-agent-npl15                       0/1     ContainerCreating   0          17s
etcd-controlplane                         1/1     Running             0          8m50s
kube-apiserver-controlplane               1/1     Running             0          8m48s
kube-controller-manager-controlplane      1/1     Running             0          8m24s
kube-flannel-ds-t8w7                       1/1     Running             0          8m37s
kube-proxy-dt7jg                          1/1     Running             0          8m37s
kube-scheduler-controlplane               1/1     Running             0          8m48s
```

After a short wait, the Elastic Agent pods will transition to the running state. Re-run the command above to ensure that both agents are active. You should also see console output similar to the following when the daemonset deployment is applied:

```bash theme={null}
daemonset.apps/elastic-agent created
clusterrolebinding.rbac.authorization.k8s.io/elastic-agent created
rolebinding.rbac.authorization.k8s.io/elastic-agent created
clusterrole.rbac.authorization.k8s.io/elastic-agent created
role.rbac.authorization.k8s.io/elastic-agent created
serviceaccount/elastic-agent created
```

## Step 4: View Metrics in Elastic Cloud

Once the Elastic Agent is enrolled, Elastic Cloud automatically starts collecting metrics from your Kubernetes cluster. In your Elastic Cloud console:

1. Click on **Confirm data**.
2. Select **View Kubernetes metrics** on the dashboard.

<Frame>
  ![The image shows a preview of incoming data logs in an Elastic interface, detailing various agent activities and configurations. It includes timestamps, agent names, types, versions, and cloud instance information.](https://kodekloud.com/kk-media/image/upload/v1752874196/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Monitoring-Kubernetes-Cluster-using-in-Elastic-Agent/elastic-data-logs-preview.jpg)
</Frame>

Within a few minutes, you will see metrics such as node details, memory usage, CPU core counts, and even information about the top memory-intensive pods appear on the dashboard. For instance, the default dashboard displays the Elastic Agent running in the `kube-system` namespace:

<Frame>
  ![The image shows a dashboard from Elastic displaying Kubernetes metrics, including memory usage and pod information, with a filter option for namespaces.](https://kodekloud.com/kk-media/image/upload/v1752874197/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Monitoring-Kubernetes-Cluster-using-in-Elastic-Agent/elastic-kubernetes-metrics-dashboard.jpg)
</Frame>

<Callout icon="lightbulb">
  If you require a customized view, you can clone or modify the dashboard. However, note that managed dashboards provided by Elastic Cloud are maintained by the Elastic Agent and are not immediately editable.
</Callout>

## Step 5: Clean Up

<Callout icon="triangle-alert">
  If you're using a free trial Elastic Cloud account, be sure to delete the deployment after your trial period ends to prevent ongoing charges.
</Callout>

To delete your deployment:

1. Navigate to your profile in Elastic Cloud.
2. Click on **Organization**, then **Elastic**.
3. On the home page, click **Manage** and choose **Delete deployment**.
4. Confirm deletion by typing the cluster name.

This ensures that you will not incur any unwanted costs after your trial period.

## Conclusion

This guide demonstrated how to seamlessly monitor your Kubernetes cluster with Elastic Agent, leveraging the robust observability and logging capabilities of Elastic Cloud. For further reading, explore additional resources:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Elastic Documentation](https://www.elastic.co/guide/index.html)

Thank you for following this guide. Happy monitoring, and we look forward to bringing you more insightful lessons in the future!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/be2630b4-1d09-403d-98f4-71c5ea9f2df7/lesson/f3c8e2fb-8e2f-492d-93a5-ca25d042ae56" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/be2630b4-1d09-403d-98f4-71c5ea9f2df7/lesson/6e871d7f-dc8f-4e8a-9251-3c7090d9e394" />
</CardGroup>


# Setting up Free Elastic Cloud Account

Source: https://notes.kodekloud.com/docs/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring/Elastic-Cloud/Setting-up-Free-Elastic-Cloud-Account/page

This article provides a step-by-step guide to setting up a free Elastic Cloud account for a 14-day trial.

Welcome to this hands-on guide for creating your first Elastic Cloud account. Elastic Cloud offers a 14-day free trial that allows you to explore its powerful features without any commitment. Follow the steps below to get started with your trial account.

## Step 1: Finding Elastic Cloud

1. Open your Google Chrome (or your preferred browser) and search for "Elastic Cloud."
2. Click on the first link in the search results. This will lead you to the Elastic Cloud website where the free trial is prominently featured.

<Frame>
  ![The image shows a Google search results page for "elastic cloud," featuring sponsored links and information about Elastic Cloud services and webinars.](https://kodekloud.com/kk-media/image/upload/v1752874198/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Setting-up-Free-Elastic-Cloud-Account/google-search-elastic-cloud-results.jpg)
</Frame>

## Step 2: Start Your Free Trial

1. Click on the **"Start Free Trial"** button.
2. You will see several sign-up options, including registration via cloud marketplaces and a direct sign-up for an Elastic Cloud account.
3. For this guide, we will register directly with Elastic Cloud. At the time of recording, no credit card is required to sign up for the free trial.

<Frame>
  ![The image shows a sign-up page for a free trial of Elastic, with options to sign up via email or through cloud marketplaces like Amazon Web Services, Google Cloud, and Microsoft Azure.](https://kodekloud.com/kk-media/image/upload/v1752874199/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Setting-up-Free-Elastic-Cloud-Account/elastic-free-trial-signup-page.jpg)
</Frame>

<Callout icon="lightbulb">
  If you’re exploring Elastic Cloud for evaluation, you can register without providing detailed company information—just enter "Not Available" when prompted.
</Callout>

## Step 3: Registration Process

1. Select **Google** as your preferred sign-in method.
2. Choose your email ID and click **"Continue."**
3. Fill in your full name and company details. If you do not wish to provide your company information, simply enter **"Not Available."**
4. When asked about your experience with Elastic, select **"I am new"** and choose the **"Evaluate Elastic for my project"** use case.

<Frame>
  ![The image shows a registration form for Elastic, asking for user information such as full name, company, experience level, and areas of interest. There are options to select interests and actions related to Elastic services.](https://kodekloud.com/kk-media/image/upload/v1752874200/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Setting-up-Free-Elastic-Cloud-Account/elastic-registration-form-user-info.jpg)
</Frame>

5. Click **"Next."**
6. If additional details are required, enter **"observability logs"** or select one of the available options.
7. Continue by clicking **"Next"** and wait for the registration process to complete.

## Step 4: Configuring Your Deployment

1. Name your deployment (e.g., **"Elastic Cloud"**) while keeping the remaining settings at their defaults.

2. By default, Elastic Cloud deploys your environment on [Google Cloud Platform (GCP)](https://cloud.google.com/). To choose a different provider, click **"Edit Settings"** and select your preferred cloud provider. For this demonstration, we are using the default GCP.

3. You can also select the hardware profile. Options include vector search optimized, storage optimized, and more. If you are new to Elastic Cloud, it is recommended to leave these options at their default values.

4. Click on **"Create Deployment."**

Once your deployment is ready, you will be redirected to a page that displays your Kibana UI.

<Frame>
  ![The image shows a web interface for creating a deployment on Elastic Cloud, with options to select the cloud provider, region, hardware profile, and version.](https://kodekloud.com/kk-media/image/upload/v1752874201/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Setting-up-Free-Elastic-Cloud-Account/elastic-cloud-deployment-interface.jpg)
</Frame>

## Step 5: Reviewing Your Deployment

1. To view the details of your deployment, click on your account and navigate to **"Organization."**
2. Here, you will see your organization details (typically, only you as the user). Then, click on **"Cloud"** to review your deployment’s status, ensuring it is healthy and that the cloud provider's details are correctly displayed.
3. Although you have the option to create additional deployments, continue with the one you just created.

<Frame>
  ![The image shows a dashboard for Elastic Cloud, featuring options for creating deployments, serverless projects, and accessing support, training, news, and community events.](https://kodekloud.com/kk-media/image/upload/v1752874202/notes-assets/images/EFK-Stack-Enterprise-Grade-Logging-and-Monitoring-Setting-up-Free-Elastic-Cloud-Account/elastic-cloud-dashboard-options.jpg)
</Frame>

## Step 6: Accessing Kibana and Next Steps

1. Click the **"Open"** button to launch your Kibana URL, where you can start monitoring and analyzing your data.
2. The next step in this series will demonstrate how to integrate your Kubernetes cluster with Elastic Cloud to collect and forward Kubernetes metrics to Elasticsearch.

<Callout icon="lightbulb">
  In the next article, we will walk you through the process of integrating a Kubernetes cluster with Elastic Cloud for monitoring purposes. Stay tuned!
</Callout>

Thank you for following this guide. Enjoy exploring Elastic Cloud and the powerful observability tools it offers!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/efk-stack-enterprise-grade-logging-and-monitoring/module/be2630b4-1d09-403d-98f4-71c5ea9f2df7/lesson/c26fd8bf-a34f-4eab-bde3-91a541b4b10d" />
</CardGroup>
