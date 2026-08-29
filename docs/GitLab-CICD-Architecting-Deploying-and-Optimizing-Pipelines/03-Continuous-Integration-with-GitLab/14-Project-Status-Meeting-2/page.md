# Project Status Meeting 2

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Project-Status-Meeting-2/page

This article discusses issues with running CI tests against a production database and how to refactor the pipeline to use a dedicated test instance.

Welcome to the second project status meeting! In this session, we’ll investigate how our CI/CD pipeline inadvertently hit the production database and refactor it to use a dedicated test instance.

***

## The Issue: Tests Pointing at Production

After wrapping up the first three tasks, Alice was pulled into an urgent meeting. Monitoring alerts revealed that the production MongoDB cluster had become sluggish and occasionally unresponsive—right after the team enabled [GitLab CI/CD pipelines](https://docs.gitlab.com/ee/ci/).

Reviewing the pipeline, Alice saw two test jobs both connecting directly to the production database via environment variables:

```yaml theme={null}
variables:
  MONGO_URI: 'mongodb+srv://supercluster.d3jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD

unit_testing:
  stage: test
  image: node:17-alpine3.14
  cache:
    key:
      files:
        - package-lock.json
      prefix: node_modules
  before_script:
    - npm install
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    name: Moca-Test-Result
    paths:
      - test-results.xml
    reports:
      junit: test-results.xml

code_coverage:
  stage: test
  image: node:17-alpine3.14
  cache:
    key:
      files:
        - package-lock.json
      prefix: node_modules
  before_script:
    - npm install
  script:
    - npm run coverage
  artifacts:
    when: always
    expire_in: 3 days
    name: Coverage-Report
    paths:
      - coverage/
```

<Callout icon="triangle-alert">
  Never run CI tests against your production database. This can lead to performance degradation, data corruption, and security risks.
</Callout>

***

## Why Use a Dedicated Test Database?

Running tests against production can:

* Introduce load and latency for real users.
* Accidentally modify or delete critical data.
* Complicate debugging because of shared state.

Instead, spin up an isolated MongoDB instance or use a mock service.

***

## Using GitLab CI Services

GitLab CI/CD supports **services**—auxiliary containers that start alongside your job. You can:

* Launch a database container (e.g., `mongo:4.4`)
* Seed it with test data in `before_script`
* Point your application to `localhost` or the service alias

Read more in the [GitLab Services documentation](https://docs.gitlab.com/ee/ci/services/).

<Callout icon="lightbulb">
  Services are defined per-job. Each service runs in its own Docker container, linked to the job container.
</Callout>

***

## Refactored Pipeline Configuration

Below is a revised `.gitlab-ci.yml` that replaces the production connection with a local MongoDB service:

```yaml theme={null}
variables:
  MONGO_INITDB_DATABASE: testdb
  MONGO_INITDB_ROOT_USERNAME: testuser
  MONGO_INITDB_ROOT_PASSWORD: testpass

.default_test_template: &test_template
  stage: test
  image: node:17-alpine3.14
  services:
    - name: mongo:4.4
      alias: mongo
  before_script:
    - npm install
    - |
      # Wait for MongoDB to be ready
      until mongo --host mongo -u $MONGO_INITDB_ROOT_USERNAME \
        -p $MONGO_INITDB_ROOT_PASSWORD \
        --eval "db.adminCommand('ping')" &>/dev/null; do
        echo "Waiting for MongoDB..."
        sleep 2
      done
    - npm run seed-test-data   # seed-test-data script should populate 'testdb'
  variables:
    MONGO_URI: "mongodb://$MONGO_INITDB_ROOT_USERNAME:$MONGO_INITDB_ROOT_PASSWORD@mongo:27017/$MONGO_INITDB_DATABASE"

unit_testing:
  <<: *test_template
  script:
    - npm test
  artifacts:
    when: always
    expire_in: 3 days
    name: moca-test-result
    paths:
      - test-results.xml
    reports:
      junit: test-results.xml

code_coverage:
  <<: *test_template
  script:
    - npm run coverage
  artifacts:
    when: always
    expire_in: 3 days
    name: coverage-report
    paths:
      - coverage/
```

***

## Job Configuration Comparison

| Job            | Original DB                | Refactored with Services  |
| -------------- | -------------------------- | ------------------------- |
| unit\_testing  | Production MongoDB cluster | Local `mongo:4.4` service |
| code\_coverage | Production MongoDB cluster | Local `mongo:4.4` service |

***

## Further Reading and References

* [GitLab CI/CD Services](https://docs.gitlab.com/ee/ci/services/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [MongoDB Docker Hub](https://hub.docker.com/_/mongo)
* [Node.js Alpine Images](https://hub.docker.com/_/node)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/98a18f73-b886-4805-9228-6eba0c1c0d77" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/8b61573a-eac0-457e-b4f0-88b11565af47" />
</CardGroup>
