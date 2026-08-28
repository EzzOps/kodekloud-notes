# list pods in the jenkins namespace
kubectl -n jenkins get po

# view events that show scheduling, image pulls, starts, and kills
kubectl -n jenkins get events --sort-by='.lastTimestamp'
```

Example outputs often include scheduling, pulling and started events:

```text theme={null}
# NAME                                           READY   STATUS    RESTARTS   AGE
# LAST SEEN   TYPE    REASON    OBJECT                                     MESSAGE
# 10s         Normal  Scheduled pod/k8s-cloud-agent-demo-4...       Successfully assigned jenkins/...
# 9s          Normal  Pulling   pod/...                                    Pulling image "node:18-alpine"
# 8s          Normal  Pulled    pod/...                                    Successfully pulled image "node:18-alpine"
# 5s          Normal  Started   pod/...                                    Started container node-container
# 2s          Normal  Killing   pod/...                                    Stopping container node-container
```

## Pod details added by the plugin

Every provisioned pod includes:

* The containers you defined plus the Jenkins inbound agent (jnlp) container injected by the plugin.
* Workspace volume (typically `emptyDir`).
* Environment variables and arguments to start the jnlp agent.
* Resource requests/limits and any `securityContext` you configured.
* Pod events that show lifecycle steps from schedule → pull → start → terminate.

## Quick reference: Inline YAML vs Pod Template

| Method                      | When to use                                           | Example / notes                                                       |
| --------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------- |
| Inline YAML                 | Per-job custom pod specs or demo pipelines            | Use `agent { kubernetes { yaml '''...''' }}` inside the pipeline      |
| Pod template (cloud config) | Reusable specs across many pipelines, central control | Add templates in the Kubernetes cloud configuration in Jenkins        |
| Selecting cloud             | When multiple clouds exist                            | Use `cloud 'dasher-prod-k8s-us-east'` in the `kubernetes` agent block |

## Conclusion

The Jenkins Kubernetes plugin provisions ephemeral pods per build, enabling flexible, isolated build environments. Best practices:

* Use inline YAML for job-specific setups or pod templates for central reuse.
* Set `defaultContainer` for typical steps and use `container('name') { ... }` for specialized runtimes.
* Inspect lifecycle and debugging information with `kubectl get po` and `kubectl get events`.
* Remember pod retention settings (e.g., `Never`) may delete pods immediately after build completion.

<Callout icon="lightbulb">
  Consider Pod Security Admission (PSA) and cluster policies when designing pod specs. Avoid running containers as root where possible; prefer images that run as non-root users and add a `securityContext` in your pod YAML when needed. See Kubernetes PSA docs: [https://kubernetes.io/docs/concepts/security/pod-security-admission/](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
</Callout>

That is all for now.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/d1f217e1-bfef-4ba3-adf8-1411e911e0bc/lesson/e1687734-24d9-4f9a-8706-97f6a20cc59f" />
</CardGroup>


# Utilize newContainerPerStage

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Agents-and-Nodes-in-Jenkins/Utilize-newContainerPerStage/page

Explains Jenkins Pipeline option newContainerPerStage to run a fresh Docker container per stage versus reusing a single container, showing impacts on filesystem sharing and isolation.

This guide explains why and when to use the `newContainerPerStage` directive in Jenkins Pipeline. It walks through examples that show the difference between reusing a single container for all stages (the default when using a top-level `docker`/`dockerfile` agent) and launching a fresh container per stage with `options { newContainerPerStage() }`.

## When you might run different agents per stage

Often pipelines define different agents at the stage level (for example, a global `any` agent with a single stage that uses a `dockerfile` agent). A pipeline that mixes global and per-stage agents can look like this:

```groovy theme={null}
pipeline {
  agent any

  stages {
    stage('S1-Any Agent') {
      steps {
        // runs on the global 'any' agent
      }
    }

    stage('S2-Ubuntu Agent') {
      agent { label 'ubuntu' }
      steps {
        // runs on an Ubuntu node
      }
    }

    stage('S3-Docker Image Agent') {
      agent { docker 'node:18-alpine' }
      steps {
        // runs inside docker image
      }
    }

    stage('S4-Dockerfile Agent') {
      agent {
        dockerfile {
          filename 'Dockerfile.cowsay'
          label 'ubuntu-docker-jdk17-node20'
        }
      }
      steps {
        sh 'node -v'
      }
    }
  }
}
```

In the next sections we demonstrate switching from a mix of per-stage agents to a single top-level Dockerfile-based agent — and how the `newContainerPerStage` option changes runtime behavior.

## Top-level `dockerfile` agent (single container reused for all stages)

If you configure a top-level `dockerfile` agent, Jenkins will build the image, run a container from that image on the chosen node, and reuse that container for every stage in the pipeline. For example:

```groovy theme={null}
pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile.cowsay'
      label 'ubuntu-docker-jdk17-node20'
    }
  }

  stages {
    stage('Stage-1') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
      }
    }

    stage('Stage-2') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
      }
    }

    stage('Stage-3') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
      }
    }

    stage('Stage-4') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
      }
    }
  }
}
```

When a pipeline runs this way, Jenkins:

* Builds the image from the specified Dockerfile (`Dockerfile.cowsay`).
* Starts a single container from that image on the selected node.
* Reuses the same container and workspace for all stages.
* Stops and removes the container when the pipeline completes.

<Frame>
  <img alt="Screenshot of a Jenkins pipeline page for &#x22;pipeline-external-agent&#x22; showing multiple build runs with stage progress indicators (mostly green checkmarks) across stages like Checkout SCM, Agent Setup, Stage-1..Stage-4. The left sidebar lists pipeline actions (Status, Changes, Build Now, Configure) and a build history panel." />
</Frame>

Controller logs for such a run show the Docker image build and the container start:

```console theme={null}
[Pipeline] sh
+ docker build -t 0f559f3f6ac2e220b616594d407b50bd36d83f74 -f Dockerfile.cowsay .
#1 [internal] load build definition from Dockerfile.cowsay
#1 DONE 0.0s
#2 [internal] load metadata for docker.io/library/node:18-alpine
#2 DONE 0.0s
#4 [1/2] FROM docker.io/library/node:18-alpine
#4 DONE 0.0s
#5 [2/2] RUN apk update && apk add --no-cache git perl && cd /tmp && git clone https://github.com/jasonm23/cowsay.git && cd cowsay ; ./install.sh /usr/local
#5 CACHED
#6 exporting to image
#6 writing image sha256:d76b723... done
[Pipeline] withDockerContainer
$ docker run -t -d -u 0:0 -w /home/jenkins-agent/workspace/pipeline-external-agent -v /home/jenkins-agent/workspace/pipeline-external-agent:/home/jenkins-agent/workspace/pipeline-external-agent:rw,z 0f559f3f6ac2e220b616594d407b50bd36d83f74 cat
```

### Sharing files via the container filesystem

Because the same container and workspace are reused, files written by one stage to the container filesystem (for example, `/tmp`) will still be present for subsequent stages. Example pipeline that writes and reads a transient file:

```groovy theme={null}
pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile.cowsay'
    }
  }

  stages {
    stage('Stage-1') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
        echo "********************************************************************************************************"
        sh 'echo $((RANDOM)) > /tmp/imp-file-$BUILD_ID'
        sh 'ls -ltr /tmp/imp-file-$BUILD_ID'
        sh 'cat /tmp/imp-file-$BUILD_ID'
        echo "********************************************************************************************************"
      }
    }

    stage('Stage-2') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
        echo "####################################################################################################"
        sh 'ls -ltr /tmp/imp-file-$BUILD_ID'
        sh 'cat /tmp/imp-file-$BUILD_ID'
        echo "####################################################################################################"
      }
    }

    stage('Stage-3') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
        echo "####################################################################################################"
        sh 'ls -ltr /tmp/imp-file-$BUILD_ID'
        sh 'cat /tmp/imp-file-$BUILD_ID'
        echo "####################################################################################################"
      }
    }

    stage('Stage-4') {
      steps {
        sh 'node -v'
        sh 'npm -v'
        sh 'cowsay -f dragon This is running on Docker Container'
        echo "########################################################################################################"
        sh 'ls -ltr /tmp/imp-file-$BUILD_ID'
        sh 'cat /tmp/imp-file-$BUILD_ID'
        echo "########################################################################################################"
        sh 'sleep 120s' // keep container alive briefly for demo
      }
    }
  }
}
```

Trimmed logs (showing the same random number read across stages):

```console theme={null}
+ ls -ltr /tmp/imp-file-7
-rw-r--r-- 1 109 112 5 Nov 10 07:42 /tmp/imp-file-7
+ cat /tmp/imp-file-7
7577

