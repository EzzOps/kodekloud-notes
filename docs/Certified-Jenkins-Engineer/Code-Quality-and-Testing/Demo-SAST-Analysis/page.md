# Demo SAST Analysis

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Code-Quality-and-Testing/Demo-SAST-Analysis/page

Perform Static Application Security Testing on JavaScript code using SonarQube, covering configuration, project creation, local analysis, and Jenkins integration.

Perform Static Application Security Testing (SAST) on your JavaScript (Node.js) code using SonarQube. We assume SonarQube is running at `http://<host>:9000`.

## 1. Configure the Default Quality Gate

1. Log in to SonarQube and navigate to **Quality Gates**.
2. Select **Dasher-Quality-Gate** and click **Set as default**.
3. Verify the key condition: **Overall Coverage \< 90%**.

<Callout icon="lightbulb">
  Quality Gates enforce your code quality standards automatically. Failing criteria (e.g., coverage, duplications, maintainability) will mark the gate as failed.
</Callout>

<Frame>
  ![The image shows a SonarQube interface displaying a quality gate configuration named "Dasher-Quality-Gate," with conditions for code metrics like coverage, duplicated lines, and maintainability. It includes a warning about adding extra conditions to the "Clean as You Code" quality gate.](https://kodekloud.com/kk-media/image/upload/v1752870476/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/sonarqube-dasher-quality-gate-config.jpg)
</Frame>

## 2. Create a New Project

### 2.1. Define Project Basics

1. Click **Create Project** → **Manually**.
2. Fill in the form:
   * Project Display Name: `Solar-System-Project`
   * Project Key: `Solar-System-Project`
   * Main Branch Name: `main`

<Frame>
  ![The image shows a SonarQube interface for creating a new project, with fields for project display name, project key, and main branch name. The project is named "Solar-System-Project."](https://kodekloud.com/kk-media/image/upload/v1752870477/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/sonarqube-new-project-interface.jpg)
</Frame>

### 2.2. Select Technology and OS

* Under **Technology**, choose **Other**.
* For **Operating System**, select **Linux**.

<Frame>
  ![The image shows a SonarQube dashboard for a project named "Solar-System-Project," offering integration options with various CI tools like Jenkins, GitHub Actions, and GitLab CI. There is also a note about the embedded database being for evaluation purposes only.](https://kodekloud.com/kk-media/image/upload/v1752870478/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/sonarqube-dashboard-solar-system-project.jpg)
</Frame>

### 2.3. Generate an Authentication Token

1. In the project dashboard, click **Generate Token**.
2. Provide a name and select **No expiration** (for demo only).

<Callout icon="triangle-alert">
  Avoid using tokens without expiration in production. Rotate your tokens regularly.
</Callout>

<Frame>
  ![The image shows a SonarQube dashboard for a project named "Solar-System-Project," where a token is being generated for project analysis. There is a dropdown menu for setting the token expiration, with options like 30 days, 1 year, and no expiration.](https://kodekloud.com/kk-media/image/upload/v1752870479/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/sonarqube-dashboard-solar-system-token.jpg)
</Frame>

## 3. Local Analysis with sonar-scanner

Install the SonarQube Scanner locally or via your package manager. Then run:

```shell theme={null}
sonar-scanner \
  -Dsonar.projectKey=Solar-System-Project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://<host>:9000 \
  -Dsonar.login=<YOUR_TOKEN>
```

## 4. Jenkins Pipeline Configuration

Integrate SAST into your CI by adding a SonarQube stage to your `Jenkinsfile`:

```groovy theme={null}
pipeline {
  agent any
  environment {
    SONAR_SCANNER_HOME = tool 'sonarqube-scanner-6.1.0'
  }
  stages {
    stage('Installing Dependencies')   { steps { /* ... */ } }
    stage('Dependency Scanning')      { steps { /* ... */ } }
    stage('Unit Testing')             { steps { /* ... */ } }
    stage('Code Coverage')            { steps { /* ... */ } }
    stage('SAST - SonarQube') {
      steps {
        sh 'echo $SONAR_SCANNER_HOME'
        sh """
          $SONAR_SCANNER_HOME/bin/sonar-scanner \
            -Dsonar.projectKey=Solar-System-Project \
            -Dsonar.sources=app.js \
            -Dsonar.host.url=http://<host>:9000 \
            -Dsonar.login=<YOUR_TOKEN>
        """
      }
    }
  }
}
```

For more options, see the [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/) guide.

## 5. Installing SonarScanner in Jenkins

1. Go to **Manage Jenkins** → **Manage Plugins**.
2. Under **Available**, search for `sonar` and install **SonarQube Scanner**. Restart Jenkins.

<Frame>
  ![The image shows the Jenkins plugin management interface, specifically the "Available plugins" section, with a search for "sonar" displaying plugins like SonarQube Scanner and Sonar Quality Gates.](https://kodekloud.com/kk-media/image/upload/v1752870480/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/jenkins-plugin-management-sonar-search.jpg)
</Frame>

<Frame>
  ![The image shows a Jenkins interface displaying the download progress of plugins, with statuses for SonarQube Scanner and other tasks.](https://kodekloud.com/kk-media/image/upload/v1752870481/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/jenkins-plugin-download-progress.jpg)
</Frame>

3. After restart, navigate to **Manage Jenkins** → **Global Tool Configuration** → **SonarQube Scanner**.
   * Name: `sonarqube-scanner-6.1.0`
   * Select **Install automatically from Maven Central**

<Frame>
  ![The image shows a Jenkins configuration screen for adding a SonarQube Scanner installation, with options to set the name and version, and an "Install automatically" checkbox selected.](https://kodekloud.com/kk-media/image/upload/v1752870482/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/jenkins-sonarqube-scanner-configuration.jpg)
</Frame>

## 6. First SonarQube Analysis Result

Run your Jenkins pipeline. After it completes, refresh SonarQube:

```text theme={null}
ANALYSIS SUCCESSFUL, you can find the results at: http://<host>:9000/dashboard?id=Solar-System-Project
```

<Frame>
  ![The image shows a SonarQube dashboard for a project named "Solar-System-Project," indicating a failed quality gate due to insufficient code coverage. It displays metrics such as bugs, vulnerabilities, security hotspots, and code smells.](https://kodekloud.com/kk-media/image/upload/v1752870484/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/sonarqube-dashboard-solar-system-failed.jpg)
</Frame>

Coverage is reported as 0%, so the Quality Gate fails (coverage \< 90%).

## 7. Adding Code Coverage Reports

1. Generate coverage before the SonarQube stage:

   ```bash theme={null}
   npm run coverage
   ```

   This creates `./coverage/lcov.info`.

2. Import the report by updating the scanner command:

   ```groovy theme={null}
   stage('SAST - SonarQube') {
     steps {
       sh 'echo $SONAR_SCANNER_HOME'
       sh """
         $SONAR_SCANNER_HOME/bin/sonar-scanner \
           -Dsonar.projectKey=Solar-System-Project \
           -Dsonar.sources=app.js \
           -Dsonar.host.url=http://<host>:9000 \
           -Dsonar.javascript.lcov.reportPaths=./coverage/lcov.info \
           -Dsonar.login=<YOUR_TOKEN>
       """
     }
   }
   ```

After rerunning the pipeline, your coverage will appear (e.g., 73%) but still below 90%.

<Frame>
  ![The image shows a SonarQube dashboard for a project named "Solar-System-Project," indicating a failed quality gate due to code coverage being less than 90%. It displays metrics such as bugs, vulnerabilities, security hotspots, and code smells.](https://kodekloud.com/kk-media/image/upload/v1752870485/notes-assets/images/Certified-Jenkins-Engineer-Demo-SAST-Analysis/sonarqube-dashboard-solar-system-failed-2.jpg)
</Frame>

<Callout icon="lightbulb">
  Since SonarQube doesn’t return the Quality Gate status to Jenkins by default, your pipeline may remain green. In the next tutorial, we’ll configure the [SonarQube Quality Gate plugin](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner-for-jenkins/) to fail builds when the gate fails.
</Callout>

***

## Links and References

* [SonarQube Documentation](https://docs.sonarqube.org/latest/)
* [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
* [npm test scripts](https://docs.npmjs.com/cli/v7/using-npm/scripts)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/7214771c-8a65-4b34-94a9-43665202a4e4/lesson/a2542195-f04e-405c-b493-e2730afb6127" />
</CardGroup>
