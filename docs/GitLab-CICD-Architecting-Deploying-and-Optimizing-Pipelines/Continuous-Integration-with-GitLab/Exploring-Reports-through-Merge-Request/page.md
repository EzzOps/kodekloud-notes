# Exploring Reports through Merge Request

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Exploring-Reports-through-Merge-Request/page

This guide explores using GitLab CI’s reports keyword to display test and coverage reports in Merge Requests for immediate feedback.

In this guide, we’ll dive into GitLab CI’s `reports` keyword to display both test and coverage reports directly in a Merge Request (MR). Instead of merely storing artifacts, you’ll provide reviewers with immediate feedback—failing tests, coverage metrics, and line-by-line highlights.

## Configuring JUnit and Coverage Reports

Add JUnit and Cobertura reporting to your `.gitlab-ci.yml`:

```yaml theme={null}
variables:
  MONGO_URI: 'mongodb+srv://supercluster.d83jj.mongodb.net/superData'
  MONGO_USERNAME: superuser
  MONGO_PASSWORD: $M_DB_PASSWORD

stages:
  - test

unit_testing:
  stage: test
  image: node:17-alpine3.14
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
  before_script:
    - npm install
  script:
    - npm run coverage
  artifacts:
    name: Code-Coverage-Result
    when: always
    expire_in: 3 days
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/ci_cobertura-coverage.xml
```

<Callout icon="lightbulb">
  Setting `expire_in: 3 days` keeps recent results accessible without long-term storage costs.
</Callout>

## Editing Multiple Files in the Web IDE

1. Open the project in GitLab’s Web IDE.
2. Switch to your feature branch.
3. Remove any placeholder jobs.
4. Copy in the CI definitions above.

