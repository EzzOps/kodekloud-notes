# Custom Controllers

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Security/Custom-Controllers/page

This article explores developing custom controllers for managing Kubernetes resources, specifically focusing on FlightTicket objects and their interactions with the Kubernetes API.

In this lesson, we explore how to develop custom controllers for managing your Kubernetes resources. Building on our previous work with Custom Resource Definitions (CRDs), we now introduce FlightTicket objects. These objects, along with their details, are stored in etcd. The custom controller monitors the status of these FlightTicket objects in etcd and performs actions such as booking, editing, or canceling flight tickets by invoking the appropriate flight booking API.

A controller is a process or piece of code that continuously observes the Kubernetes cluster for specific events (like changes to FlightTicket objects) and takes corresponding actions.

For example, consider the following YAML definition of a FlightTicket resource:

```yaml theme={null}
