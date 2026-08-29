# "Welcome to the Spring Boot service!"
```

### 2. GET /increment/

This endpoint demonstrates inter-service communication. It sends the provided number to the Node.js `/plusone` service and returns the incremented result.

```bash theme={null}
curl http://localhost:8080/increment/41
# 42
```

### 3. GET /compare/

Performs a conditional check on the input number:

* If `number` ≤ 50: returns `"{number} is less than or equal to 50"`.
* If `number` > 50: returns `"{number} is greater than 50"`.

```bash theme={null}
curl http://localhost:8080/compare/50
curl http://localhost:8080/compare/77
# "77 is greater than 50"
```

> **triangle-alert** Port conflicts can occur if other services use ports 5000 or 8080. Always verify available ports before starting the containers.

***

## Course Roadmap

Throughout this course, you will:

* Containerize and Dockerize the Spring Boot application.
* Deploy Spring Boot securely on Kubernetes with best practices.
* Leverage an existing Docker image for the Node.js service.
* Explore service-to-service REST communication and error handling.

By the end, you’ll have a fully functioning microservices demo running on Kubernetes, complete with automated builds and deployments. Let’s dive in!

***

## Links and References

* [Node.js Official Site](https://nodejs.org/)
* [Spring Boot Documentation](https://spring.io/projects/spring-boot)
* [Docker Documentation](https://docs.docker.com/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/be616027-6bb3-4575-bbf7-4561ffe87d44)


# Unit Tests Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Unit-Tests-Basics/page

This article covers unit testing practices, running tests with Maven, and measuring code coverage using JaCoCo.

Unit testing is a software development practice where individual units—such as functions, methods, or classes—are tested in isolation to ensure they behave as expected. By adopting unit tests early, teams can:

| Benefit                        | Description                                                           |
| ------------------------------ | --------------------------------------------------------------------- |
| Early Defect Detection         | Identify bugs at the development stage before they propagate.         |
| Faster Feedback Loop           | Run tests quickly and fix issues immediately.                         |
| Lower Maintenance Costs        | Catching issues early reduces expensive, late-stage fixes.            |
| Improved Code Quality & Design | Writing tests encourages cleaner, modular code and better API design. |

## Running Unit Tests with Maven

In a Maven-based project, execute all unit tests with:

```bash theme={null}
mvn test
```

Maven automatically scans `src/test/java` (and any additional test directories you’ve configured), runs tests, and fails the build if any test does not pass:

```bash theme={null}
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[ERROR] Tests run: 3, Failures: 1, Errors: 0, Skipped: 0
[INFO] -------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] -------------------------------------------------------
[INFO] Total time:  30.123 s
[INFO] Finished at: 2024-06-15T14:22:10+00:00
[INFO] -------------------------------------------------------
```

> **lightbulb** By default, Maven looks for test classes matching `**/*Test.java` under `src/test/java`. You can customize this in the `<build><plugins>` section of your `pom.xml`.

> **triangle-alert** A failing test will stop the Maven build. Ensure you fix or temporarily disable flaky tests to keep CI pipelines green.

## Measuring Code Coverage with JaCoCo

[JaCoCo](https://www.eclemma.org/jacoco/) is the de facto tool for generating Java code coverage reports. When integrated into Maven, it produces detailed HTML reports showing line and branch coverage.

### 1. Add the JaCoCo Plugin

Include the following snippet in your `pom.xml` under `<build><plugins>`:

```xml theme={null}
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.10</version>
  <executions>
    <execution>
      <goals>
        <goal>prepare-agent</goal>
      </goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals>
        <goal>report</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

> **lightbulb** You can configure coverage thresholds to enforce minimum percentages. If thresholds are not met, the build will fail.

### 2. Generate the Report

Run your tests and generate the coverage report:

```bash theme={null}
mvn clean test
```

After completion, open:

```text theme={null}
target/site/jacoco/index.html
```

to view:

* **Overall Coverage:** Total percentage of covered code.
* **Per-Package/Class Breakdown:** Drill down into modules.
* **Covered vs. Uncovered Lines:** Visual indicators in source code.

| Report Section | Description                               |
| -------------- | ----------------------------------------- |
| Summary        | High-level percentages for lines/branches |
| Packages       | Coverage grouped by Java packages         |
| Classes        | Detailed per-class metrics                |
| Source Code    | Color-coded, line-by-line coverage view   |

## Links and References

* [JaCoCo Official Site](https://www.eclemma.org/jacoco/)
* [Maven Surefire Plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)
* [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)

Thank you for reading!

- [Watch Video](https://learn.kodekloud.com/user/courses/devsecops-kubernetes-devops-security/module/6942848d-9481-472e-a8ec-47357cf8ceaa/lesson/aba08a1a-e011-499a-b5ab-eb79a2e21d47)
