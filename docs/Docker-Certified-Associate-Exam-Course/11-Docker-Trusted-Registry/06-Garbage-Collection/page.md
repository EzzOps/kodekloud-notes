# Explicitly specifying Docker Hub
image: docker.io/httpd/httpd

# Omitting the registry (defaults to Docker Hub)
image: httpd/httpd
```

> **lightbulb** If you leave out the registry host, Docker assumes `docker.io`. Always include the full path when pushing to a private registry.

***

## Using an Internal Registry

In a Docker Enterprise environment with your own registry (e.g., `registry.company.org`), image references must include that host:

```text theme={null}
registry.company.org/httpd/httpd
```

> **triangle-alert** If you don’t have a DNS entry for your registry, you can use its IP address. However, using a stable DNS name is recommended to avoid future disruptions.

### 1. Build and Tag Your Image

Build your application and tag it for the internal registry. Replace `54.145.234.153` with your registry’s IP or hostname, and adjust the namespace/repository as needed:

```bash theme={null}
docker build . -t 54.145.234.153/yogeshraheja/kodekloud
```

### 2. Create the Repository in DTR UI

Before pushing, create the repository via the DTR web interface:

* Click **New Repository**.
* Enter the **Namespace** (user or organization).
* Provide a **Repository name**.
* (Optional) Add a **Description**.
* Set the **Visibility** (public or private).

![The image shows a form for creating a new repository, with fields for the repository name, description, and visibility options (public or private).](https://kodekloud.com/kk-media/image/upload/v1752873960/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Trusted-Registry-Operations/new-repository-form-fields.jpg)

### 3. Push the Image to DTR

With the repository created, push your tagged image:

```bash theme={null}
# Build and tag (if not already done)
docker build . -t 54.145.234.153/yogeshraheja/kodekloud

# Push to your private registry
docker push 54.145.234.153/yogeshraheja/kodekloud
```

Once the push completes, you’ll see the repository listed under **Repositories** in the DTR interface.

![The image shows a Docker Enterprise Trusted Registry interface with a repository named "yogeshraja / kodekloud" displayed. The sidebar includes options like Repositories, Organizations, Users, and System.](https://kodekloud.com/kk-media/image/upload/v1752873961/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Trusted-Registry-Operations/docker-enterprise-trusted-registry.jpg)

### 4. Pulling the Image

Other team members can now retrieve the image:

```bash theme={null}
docker pull 54.145.234.153/yogeshraha/kodekloud
```

This completes the standard workflow: build, tag, create, push, and pull images within Docker Trusted Registry.

***

## Links and References

* [Docker Official Documentation](https://docs.docker.com/)
* [Docker Trusted Registry Guide](https://docs.docker.com/ee/dtr/)
* [Docker Hub](https://hub.docker.com/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d0ef5db6-09b0-45f3-a220-9036d58086c6/lesson/c82b52a7-775f-4f0c-82b8-0915b762e546)


# Garbage Collection

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Trusted-Registry/Garbage-Collection/page

Managing disk space in Docker Trusted Registry by running garbage collection to reclaim storage from unreferenced layers after image tag deletion.

Managing disk space in Docker Trusted Registry (DTR) is essential for stable registry performance. DTR stores images as layers, and when you delete an image tag via the UI, only the tag is removed—the underlying layers remain on disk. To reclaim storage, you must run garbage collection (GC), which identifies and deletes unreferenced layers.

## Why Garbage Collection Matters

* Layers are shared across multiple images and tags.
* Deleting a tag does **not** free disk space immediately.
* Premature removal of shared layers can break other images.

> **lightbulb** Only image tags are removed when you delete an image in the UI. Layers stay on disk until garbage collection runs.

## Configuring Garbage Collection

In the DTR UI, navigate to **System** → **Garbage Collection**. Choose one of the following schedule options:

| Schedule Option | Description                                             |
| --------------- | ------------------------------------------------------- |
| Interval        | Run GC at a recurring interval (e.g., daily).           |
| Until done      | Perform a full scan and delete all unreferenced layers. |
| Fixed duration  | Run GC for a specified number of minutes.               |
| Never           | Disable GC; disk usage will continue to grow.           |

> **triangle-alert** Garbage collection is CPU- and I/O-intensive. Schedule it during off-peak hours to minimize performance impact.

![The image contains notes about garbage collection in a system, explaining that deleting images doesn't free up space and detailing the process and considerations for scheduling garbage collection.](https://kodekloud.com/kk-media/image/upload/v1752873962/notes-assets/images/Docker-Certified-Associate-Exam-Course-Garbage-Collection/garbage-collection-notes-system.jpg)

## Garbage Collection Workflow

1. **Read-only mode**\
   DTR blocks image pushes and modifications; pulls remain allowed.
2. **Marking**\
   DTR scans for unreferenced layers and marks them.
3. **Deletion**\
   DTR deletes the marked layers, reclaiming disk space.

Plan a maintenance window, as GC can temporarily impact registry operations.

## Links and References

* [Docker Trusted Registry Garbage Collection](https://docs.docker.com/ee/dtr/gc/)
* [Docker Enterprise Documentation](https://docs.docker.com/ee/)
* [Registry Maintenance Best Practices](https://docs.docker.com/registry/maintenance/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d0ef5db6-09b0-45f3-a220-9036d58086c6/lesson/3865ce68-44ef-4ba3-9f64-5392584fe186)
