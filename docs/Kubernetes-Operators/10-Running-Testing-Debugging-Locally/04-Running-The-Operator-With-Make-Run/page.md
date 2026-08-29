# Running The Operator With Make Run

Source: https://notes.kodekloud.com/docs/Kubernetes-Operators/Running-Testing-Debugging-Locally/Running-The-Operator-With-Make-Run/page

Using make run runs the operator locally against a real cluster for fast iterative development and debugging of reconcile logic before packaging and in-cluster deployment.

Using `make run` moves the operator's brain from a pod in the cluster to a process on your workstation while it still manipulates real cluster objects. This gives you a fast, interactive workbench to iterate on reconcile logic before you package or deploy anything.

The cluster is the building; the controller is the technician with a radio. In production the technician works inside the building (as a pod). During local development the technician sits at your desk, but

<Frame>
  <img alt="The image compares &#x22;In Production&#x22; with &#x22;Local dev&#x22; environments, showing a technician working inside a pod in production and a stick figure holding a tool on a table." />
</Frame>

the radio still reaches the building. The API server is that radio link: Deployments, Services, ConfigMaps and other web app resources remain real cluster objects that your locally-run controller reads and modifies.

<Frame>
  <img alt="The image shows a schematic of a building labeled &#x22;Cluster&#x22; with icons representing different components and text indicating &#x22;The Objects Are Still Real&#x22; and &#x22;Real objects, not mocked.&#x22;" />
</Frame>

Why use local mode? It shortens the edit → run → observe loop:

* Stop the manager.
* Change the code.
* Start the manager locally.
* Apply a WebApp resource.
* Observe what the controller does.

This is the quickest way to answer: did my reconcile logic behave the way I expect?

Before the controller can act on a custom resource, the API server must know the resource schema. `make install` applies the CustomResourceDefinition (CRD) for the WebApp type so the API server recognizes it. If the CRD is not installed, the cluster cannot understand the object you want to watch even if your controller is running.

```bash theme={null}
