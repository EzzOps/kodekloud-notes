# ls
bin   dev   boot   docker-entrypoint.sh  home   lib64   mnt   proc   run   srv   tmp   var
docker-entrypoint.d  etc   lib   media   opt   root   sbin   sys   usr
#
```

displays the pod’s file structure. This manual approach is ideal for a few deployments, but it can be less efficient when managing numerous configurations.

***

## Method 2: Deploying an Application by Importing a Git Repository

For a streamlined deployment process, import your application directly from a Git repository. In this example, we deploy a basic Go Web API application that returns "Welcome to the Go Web API!" on its homepage and provides a JSON endpoint.

Below is the primary Go code for this application:

```go theme={null}
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
)

type whoami struct {
    Name  string
    Title string
    State string
}

func main() {
    request()
}

func whoAmI(response http.ResponseWriter, r *http.Request) {
    who := []whoami{
        {
            Name:  "Michael Levan",
            Title: "Kubernetes Engineer",
            State: "ND",
        },
    }
    json.NewEncoder(response).Encode(who)
    fmt.Println("Endpoint Hit:", who)
}

func homePage(response http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(response, "Welcome to the Go Web API!")
    fmt.Println("Endpoint Hit: homePage")
}

func aboutMe(response http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(response, "A little bit about Michael Levan...")
    fmt.Println("Endpoint Hit: MichaelLevan")
}

