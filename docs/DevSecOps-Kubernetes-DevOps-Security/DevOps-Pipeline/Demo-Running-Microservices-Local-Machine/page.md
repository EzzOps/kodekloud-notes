# Create the Deployment
kubectl -n default create deployment node-app --image=siddharth67/node-service:v1

# Expose as ClusterIP on port 5000
kubectl -n default expose deployment node-app \
  --name=node-service \
  --port=5000 \
  --target-port=5000

# Verify
kubectl -n default get all
```

Expected output:

```bash theme={null}
NAME                             READY   STATUS    RESTARTS   AGE
pod/node-app-6b8496465-tsrkf     1/1     Running   0          24s

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/node-service    ClusterIP   10.96.198.94    <none>        5000/TCP   4s
```

The Node.js service is now reachable at `http://node-service:5000`.

***

## Numeric Spring Boot Application

Update your controller to call the Kubernetes service instead of `localhost`. Example:

```java theme={null}
package com.devsecops;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
public class NumericController {
    private final Logger logger = LoggerFactory.getLogger(NumericController.class);
    private static final String BASE_URL = "http://node-service:5000/plussone";

    private final RestTemplate restTemplate;

    public NumericController(RestTemplateBuilder builder) {
        this.restTemplate = builder.build();
    }

    @GetMapping("/")
    public String welcome() {
        return "Kubernetes DevSecOps";
    }

    @GetMapping("/increment/{value}")
    public String increment(@PathVariable int value) {
        ResponseEntity<String> response =
            restTemplate.getForEntity(BASE_URL + "/" + value, String.class);
        return response.getBody();
    }

    @GetMapping("/compare/{value}")
    public String compareToFifty(@PathVariable int value) {
        return (value < 50) ? "Less than 50" : "Greater than 50";
    }
}
```

Commit all changes to your `main` branch—Jenkins will automatically trigger the pipeline.

***

## Verifying the Deployment

After the pipeline completes, verify both applications:

```bash theme={null}
kubectl -n default get all
```

Sample output:

```bash theme={null}
NAME                                READY   STATUS    RESTARTS   AGE
pod/devsecops-xxxxx-xxxxx          1/1     Running   0          2m

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/devsecops-svc   NodePort    10.96.xxx.xxx   <none>        8080:31933/TCP   2m
service/node-service    ClusterIP   10.96.xxx.xxx   <none>        5000/TCP         5m
```

Access the Numeric application via NodePort:

* `http://<NODE_IP>:31933/` → `Kubernetes DevSecOps`
* `http://<NODE_IP>:31933/increment/77` → `78`
* `http://<NODE_IP>:31933/compare/44` → `Less than 50`
* `http://<NODE_IP>:31933/compare/95` → `Greater than 50`

Both services communicate seamlessly within the Kubernetes cluster.

***

