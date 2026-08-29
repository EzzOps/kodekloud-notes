# List pods (if a Kubernetes-based lab environment is provided)
kubectl get pods

# Show services
kubectl get svc
```

<Frame>
  <img alt="The image is a slide titled &#x22;Course Topics Overview&#x22; with a teal left panel and white content area. It lists five numbered Kafka course topics: Introduction to Kafka; Components & Architecture; Producers and Consumers; Kafka Topics & Partitions; and Kafka Environment Setup." />
</Frame>

As you progress through the labs, you'll develop and configure producers and consumers to send and receive messages from Kafka topics. Labs are ordered to move you from basic concepts to practical development and deployment, with each task building on the previous one so you can validate understanding incrementally.

Next steps

* Start the first lab in this lesson (Introduction to Kafka).
* Follow the Overview for concepts, then complete Tasks using the embedded terminal.
* Use Hint/Solution if needed, and run the Check step to confirm completion.

Links and references

* Apache Kafka documentation: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
* Confluent Kafka resources: [https://www.confluent.io/resources/](https://www.confluent.io/resources/)
* Kafka tutorials and examples: [https://kafka.apache.org/quickstart](https://kafka.apache.org/quickstart)

Now, let's jump in — navigate to the first lab and begin.

- [Watch Video](https://learn.kodekloud.com/user/courses/learn-by-doing-beginner-s-guide-to-apache-kafka-foundations-and-development/module/3e950c1f-5f14-4d73-9df6-7040a387aa53/lesson/cd8d8340-7c85-4115-9026-832cec952418)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Learn-By-Doing-Deploying-and-Managing-the-EFK-Stack-on-Kubernetes/Learn-by-Doing-EFK-Stack/Course-Introduction/page

Hands-on course teaching deployment, configuration, scaling, monitoring and securing the EFK stack on Kubernetes using live labs and guided exercises

Welcome to this learn-by-doing lesson: "Deploying and Managing the EFK Stack on Kubernetes." I’m Vijin Palazhi, and along with Harshita Joshi, we’ll guide you through hands-on labs that teach how to deploy, configure, scale, monitor, and secure the EFK stack (Elasticsearch, Fluentd, Kibana) on Kubernetes.

This course is designed for DevOps engineers, system administrators, and cloud professionals who want practical, repeatable workflows for log aggregation, analysis, and visualization in Kubernetes environments. You will get step-by-step exercises, live cluster access, and verification checks so you can validate each hands-on task as you progress.

<Frame>
  <img alt="The image illustrates a diagram showing three roles—DevOps Engineers, System Administrators, and Cloud Professionals—connected to the task of &#x22;Deploy & Manage&#x22; in the center." />
</Frame>

What you’ll practice

* Deploy Elasticsearch on Kubernetes to store and index logs.
* Collect and forward logs using Fluentd as the aggregator/log shipper.
* Visualize and explore logs with Kibana dashboards.
* Configure persistence, resource requests/limits, and cluster scaling.
* Monitor cluster health and secure the EFK stack for production use.

Each lab builds on the previous one so you move from fundamentals to production-ready patterns.

How the labs work

* Open the terminal in the lab by clicking the toggle icon. This connects directly to a live Kubernetes cluster provisioned for the exercise.
* Use the Hint and Solution tabs if you get stuck; they’re designed to guide rather than replace the learning.
* After you complete a step, click the Check button to validate the task and unlock the next step.

> **lightbulb** Use the terminal to run Kubernetes commands against the live cluster. If a task asks you to create or switch to a namespace, follow the exact command shown in the Tasks tab and then use the Check button to validate. Example namespace creation and switch:

  ```bash theme={null}
  kubectl create namespace elastic-stack
  kubectl config set-context --current --namespace=elastic-stack
  ```

<Frame>
  <img alt="The image shows logos of Elasticsearch, Fluentd, and Kibana inside a box that includes the Kubernetes logo, with a &#x22;Deploy&#x22; rocket icon below." />
</Frame>

Lab navigation and UI

* Overview tab: read the conceptual context and objectives for the module.
* Tasks tab: follow workbook-style instructions with exact commands and validations.
* Terminal: run commands directly against the sandbox cluster.
* Toggle Panel Size: expand or collapse the terminal panel for better visibility.

<Frame>
  <img alt="The image is a screenshot from a lab course titled &#x22;Introduction to Kubernetes and the EFK Stack,&#x22; detailing navigation steps for a learning environment with tabs for &#x22;Overview&#x22; and &#x22;Task.&#x22; It includes instructions on using the &#x22;Toggle Panel Size&#x22; feature." />
</Frame>

Course scope and progression
This lesson begins with Kubernetes and EFK fundamentals, then moves on to practical deployment and operational tasks:

| Module focus             | What you’ll learn                                     | Example outcome                                            |
| ------------------------ | ----------------------------------------------------- | ---------------------------------------------------------- |
| Core concepts            | Basics of Kubernetes and the EFK components           | Understand how Elasticsearch, Fluentd, and Kibana interact |
| Elasticsearch deployment | Stateful workloads, persistence, and scaling          | Run a resilient Elasticsearch cluster on Kubernetes        |
| Fluentd integration      | DaemonSet configuration and log forwarding            | Collect node and application logs reliably                 |
| Kibana setup             | Dashboards, visualizations, and index patterns        | Explore and visualize logs stored in Elasticsearch         |
| Production readiness     | Resource limits, persistence, and monitoring          | Harden and scale the EFK stack for real workloads          |
| Security & monitoring    | TLS, authentication, and observability best practices | Secure access and monitor cluster health and logs          |

<Frame>
  <img alt="The image shows a tutorial interface with a task focused on deploying Elasticsearch on Kubernetes, instructing users to create and switch to a namespace called &#x22;elastic-stack.&#x22; There is a simple code terminal on the right side." />
</Frame>

Best practices emphasized in this course

* Use namespaced resources (for example, use `elastic-stack` as the deployment namespace).
* Define resource requests and limits to ensure stable performance.
* Persist Elasticsearch data using appropriate StorageClasses and PersistentVolumeClaims.
* Run Fluentd as a DaemonSet to collect logs across nodes.
* Secure Kibana and Elasticsearch endpoints for production access.

> **warning** This course uses a live sandbox Kubernetes cluster for labs. Do not use production credentials or expose sensitive data while completing exercises. Always follow your organization’s security policies when applying these patterns to production.

<Frame>
  <img alt="The image showcases an overview of course topics related to Kubernetes and the EFK (Elasticsearch, Fluentd, Kibana) Stack, with eight specific topics listed." />
</Frame>

Next steps
Ready to begin? Open the first lab, read the Overview tab, then follow the Tasks tab. Start by creating the `elastic-stack` namespace and proceed through the deployment, configuration, and validation steps.

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Elasticsearch (Elastic)](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
* [Fluentd Documentation](https://docs.fluentd.org/)
* [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/learn-by-doing-deploying-and-managing-the-efk-stack-on-kubernetes/module/7e1e94f6-6bde-47ce-852e-979b8caa89dc/lesson/4dfe1e2f-5433-43a5-b3c4-1ff048199aba)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/learn-by-doing-deploying-and-managing-the-efk-stack-on-kubernetes/module/7e1e94f6-6bde-47ce-852e-979b8caa89dc/lesson/247ed6e4-d5a2-4ca3-ac01-588f55334fec)
