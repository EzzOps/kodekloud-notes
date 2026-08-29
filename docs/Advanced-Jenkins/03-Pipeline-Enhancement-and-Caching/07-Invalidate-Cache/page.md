# HELP jvm_memory_bytes_used Used bytes of a given JVM memory area.
# TYPE jvm_memory_bytes_used gauge
jvm_memory_bytes_used{area="heap",} 1.051688996E8
jvm_memory_used{area="nonheap",} 1.18338064E8
# HELP jvm_memory_pool_bytes_used Used bytes of a given JVM memory pool.
# TYPE jvm_memory_pool_bytes_used gauge
jvm_memory_pool_bytes_used{pool="Metaspace",} 8.5643168E7
jvm_memory_pool_bytes_used{pool="G1 Old Gen",} 1.02023168E8
# HELP jvm_memory_bytes_committed Committed (bytes) of a given JVM memory area.
# TYPE jvm_memory_bytes_committed gauge
jvm_memory_bytes_committed{area="heap",} 3.5651584E8
```

Run Prometheus + Grafana (example Docker Compose)
This Docker Compose example brings up Prometheus and Grafana. Grafana is configured with `admin` / `password` credentials and is reachable on host port `8081`. Prometheus reads `/etc/prometheus/prometheus.yml` from the `./prometheus` folder.

```yaml theme={null}
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    ports:
      - 9090:9090
    restart: unless-stopped
    volumes:
      - ./prometheus:/etc/prometheus
      - prom_data:/prometheus

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - 8081:3000
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password
    volumes:
      - ./grafana:/etc/grafana/provisioning/datasources

volumes:
  prom_data:
```

Prometheus configuration: `prometheus.yml`
Place this minimal `prometheus.yml` in `./prometheus/prometheus.yml` (update the Jenkins target to your host/IP):

```yaml theme={null}
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    metrics_path: /metrics
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'jenkins'
    metrics_path: /prometheus
    scheme: http
    static_configs:
      - targets: ['64.227.187.25:8080']  # replace with your Jenkins host:port
```

Start the stack

```bash theme={null}
# from the directory containing docker-compose.yml
docker compose up -d
```

Example Docker Compose output:

```text theme={null}
[+] Running 4/4
✔ Network prometheus-grafana_default    Created      0.1s
✔ Volume "prometheus-grafana_prom_data" Created      0.0s
✔ Container prometheus                  Started      0.6s
✔ Container grafana                     Started      0.6s
```

Verify Prometheus is scraping Jenkins

* Open Prometheus at `http://<vm-ip>:9090` (or `http://localhost:9090`).
* Navigate to Status → Targets and confirm the `jenkins` job target is UP and scraping the `/prometheus` path.

Exploring Jenkins metrics in Prometheus
Common metric names exposed by the plugin:

| Metric                          | What it measures                        | Example query                                   |
| ------------------------------- | --------------------------------------- | ----------------------------------------------- |
| `jenkins_job_count_value`       | Total number of jobs                    | `jenkins_job_count_value`                       |
| `jenkins_plugins_active`        | Number of active plugins (gauge)        | `jenkins_plugins_active`                        |
| `jenkins_plugins_withUpdate`    | Plugins with available updates (gauge)  | `jenkins_plugins_withUpdate`                    |
| `jenkins_job_queuing_duration`  | Job queue durations (histogram/summary) | `jenkins_job_queuing_duration{quantile="0.95"}` |
| `jenkins_executor_in_use_value` | Executors currently in use              | `jenkins_executor_in_use_value`                 |

Example Prometheus expression queries:

```text theme={null}
jenkins_job_count_value
jenkins_plugins_withUpdate
jenkins_job_queuing_duration{quantile="0.95"}
```

Prometheus sample metric lines:

```text theme={null}
jenkins_job_count_value{instance="64.227.187.25:8080", job="jenkins"} 22
jenkins_plugins_withUpdate{instance="64.227.187.25:8080", job="jenkins"} 77
```

