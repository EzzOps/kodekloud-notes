# Edit or create the configuration file on the host
vi prometheus.yml

# Run Prometheus in Docker with a bind mount and port mapping
docker run -d \
  --name prometheus \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
  -v /path/to/data:/prometheus \
  -p 9090:9090 \
  prom/prometheus
```

Prometheus Docker run flags and their purpose

| Flag / Option                                                  | Purpose                                              | Example / Notes                                                                      |
| -------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `-d`                                                           | Run the container in detached mode                   | Keeps container running in background                                                |
| `--name prometheus`                                            | Assign a friendly container name                     | Use this instead of container ID when managing                                       |
| `-v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml:ro` | Bind mount host config into container (read-only)    | Replace `/path/to/prometheus.yml` with the absolute path on your host                |
| `-v /path/to/data:/prometheus`                                 | Persist Prometheus TSDB data outside the container   | Optional but recommended for long-term metrics                                       |
| `-p 9090:9090`                                                 | Map host port 9090 to container port 9090            | Access UI at `http://localhost:9090` on the host                                     |
| `prom/prometheus`                                              | Image name (official Prometheus image on Docker Hub) | [https://hub.docker.com/r/prom/prometheus](https://hub.docker.com/r/prom/prometheus) |

Best practices and operational notes

* Always use an absolute path for the host side of bind mounts (e.g., `/home/user/prometheus.yml`), otherwise Docker may create unexpected anonymous volumes.
* The bind mount keeps the container's Prometheus configuration in sync with the host file: editing the host `prometheus.yml` will immediately update the file inside the container. Prometheus, however, needs to reload the configuration for changes to take effect.

> **warning** Prometheus will not automatically apply edited configs unless it reloads them. Either restart the container or trigger a config reload via Prometheus' reload mechanism (for example, POST to `/-/reload` if available). Check the Prometheus configuration reloading docs: [https://prometheus.io/docs/prometheus/latest/configuration/configuration/#reloading-configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#reloading-configuration)

Accessing the Prometheus UI

After the container starts, open your browser and go to:

[http://localhost:9090](http://localhost:9090)

This opens the Prometheus expression browser, status pages, and API endpoints.

Links and references

* Prometheus configuration and reloading: [https://prometheus.io/docs/prometheus/latest/configuration/configuration/](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
* Docker networking (host.docker.internal, networking details): [https://docs.docker.com/desktop/networking/](https://docs.docker.com/desktop/networking/)
* Official Prometheus Docker image on Docker Hub: [https://hub.docker.com/r/prom/prometheus](https://hub.docker.com/r/prom/prometheus)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/3ab9bea4-bfdd-474e-849b-ed7446b550d4)


# Client Library

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Push-Gateway/Client-Library/page

Guide to using the Python prometheus_client to push, merge, and delete metrics to Prometheus Pushgateway with examples and registry usage

In this lesson you'll learn how to push metrics to the Prometheus Pushgateway using the official Python client library, `prometheus_client`. This walkthrough covers the three primary push operations, the common workflow for creating and registering metrics, and examples of using the client API.

* Keywords: Prometheus Pushgateway, `prometheus_client`, `pushadd_to_gateway`, `push_to_gateway`, `delete_from_gateway`, `CollectorRegistry`, `Gauge`

## Pushgateway operations at a glance

| Operation           | HTTP method | Python function       | Behavior                                                           | Example                                                               |
| ------------------- | ----------- | --------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------- |
| push (replace)      | PUT         | `push_to_gateway`     | Replace all metrics for the specified job/grouping labels          | `push_to_gateway('pushgateway:9091', job='batch', registry=registry)` |
| pushadd (merge/add) | POST        | `pushadd_to_gateway`  | Add or merge metrics into the group without deleting other metrics | `pushadd_to_gateway('user2:9091', job='batch', registry=registry)`    |
| delete              | DELETE      | `delete_from_gateway` | Remove all metrics for the specified job/grouping labels           | `delete_from_gateway('pushgateway:9091', job='batch')`                |

## Minimal Python example

Below is a concise example that demonstrates the typical workflow:

1. Create a `CollectorRegistry`.
2. Define and register a `Gauge`.
3. Set a value.
4. Push the registry to the Pushgateway using `pushadd_to_gateway` (POST-like merge behavior).

```python theme={null}
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway
