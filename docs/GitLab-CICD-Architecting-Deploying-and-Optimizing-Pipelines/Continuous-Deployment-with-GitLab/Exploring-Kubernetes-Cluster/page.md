# 1. Build and push to GitLab Container Registry
publish_gitlab_container_registry:
  stage: containerization
  needs:
    - docker_build
    - docker_test
  image: docker:24.0.5
  services:
    - docker:24.0.5-dind
  script:
    - docker load -i image/solar-system-image-$CI_PIPELINE_ID.tar
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD"
    - docker tag $DOCKER_USERNAME/solar-system:$IMAGE_VERSION $CI_REGISTRY_IMAGE/ss-image:$IMAGE_VERSION
    - docker push $CI_REGISTRY_IMAGE/ss-image:$IMAGE_VERSION

# 2. Deploy to development on Kubernetes
k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  before_script:
    - wget -qO kubectl "https://storage.googleapis.com/kubernetes-release/release/$(wget -qO - https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
    - chmod +x kubectl && mv kubectl /usr/local/bin/
    - apk add --no-cache gettext
  script:
    - export KUBECONFIG=$DEV_KUBE_CONFIG
    - kubectl version --client -o yaml
    - kubectl config get-contexts
    - kubectl get nodes
    - export INGRESS_URL=$(kubectl -n ingress-nginx get svc ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    - kubectl -n $NAMESPACE create secret generic mongo-db-creds \
        --from-literal=MONGO_URI=$MONGO_URI \
        --from-literal=MONGO_USERNAME=$MONGO_USERNAME \
        --from-literal=MONGO_PASSWORD=$MONGO_PASSWORD \
        --save-config \
        --dry-run=client -o yaml | kubectl apply -f -
    - for file in kubernetes/manifest/*.yaml; do envsubst < $file | kubectl apply -f -; done
    - kubectl -n $NAMESPACE get all,secret,ing
  artifacts:
    reports:
      dotenv: app_ingress_url.env
  environment:
    name: development
    url: https://$INGRESS_URL

# 3. Integration tests against development
k8s_dev_integration_testing:
  stage: dev-deploy
  image: alpine:3.7
  needs:
    - k8s_dev_deploy
  before_script:
    - apk add --no-cache curl jq
  script:
    - echo "Testing endpoint: https://$INGRESS_URL"
    - curl -s -k https://$INGRESS_URL/Live | jq -r .status | grep -i live
    - curl -s -k https://$INGRESS_URL/ready | jq -r .status | grep -i ready
```

***

## 3. Static vs. Dynamic Environments

GitLab supports two environment types:

| Environment Type | Description                                  | Creation Method                                              |
| ---------------- | -------------------------------------------- | ------------------------------------------------------------ |
| Static           | Predefined before pipeline runs              | Manual via **Operations > Environments** in the UI           |
| Dynamic          | Generated on the fly by pipeline definitions | Specified in job’s `environment` section in `.gitlab-ci.yml` |

***

## 4. Creating a Static Environment

1. In GitLab, navigate to **Operations** > **Environments** > **New environment**.
2. Enter the **Name** and optional **External URL**.
3. (Optional) Link a GitLab Agent for Kubernetes.
4. Click **Save**.

<Frame>
  ![The image shows a GitLab interface for creating a new environment, with fields for the environment name, external URL, and GitLab agent selection. The URL field has a validation message indicating it should start with "http://" or "https://".](https://kodekloud.com/kk-media/image/upload/v1752877192/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Environment-and-Deployments/gitlab-new-environment-interface.jpg)
</Frame>

After saving, the new environment appears in the list (initially with no deployments):

<Frame>
  ![The image shows a GitLab environment page with a "development" environment listed but no deployments yet. The interface includes options for managing environments and related settings.](https://kodekloud.com/kk-media/image/upload/v1752877193/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Environment-and-Deployments/gitlab-development-environment-page.jpg)
</Frame>

***

## 5. Running the Pipeline & Viewing Deployments

Once you push changes or create a Merge Request, the pipeline executes:

* **Containerization**
* **Testing**
* **Deployment**

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a NodeJS project, displaying stages like containerization and deployment with job statuses.](https://kodekloud.com/kk-media/image/upload/v1752877194/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Environment-and-Deployments/gitlab-cicd-nodejs-pipeline.jpg)
</Frame>

After a successful deployment, visit **Operations** > **Environments** to see deployment details: commit ID, job name, timestamp, and more.

<Frame>
  ![The image shows a GitLab environment page with a successful deployment in the "development" environment. It includes details about the trigger, job, and branch used for deployment.](https://kodekloud.com/kk-media/image/upload/v1752877195/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Environment-and-Deployments/gitlab-successful-deployment-development.jpg)
</Frame>

Click **Open live environment** to launch your application. This link uses the `url` specified in your job’s environment settings and is also visible in Merge Requests for quick previews.

***

## 6. Rollback and Redeploy

If a deployment fails or you need to revert changes, GitLab offers **Finish**, **Rollback**, and **Redeploy** actions:

<Frame>
  ![The image shows a GitLab environment page displaying a list of deployment jobs with their statuses, IDs, commit messages, and actions. The sidebar includes options for managing various aspects of the project, such as code, build, and deploy.](https://kodekloud.com/kk-media/image/upload/v1752877196/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Environment-and-Deployments/gitlab-deployment-jobs-statuses.jpg)
</Frame>

* **Rollback**: Reverts to the last successful deployment (using the recorded commit ID).
* **Redeploy**: Re-runs the deployment job for the same commit.

<Callout icon="triangle-alert">
  Use rollback carefully: any data migrations or schema changes may not be reversible.
</Callout>

***

## Links and References

* [GitLab CI/CD Environments Documentation](https://docs.gitlab.com/ee/ci/environments/)
* [Kubernetes Official Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/6673ba1b-449a-401a-822a-86bfc7c1f2ad" />
</CardGroup>


# Exploring Kubernetes Cluster

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Exploring-Kubernetes-Cluster/page

This guide covers inspecting a GKE cluster, listing nodes, viewing namespaces, deploying an NGINX app, and preparing namespaces for GitLab CI/CD.

This guide walks you through inspecting a Google Kubernetes Engine (GKE) cluster. You’ll learn how to list nodes, view namespaces, deploy a sample NGINX app with Ingress, verify your kubeconfig, and prepare namespaces for GitLab CI/CD.

## Inspecting Cluster Nodes on GKE

<Callout icon="lightbulb">
  Make sure you’ve authenticated with GKE and set up `kubectl` (or aliased as `k`) using:

  ```bash theme={null}
  gcloud container clusters get-credentials <CLUSTER_NAME> --zone <ZONE> --project <PROJECT_ID>
  ```
</Callout>

List your cluster’s worker nodes:

```bash theme={null}
k get nodes
```

Example output:

```bash theme={null}
NAME                                         STATUS   ROLES     AGE   VERSION
gke-cluster-1-default-pool-36b5f551-hzvn     Ready    <none>    20m   v1.29.0-gke.1381000
gke-cluster-1-default-pool-36b5f551-rsc0     Ready    <none>    20m   v1.29.0-gke.1381000
```

These nodes are running Kubernetes v1.29.0.

## Viewing Namespaces and the NGINX Ingress Controller

Show all namespaces:

```bash theme={null}
k get namespaces
```

Locate the `ingress-nginx` namespace and inspect its resources:

```bash theme={null}
k -n ingress-nginx get all
```

You should see:

* A Deployment managing the Ingress Controller pod
* A `LoadBalancer` Service exposing a public IP

## Deploying a Sample NGINX Application

In the `default` namespace, the following resources route traffic through the Ingress Controller:

```bash theme={null}
k -n default get all
k -n default get ingress
```

Sample output:

```bash theme={null}