Add Prometheus as a Grafana data source

1. Log in to Grafana at `http://<vm-ip>:8081` using the admin credentials.
2. Add a new Prometheus data source. If Grafana and Prometheus are in the same Docker network, use `http://prometheus:9090`. If accessing externally, use `http://<vm-ip>:9090`.

<Frame>
  <img alt="A dark-themed Grafana settings page for a Prometheus data source named &#x22;Jenkins-Prometheus,&#x22; showing connection details including the Prometheus server URL set to &#x22;http://prometheus:9090.&#x22;" />
</Frame>

Import a Jenkins dashboard
Grafana has community dashboards for Jenkins. Search Grafana Dashboards for "Jenkins" and import one that fits your needs — for example, dashboard ID 9964 ("Jenkins: Performance and Health Overview"). To import:

* In Grafana go to Dashboards → Import
* Enter dashboard ID `9964`, select a name and folder, and map the panels to your Prometheus data source

<Frame>
  <img alt="A Grafana Labs webpage showing a &#x22;Jenkins: Performance and Health Overview&#x22; dashboard screenshot with multiple metrics and graphs. A right-hand panel offers options to get the dashboard (create account, copy ID, download JSON)." />
</Frame>

<Frame>
  <img alt="A Grafana &#x22;Import dashboard&#x22; screen showing the process of importing a &#x22;Jenkins: Performance and Health Overview&#x22; dashboard from Grafana.com. The page displays fields for name, folder, UID and selecting a Prometheus data source." />
</Frame>

Generate test metric activity in Jenkins
To see activity in dashboards, create a simple Jenkins Pipeline job and run it repeatedly:

1. Create a new Pipeline job (e.g., `monitor-jenkins`).
2. Use an inline Pipeline script like:

```groovy theme={null}
node {
    stage('Sleep') {
        sh 'sleep 2'
    }
}

node('ubuntu-docker-jdk17-node20') {
    stage('Echo') {
        sh 'echo "1s"'
    }
}
```

<Frame>
  <img alt="A browser screenshot of the Jenkins &#x22;New Item&#x22; page in dark mode showing the item name field filled with &#x22;monitor-jenkins&#x22; and selectable job types (Freestyle project, Pipeline, Multi-configuration project, Folder). The page includes an OK button at the bottom and standard browser UI at the top." />
</Frame>

Make sure the node label you reference exists and matches an available agent. The agent label can be verified on the agent details page:

<Frame>
  <img alt="A screenshot of the Jenkins web UI showing the &#x22;Agent ubuntu-agent&#x22; details page. The agent is connected and a label &#x22;ubuntu-docker-jdk17-node20&#x22; is highlighted, with the left sidebar of Jenkins management options visible." />
</Frame>

Trigger the pipeline several times (Build Now). Prometheus will scrape the metrics at its configured interval and Grafana dashboards will begin to reflect the activity. You should see panels for JVM memory, CPU, job counts (total/successful/failed), executor usage, queue durations, and other Jenkins metrics. Customize panels (time series, gauge, heatmap, etc.) and refine PromQL queries to suit your monitoring and alerting needs.

<Frame>
  <img alt="A Grafana dashboard screenshot showing Jenkins performance and health metrics, with panels for JVM free memory, memory usage, Jenkins health, CPU usage, job counts (total/successful/failed), job duration and executor stats. The left sidebar shows navigation items like Dashboards, Explore, Alerting and Administration." />
</Frame>

Prometheus summaries & quantiles
The Prometheus exposition may include quantiles for summaries/histograms. Example for queue durations:

```text theme={null}
jenkins_job_queuing_duration{instance="64.227.187.25:8080", job="jenkins", quantile="0.5"} 7.04
jenkins_job_queuing_duration{instance="64.227.187.25:8080", job="jenkins", quantile="0.95"} 13.0
```

These quantiles help with capacity planning and diagnosing issues like executor saturation or slow builds.

Further reading & references

