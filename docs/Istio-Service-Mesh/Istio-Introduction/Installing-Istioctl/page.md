# Installing Istioctl

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Istio-Introduction/Installing-Istioctl/page

Guide to installing istioctl, preparing Minikube with ingress addon, troubleshooting macOS driver issues, downloading Istio release, adding istioctl to PATH and running prechecks

This guide walks you through installing the Istio client (`istioctl`) and preparing a local Minikube cluster that supports the ingress addon. It preserves key troubleshooting output and step-by-step commands so you can reproduce the process and verify your environment.

Prerequisites:

* Minikube installed locally. See Minikube docs: [https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/).
* kubectl configured to use your Minikube cluster.
* Docker is optional — you may use a VM-based driver instead.

## 1) Start Minikube (driver selection)

When you run `minikube start` without specifying a driver, Minikube automatically selects a default driver. If Docker is running it may choose the Docker driver and run the cluster inside a Docker container.

On macOS, the Docker driver has a networking limitation: the Minikube ingress addon is not supported for the Docker driver on Darwin (macOS). An example session that demonstrates this limitation:

```bash theme={null}
istiotraining@local ~ $ minikube start
😄  minikube v1.16.0 on Darwin 10.15.7
✨  Automatically selected the docker driver. Other choices: hyperkit, virtualbox
👍  Starting control plane node minikube in cluster minikube
🛟  Creating docker container (CPUs=2, Memory=1987MB) ...
🐳  Preparing Kubernetes v1.20.0 on Docker 20.10.0 ...
 ▪ Generating certificates and keys ...
 ▪ Booting up control plane ...
 ▪ Configuring RBAC rules ...
 Verifying Kubernetes components...
 Enabled addons: storage-provisioner, default-storageclass
🎉  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
istiotraining@local ~ $ minikube addons enable ingress

✖  Exiting due to MK_USAGE: Due to networking limitations of driver docker on darwin, ingress addon is not supported.
Alternatively to use this addon you can use a vm-based driver:

    'minikube start --vm=true'

To track the update on this work in progress feature please check:
https://github.com/kubernetes/minikube/issues/7332
```

<Callout icon="lightbulb">
  On macOS, if you need the ingress addon, use a VM-based driver (for example, `hyperkit`) rather than the Docker driver.
</Callout>

If you encounter this limitation, delete the Docker-based Minikube cluster and start Minikube using a VM-based driver (for example, hyperkit).

Example: delete the Docker-based cluster and restart with a VM-based driver:

```bash theme={null}
istiotraining@local ~ $ minikube delete
🔥  Deleting "minikube" in docker ...
🔥  Deleting container "minikube" ...
🔥  Removing /Users/istiotraining/.minikube/machines/minikube ...
💀  Removed all traces of the "minikube" cluster.

istiotraining@local ~ $ minikube start --vm=true
😄  minikube v1.16.0 on Darwin 10.15.7
✨  Automatically selected the hyperkit driver
🔥  Starting control plane node minikube in cluster minikube
⚙️  Creating hyperkit VM (CPUs=2, Memory=4000MB, Disk=20000MB) ...
🚜  Preparing Kubernetes v1.20.0 on Docker 20.10.0 ...
  ▪  Generating certificates and keys ...
  ▪  Booting up control plane ...
  ▪  Configuring RBAC rules ...
●  Verifying Kubernetes components...
✨  Enabled addons: storage-provisioner, default-storageclass
🎉  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default

istiotraining@local ~ $ minikube addons enable ingress
●  Verifying ingress addon...
✨  The 'ingress' addon is enabled
```

<Callout icon="warning">
  Switching drivers will recreate the Minikube VM. Delete the existing cluster if you want to change drivers (`minikube delete`). Back up any local resources you need before deleting.
</Callout>

## 2) Download the Istio release (installs istioctl)

A convenient way to get the latest Istio release (and the `istioctl` binary) is to use the official Istio download script. This script downloads a release archive into a directory named `istio-<version>` in your current folder:

```bash theme={null}
