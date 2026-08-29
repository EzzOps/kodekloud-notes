# What are Job Containers

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/What-are-Job-Containers/page

Explains using Docker job containers and service containers in GitHub Actions to create reproducible, faster, and isolated CI environments with examples and best practices.

Let's talk about job containers in GitHub Actions.

<Frame>
  <img alt="A turquoise-to-light-green gradient presentation slide with the title &#x22;Job Containers&#x22; in white text near the center-right. Small &#x22;© Copyright KodeKloud&#x22; text appears in the bottom-left corner." />
</Frame>

When authoring a GitHub Actions workflow, you select a runner for each job. The most common choice is a GitHub-hosted virtual machine such as `ubuntu-latest`. These hosted VMs include a pre-configured environment with many common tools and runtimes (language runtimes, package managers, CLI tools, browsers, and cached Docker images).

If a required runtime or package version is not preinstalled, you add steps to the job to install them. For example, a typical workflow that sets up Node.js, installs dependencies, and runs tests looks like this:

```yaml theme={null}
name: My Awesome App
on: push
jobs:
  unit-testing:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: npm ci

      - name: Install testing packages
        run: npm install --no-save some-testing-package

      - name: Run tests
        run: npm test
```

Installing runtimes and packages at job runtime increases execution time, which can lengthen feedback loops and raise GitHub Actions usage costs. Job containers let you avoid repeated setup by running the job inside a Docker image that already contains the required runtime and tools.

What is a job container?

* A job container is a Docker image that GitHub starts on the hosted runner and uses to execute all the job's steps.
* The hosted VM still boots, but the job steps run inside the container's environment.
* This provides a fast, consistent environment that you control via the image.

Benefits of running jobs inside containers:

* Isolation — Jobs run in isolated containers, reducing conflicts with the host VM and other jobs.
* Reproducibility — A specific image yields the same environment across runs and runners.
* Security — Containerization limits access to the host and lets you constrain permissions for untrusted workloads.

| Benefit         | What it means for CI                               |
| --------------- | -------------------------------------------------- |
| Isolation       | Limits side effects and dependency collisions      |
| Reproducibility | Deterministic builds and tests across environments |
| Faster runs     | Preinstalled runtimes and tools reduce setup time  |
| Cost control    | Less time spent installing temporary dependencies  |

To use a job container, specify the `container` key under the job. If your container image already contains Node.js 20 and the test packages, you can remove the runtime/setup steps and rely on the image:

```yaml theme={null}
name: My Awesome App
on: push
jobs:
  unit-testing:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/node-and-packages:20
      credentials:
        username: alice
        password: ${{ secrets.PWD }}

    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

When this workflow runs, GitHub creates the hosted runner (for example, the Ubuntu VM), pulls the specified container image, starts the container, and executes the job steps inside it. Because the image already contains the runtime and test packages, jobs start and finish faster and behave more predictably.

> **lightbulb** Using a container image with preinstalled runtimes and tools reduces per-run setup time, speeds up CI feedback, and can lower your GitHub Actions usage costs.

A common caution: avoid connecting CI jobs directly to production databases or services. Tests that run against production resources can affect performance and compromise data integrity. For tests that need databases or other services, use dedicated test instances or GitHub Actions service containers.

> **warning** Do not run CI tests directly against production databases or services. Use isolated test instances or service containers to protect production systems.

Service containers

* Service containers run as additional Docker containers alongside your job container and are accessible via network hostnames.
* Use service containers for databases, caching layers, or any supporting service your tests require.

Example: provide a PostgreSQL service to a job:

```yaml theme={null}
jobs:
  unit-testing:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/node-and-packages:20

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - name: Wait for Postgres
        run: |
          until pg_isready -h postgres -U postgres; do
            sleep 1
          done
      - name: Run tests
        run: npm test
```

Combining job containers (for prebuilt environments) with service containers (for supporting services like databases) yields fast, reproducible, and safer CI pipelines.

Further reading and references

* [GitHub Actions: About workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)
* [GitHub Actions: GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
* [GitHub Actions: Using a container to run a job](https://docs.github.com/en/actions/using-jobs/using-a-container-to-run-a-job)
* [GitHub Actions: Using service containers](https://docs.github.com/en/actions/using-jobs/using-service-containers)
* [Docker documentation](https://docs.docker.com/)
* [Postgres Docker Hub image](https://hub.docker.com/_/postgres)

- [Watch Video](https://learn.kodekloud.com/user/courses/github-actions/module/6136c7b5-8fe0-4a84-ae77-0274623512d5/lesson/9335c684-a9a3-49dc-93fd-405b2cf3b19e)