## Links & References

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [Docker Hub](https://hub.docker.com/)
* [Spring Boot Reference Guide](https://docs.spring.io/spring-boot/docs/current/reference/html/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/a0425702-2a0f-4cef-aa40-28dfa0a1d13f" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/391995ae-bfe7-4b8d-845d-a46becf963fc" />
</CardGroup>


# Demo Running Microservices Local Machine

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Demo-Running-Microservices-Local-Machine/page

This tutorial demonstrates setting up and running Spring Boot and Node.js microservices locally.

In this tutorial, we’ll set up and run two cooperating microservices on your local machine:

1. **Spring Boot “numeric” service**
2. **Node.js “plus-one” service** (packaged in Docker)

By the end, you’ll be able to call endpoints on the Spring Boot app that delegate to the Node.js service and observe the logs in both environments.

***

## 1. Clone and Import the Project

1. Clone the Git repository and open it in your IDE of choice (Spring Tool Suite, IntelliJ, VSCode, etc.).

<Frame>
  ![The image shows a Windows File Explorer window open to a directory named "devsecops-k8s-demo," containing various folders and files. The desktop taskbar is visible at the bottom, displaying several application icons.](https://kodekloud.com/kk-media/image/upload/v1752873585/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Running-Microservices-Local-Machine/windows-file-explorer-devsecops-k8s-demo.jpg)
</Frame>

2. Import the project as a Maven project:

<Frame>
  ![The image shows the Spring Tool Suite IDE with an "Import Maven Projects" dialog open, displaying options to select Maven projects from a specified directory. The desktop taskbar is visible at the bottom with various application icons.](https://kodekloud.com/kk-media/image/upload/v1752873586/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Running-Microservices-Local-Machine/spring-tool-suite-import-maven-dialog.jpg)
</Frame>

***

## 2. Inspect the Maven POM

Open the `pom.xml` file at the project root. You’ll find the Spring Boot parent and starter dependencies:

```xml theme={null}
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="
           http://maven.apache.org/POM/4.0.0
           http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>numeric</groupId>
  <artifactId>numeric</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <name>numeric</name>
  <description>Demo for DevSecOps</description>

  <properties>
    <java.version>1.8</java.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```

For more details on Maven POM configuration, refer to the [Maven Reference Documentation](https://maven.apache.org/pom.html).

***

## 3. Review the Spring Boot Controller

The core logic resides in `NumericController.java`. It defines three endpoints:

```java theme={null}
package com.devsecops;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
public class NumericController {
    private final Logger logger = LoggerFactory.getLogger(getClass());

    // For Kubernetes use:
    private static final String baseURL = "http://node-service:5000/plusone";
    // For local testing, uncomment the line below and comment out the Kubernetes URL:
    // private static final String baseURL = "http://localhost:5000/plusone";

    private final RestTemplate restTemplate = new RestTemplate();

    @GetMapping("/")
    public String welcome() {
        return "Kubernetes DevSecOps";
    }

    @GetMapping("/compare/{value}")
    public String compareToFifty(@PathVariable int value) {
        return (value > 50) ? "Greater than 50" : "Smaller than or equal to 50";
    }

    @GetMapping("/increment/{value}")
    public ResponseEntity<String> increment(@PathVariable int value) {
        logger.info("Value received in request: " + value);
        ResponseEntity<String> response =
            restTemplate.getForEntity(baseURL + "/" + value, String.class);
        String nodeResponse = response.getBody();
        String body = "Spring received: " + value + "\nNode response: " + nodeResponse;
        return ResponseEntity.ok(body);
    }
}
```

<Callout icon="lightbulb">
  Toggle the `baseURL` between `localhost` (for local debugging) and `node-service` (for Kubernetes) before running the app.
</Callout>

***

## 4. Run the Node.js “plus-one” Service in Docker

Ensure Docker is installed and running on your machine.

<Callout icon="triangle-alert">
  Make sure port **5000** is free. If another service is using this port, stop it or choose a different host port.
</Callout>

Execute:

```bash theme={null}
docker run -p 5000:5000 siddharth67/node-service:v1
```

You should see output similar to:

```bash theme={null}
> node app.js
HOSTNAME is 6dceae5489
```

### 4.1 Test the Node.js Service

In a browser or via `curl`:

```bash theme={null}
curl http://localhost:5000/plusone/999
```

Expected response: `1000`

<Frame>
  ![The image shows a web browser displaying a page with the number "1000" on it. The URL in the address bar is "localhost:5000/plusone/999".](https://kodekloud.com/kk-media/image/upload/v1752873587/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Running-Microservices-Local-Machine/web-browser-page-number-1000.jpg)
</Frame>

***

## 5. Run and Test the Spring Boot Application

Start the Spring Boot service:

* In your IDE: **Run As → Spring Boot App**
* Or via Maven:

  ```bash theme={null}
  mvn spring-boot:run
  ```

By default, it listens on port **8080**. Test the endpoints:

| Endpoint             | Method | Description                               | Example Command                           |
| -------------------- | ------ | ----------------------------------------- | ----------------------------------------- |
| `/`                  | GET    | Welcome message                           | `curl http://localhost:8080/`             |
| `/compare/{value}`   | GET    | Compare number to 50                      | `curl http://localhost:8080/compare/55`   |
| `/increment/{value}` | GET    | Increment via Node.js service and respond | `curl http://localhost:8080/increment/55` |

**Sample Responses**

1. Welcome:

   ```bash theme={null}
   $ curl http://localhost:8080/
   Kubernetes DevSecOps
   ```

2. Compare:

   ```bash theme={null}
   $ curl http://localhost:8080/compare/55
   Greater than 50
   ```

3. Increment:

   ```bash theme={null}
   $ curl http://localhost:8080/increment/55
   Spring received: 55
   Node response: 56
   ```

<Frame>
  ![The image shows a web browser displaying a local URL with the number "56" on a blank page. The browser has multiple tabs open, and there is a small video call or webcam feed in the top right corner.](https://kodekloud.com/kk-media/image/upload/v1752873588/notes-assets/images/DevSecOps-Kubernetes-DevOps-Security-Demo-Running-Microservices-Local-Machine/web-browser-local-url-56-tabs.jpg)
</Frame>

In your IDE console, look for:

```bash theme={null}
... INFO ... NumericController     : Value received in request: 55
```

In the Docker container logs you’ll see:

```bash theme={null}
Value Received = 55
```

***

## 6. Next Steps

Before deploying to Kubernetes:

1. Switch `baseURL` back to
   ```java theme={null}
   private static final String baseURL = "http://node-service:5000/plusone";
   ```
2. Configure a Maven build and set up a Jenkins pipeline to automate the Spring Boot deployment.

***

## Links and References

* [Spring Boot Reference Guide](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/)
* [Docker Documentation](https://docs.docker.com/)
* [Maven POM Reference](https://maven.apache.org/pom.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/b35daf6a-2301-428d-b877-2806476a26d3" />
</CardGroup>
