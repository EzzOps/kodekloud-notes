# Prometheus

Source: https://notes.kodekloud.com/docs/Jenkins/Systems-Administration-with-Jenkins/Prometheus/page

This article explains how to integrate Prometheus with Jenkins to automatically expose and monitor Jenkins metrics.

In this lesson, we explore how the Jenkins Prometheus Metrics Plugin automatically exposes Jenkins metrics on a dedicated endpoint. By accessing the URL `http://<jenkins_server_ip>:8080/Prometheus`, you can view metrics output similar to the sample below:

```plaintext theme={null}
