# Installation steps for Apache HTTPD...
```

* **Parent image**: `debian:buster-slim`
* Installs Apache HTTPD on a minimal Debian base.

## 3. Exploring the Debian Base Image

The Debian “slim” image originates from `scratch`:

```dockerfile theme={null}
FROM scratch
ADD rootfs.tar.xz /
CMD ["bash"]
```

* **Base image**: `scratch`
* Unpacks a minimal Debian filesystem from a tarball.

<Callout icon="triangle-alert">
  You cannot push or pull the `scratch` image—it's only referenced in `FROM scratch` directives.
</Callout>

### Table: Image Lineage at a Glance

| Layer          | Image Tag               | Parent               | Description                              |
| -------------- | ----------------------- | -------------------- | ---------------------------------------- |
| Application    | `custom-web-app:latest` | `httpd:latest`       | Apache HTTPD plus your `index.html`      |
| HTTPD Official | `httpd:latest`          | `debian:buster-slim` | Official Apache HTTPD on Debian          |
| Debian Base    | `debian:buster-slim`    | `scratch`            | Minimal Debian filesystem from `scratch` |

## 4. Additional Official Image Chains

### Ubuntu → MongoDB

1. **Ubuntu minimal from scratch**:
   ```dockerfile theme={null}
   FROM scratch
   ADD ubuntu-xenial-core-cloudimg-amd64-root.tar.gz /
   ```
2. **MongoDB on Ubuntu**:
   ```dockerfile theme={null}
   FROM ubuntu:xenial

   RUN groupadd -r mongodb \
    && useradd -r -g mongodb mongodb

   RUN set -eux; \
       apt-get update; \
       apt-get install -y --no-install-recommends \
           ca-certificates jq numactl; \
       if ! command -v ps >/dev/null; then \
           apt-get install -y --no-install-recommends procps; \
       fi
   ```

### WordPress → PHP → Debian

The [official WordPress image](https://hub.docker.com/_/wordpress) builds on the [official PHP image](https://hub.docker.com/_/php), which in turn uses Debian—demonstrating another `scratch` → Debian → PHP → WordPress chain.

<Frame>
  ![The image illustrates a comparison between base and parent images, showing different software stacks built on top of base images like Debian and Ubuntu, leading to applications like WordPress, MongoDB, and a custom web app.](https://kodekloud.com/kk-media/image/upload/v1752873911/notes-assets/images/Docker-Certified-Associate-Exam-Course-Base-vs-Parent-Image/base-parent-images-comparison.jpg)
</Frame>

## 5. The `scratch` Image: Docker’s True Base

* **`scratch`** is Docker’s reserved, empty image.
* It marks the very beginning of any build.
* By adding a minimal OS filesystem on top of `scratch`, maintainers create base images (Debian, Alpine, Ubuntu), which then serve as parents for application and service images.

For more details on building and using base images, see the [official Docker documentation on base images](https://docs.docker.com/develop/develop-images/baseimages/).

***

## Links and References

* [Docker Base Image Documentation](https://docs.docker.com/develop/develop-images/baseimages/)
* [HTTPD Official Image](https://hub.docker.com/_/httpd)
* [Debian Official Image](https://hub.docker.com/_/debian)
* [Ubuntu Official Image](https://hub.docker.com/_/ubuntu)
* [MongoDB Official Image](https://hub.docker.com/_/mongo)
* [WordPress Official Image](https://hub.docker.com/_/wordpress)
* [PHP Official Image](https://hub.docker.com/_/php)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/f2e605a0-1ea7-434b-a139-0db000b0a250/lesson/1aa19d98-d6fe-4487-987a-6c506ee0cf03" />
</CardGroup>


# Build Cache

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Image-Management/Build-Cache/page

Efficient use of Docker’s build cache can speed up image builds by reusing unchanged layers.

Efficient use of Docker’s build cache can dramatically speed up your image builds. Docker creates a cache layer for each instruction in your Dockerfile. When you rebuild the image, Docker reuses layers whose instructions and contexts haven’t changed, avoiding redundant work.

## How Docker’s Build Cache Works

```dockerfile theme={null}
FROM ubuntu
RUN apt-get update
RUN apt-get install -y python python3-pip
RUN pip3 install flask
COPY app.py /opt/source-code
ENTRYPOINT ["flask", "run"]
```

* Each `RUN`, `COPY`, or `ADD` instruction produces a layer.
* After a successful build, layers are stored in the local cache.
* On subsequent builds, Docker compares:
  1. The instruction itself.
  2. Any files referenced by `COPY`/`ADD`.
* If both match the cached layer, Docker reuses it.
* Any change invalidates that layer **and all subsequent layers**, triggering a rebuild from that point.

### Cache Invalidation Example

Changing the pip install command:

```dockerfile theme={null}
RUN pip3 install flask flask-mysql
```

Invalidates the `pip3 install` layer and everything that follows—earlier layers remain cached. Similarly, updating `app.py` in:

```dockerfile theme={null}
COPY app.py /opt/source-code
```

busts the cache from that layer onward.

***

## Cache Busting with Combined Instructions

Separating `apt-get update` and `apt-get install` can lead to stale package lists:

```dockerfile theme={null}
RUN apt-get update
RUN apt-get install -y python python3-pip python-dev
```

<Callout icon="triangle-alert">
  Stale package lists may cause installation of outdated or missing packages.
</Callout>

Instead, combine them:

```dockerfile theme={null}
RUN apt-get update && \
    apt-get install -y \
      python \
      python-dev \
      python3-pip
```

* Forces an update immediately before installation.
* Lists packages alphabetically and on separate lines for readability.

<Callout icon="lightbulb">
  Always include `&& rm -rf /var/lib/apt/lists/*` if you want to reduce image size.
</Callout>

### Version Pinning

Pinning package versions ensures consistent builds across environments:

```dockerfile theme={null}
RUN apt-get update && \
    apt-get install -y \
      python \
      python-dev \
      python3-pip=20.0.2
```

***

## Optimizing Instruction Order

Place instructions that change least frequently at the top of your Dockerfile. This maximizes cache reuse.

| Instruction Type         | Change Frequency | Caching Benefit                          |
| ------------------------ | ---------------- | ---------------------------------------- |
| Base Image & System      | Low              | Cached once unless you change the base   |
| Package Installation     | Low–Medium       | Reused until you add or remove packages  |
| Application Dependencies | Medium           | Rebuilt when dependencies change         |
| Application Code         | High             | Only this layer rebuilds on code changes |

### Example: Optimal Order

```dockerfile theme={null}
FROM ubuntu