<Frame>
  ![The image shows a GitLab repository interface with a list of files and directories, along with options for editing and managing the project. A tooltip is visible, providing information about using the Web IDE.](https://kodekloud.com/kk-media/image/upload/v1752877250/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Reports-through-Merge-Request/gitlab-repository-interface-web-ide.jpg)
</Frame>

## Introducing a Test Failure

In `app-test.js`, force a test to fail by expecting `"Planet-Mercury"` instead of `"Mercury"`:

```javascript theme={null}
let chaiHttp = require("chai-http");
chai.should();
chai.use(chaiHttp);

describe('Planets API Suite', () => {
  describe('Fetching Planet Details', () => {
    it('it should fetch a planet named Mercury', (done) => {
      let payload = { id: 1 };
      chai.request(server)
        .post('/planet')
        .send(payload)
        .end((err, res) => {
          res.should.have.status(200);
          res.body.should.have.property('id').eql(1);
          // Expect mismatch to simulate failure
          res.body.should.have.property('name').eql('Planet-Mercury');
          done();
        });
    });

    it('it should fetch a planet named Venus', (done) => {
      let payload = { id: 2 };
      // additional test code here
    });
  });
});
```

## Creating a Coverage Gap

Introduce an untested line in `app.js`:

```javascript theme={null}
mongoose.connect(process.env.MONGO_URI, {
  user: process.env.MONGO_USERNAME,
  pass: process.env.MONGO_PASSWORD,
  useNewUrlParser: true,
  useUnifiedTopology: true
}, function(err) {
  if (err) {
    console.log("error!! " + err);
    console.log("DB Connection error!! " + err);
  } else {
    // console.log("MongoDB Connection Successful")
  }
});
```

## Running the Pipeline

Commit and push your changes. A new pipeline will start automatically:

```yaml theme={null}
sample-job:
  stage: test
  needs:
    - code_coverage
  image: node:17-alpine3.14
  script:
    - echo testing sample job
```

<Frame>
  ![The image shows a GitLab CI/CD pipeline interface for a project named "Solar System NodeJS Pipeline," displaying two jobs: "code\_coverage" and "unit\_testing." The pipeline is currently running, with options to cancel or delete it.](https://kodekloud.com/kk-media/image/upload/v1752877251/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Reports-through-Merge-Request/gitlab-ci-cd-solar-system-pipeline.jpg)
</Frame>

<Callout icon="triangle-alert">
  Align your coverage thresholds with team guidelines to avoid unexpected failures.
</Callout>

## Other Report Types

GitLab supports multiple report formats:

| Report Type | Format                  | CI Keyword                | Example Path                      |
| ----------- | ----------------------- | ------------------------- | --------------------------------- |
| JUnit       | JUnit XML               | `reports:junit`           | `test-results.xml`                |
| Coverage    | Cobertura XML           | `reports:coverage_report` | `coverage/cobertura-coverage.xml` |
| RSpec JUnit | RspecJunitFormatter XML | `reports:junit`           | `rspec.xml`                       |

```yaml theme={null}
rspec:
  stage: test
  script:
    - bundle install
    - rspec --format RspecJunitFormatter --out rspec.xml
  artifacts:
    reports:
      junit: rspec.xml

artifacts:
  reports:
    coverage_report:
      coverage_format: cobertura
      path: coverage/cobertura-coverage.xml
```

<Frame>
  ![The image shows a GitLab documentation page about unit test reports, specifically focusing on viewing failed tests. It includes a screenshot of a test summary panel with details of test failures.](https://kodekloud.com/kk-media/image/upload/v1752877252/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Reports-through-Merge-Request/gitlab-unit-test-reports-failed-tests.jpg)
</Frame>

<Frame>
  ![The image shows a GitLab documentation page about test coverage visualization, explaining how coverage information is displayed and providing configuration details.](https://kodekloud.com/kk-media/image/upload/v1752877253/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Reports-through-Merge-Request/gitlab-test-coverage-visualization.jpg)
</Frame>

## Viewing Test Failures in the Job Log

After the pipeline runs, review the job log for failures and coverage warnings:

```text theme={null}
ERROR: Coverage for lines (86.48%) does not meet global threshold (90%)
...
ERROR: Job failed: exit code 1
```

<Frame>
  ![The image shows a GitLab CI/CD pipeline report for a NodeJS project, indicating a failed pipeline with one test failure out of eleven tests. The failed test is related to fetching a planet named Mercury.](https://kodekloud.com/kk-media/image/upload/v1752877254/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Reports-through-Merge-Request/gitlab-cicd-nodejs-failed-test-mercury.jpg)
</Frame>

## Exploring Reports in a Merge Request

1. Push your feature branch and open an MR titled **Exploring GitLab CI/CD**:

<Frame>
  ![The image shows a GitLab interface for creating a new merge request, with fields for the title, description, assignee, and reviewer. The project is named "Solar System" under the "demos-group."](https://kodekloud.com/kk-media/image/upload/v1752877256/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Reports-through-Merge-Request/gitlab-merge-request-solar-system.jpg)
</Frame>

2. The MR pipeline runs via these workflow rules:

   ```yaml theme={null}
   workflow:
     name: Solar System NodeJS Pipeline
     rules:
       - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH =~ /^feature/'
         when: always
       - if: '$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME =~ /^feature/ && $CI_PIPELINE_SOURCE == "merge_request_event"'
         when: always
   ```

3. Check the MR sidebar for:
   * A test summary (e.g., 1/11 failed)
   * Coverage percentage
   * Detailed assertion errors

<Frame>
  ![The image shows a GitLab interface with a merge request titled "Exploring gitlab cicd." The merge request pipeline has failed, with 1 out of 11 tests failing.](https://kodekloud.com/kk-media/image/upload/v1752877257/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Exploring-Reports-through-Merge-Request/gitlab-merge-request-failed-pipeline.jpg)
</Frame>

4. In the **Changes** tab, you’ll see diffs highlighting:
   * Modified test expectations
   * New console logs in `app.js`
   * Coverage gaps (orange) and covered lines (green)

## Conclusion

By using GitLab CI’s `reports` keyword, you surface test results and coverage details directly within Merge Requests. This streamlines code reviews, enabling teams to catch failures and coverage gaps before merging.

## Links and References

* [GitLab CI/CD Reports Documentation](https://docs.gitlab.com/ee/ci/testing/test_report.html)
* [JUnit Format Specification](https://junit.org/junit5/docs/current/user-guide/#running-tests-build-junit)
* [Cobertura Coverage Format](https://cobertura.github.io/cobertura/coverage-format.html)
* [GitLab Web IDE](https://docs.gitlab.com/ee/user/project/web_ide/)
* [Chai HTTP](https://www.chaijs.com/plugins/chai-http/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/5f42aa70-1bcb-4024-a815-ea8db1bbf66b" />
</CardGroup>
