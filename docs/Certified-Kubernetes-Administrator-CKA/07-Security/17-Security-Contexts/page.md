# Output: yes
kubectl auth can-i delete nodes
# Output: no
kubectl auth can-i create deployments --as dev-user
# Output: no
kubectl auth can-i create pods --as dev-user
# Output: yes
```

You can also specify a namespace in your commands to verify permissions scoped to that particular namespace.

## Limiting Access to Specific Resources

In some scenarios, you may want to restrict user access to a select group of resources. For example, if you have multiple pods in a namespace but only intend to provide access to pods named "blue" and "orange," you can utilize the `resourceNames` field in the role rule.

Start with a basic role definition without any resource-specific restrictions:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "create", "update"]
```

Then, update the rule to restrict access solely to the "blue" and "orange" pods:

```yaml theme={null}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "create", "update"]
  resourceNames: ["blue", "orange"]
```

## Conclusion

This lesson provided an in-depth look at implementing Role-Based Access Controls in Kubernetes. You learned how to create roles and role bindings, verify permissions, and restrict access to specific resources. Practicing these exercises will enhance your grasp of RBAC and help you manage Kubernetes security effectively.

For additional details on Kubernetes RBAC, refer to the [Kubernetes Documentation](https://kubernetes.io/docs/) and explore best practices for securing your clusters.

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/77826599-d456-4cb5-8cbc-b713cc077b45/lesson/494f426c-e040-4b7c-bc73-5b449782efeb)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/77826599-d456-4cb5-8cbc-b713cc077b45/lesson/ca89c1b4-0d46-460f-81e5-2ce2bbb26146)


# Security Contexts

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Security/Security-Contexts/page

This lesson explains how to secure containers in Kubernetes by configuring security settings at the pod and container levels.

Hello, and welcome to this lesson on Security Contexts in Kubernetes. My name is Mumshad Mannambeth, and in this guide, we'll explain how you can secure your containers by configuring security settings at both the pod and container levels.

When you run a Docker container, you have the flexibility to define various security parameters. For example, you can set a specific user ID or modify Linux capabilities. Consider the following Docker commands:

```bash theme={null}
docker run --user=1001 ubuntu sleep 3600
docker run --cap-add MAC_ADMIN ubuntu
```

These configurations help manage the security of Docker containers, and similar settings are available in Kubernetes.

In Kubernetes, containers are always encapsulated in pods. You can define security settings either at the pod level, which affects all containers in the pod, or at the container level where the settings apply specifically to one container. Note that if the same security configuration is set at both the pod and container levels, the container-specific settings take precedence over the pod-level configurations.

Below is an example of a pod definition that configures the security context at the container level, using an Ubuntu image that runs the `sleep` command:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
        runAsUser: 1000
        capabilities:
          add: ["MAC_ADMIN"]
```

This configuration instructs Kubernetes to run the container as user ID 1000 and adds the `MAC_ADMIN` capability. If your goal is to enforce these security settings across all containers within a single pod, you can define the security context at the pod level instead.

> **lightbulb** For more hands-on practice with viewing, configuring, and troubleshooting security contexts in Kubernetes, check out the available lab resources.

By leveraging security contexts, you enhance the security posture of your containerized applications in Kubernetes. For additional guidance, you may find the following resources useful:

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Kubernetes Concepts: Security Contexts](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

Thank you for following along, and happy securing!

- [Watch Video](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/77826599-d456-4cb5-8cbc-b713cc077b45/lesson/64d6108a-af51-49d4-9019-c5641a145195)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator/module/77826599-d456-4cb5-8cbc-b713cc077b45/lesson/dc4ab297-ee13-4ee9-ba36-c70608f4b3ed)
