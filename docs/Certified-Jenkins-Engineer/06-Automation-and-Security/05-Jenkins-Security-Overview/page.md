# Jenkins Security Overview

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Automation-and-Security/Jenkins-Security-Overview/page

This article discusses securing Jenkins CI/CD environments through authentication and authorization strategies, emphasizing the principle of least privilege.

Securing your Jenkins CI/CD environment involves implementing robust authentication and fine-grained authorization strategies. By adhering to the principle of least privilege, you restrict access so that users can only perform tasks essential to their role.

![The image illustrates Jenkins security, highlighting protection against unauthorized access and malicious actions, with a focus on the concept of least privilege.](https://kodekloud.com/kk-media/image/upload/v1752870401/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Security-Overview/jenkins-security-least-privilege.jpg)

> **lightbulb** Least privilege reduces your attack surface. Always review permission assignments regularly and audit access logs.

## Authentication vs. Authorization

Authentication confirms a user’s identity (e.g., username/password, API token), while authorization controls access to resources and actions once authenticated.

![The image compares authentication and authorization, showing authentication as verifying a user's identity and authorization as determining user permissions.](https://kodekloud.com/kk-media/image/upload/v1752870402/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Security-Overview/authentication-authorization-comparison.jpg)

**Analogy**

* **Authentication**: Presenting your ID at a hotel front desk.
* **Authorization**: Receiving a room key that opens only your assigned room.

## Jenkins Authentication Methods

Jenkins integrates with various identity providers to authenticate users:

| Method                           | Description                                                | Use Case                             |
| -------------------------------- | ---------------------------------------------------------- | ------------------------------------ |
| Jenkins User Database            | Manage credentials and users directly in Jenkins.          | Small teams or trial installations   |
| Unix User/Group Database         | Use existing Unix system accounts and groups.              | UNIX-centric environments            |
| Servlet Container Security       | Leverage your web server’s security (e.g., Apache, Nginx). | Integrated web server authentication |
| External LDAP / Active Directory | Centralize directory services via LDAP or Microsoft AD.    | Enterprise-scale user management     |
| SAML 2.0 SSO                     | Single Sign-On with SAML-based identity providers.         | Organizations with SSO requirements  |

![The image outlines authentication options in Jenkins, including built-in choices like Jenkins User Database and expanding options like Active Directory.](https://kodekloud.com/kk-media/image/upload/v1752870403/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Security-Overview/jenkins-authentication-options-diagram.jpg)

### Selecting the Right Authentication

For small teams, Jenkins’ internal user database is often sufficient. In larger organizations, integrating with LDAP or Active Directory streamlines user management and enforces corporate policies.

![The image shows a Jenkins security settings interface, highlighting authentication options such as "Jenkins' own user database" and others. The title suggests it's about choosing the right authentication approach in Jenkins.](https://kodekloud.com/kk-media/image/upload/v1752870405/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Security-Overview/jenkins-security-authentication-settings.jpg)

## Authorization Strategies in Jenkins

Authorization dictates what authenticated users can access and modify. It involves three key elements:

* **Resource**: The target of an operation (e.g., build job, delete credentials).
* **Role**: A set of permissions grouped for convenience (e.g., Developer role with build and read rights).
* **Requester**: The user or group assigned roles for specific resources.

![The image explains the concept of authorization in Jenkins, highlighting three components: Resource, Role, and Requester, each with a brief description.](https://kodekloud.com/kk-media/image/upload/v1752870406/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Security-Overview/jenkins-authorization-resource-role-requester.jpg)

> **triangle-alert** Grant permissions conservatively. Avoid assigning administrative rights unless explicitly required.

### Matrix-Based Security

Global matrix security allows you to define permissions at the Jenkins system level. Permissions are arranged in a tabular view with resources across the top and users/groups down the side.

![The image shows a Jenkins authorization matrix, displaying user and group permissions across various categories like Overall, Credentials, Agent, Job, Run, View, SCM, and Metrics. Each user or group has specific permissions indicated by checkboxes.](https://kodekloud.com/kk-media/image/upload/v1752870407/notes-assets/images/Certified-Jenkins-Engineer-Jenkins-Security-Overview/jenkins-authorization-matrix-permissions.jpg)

| Category   | Overall | Credentials | Agent | Job | Run | View | SCM | Metrics |
| ---------- | :-----: | :---------: | :---: | :-: | :-: | :--: | :-: | :-----: |
| admin      |    ✔    |      ✔      |   ✔   |  ✔  |  ✔  |   ✔  |  ✔  |    ✔    |
| developers |    ✘    |      ✘      |   ✔   |  ✔  |  ✔  |   ✘  |  ✔  |    ✘    |
| viewers    |    ✘    |      ✘      |   ✘   |  ✔  |  ✔  |   ✔  |  ✘  |    ✘    |

### Project-Based Matrix Authorization

For advanced use cases, enable per-project authorization to assign different permission sets to individual pipelines or folders. This strategy isolates access and limits the scope of each role.

***

## Links and References

* [Jenkins Authentication Documentation](https://www.jenkins.io/doc/book/security/authentication/)
* [Jenkins Authorization Strategies](https://www.jenkins.io/doc/book/security/authorization/)
* [Role-Based Access Control Plugin](https://plugins.jenkins.io/role-strategy/)
* [LDAP Plugin for Jenkins](https://plugins.jenkins.io/ldap/)

Always enforce least privilege, audit permissions regularly, and integrate with your existing identity management systems to maintain a secure and compliant Jenkins environment.

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/4d6d1f39-307c-4fdb-8d2b-834c1650e792/lesson/b5b7dd7b-2a35-45bb-8dcd-72894e2f4299)
