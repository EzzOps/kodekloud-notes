# restart docker
$ sudo systemctl restart docker

# verify metrics endpoint
$ curl http://localhost:9323/metrics
```

Then add a Prometheus scrape job to pull those metrics. If Prometheus runs on a different host, replace `127.0.0.1` with the Docker host IP or hostname:

```yaml theme={null}
scrape_configs:
  - job_name: "docker"
    static_configs:
      - targets: ["12.1.13.4:9323"]
```

Notes:

* Use a stable hostname or IP for the target so Prometheus can reliably scrape metrics.
* Consider network/firewall rules and authentication if scraping remotely.

## 2. Enable cAdvisor for per-container metrics

cAdvisor (Container Advisor) provides per-container metrics: CPU, memory, filesystem usage, process counts, and container uptime. Run cAdvisor on the Docker host so it can inspect containers and the host filesystem.

Example `docker-compose.yml` for cAdvisor:

```yaml theme={null}
version: '3.4'
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    container_name: cadvisor
    privileged: true
    devices:
      - "/dev/kmsg:/dev/kmsg"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker:/var/lib/docker:ro
      - /dev/disk:/dev/disk:ro
    ports:
      - 8080:8080
```

Start cAdvisor and confirm its metrics endpoint:

```bash theme={null}
$ docker-compose up -d
$ curl http://localhost:8080/metrics
```

If you need the project source or more configuration options, see the cAdvisor repository: `https://github.com/google/cadvisor`.

> **warning** cAdvisor requires elevated privileges and host volumes to provide accurate metrics. Run it only on trusted hosts and review security implications (`privileged: true`, host mounts).

Add a Prometheus scrape job for cAdvisor (replace the host/IP as needed):

```yaml theme={null}
scrape_configs:
  - job_name: "cadvisor"
    static_configs:
      - targets: ["12.1.13.4:8080"]
```

## 3. What metrics to expect

* Docker Engine metrics: engine/daemon-level metrics such as daemon CPU usage, queue lengths, API request durations, image build counts, and engine errors.
* cAdvisor metrics: per-container resource metrics — CPU and memory usage by container, filesystem I/O, process counts inside containers, and container lifetime statistics.

Use Docker Engine metrics to monitor the health and behavior of the Docker daemon. Use cAdvisor for container-level resource visibility and troubleshooting.

## 4. Quick comparison

| Metric Source | Exposed Metrics                                              | Typical Use Case                                     | Notes                                                        |
| ------------- | ------------------------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------ |
| Docker Engine | Daemon CPU, internal counters, API operation metrics         | Monitor Docker daemon health and operational metrics | Enabled via `daemon.json` and experimental `metrics-addr`    |
| cAdvisor      | CPU/memory per container, filesystem, process counts, uptime | Per-container resource usage and debugging           | Runs as a container; needs privileged access and host mounts |

## 5. Troubleshooting checklist

* If `curl` to the metrics endpoint times out, check firewall rules and whether Docker/cAdvisor is bound to localhost vs 0.0.0.0.
* Use correct host/IP in Prometheus `targets` when Prometheus is remote.
* Confirm container mounts and privileges for cAdvisor if metrics are missing or incomplete.
* Check Docker daemon logs (`sudo journalctl -u docker`) for errors after editing `daemon.json`.

## Links and references

* Prometheus documentation: [https://prometheus.io/docs/](https://prometheus.io/docs/)
* cAdvisor GitHub: `https://github.com/google/cadvisor`
* Docker daemon docs: [https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file](https://docs.docker.com/engine/reference/commandline/dockerd/#daemon-configuration-file)

<Frame>
  <img alt="The image compares Docker Engine metrics with cAdvisor metrics, highlighting the differences in CPU/memory usage, process information, and container-specific metrics." />
</Frame>

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/3d28738a-eeee-491d-985d-71519bd728e8)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/8a6a6f76-ea0b-4965-94dd-46cd20a39a7f)


# Node Exporter systemd

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Node-Exporter-systemd/page

Instructions to install and configure node_exporter as a systemd service, create a dedicated non-login user, enable it at boot, and verify metrics are exposed.

As with [Prometheus](https://prometheus.io/), starting node\_exporter directly runs it in the foreground and does not enable it to start automatically on boot. To have systemd manage node\_exporter (so you can use commands like `systemctl start node_exporter` and have it start on boot), follow the steps below.

Overview of the steps

* Download and extract the node\_exporter binary (if you haven't already).
* Move the binary to `/usr/local/bin`.
* Create a dedicated (non-login) user for node\_exporter.
* Ensure the node\_exporter binary is owned by that user.
* Add a systemd service unit for node\_exporter.
* Reload systemd, start, enable, and verify the service.
* Verify metrics are exposed at `/metrics`.

Commands and service unit

1. Change into the node\_exporter directory (after downloading and extracting):

```bash theme={null}
