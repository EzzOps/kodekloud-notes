# Initial state: existing deployment running 4 replicas
kubectl -n beta get pods,deploy
NAME                                          READY   STATUS    RESTARTS   AGE
pod/highway-animation-1-77dd97f459-65rm8      1/1     Running   0          4h13m
pod/highway-animation-1-77dd97f459-9dhpq      1/1     Running   0          4h13m
pod/highway-animation-1-77dd97f459-gksf2      1/1     Running   0          4h13m
pod/highway-animation-1-77dd97f459-lbf8w      1/1     Running   0          4h13m

NAME                                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/highway-animation-1          4/4     4            4           4h13m
```

2. Apply the Rollout manifest (example uses a public gist). This creates the Rollout and the blue/green services:

```bash theme={null}
kubectl -n beta apply -f https://gist.github.com/sidd-harth/5dedab96d94373e4f1f1317f33d3781f/raw/dcf228b4e2e8b12c912fb4f1fbb3f858e435fd0f/rollout-1-demo.yml
# Expected output:
# rollout.argoproj.io/highway-animation-rollout created
# service/highway-bluegreen-active created
# service/highway-bluegreen-preview created
```

3. After applying, new Rollout-managed pods will be created while the original Deployment pods continue running until the rollout completes:

```bash theme={null}
kubectl -n beta get pods,deploy
NAME                                               READY   STATUS             RESTARTS   AGE
pod/highway-animation-1-77dd97f459-65rm8           1/1     Running            0          4h19m
pod/highway-animation-1-77dd97f459-9dhpq           1/1     Running            0          4h19m
pod/highway-animation-1-77dd97f459-gksf2           1/1     Running            0          4h19m
pod/highway-animation-1-77dd97f459-lbf8w           1/1     Running            0          4h19m
pod/highway-animation-rollout-5f9c6d59f-m6fxg      0/1     ContainerCreating  0          3s
pod/highway-animation-rollout-5f9c6d59f-nq44x      0/1     Pending            0          2s
pod/highway-animation-rollout-5f9c6d59f-pmls4      0/1     Pending            0          2s
pod/highway-animation-rollout-5f9c6d59f-qcxb4      0/1     Pending            0          2s

NAME                                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/highway-animation-1               4/4     4            4           4h19m
```

4. When the Rollout becomes healthy, Rollout pods will reach Running and the original Deployment pods are terminated according to the scaleDown policy:

```bash theme={null}
kubectl -n beta get pods,deploy
NAME                                               READY   STATUS        RESTARTS   AGE
pod/highway-animation-1-77dd97f459-65rm8           1/1     Terminating   0          4h20m
pod/highway-animation-1-77dd97f459-9dhpq           1/1     Terminating   0          4h20m
pod/highway-animation-1-77dd97f459-gksf2           1/1     Terminating   0          4h20m
pod/highway-animation-1-77dd97f459-lbf8w           1/1     Terminating   0          4h20m
pod/highway-animation-rollout-5f9c6d59f-m6fxg      1/1     Running       0          53s
pod/highway-animation-rollout-5f9c6d59f-nq44x      1/1     Running       0          52s
pod/highway-animation-rollout-5f9c6d59f-pmls4      1/1     Running       0          52s
pod/highway-animation-rollout-5f9c6d59f-qcxb4      1/1     Running       0          52s
```

At this point the Rollout resource controls the application; the original Deployment has been scaled down according to the scaleDown policy, and the blue/green services allow controlled traffic promotion and preview testing.

<Callout icon="lightbulb">
  Note: Using workloadRef allows you to convert an existing Deployment to be managed by Argo Rollouts without rewriting the pod template. Review the available scaleDown options (onSuccess, never, progressive) to choose the behavior that suits your release workflow.
</Callout>

Links and references

* Argo Rollouts documentation: [https://argoproj.github.io/argo-rollouts/](https://argoproj.github.io/argo-rollouts/)
* Kubernetes Deployments: [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* Example manifest used in this demo: [https://gist.github.com/sidd-harth/5dedab96d94373e4f1f1317f33d3781f](https://gist.github.com/sidd-harth/5dedab96d94373e4f1f1317f33d3781f)

That's all for now.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/196ad805-5a18-4575-b30f-21fe0f0cb005" />
</CardGroup>


# Demo Health Check

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Demo-Health-Check/page

Guide to deploying an Argo Rollouts blue/green rollout, exposing services, and using a /health endpoint for AnalysisTemplate based gating of manual promotion.

In this lesson you'll:

* Create a namespace.
* Deploy an Argo Rollout with a blue/green strategy.
* Verify the application's /health endpoint — suitable for use in an AnalysisTemplate and AnalysisRun to gate promotion.

The Rollout below (save as `rollout-initial.yaml`) runs five replicas of the "highway-animation" app (blue variant), sets a `POD_COUNT` environment variable, and configures blue/green with manual promotion (`autoPromotionEnabled: false`) so promotion can be done manually or via an analysis.

```yaml theme={null}