...

+ cat /tmp/imp-file-7
7577
```

While the Stage-4 sleep keeps the container alive, you can confirm the file exists by inspecting the container on the controller:

```console theme={null}
$ docker ps
CONTAINER ID   IMAGE                                      STATUS
d1ae29e5fc61   0f559f3f6ac2...                            Up About a minute

$ docker exec -it d1ae29e5fc61 sh
/var/lib/jenkins/workspace/pipeline-external-agent $ cat /tmp/imp-file-7
7577
```

## Isolated containers per stage with `newContainerPerStage()`

If you need strict isolation between stages — for example, to ensure no filesystem state is carried over — use the `newContainerPerStage()` option. When applied together with a top-level `dockerfile` (or `docker`) agent, Jenkins will create a fresh container for each stage using the same image definition.

<Callout icon="lightbulb">
  Using `options { newContainerPerStage() }` makes Jenkins run each stage in a brand-new container created from the same Dockerfile. Files written to the container filesystem in one stage will not be visible in subsequent stages.
</Callout>

Example pipeline with `newContainerPerStage()`:

```groovy theme={null}
pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile.cowsay'
    }
  }

  options {
    newContainerPerStage()
  }

  stages {
    stage('Stage-1') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
        sh 'echo $((RANDOM)) > /tmp/imp-file-$BUILD_ID'
        sh 'ls -ltr /tmp/imp-file-$BUILD_ID'
        sh 'cat /tmp/imp-file-$BUILD_ID'
      }
    }

    stage('Stage-2') {
      steps {
        sh 'cat /etc/os-release'
        sh 'node -v'
        sh 'npm -v'
        sh 'ls -ltr /tmp/imp-file-$BUILD_ID'
        sh 'cat /tmp/imp-file-$BUILD_ID'
      }
    }
  }
}
```

Note: The `ls` and `cat` calls in `Stage-2` will typically fail because those files were created in the previous stage's container, not the current one.

When `newContainerPerStage()` is enabled, you will observe:

* Jenkins builds (or validates) the image and runs a new container for each stage.
* Files created inside one stage's container are not present in the next stage's container.
* Expect `No such file or directory` errors when trying to access stage-local files created previously.

Example trimmed failure log from Stage-2:

```console theme={null}
+ docker build -t 0f559f3f6ac2e220b... -f Dockerfile.cowsay .
$ docker run -t -d ... 0f559f3f6ac2e220b... cat
+ ls -ltr /tmp/imp-file-8
ls: /tmp/imp-file-8: No such file or directory
```

## Quick comparison

|           Behavior |                            Top-level `dockerfile` agent (default) |                          `options { newContainerPerStage() }` |
| -----------------: | ----------------------------------------------------------------: | ------------------------------------------------------------: |
| Containers created |                               Single container created and reused |                          New container created for each stage |
| Filesystem sharing |                                Yes — files persist between stages |                    No — each container has a fresh filesystem |
|           Use case | When stages need to share transient data (fast local persistence) | When you want strict stage isolation to avoid state carryover |
|   Node requirement |                                             Runs on the same node |                  Runs on the same node (different containers) |

## Summary

* A top-level `dockerfile` or `docker` agent builds the image and reuses a single container and workspace across all stages. Useful when you want to share files or state via the container filesystem.
* `options { newContainerPerStage() }` forces Jenkins to create a fresh container for each stage (using the same image definition). Use this when you need strict isolation between stages and want to avoid accidental state carryover.
* Choose the mode that matches your pipeline needs: inter-stage filesystem sharing vs. per-stage isolation.

## Links and references

* [Jenkins Pipeline: Agents documentation](https://www.jenkins.io/doc/book/pipeline/syntax/#agent)
* [Jenkins Pipeline: Options](https://www.jenkins.io/doc/book/pipeline/syntax/#options)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/d1f217e1-bfef-4ba3-adf8-1411e911e0bc/lesson/35e85091-048f-4fcf-a013-edde048ace6a" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/advanced-jenkins/module/d1f217e1-bfef-4ba3-adf8-1411e911e0bc/lesson/0dcae6c1-c8da-4ead-a160-d8e6c23bd8bf" />
</CardGroup>