func request() {
    http.HandleFunc("/", homePage)
    http.HandleFunc("/whoami", whoAmI)
    http.HandleFunc("/about", aboutMe)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

To deploy this Go Web API application:

1. Copy the HTTPS link of the Git repository.
2. In the Developer view of the OpenShift web console, click **Add**, then scroll down to **Git Repository**.
3. Paste the Git repository URL. The web console will detect the Dockerfile in the repository and use it to build and deploy your application.
4. Provide a unique name for your application (e.g., GoWebAPI or goweb).

![The image shows the Red Hat OpenShift Container Platform interface, specifically the "Import from Git" section where a Git repository URL is being validated.](https://kodekloud.com/kk-media/image/upload/v1752882706/notes-assets/images/OpenShift-4-Deploying-applications-web-console/openshift-import-from-git-interface.jpg)

![The image shows a Red Hat OpenShift Container Platform interface where a user is configuring a Dockerfile import strategy, entering an application name "goweb" and a component name "go-web-api-git."](https://kodekloud.com/kk-media/image/upload/v1752882707/notes-assets/images/OpenShift-4-Deploying-applications-web-console/openshift-dockerfile-import-goweb.jpg)

5. Configure additional settings such as the target port, which sets the exposed port of your application. OpenShift automatically creates a route—a public URL—so your application can be accessed externally.

![The image shows a Red Hat OpenShift Container Platform interface, specifically the "DeploymentConfig" section with advanced options for setting a target port and creating a route to the application.](https://kodekloud.com/kk-media/image/upload/v1752882708/notes-assets/images/OpenShift-4-Deploying-applications-web-console/openshift-deploymentconfig-interface.jpg)

After clicking **Create**, the build starts automatically. Once the build completes successfully, verify the pod status by navigating to **Workloads** > **Pods**.

![The image shows the Red Hat OpenShift Container Platform interface, displaying a topology view with applications and resources like pods and builds. The sidebar includes options such as Topology, Observe, and Search.](https://kodekloud.com/kk-media/image/upload/v1752882709/notes-assets/images/OpenShift-4-Deploying-applications-web-console/red-hat-openshift-topology-view.jpg)

![The image shows a Red Hat OpenShift Container Platform interface displaying details of a pod named "goweb-1-build" with a status of "Completed." The interface includes various tabs and a sidebar with options like "Pods" and "Deployments."](https://kodekloud.com/kk-media/image/upload/v1752882710/notes-assets/images/OpenShift-4-Deploying-applications-web-console/red-hat-openshift-pod-goweb-1.jpg)

Finally, check the **Routes** section under **Networking**. Click the route URL to confirm that the homepage displays “Welcome to the Go Web API!”—indicating your application is running properly.

***

## Summary

This guide demonstrated two methods to deploy applications using the OpenShift web console:

* Manually creating a deployment with a custom YAML manifest.
* Importing an application directly from a Git repository, which automatically builds and deploys your code using the provided Dockerfile and configuration settings.

Both methods streamline deployment management and offer flexibility based on your project needs. In upcoming sections, we will discuss deploying full-blown applications via the terminal using kubectl.

For more information on related topics, visit the following resources:

* [OpenShift Documentation](https://docs.openshift.com/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/openshift-4/module/0bce3da1-167c-4f11-a004-4d57bfc7adac/lesson/80a1a010-3255-44cc-a605-98ed79d9edfa)


# Projects and Users

Source: https://notes.kodekloud.com/docs/OpenShift-4/Openshift-Concepts-Projects-and-Users/Projects-and-Users/page

This article covers managing projects and users in OpenShift, focusing on resource organization, user types, and authentication methods.

Hello, and welcome to this detailed lesson on managing projects and users in OpenShift.

In this guide, you will gain a comprehensive understanding of how OpenShift organizes resources using projects and how it handles user management and authentication. This knowledge is invaluable for ensuring secure, isolated, and efficient operations within your OpenShift cluster.

## Understanding Projects

Once your OpenShift cluster is up and running—with both UI and CLI access—you can start exploring its core concepts. OpenShift projects are essential for organizing and managing resources efficiently. They allow teams to work in isolation, even in a consolidated environment where resources are shared.

Consider a large Kubernetes cluster handling hundreds of deployments, pods, and services. In such environments, multiple teams might inadvertently have resource conflicts or unwanted access to each other's deployments. OpenShift projects mitigate these risks by grouping resources and enforcing isolation.

Under the hood, projects in OpenShift are implemented as Kubernetes namespaces. When a project is created, Kubernetes automatically prefixes resource names for basic grouping, while OpenShift ensures full grouping and isolation in a seamless manner.

Below is a diagram that illustrates how multiple projects are structured. In this image, each project contains a service called "teamX.myservice" connected to various components (shown as red cubes), with servers arranged in a row at the bottom.

![The image is a diagram showing four projects, each with a service labeled "teamX.myservice" and connected to multiple components, represented by red cubes. Below, there are icons of servers arranged in a row.](https://kodekloud.com/kk-media/image/upload/v1752882711/notes-assets/images/OpenShift-4-Projects-and-Users/teamx-myservice-projects-diagram.jpg)

Once a project is created, you can deploy applications without the hassle of manually managing namespaces—OpenShift automates these details to streamline your workflow.

## User Management in OpenShift

OpenShift features robust user management capabilities by categorizing users into three primary types:

1. **Regular Users:**\
   These are everyday users such as developers who interact with the platform to deploy and maintain applications. An example of a regular user is the typical "developer" account.

2. **System Users:**\
   These are specialized accounts designated for managing the infrastructure. They include cluster administrators and node-specific users. By default, OpenShift creates several system accounts (e.g., "system:admin", "system:master"). These accounts use a `system:` prefix to distinguish them from regular user accounts.

3. **Service Accounts:**\
   Service accounts are used within projects to enable secure communication between internal application components. For instance, a web server might use a service account to connect to a database. These accounts are automatically prefixed with `system:serviceaccount`.

Below is a code snippet showcasing example names of system and service accounts:

```bash theme={null}
system:admin
system:master
system:serviceaccount:proj1:db_user
```

The image below visually summarizes the three types of users. It features icons that represent a regular user ("developer"), a system user ("system:admin"), and a service account (illustrated by an Android robot).

![The image shows three user types: "Regular" with a simple person icon, "System" with a female silhouette icon, and an Android robot icon, each labeled with roles like "developer" and "system:admin".](https://kodekloud.com/kk-media/image/upload/v1752882712/notes-assets/images/OpenShift-4-Projects-and-Users/user-types-icons-developer-admin.jpg)

> **lightbulb** Understanding the differences between these user types is crucial for setting up proper access control and ensuring your cluster remains secure.

## OAuth and User Authentication

OpenShift integrates an OAuth server directly into the Master, which governs user authentication and authorization. This approach simplifies login processes and secures access to your cluster.

In simple deployments, such as when using Minishift in an all-in-one mode, OpenShift is configured with an "allow-all" identity provider. This means any user can log in using any password, and if a user doesn't exist, OpenShift will automatically create the account on the first login. Note that in this configuration, the password is not actually validated.

For more secure environments, the "deny-all" identity provider is the default. Here, no user can access the cluster unless an administrator explicitly creates and enables their account. If you need to modify these settings, you can update the master configuration at `/etc/openshift/master/master-config.yaml`.

The following diagram outlines the behavior of the OAuth server for both "Allow All" and "Deny All" configurations. It also highlights the location of the master configuration file.

![The image shows a diagram related to an OAuth Server with icons representing "Allow All" and "Deny All" configurations, along with a file path: /etc/openshift/master/master-config.yaml.](https://kodekloud.com/kk-media/image/upload/v1752882713/notes-assets/images/OpenShift-4-Projects-and-Users/oauth-server-allow-deny-diagram.jpg)

> **triangle-alert** In production environments, always opt for a secure identity provider configuration to prevent unauthorized access.

## Conclusion

This lesson has provided you with a thorough introduction to projects and user management in OpenShift. You learned how projects facilitate isolated deployments through Kubernetes namespaces and how OpenShift’s intuitive grouping and access controls simplify resource management. Additionally, the lesson clarified the distinctions between regular users, system users, and service accounts, as well as reviewed the OAuth server configurations that secure your cluster.

Thank you for joining this lesson. For further reading and more detailed instructions, please consult the [OpenShift Documentation](https://docs.openshift.com/). See you in the next lesson!

- [Watch Video](https://learn.kodekloud.com/user/courses/openshift-4/module/0bce3da1-167c-4f11-a004-4d57bfc7adac/lesson/53f80255-ff0e-4358-abf7-4ace4f207b9a)
