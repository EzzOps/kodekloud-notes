# ClientVersion and ServerVersion details
$ kubectl get nodes
# Lists nodes
$ export INGRESS_IP=139.48.208.48
$ kubectl -n $NAMESPACE create secret generic mongo-db-creds \
    --from-literal=MONGO_URI=$MONGO_URI \
    --from-literal=MONGO_USERNAME=$MONGO_USERNAME \
    --from-literal=MONGO_PASSWORD=$MONGO_PASSWORD \
    --dry-run=client -o yaml | kubectl apply -f -
secret/mongo-db-creds created
$ for manifest in kubernetes/manifest/*.yaml; do
    envsubst < $manifest | kubectl apply -f -
  done
deployment.apps/solar-system created
ingress.networking.k8s.io/solar-system created
service/solar-system created
$ kubectl -n $NAMESPACE get all,secret,ingress
# Pods, services, deployment, secret, and ingress listed
```

***

## 7. Verify Deployment Locally

Check all resources in `development`:

```bash theme={null}
kubectl -n development get all
```

```text theme={null}
NAME                                   READY   STATUS    RESTARTS   AGE
pod/solar-system-86fc65474-5klmr       1/1     Running   0          3m10s
pod/solar-system-86fc65474-fcfpq       1/1     Running   0          3m10s

NAME                   TYPE        CLUSTER-IP      PORT(S)          AGE
service/solar-system   NodePort    10.102.111.40   3000:30654/TCP   3m5s

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/solar-system 2/2     2            2           3m10s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/solar-system-86f65474      2         2         2       3m10s
```

Retrieve the Ingress host:

```bash theme={null}
kubectl -n development get ingress
```

```text theme={null}
NAME           HOSTS                                               ADDRESS         PORTS   AGE
solar-system   solar-system-development.139.84.208.48.nip.io       139.84.208.48   80,443  3m33s
```

Open the application in your browser (accept the self-signed certificate):

[http://solar-system-development.139.84.208.48.nip.io](http://solar-system-development.139.84.208.48.nip.io)

![The image shows a digital representation of the solar system with planets orbiting the sun, accompanied by a user interface for exploring the planets.](https://kodekloud.com/kk-media/image/upload/v1752877203/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Create-Secret-and-Deploy-to-K8S-Dev-Environment/solar-system-planets-exploration.jpg)

Search for a planet by number (e.g., **3** for Earth):

![The image shows a webpage about the solar system, featuring an illustration of Earth and a description of the planet. There is a search interface for exploring planets.](https://kodekloud.com/kk-media/image/upload/v1752877204/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Create-Secret-and-Deploy-to-K8S-Dev-Environment/solar-system-earth-illustration.jpg)

***

## 8. Next Steps

To improve reliability, integrate health checks into your pipeline:

* `GET /live` → `{"status":"live"}`
* `GET /ready` → `{"status":"ready"}`, HTTP 200

These endpoints can be tested with tools like [k6](https://k6.io/) or [Postman CLI](https://www.postman.com/).

***

## Links and References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
* [HashiCorp Vault](https://www.vaultproject.io/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/898b391e-8316-4896-8c70-11ff28d984b8)


# Job Fetch Ingress URL amp Integration testing

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Deployment-with-GitLab/Job-Fetch-Ingress-URL-amp-Integration-testing/page

This guide extends a GitLab CI pipeline by adding an integration testing job to verify service endpoints after deploying to Kubernetes.

In this guide, we’ll extend our GitLab CI pipeline by adding an integration testing job. After deploying to Kubernetes, we’ll extract the Ingress host URL, save it as a dotenv report, and consume it in downstream tests to verify our service endpoints.

***

## 1. Define the Integration Testing Job

Begin by declaring a `k8s_dev_integration_testing` job in the `dev-deploy` stage. This job installs `curl` and `jq`, then probes the `/live` and `/ready` endpoints to confirm service health:

```yaml theme={null}
k8s_dev_integration_testing:
  stage: dev-deploy
  image: alpine:3.7
  before_script:
    - apk --no-cache add curl jq
  script:
    - curl -s -k https://$INGRESS_URL/live  | jq -r .status | grep -i live
    - curl -s -k https://$INGRESS_URL/ready | jq -r .status | grep -i ready
```

***

## 2. Capture the Ingress Host URL in CI

After your application manifests are applied, list the Ingress resource to confirm its host:

```bash theme={null}
kubectl -n development get ing
```

```plain theme={null}
NAME           CLASS    HOSTS                                          ADDRESS         PORTS   AGE
solar-system   <none>   solar-system-development.139.84.208.48.nip.io 139.84.208.48   80,443  39m
```

Extract the hostname via JSONPath:

```bash theme={null}
kubectl -n development get ing -o jsonpath="{.items[0].spec.tls[0].hosts[0]}"
```

Automate this in your deploy job and append the result to a dotenv file:

```yaml theme={null}
k8s_dev_deploy:
  stage: dev-deploy
  image: alpine:3.7
  script:
    - export KUBECONFIG=$DEV_KUBE_CONFIG
    - kubectl version -o yaml
    - kubectl config get-contexts
    - kubectl get nodes
    - export INGRESS_IP=$(kubectl -n ingress-nginx get svc ingress-nginx-controller \
        -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
    - echo "🔍 Ingress IP: $INGRESS_IP"
    - kubectl -n $NAMESPACE create secret generic mongo-db-creds \
        --from-literal=MONGO_URI=$MONGO_URI \
        --from-literal=MONGO_USERNAME=$MONGO_USERNAME \
        --from-literal=MONGO_PASSWORD=$MONGO_PASSWORD \
        --save-config --dry-run=client -o yaml | kubectl apply -f -
    - for manifest in kubernetes/manifest/*.yaml; do
        envsubst < "$manifest" | kubectl apply -f -
      done
    - echo "INGRESS_URL=$(kubectl -n $NAMESPACE get ing \
        -o jsonpath='{.items[0].spec.tls[0].hosts[0]}')" >> app_ingress_url.env
  artifacts:
    reports:
      dotenv: app_ingress_url.env
```

> **lightbulb** By registering `app_ingress_url.env` as a dotenv report, GitLab exposes `INGRESS_URL` as a CI variable for subsequent jobs.

![The image shows a GitLab documentation page about artifacts:reports:dotenv, detailing how environment variables are collected and used in CI/CD pipelines. The page includes rules and exceptions for handling .env files.](https://kodekloud.com/kk-media/image/upload/v1752877206/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Fetch-Ingress-URL-amp-Integration-testing/gitlab-artifacts-reports-dotenv.jpg)

***

## 3. Consume the Ingress URL in Integration Tests

Now update the integration testing job to depend on the deploy job. This ensures that `INGRESS_URL` is available:

```yaml theme={null}
k8s_dev_integration_testing:
  stage: dev-deploy
  needs:
    - k8s_dev_deploy
  image: alpine:3.7
  before_script:
    - apk --no-cache add curl jq
  script:
    - echo "Using Ingress URL: $INGRESS_URL"
    - curl -s -k https://$INGRESS_URL/live  | jq -r .status | grep -i live
    - curl -s -k https://$INGRESS_URL/ready | jq -r .status | grep -i ready
```

***

## 4. Visualize the Pipeline

After committing your `.gitlab-ci.yml`, your pipeline in the **dev-deploy** stage will include two sequential jobs:

![The image shows a GitLab Pipeline Editor interface with a successful pipeline visualization, including stages for containerization and deployment.](https://kodekloud.com/kk-media/image/upload/v1752877207/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Fetch-Ingress-URL-amp-Integration-testing/gitlab-pipeline-editor-successful-visualization.jpg)

Upon completion, both jobs report success:

![The image shows a GitLab CI/CD pipeline interface for a NodeJS project called "Solar System," displaying successful stages for containerization and deployment.](https://kodekloud.com/kk-media/image/upload/v1752877208/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Job-Fetch-Ingress-URL-amp-Integration-testing/gitlab-cicd-nodejs-solar-system.jpg)

***

## References

* [GitLab CI/CD Pipelines](https://docs.gitlab.com/ee/ci/pipelines/)
* [GitLab artifacts:reports:dotenv](https://docs.gitlab.com/ee/ci/yaml/#artifactsreportsdotenv)
* [kubectl Overview](https://kubernetes.io/docs/reference/kubectl/overview/)
* [JSONPath in kubectl](https://kubernetes.io/docs/reference/kubectl/jsonpath/)

- [Watch Video](https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/df17ec22-8cda-4af7-af44-10f9f061d4a8/lesson/481b65e9-0fe9-4981-9229-b304b205fc61)
