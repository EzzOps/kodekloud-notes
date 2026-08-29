# Pipeline Monitoring with Prometheus and Grafana

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Optimization-Security-and-Monitoring/Pipeline-Monitoring-with-Prometheus-and-Grafana/page

This guide details a centralized monitoring solution for GitLab CI/CD pipelines using Prometheus and Grafana.

In this guide, we’ll architect a centralized monitoring solution for all your GitLab CI/CD pipelines using the [GitLab CI Pipelines Exporter][1], Prometheus, and Grafana. Collect metrics across multiple projects and visualize them in real time.

## 1. GitLab’s Built-in CI/CD Analytics

GitLab offers a per-project CI/CD analytics dashboard that displays overall pipeline success rates and duration trends. While convenient for a handful of repositories, it doesn’t scale to dozens of projects:

![The image shows a CI/CD analytics dashboard from GitLab, displaying overall pipeline statistics and a chart of pipeline durations for the last 30 commits.](https://kodekloud.com/kk-media/image/upload/v1752877370/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/gitlab-cicd-analytics-dashboard.jpg)

## 2. Centralized Pipeline Monitoring

To obtain a global view, pair Prometheus with Grafana and the GitLab CI Pipelines Exporter:

![The image shows a GitLab documentation page about pipeline monitoring, including text and a dashboard screenshot with metrics and visualizations.](https://kodekloud.com/kk-media/image/upload/v1752877371/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/gitlab-pipeline-monitoring-dashboard.jpg)

The **GitLab CI Pipelines Exporter** polls GitLab’s API, translates pipelines, jobs, and environment metrics into Prometheus format, and ships three Grafana dashboards out of the box.

## 3. GitLab CI Pipelines Exporter

![The image shows a GitHub repository page for "gitlab-ci-pipelines-exporter," including file listings, a README section, and contributor information. The repository is primarily written in Go.](https://kodekloud.com/kk-media/image/upload/v1752877372/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Pipeline-Monitoring-with-Prometheus-and-Grafana/github-repo-gitlab-ci-pipelines.jpg)

### 3.1 Installation Options

Choose the installer that matches your environment:

| Platform         | Install Command                                                                                                                        |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| macOS (Homebrew) | `brew install mvisonneau/tap/gitlab-ci-pipelines-exporter`                                                                             |
| Docker           | `docker run -it --rm quay.io/mvisonneau/gitlab-ci-pipelines-exporter:latest`                                                           |
| Windows (Scoop)  | `scoop bucket add gitlab-ci-pipelines-exporter https://github.com/mvisonneau/scoops`<br />`scoop install gitlab-ci-pipelines-exporter` |
| Nix              | `nix-env -iA nixos.prometheus-gitlab-ci-pipelines-exporter`                                                                            |

### 3.2 Quickstart Example

A Docker Compose quickstart brings up the exporter, Prometheus, and Grafana in one go:

```bash theme={null}
git clone https://github.com/mvisonneau/gitlab-ci-pipelines-exporter.git
cd gitlab-ci-pipelines-exporter/examples/quickstart
