# Devops Tools

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Introduction/Devops-Tools/page

This guide explores essential DevOps tools and practices for developing, deploying, and monitoring applications from initial idea to production.

When diving into DevOps, you encounter a diverse set of tools, including Docker, Kubernetes, Ansible, Terraform, Git, GitHub, Jenkins, Prometheus, and Grafana. Although this array of technologies might initially seem overwhelming, this guide walks you through a real-world scenario that demonstrates how each tool plays a crucial role as your application and infrastructure evolve.

## From Idea to First Release

Every great project starts with an idea—imagine building a website that books tickets to Mars, helping users avoid long queues and high prices. As with any innovative project, you start writing code. Hours later, the first version is ready. However, this version is running on your local machine, accessible via HTTP on localhost (port 8080):

```python theme={null}
def book_my_ticket_to_mars():
    # world changing code here
