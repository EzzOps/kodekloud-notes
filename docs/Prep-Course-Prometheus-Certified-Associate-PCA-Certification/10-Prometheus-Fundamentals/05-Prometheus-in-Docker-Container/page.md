# Prometheus in Docker Container

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-in-Docker-Container/page

Guide to running Prometheus in a Docker container using bind-mounted configuration, exposing port 9090, and handling Docker networking and data persistence

This guide shows how to run Prometheus inside a Docker container. The typical workflow is simple:

* Pull the official Prometheus image from Docker Hub.
* Provide a Prometheus configuration file (`prometheus.yml`) from the host into the container using a bind mount.
* Expose Prometheus' HTTP port so you can access the UI and API.

When running Prometheus in a container, the configuration format remains identical to running on a VM or bare-metal server. You still provide a `prometheus.yml` with your `scrape_configs` and `global` settings. Below is a minimal configuration that instructs Prometheus to scrape itself.

<Frame>
  <img alt="The image is a flowchart illustrating the setup of Prometheus Docker, showing steps like pulling the image from DockerHub, using a Prometheus configuration file, and setting ports and bind mounts." />
</Frame>

Example `prometheus.yml`:

```yaml theme={null}
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
```

Notes about `localhost` inside a container

* `localhost:9090` refers to the container's loopback interface. Use this target when Prometheus scrapes metrics exposed by processes running in the same container (for example, Prometheus scraping itself).
* To scrape services running on the Docker host from inside the container, use `host.docker.internal:PORT` (supported on Docker Desktop) or run the container with `--network=host` on Linux. See Docker networking docs for more details: [https://docs.docker.com/desktop/networking/](https://docs.docker.com/desktop/networking/)

> **lightbulb** If you need Prometheus inside the container to reach services on the Docker host, prefer `host.docker.internal` on Docker Desktop. On Linux, `--network=host` is an easy option, but it only works on Linux hosts.

Create the `prometheus.yml` on your host (for example with `vi` or your preferred editor), then run the Prometheus container with a bind mount that maps your host configuration into `/etc/prometheus/prometheus.yml` inside the container. Expose port `9090` so you can access Prometheus from the host browser.

Example commands:

```bash theme={null}