* Jenkins Prometheus metrics plugin — plugin page (Manage Plugins in Jenkins)
* Prometheus exposition formats — [https://prometheus.io/docs/instrumenting/exposition\_formats/](https://prometheus.io/docs/instrumenting/exposition_formats/)
* Prometheus documentation — [https://prometheus.io/docs/](https://prometheus.io/docs/)
* Grafana dashboards search — [https://grafana.com/grafana/dashboards](https://grafana.com/grafana/dashboards)
* Example dashboard: Jenkins: Performance and Health Overview (ID 9964) — [https://grafana.com/grafana/dashboards/9964](https://grafana.com/grafana/dashboards/9964)

Summary
You now know how to:

* Expose Jenkins metrics via the Prometheus plugin at `/prometheus`
* Configure Prometheus to scrape Jenkins metrics
* Run Prometheus and Grafana with Docker Compose
* Add Prometheus as a Grafana data source and import a Jenkins dashboard
* Generate Jenkins activity to validate the metrics and dashboards

Use the dashboards to monitor Jenkins health, plan capacity, and create alerts when metrics indicate problems (e.g., queue growth or executor saturation).

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/fe8b8755-ab0a-429d-ac8c-a7763f723359/lesson/38c29145-23ba-4230-aee1-cefe9984deb4)


# Invalidate Cache

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Pipeline-Enhancement-and-Caching/Invalidate-Cache/page

Explains using the Jenkins Job Cacher plugin with package-lock.json to invalidate and refresh dependency caches, keeping builds fast and preventing stale node_modules.

In this lesson we show how to invalidate a Jenkins dependency cache automatically whenever project dependencies change — specifically when `package-lock.json` (or `yarn.lock`) is updated. This ensures fast builds when dependencies are unchanged, and safe cache refreshes when they are not.

<Frame>
  <img alt="A blue-to-teal gradient slide with subtle diamond shapes and centered white text that reads &#x22;Invalidate Caching.&#x22; A small &#x22;© Copyright KodeKloud&#x22; appears in the bottom-left." />
</Frame>

The Job Cacher plugin supports a cache-validity mechanism using a cache-validity deciding file (for example: `package-lock.json`). When that file changes, the plugin computes a new hash and decides whether an existing cache is still valid. Below is the Jenkins pipeline snippet used to cache `node_modules` and to make `package-lock.json` the cache-validity file.

```groovy theme={null}
options { timestamps() }
steps {
  cache(maxCacheSize: 550, caches: [
    arbitraryFileCache(
      cacheName: 'npm-dependency-cache',
      cacheValidityDecidingFile: 'package-lock.json',
      includes: '**/*',
      path: 'node_modules')
  ]) {
    sh 'node -v'
    sh 'npm install --no-audit'
    stash(includes: 'node_modules/', name: 'solar-system-node-modules')
  }
}
```

Demonstration — add a dependency locally in the repository:

```bash theme={null}
root@jenkins-controller-1 in solar-system on ⬢ feature/advanced-demo via ⬢ v20.16.0 on ☁ (us-east-2)
➜ npm install localtunnel
```

npm reports the new installation:

```console theme={null}
added 7 packages, and audited 366 packages in 2s

45 packages are looking for funding
  run `npm fund` for details

10 vulnerabilities (1 low, 4 moderate, 5 high)

To address issues that do not require attention, run:
  npm audit fix

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
```

Installing the dependency updates both `package.json` and `package-lock.json`. When you commit and push these changes the pipeline triggers, and the Job Cacher plugin computes a hash of `package-lock.json` and compares it with the hash associated with the stored cache archive.

Representative pipeline logs for the two outcomes:

1. Cache is up-to-date and is restored:

```console theme={null}
[Cache for node_modules (npm-dependency-cache) with id 3ec03583f8eaec275cb2183db769ff47] Searching cache in job specific caches...
[Cache for node_modules (npm-dependency-cache) with id 3ec03583f8eaec275cb2183db769ff47] got hash a47b9ef02dbc79db72ab6385105e0142 for cacheValidityDecidingFile(s) - actual file(s): /var/lib/jenkins/workspace/solar-system_feature_advanced-demo/package-lock.json
[Cache for node_modules (npm-dependency-cache) with id 3ec03583f8eaec275cb2183db769ff47] Found cache in job specific caches
[Cache for node_modules (npm-dependency-cache) with id 3ec03583f8eaec275cb2183db769ff47] Restoring cache...
[Cache for node_modules (npm-dependency-cache) with id 3ec03583f8eaec275cb2183db769ff47] Cache restored in 771ms
+ node -v
v22.6.0
+ npm install --no-audit
up to date in 1s

44 packages are looking for funding
  run `npm fund` for details

Stashed 4993 file(s)
[Cache for node_modules (npm-dependency-cache) ...] Skip cache creation as the cache is up-to-date
```

2. `package-lock.json` changed — cache is outdated and is recreated:

```console theme={null}
[Cache for node_modules (npm-dependency-cache) with id 3ec03583f8eaec275cb2183db769ff47] Searching cache in job specific caches...
[Cache for node_modules (npm-dependency-cache) with id 3ec03583f8eaec275cb2183db769ff47] got hash 5a15d94c8bab08a6882fddf4b8ef16c2 for cacheValidityDecidingFile(s) - actual file(s): /var/lib/jenkins/workspace/solar-system_feature_advanced-demo/package-lock.json
[Cache for node_modules (npm-dependency-cache) ...] cacheValidityDecidingFile configured, but previous hash does not match - cache outdated
[Cache for node_modules (npm-dependency-cache) ...] Skip restoring cache as no up-to-date cache exists
+ node -v
v22.6.0
+ npm install --no-audit
added 7 packages in 2s

45 packages are looking for funding
  run `npm fund` for details

Stashed 5131 file(s)
[Cache for node_modules (npm-dependency-cache) ...] Creating cache...
[Cache for node_modules (npm-dependency-cache) ...] Cache created in 2179ms
```

How it works (step-by-step)

* The plugin computes a hash of the configured cache-validity file(s) (in this example: `package-lock.json`) in the current workspace.
* It compares that hash with the hash associated with the existing cache for this job.
  * If the hashes match, the plugin restores the cache and the build step finishes quickly (for example: `npm install` reports "up to date").
  * If the hashes differ, the plugin treats the cache as outdated, skips restoration, runs the install to produce up-to-date `node_modules`, then creates a new cache using the new hash.
* Subsequent builds with the same `package-lock.json` content will restore the newly created cache until the lockfile changes again.

Quick reference table

|                                     Condition | Plugin action                               | Typical result                          |
| --------------------------------------------: | ------------------------------------------- | --------------------------------------- |
| `package-lock.json` hash matches stored cache | Restore cache                               | `npm install` is fast — "up to date"    |
|              `package-lock.json` hash differs | Skip restore, run install, create new cache | Fresh `node_modules` created and cached |

> **lightbulb** Use `cacheValidityDecidingFile` (for example, `package-lock.json` or `yarn.lock`) so the Job Cacher invalidates dependency caches whenever the lockfile changes. This maintains build speed for unchanged dependencies while preventing stale or incompatible modules from being reused.

Links and references

* Job Cacher plugin (Jenkins) — check the plugin documentation in your Jenkins instance or the plugin site for configuration details.
* Jenkins pipeline documentation: [https://www.jenkins.io/doc/book/pipeline/](https://www.jenkins.io/doc/book/pipeline/)
* npm lockfile formats and behavior: [https://docs.npmjs.com/cli/v9/configuring-npm/package-lock-json](https://docs.npmjs.com/cli/v9/configuring-npm/package-lock-json)

That's all for now.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/5352396d-b54f-4910-a874-f2aa70e88823/lesson/76c00408-e665-402e-a09d-1715cee27864)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/advanced-jenkins/module/5352396d-b54f-4910-a874-f2aa70e88823/lesson/495a7c20-3447-469a-aa67-d330dcb9c00d)
