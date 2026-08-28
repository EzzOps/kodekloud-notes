# Manually Promote to Staging Environment via agentK

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Manually-Promote-to-Staging-Environment-via-agentK/page

This guide explains how to manually promote applications to the staging environment using GitLabs Kubernetes Agent.

To streamline manual promotions to staging, use GitLab’s Kubernetes Agent (AgentK) to authenticate your CI/CD jobs. This guide walks through deploying to the `staging` namespace and updating your pipeline to leverage the Agent’s built-in `KUBECONFIG` context.

<Callout icon="lightbulb">
  * A configured GitLab Kubernetes Agent with `ci_access` enabled in `config.yaml`
  * Defined CI/CD variables: `DEV_KUBE_CONFIG`, `NAMESPACE`, `MONGO_*`, `DOCKER_USERNAME`
  * The `staging` namespace created on your cluster
</Callout>

## 1. Verify the Staging Namespace Is Empty

Confirm there are no existing resources in `staging`:

```bash theme={null}
kubectl -n staging get all
```

No resources should be returned.

You can also verify in GitLab under **Environments**:

<Frame>
  ![The image shows a GitLab interface displaying the "Environments" section with two active environments: "development" and "staging." There are no deployments for the "staging" environment, and options to manage environments are visible.](https://kodekloud.com/kk-media/image/upload/v1752877216/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-environments-development-staging.jpg)
</Frame>

## 2. Review the Current Development Deploy Job

Our `.gitlab-ci.yml` defines a `k8s_dev_deploy` job that uses a self-managed `KUBECONFIG`. It builds the image, injects secrets, and applies manifests:

```yaml theme={null}
variables:
  DOCKER_USERNAME: siddhanth67
  IMAGE_VERSION: $CI_PIPELINE_ID
  K8S_IMAGE: $DOCKER_USERNAME/solar-system:$IMAGE_VERSION
  MONGO_URI: mongodb+srv://supercluster.d83j.mongodb.net/superData
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD

k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  before_script:
    - wget https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    - chmod +x ./kubectl && mv ./kubectl /usr/bin/kubectl
    - apk add --no-cache gettext && envsubst -V
  script:
    - export KUBECONFIG=$DEV_KUBE_CONFIG
    - kubectl version -o yaml
    - kubectl config get-contexts
    - kubectl get nodes
    - |
      export INGRESS_IP=$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
        -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
    - echo "Ingress IP: $INGRESS_IP"
    - kubectl -n $NAMESPACE create secret generic mongo-db-creds \
        --from-literal=MONGO_URI=$MONGO_URI \
        --from-literal=MONGO_USERNAME=$MONGO_USERNAME \
        --from-literal=MONGO_PASSWORD=$MONGO_PASSWORD \
        --save-config --dry-run=client -o yaml \
      | kubectl apply -f -
    - for f in kubernetes/manifest/*.yaml; do envsubst < $f | kubectl apply -f -; done
  environment:
    name: development
    url: https://$INGRESS_IP.nip.io
  artifacts:
    reports:
      dotenv: app_ingress_url.env
```

## 3. Connect the GitLab Kubernetes Agent

In `config.yaml`, enable CI access so each job automatically receives the Agent’s kubeconfig:

```yaml theme={null}
ci_access:
  groups:
    - id: path/to/group/subgroup
```

Now `$KUBECONFIG` is populated by the Agent in every CI job.

<Frame>
  ![The image shows a GitLab interface displaying a connected Kubernetes cluster with details such as connection status, last contact, version, and agent ID. There's also a sidebar with various options like "Environments" and "Kubernetes clusters."](https://kodekloud.com/kk-media/image/upload/v1752877218/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-kubernetes-cluster-interface.jpg)
</Frame>

## 4. Minimal Deploy Example

A concise example using `bitnami/kubectl` to switch context:

```yaml theme={null}
deploy:
  image: bitnami/kubectl:latest
  entrypoint: ['']
  script:
    - kubectl config get-contexts
    - kubectl config use-context path/to/agent/project:agent-name
    - kubectl get pods
```

For more details, see the [GitLab Kubernetes deployments guide](https://docs.gitlab.com/ee/ci/examples/kubernetes_deployments.html).

## 5. Add the Staging Deploy Job

Copy the `k8s_dev_deploy` job, rename it to `k8s_stage_deploy`, and update it to use the Agent’s `$KUBECONFIG`. Remove custom kubeconfig logic. Add `when: manual` so it only runs on demand.

<Callout icon="lightbulb">
  Ensure you have added `stage-deploy` to the top-level `stages` list and set `NAMESPACE: staging`.
</Callout>

```yaml theme={null}
k8s_stage_deploy:
  stage: stage-deploy
  image: alpine:3.7
  when: manual
  before_script:
    - wget https://storage.googleapis.com/kubernetes-release/release/$(wget -q -O - https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    - chmod +x ./kubectl && mv ./kubectl /usr/bin/kubectl
    - apk add --no-cache gettext && envsubst -V
  script:
    # Inspect and switch the Agent context
    - cat $KUBECONFIG
    - kubectl config get-contexts
    - kubectl config use-context demos-group/solar-system:kk-gitlab-agent
    - kubectl get po -A

    # Deploy application
    - |
      export INGRESS_IP=$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
        -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
    - echo "Ingress IP: $INGRESS_IP"
    - kubectl -n $NAMESPACE create secret generic mongo-db-creds \
        --from-literal=MONGO_URI=$MONGO_URI \
        --from-literal=MONGO_USERNAME=$MONGO_USERNAME \
        --from-literal=MONGO_PASSWORD=$MONGO_PASSWORD \
        --save-config --dry-run=client -o yaml \
      | kubectl apply -f -
    - for f in kubernetes/manifest/*.yaml; do envsubst < $f | kubectl apply -f -; done
    - kubectl -n $NAMESPACE get all,secret,ing
    - echo "INGRESS_URL=$(kubectl -n $NAMESPACE get ing \
        -o jsonpath="{.items[0].spec.tls[0].hosts[0]}")" >> app_ingress_url.env
  artifacts:
    reports:
      dotenv: app_ingress_url.env
  environment:
    name: staging
    url: https://${INGRESS_URL}
```

## 6. Add Integration Tests for Staging

Verify your `/live` and `/ready` health endpoints:

```yaml theme={null}
k8s_stage_integration_testing:
  stage: stage-deploy
  image: alpine:3.7
  needs:
    - k8s_stage_deploy
  before_script:
    - apk add --no-cache curl jq
  script:
    - echo "Testing URL: $INGRESS_URL"
    - curl -s -k https://$INGRESS_URL/live  | jq -r .status | grep -i live
    - curl -s -k https://$INGRESS_URL/ready | jq -r .status | grep -i ready
```

## 7. Pipeline Visualization

Your CI pipeline now spans four stages (test, containerization, dev-deploy, stage-deploy) and includes manual promotion:

<Frame>
  ![The image shows a GitLab Pipeline Editor interface with a visualized CI/CD pipeline, including stages like testing, containerization, and deployment. The pipeline includes steps such as unit testing, docker build, and Kubernetes deployment.](https://kodekloud.com/kk-media/image/upload/v1752877219/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-pipeline-editor-cicd-diagram.jpg)
</Frame>

## 8. Manual Promotion in GitLab

The `k8s_stage_deploy` job is set to manual:

<Frame>
  ![The image is a screenshot of a GitLab documentation page about creating jobs that must be run manually. It includes information on specifying manual jobs in the .gitlab-ci.yml file and describes types of manual jobs.](https://kodekloud.com/kk-media/image/upload/v1752877220/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-manual-jobs-documentation.jpg)
</Frame>

## 9. Trigger the Manual Job

Navigate to **CI/CD → Pipelines**, then click the ▶️ icon next to `k8s_stage_deploy`. You can override variables before starting:

<Frame>
  ![The image shows a GitLab CI/CD job interface for "k8s\_stage\_deploy," indicating that the job requires manual action to start. It allows users to input CI/CD variables before running the job.](https://kodekloud.com/kk-media/image/upload/v1752877222/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-cicd-k8s-stage-deploy.jpg)
</Frame>

Once `k8s_stage_deploy` completes, `k8s_stage_integration_testing` will run automatically.

## 10. Inspect the Deployment Logs

Important log snippets include:

```bash theme={null}
$ cat $KUBECONFIG
apiVersion: v1
kind: Config
...
contexts:
- name: demos-group/solar-system:kk-gitlab-agent
  context:
    cluster: gitLab
    user: agent:108840

$ kubectl config use-context demos-group/solar-system:kk-gitlab-agent
Switched to context "demos-group/solar-system:kk-gitlab-agent".

$ kubectl get po -A
...

$ export INGRESS_IP=$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
    -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
$ echo $INGRESS_IP
139.84.208.48

$ kubectl -n staging create secret generic mongo-db-creds ... | kubectl apply -f -
secret/mongo-db-creds created

$ kubectl -n staging get all,secret,ing
...
```

You should see your pods, services, deployments, and replicasets in `staging`.

## 11. Review CI/CD Environment Variables

In **Settings → CI/CD**, scope variables to your environments (e.g., `staging`):

<Frame>
  ![The image shows a GitLab CI/CD settings page displaying a list of environment variables, some of which are masked for security. The sidebar includes options like Deploy, Monitor, and Settings.](https://kodekloud.com/kk-media/image/upload/v1752877224/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-ci-cd-environment-variables.jpg)
</Frame>

## 12. Validate Deployment in GitLab UI

The **Environments** dashboard now reflects your successful staging deploy:

<Frame>
  ![The image shows a GitLab environment management interface with active environments for "development" and "staging." It displays deployment details, including a successful deployment status and recent activity.](https://kodekloud.com/kk-media/image/upload/v1752877225/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-environment-management-interface.jpg)
</Frame>

Under **Kubernetes services**, your service appears with its external IP:

<Frame>
  ![The image shows a GitLab environment dashboard displaying Kubernetes services with details like name, namespace, type, cluster IP, external IP, ports, and age. The sidebar includes navigation options for managing and deploying projects.](https://kodekloud.com/kk-media/image/upload/v1752877226/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/gitlab-kubernetes-dashboard-services.jpg)
</Frame>

Opening the application displays the Solar System UI:

<Frame>
  ![The image shows a stylized representation of the solar system with planets orbiting the sun, alongside a user interface for searching planets. It includes a description of the solar system and a highlighted pod identifier.](https://kodekloud.com/kk-media/image/upload/v1752877227/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Manually-Promote-to-Staging-Environment-via-agentK/solar-system-planets-ui-diagram.jpg)
</Frame>

## 13. Confirm Locally via kubectl

Finally, verify in your terminal:

```bash theme={null}
kubectl -n staging get all
```

You should now see pods, services, deployments, and replicasets matching your manifests.

***

By leveraging the GitLab Kubernetes Agent, you’ve simplified authentication, enforced manual approvals for staging, and successfully deployed your application to the staging namespace.

## Links and References

* [GitLab Kubernetes Deployments](https://docs.gitlab.com/ee/ci/examples/kubernetes_deployments.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [GitLab Documentation](https://docs.gitlab.com/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/1e328feb-4d88-44fa-b11a-b95bb858ce59" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/4be4590b-8f41-4681-902a-533a96a92ba4" />
</CardGroup>
