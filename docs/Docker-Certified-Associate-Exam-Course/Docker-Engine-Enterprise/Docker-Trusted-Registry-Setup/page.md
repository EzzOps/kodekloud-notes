# On the remote host
mkdir -p ~/client-bundle
unzip ucp-bundle-{username}.zip -d ~/client-bundle
cd ~/client-bundle
```

Here's an example public key from the bundle:

```plaintext theme={null}
-----BEGIN PUBLIC KEY-----
MIGeMA0GCSqGSIb3DQEBAQUAA4GNADCB
[AWS_SECRET_ACCESS_KEY]2HZfSmKx24QDyCFRDoA=
-----END PUBLIC KEY-----
```

<Callout icon="triangle-alert">
  Your private keys and certificates grant full access to your UCP cluster. Handle them with care.
</Callout>

## 4. Configuring Environment Variables

Execute the provided environment script to set Docker CLI variables:

```bash theme={null}
cd ~/client-bundle
eval "$(env.sh)"
```

Verify your environment settings:

| Variable           | Description                          | Example                    |
| ------------------ | ------------------------------------ | -------------------------- |
| DOCKER\_HOST       | UCP manager endpoint                 | `tcp://172.31.32.217:443`  |
| DOCKER\_CERT\_PATH | Path to client certificates and keys | `/home/user/client-bundle` |

```bash theme={null}
echo $DOCKER_HOST
# If needed, switch to the private IP
export DOCKER_HOST=tcp://172.31.32.217:443
echo $DOCKER_HOST
echo $DOCKER_CERT_PATH
# /home/user/client-bundle
```

## 5. Verifying Connectivity

Ensure your CLI can communicate with UCP:

```bash theme={null}
docker node ls
# ID                          HOSTNAME     STATUS  AVAILABILITY  MANAGER STATUS  ENGINE VERSION
# vpns18n5tj7c59rcx4t26oz06   dtrnode      Ready   Active        Active          19.03.5
# g2gzfa9lrijoyg7atl2avveu6r   * ucpmanager Ready   Active        Leader          19.03.5
docker service ls
```

If both commands succeed, your Docker CLI is correctly configured to manage UCP.

## 6. Deploying a Test Application

Create a simple HTTP service on port 83:

```bash theme={null}
docker service create \
  --name kodekloudtest \
  --publish 83:80 \
  httpd:alpine
```

Check the task status:

```bash theme={null}
docker service ps kodekloudtest
# ID            NAME               IMAGE          NODE       DESIRED STATE  CURRENT STATE
# 1yatpy8tm6gi  kodekloudtest.1    httpd:alpine   ucpworker  Running        Running 2 minutes ago
```

Visit `http://<UCP_WORKER_IP>:83` in your browser. You should see the default Apache welcome page. The service also appears under **Swarm** in the UCP console.

## 7. Cleaning Up

Remove the test service:

```bash theme={null}
docker service rm kodekloudtest
```

Refresh the UCP console; the `kodekloudtest` service will be gone.

***

## References

[1]: https://docs.docker.com/ee/engine/ "Docker Engine Enterprise Documentation"

[Universal Control Plane]: https://docs.docker.com/ee/ucp/ "UCP Docs"

[Docker Hub]: https://hub.docker.com/

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/a6a39359-7fb1-4fab-b0c2-6fc58a6ce617/lesson/6942644f-7a76-4b79-baa5-322ed1d6edb1" />
</CardGroup>


# Docker Trusted Registry Setup

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine-Enterprise/Docker-Trusted-Registry-Setup/page

This guide explores Docker Trusted Registry, its capabilities, and deployment within a Docker Universal Control Plane cluster.

In this guide, we’ll explore Docker Trusted Registry (DTR), starting with a quick recap of Docker Registry, then diving into DTR’s capabilities, and finally covering deployment and configuration within a Docker Universal Control Plane (UCP) cluster.

## Docker Registry Recap

Docker Registry is the central store for container images. By default, `docker pull` and `docker push` interact with Docker Hub. To target a private registry or another namespace, include the full path:

```bash theme={null}
