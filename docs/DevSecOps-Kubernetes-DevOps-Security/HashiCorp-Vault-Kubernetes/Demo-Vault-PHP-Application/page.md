# Demo Vault PHP Application

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/HashiCorp-Vault-Kubernetes/Demo-Vault-PHP-Application/page

Demonstrates deploying a PHP app on Kubernetes that reads secrets injected into pod filesystem by HashiCorp Vault and displays them in a minimal UI

This guide shows a simple PHP application that reads secrets injected into the pod filesystem by HashiCorp Vault (via Vault Agent Injector) and displays them in a minimal UI. It walks through cloning the repository, building the Docker image, deploying to Kubernetes, patching the Deployment with Vault annotations, and verifying that the app can read the injected secrets.

Repository: [https://github.com/sidd-harth/php-vault-example](https://github.com/sidd-harth/php-vault-example)

Quick start — clone, build, and prepare

```bash theme={null}
git clone https://github.com/sidd-harth/php-vault-example.git
cd php-vault-example
docker build -t php:vault .
```

Why this example

* Demonstrates secret injection into pod filesystem using Vault Agent Injector.
* Shows how a simple PHP app reads files mounted at predetermined paths.
* Useful for learning pod-level secret access patterns and Vault integration with Kubernetes.

Application overview

* The PHP app expects these files (mounted by the Vault injector) at runtime:
  * /vault/secrets/username
  * /vault/secrets/password
  * /vault/secrets/apikey

|         Condition | UI result                                                |
| ----------------: | :------------------------------------------------------- |
|  Any file missing | Red background with "File(s) Not Found"                  |
| All files present | Green background showing Username, Password, and API Key |

Index page (index.php)

* The example `index.php` outputs a small HTML UI and reads the three files under `/vault/secrets/`. It suppresses warnings from `file_get_contents()` using `@` for this demo; in production handle errors explicitly.

```php theme={null}
<?php
// Image reference removed from this example to keep the snippet self-contained.
echo "<table border='3'>
        <tr>
            <th><h2>Course</h2></th>
            <th><h2>Demo</h2></th>
        </tr>
        <tr>
            <td><h3><a href=\"https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security\">DevSecOps - Kubernetes, DevOps & Security</a></h3></td>
            <td><h3>HashiCorp Vault - Secret Injection through SideCar</h3></td>
        </tr>";
echo "</table><br/>";

$username = @file_get_contents("/vault/secrets/username");
$password = @file_get_contents("/vault/secrets/password");
$apikey   = @file_get_contents("/vault/secrets/apikey");

if ($username === false || $password === false || $apikey === false) {
    // There is an error opening one or more files
    echo "<body style='background-color:red'>";
    echo '<h1 style="border: 2px solid DodgerBlue;color:white;"> File(s) Not Found </h1><br/>';
} else {
    echo "<body style='background-color:lightgreen'>";
    echo "<table border='2'>
            <tr>
                <th><h3>Username</h3></th>
                <th><h3>" . htmlspecialchars($username) . "</h3></th>
            </tr>
            <tr>
                <th><h3>Password</h3></th>
                <th><h3>" . htmlspecialchars($password) . "</h3></th>
            </tr>
            <tr>
                <th><h3>API Key</h3></th>
                <th><h3>" . htmlspecialchars($apikey) . "</h3></th>
            </tr>
          </table><br/>";
}
?>
```

HTML/CSS for the page

* The app includes a small style block for the page layout and table formatting:

```html theme={null}
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
h1 {
    text-align: center;
    font-family: Bahnschrift SemiBold;
}
table, td, th {
    border: 1px solid black;
    height: 50px;
}
table {
    border-collapse: collapse;
    width: 100%;
}
.center {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
}
td {
    text-align: center;
    height: 50px;
    vertical-align: middle;
    font-family: Bahnschrift SemiBold;
}
tr {
    text-align: center;
    height: 50px;
    vertical-align: middle;
    font-family: Bahnschrift SemiBold;
}
</style>
</head>
```

Dockerfile

* Builds the PHP/Apache container and copies the app into the web root.

```dockerfile theme={null}
FROM php:7.4-apache
COPY src/ /var/www/html
EXPOSE 80
```

Kubernetes manifest

* The provided manifest creates a Deployment (replicas: 1), a NodePort Service, and a ServiceAccount named `app`. The container image referenced is `php:vault` (the image you built locally above).

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: php
  name: php
spec:
  replicas: 1
  selector:
    matchLabels:
      app: php
  strategy: {}
  template:
    metadata:
      labels:
        app: php
    spec:
      serviceAccountName: app
      containers:
      - image: php:vault
        name: php
---
apiVersion: v1
kind: Service
metadata:
  labels:
    app: php
  name: php
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: php
  type: NodePort
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app
  labels:
    app: php
```

Patch step (apply Vault Agent Injector annotations)

* The repository includes `patch-annotations-template.yaml` to add Vault Agent Injector annotations to the Deployment. Apply the base manifest first, then patch the deployment with the annotations so Vault can inject the secrets.

Example commands:

```bash theme={null}
kubectl apply -f php-app-k8s-deploy.yaml
kubectl patch deploy php -p "$(cat patch-annotations-template.yaml)"
```

Deploy and verify

1. Apply the manifest and patch the Deployment:

```bash theme={null}
kubectl apply -f php-app-k8s-deploy.yaml
kubectl patch deploy php -p "$(cat patch-annotations-template.yaml)"
```

2. Confirm the pods, services, and service accounts exist:

```bash theme={null}
kubectl get pods
