# A dictionary to store tasks with an ID
tasks = {}
task_id_counter = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    global task_id_counter
    response_text = ""

    if request.method == 'POST':
        if 'add_task' in request.form:
            task_content = request.form.get('task_content')
            if task_content:
                tasks[task_id_counter] = task_content
                task_id_counter += 1
        elif 'delete_task' in request.form:
            task_id_to_delete = int(request.form.get('task_id_to_delete'))
            tasks.pop(task_id_to_delete, None)

    return render_template('index.html', tasks=tasks)
```

### Unit Tests: test\_app.py

This file sets up the automated unit tests using Pytest.

```python theme={null}
import pytest
from app import app as flask_app, tasks

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(app, client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task(client):
    # Adjust 'task_content' as needed based on your form data
    response = client.post('/', data={'task_content': 'New Task', 'add_task': True})
    assert response.status_code == 200
    assert 'New Task' in tasks.values()

def test_delete_task(client):
    # First, add a task
    client.post('/', data={'task_content': 'Task to Delete', 'add_task': True})
    task_id_to_delete = list(tasks.keys())[0]
    response = client.post('/', data={'task_id_to_delete': task_id_to_delete, 'delete_task': True})
    assert response.status_code == 200
    assert task_id_to_delete not in tasks
```

### Dependency File: requirements.txt

This file lists the external dependencies needed to run the Flask application:

```plaintext theme={null}
blinker==1.7.0
cachetools==5.3.2
certifi==2023.11.17
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
exceptiongroup==1.2.0
Flask==3.0.1
google-ai-generativelanguage==0.4.0
google-api-core==2.15.0
google-auth==2.26.2
google-generativeai==0.3.2
googleapis-common-protos==1.62.0
grpcio==1.60.0
grpcio-status==1.60.0
idna==3.6
iniconfig==2.0.0
itsdangerous==2.1.2
Jinja2==3.1.3
MarkupSafe==2.1.4
packaging==23.2
pluggy==1.3.0
proto-plus==1.23.0
protobuf==4.25.1
pysn1==0.5.1
pysn1-modules==0.3.0
pytest==7.4.4
```

Use the command below to install the required packages:

```bash theme={null}
pip install -r requirements.txt
```

### HTML Template: index.html

The user interface for the Flask application is defined in the `templates/index.html` file. Here is an excerpt including the relevant styling:

```html theme={null}
<html>
<head>
<style>
input[type="submit"]:hover {
  background-color: #45a049;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  background-color: #fff;
  margin-bottom: 8px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.task-text {
  margin: 0;
}
</style>
</head>
<body>
    <!-- The rest of the HTML content -->
</body>
</html>
```

> **lightbulb** Ensure that all files are correctly committed to your repository before triggering the Jenkins pipeline.

## Configuring the Jenkins Pipeline with a Jenkinsfile

Below is the initial version of the Jenkinsfile that sets up the stages of the pipeline:

```groovy theme={null}
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/kodekloudhub/jenkins-project.git', branch: 'main'
                sh "ls -ltr"
            }
        }
        stage('Setup') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('Test') {
            steps {
                sh "pytest"
            }
        }
    }
}
```

This configuration consists of:

* **Checkout Stage:** Retrieves the source code from Git and lists the files.
* **Setup Stage:** Installs dependencies as specified in `requirements.txt`.
* **Test Stage:** Executes the tests using Pytest.

After verifying that everything works locally with the tests in `test_app.py`, commit your changes and push them to your repository using:

```bash theme={null}
git add .
git commit -m "initial commit"
git push origin main
```

Jenkins will pull the code, read the Jenkinsfile, and execute the defined steps. Click on a running build in Jenkins to view the console output, which shows details such as the checkout process, dependency installation, and test results.

![The image shows a Jenkins build interface for "flaskpipeline," displaying build details such as start time, duration, and GitHub repository information.](https://kodekloud.com/kk-media/image/upload/v1752879916/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-Unit-testing-with-pytest/jenkins-flaskpipeline-build-interface.jpg)

The console output will confirm the following sequence:

1. The source code is checked out (twice if the default checkout is not skipped).
2. The file list is printed using `ls -ltr`.
3. Dependencies are installed from `requirements.txt`.
4. Pytest runs and confirms that all tests pass.

## Optimizing the Pipeline: Skipping the Default Checkout

To avoid the redundant default checkout, update your Jenkinsfile with the `skipDefaultCheckout()` option:

```groovy theme={null}
pipeline {
    agent any
    options { skipDefaultCheckout() }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/kodekloudhub/jenkins-project.git', branch: 'main'
                sh 'ls -ltr'
            }
        }
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
    }
}
```

This adjustment ensures that Jenkins performs only a single checkout, executing the steps as defined in the "Checkout" stage.

After committing and pushing these changes, your pipeline will run with the optimized configuration. Below is an excerpt of the test output:

```bash theme={null}
+ pytest
============================= test session starts ==============================
platform linux -- Python 3.9.16, pytest-7.4.4, pluggy-1.3.0
rootdir: /var/lib/jenkins/workspace/flaskpipeline
collected 3 items

test_app.py ...  [100%]

============================= 3 passed in 0.14s ==============================
```

This output confirms that the tests have passed and the pipeline is executing as expected.

> **lightbulb** Integrating continuous testing within your CI/CD pipeline ensures that issues are identified early, making maintenance and scaling more efficient.

## Conclusion

By following this approach, you can seamlessly integrate a Flask application with Jenkins to perform automated unit tests using Pytest. This pipeline configuration supports continuous integration and assists in maintaining code quality throughout the development lifecycle.

For more details on continuous integration with Jenkins, visit the [Jenkins Documentation](https://www.jenkins.io/doc/).\
Further reading and additional materials can be found in links below:

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Pytest Documentation](https://docs.pytest.org/)

Happy coding and testing!

- [Watch Video](https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/4b025d4d-3ef9-479d-a483-3aa7a206a553/lesson/70b9c5c7-dd17-4348-be20-425a1830b7a0)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/4b025d4d-3ef9-479d-a483-3aa7a206a553/lesson/419d2d97-2e45-40f9-a49c-62474eaa625e)


# What is Jenkins Why do we need Jenkins

Source: https://notes.kodekloud.com/docs/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications/Jenkins/What-is-Jenkins-Why-do-we-need-Jenkins/page

This article explores Jenkins, an open source tool for automating continuous integration and delivery processes in software development.

In this lesson, we explore Jenkins—a leading open source tool designed for continuous integration and continuous delivery (CI/CD). Jenkins automates building, testing, and deploying your code, streamlining integration and delivery processes. Whether you're integrating new features, deploying updates, or running automated tests, Jenkins plays a pivotal role in ensuring that your software remains reliable and up-to-date.

Imagine pushing your code to GitHub, where Jenkins automatically detects changes. It then builds the code, executes tests, and even performs code formatting or linting. This automated process helps maintain high quality standards before deployment. For example:

![The image features the Jenkins logo and a diagram illustrating a process flow, with three icons leading to a gear symbol, under the title "What is Jenkins?"](https://kodekloud.com/kk-media/image/upload/v1752879917/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-What-is-Jenkins-Why-do-we-need-Jenkins/jenkins-logo-process-flow-diagram.jpg)

Once the build and test phases are complete, Jenkins can deploy your application to platforms such as Docker, Kubernetes, or various cloud providers through its extensive integrations. By handling repetitive tasks, Jenkins allows your team to focus on coding, leaving the details of the CI/CD pipeline to automation.

## How Jenkins Works

The Jenkins workflow typically begins when a developer commits code to a Git repository. This commit triggers a build in Jenkins, which then follows a series of preset steps, including:

* Linting and formatting the code
* Running unit and integration tests
* Building and packaging the application

If any step fails, Jenkins promptly notifies the team with detailed feedback, enabling developers to address issues and recommit their code swiftly. This rapid feedback loop ensures that the software remains in a deployable state. Consider this diagram for an overview of the process:

![The image illustrates a continuous integration process involving a commit to GitHub, triggering a build in Jenkins, and notifying the team if the build fails.](https://kodekloud.com/kk-media/image/upload/v1752879918/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-What-is-Jenkins-Why-do-we-need-Jenkins/continuous-integration-github-jenkins.jpg)

Jenkins automates the entire CI/CD pipeline by executing each stage defined in your version-controlled pipeline configuration (commonly using a Jenkinsfile). This approach helps maintain consistency and traceability across all environments.

## Advantages of Using Jenkins

Jenkins has become a popular CI/CD solution not only because it is open source and free, but also because of its numerous advantages:

* **Extensive Plugin Ecosystem:** Enhance functionality by integrating with various source control systems, deployment platforms, and testing tools.
* **Flexibility and Customization:** Configure Jenkins to support nearly any CI/CD workflow, making it adaptable to projects of various sizes and complexities.
* **Cross-Platform Compatibility:** Work effortlessly across different operating systems—Windows, macOS, and Linux—and deploy it on-premises or in the cloud.
* **Community Support:** Benefit from a large, active community that frequently updates Jenkins with security patches and improvements.
* **Pipeline as Code:** Maintain your CI/CD pipeline in code (via a Jenkinsfile) to ensure consistency and enable version control tracking.
* **Scalability:** Distribute builds across multiple machines to reduce build and test times significantly.
* **Detailed Reporting and Logging:** Monitor build statuses, test outcomes, and deployment logs, enhancing visibility and simplifying troubleshooting.

> **lightbulb** By automating repetitive tasks, Jenkins not only boosts productivity but also minimizes errors that often arise in manual build and deployment processes.

## Addressing Development Challenges with Jenkins

Manual build and deployment processes can be tedious, inconsistent, and error-prone. Without automation, teams face challenges such as:

* Tedious manual steps that risk human error
* Environment inconsistencies between development and production
* Delayed detection of integration issues
* Limited visibility into build statuses and test results
* Fragmented collaboration across distributed teams
* Resource-intensive processes that strain time and computing power

The streamlined process offered by Jenkins addresses these challenges and drives efficiency throughout the development lifecycle.

![The image is a flowchart explaining Jenkins, showing a continuous integration process with steps: Build, Test, Deploy to Staging, and Deploy to Production.](https://kodekloud.com/kk-media/image/upload/v1752879919/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-What-is-Jenkins-Why-do-we-need-Jenkins/jenkins-continuous-integration-flowchart.jpg)

> **triangle-alert** Manual development processes can lead to delayed feedback and integration errors, making continuous integration with Jenkins essential for modern software development.

## Overcoming Manual Process Pitfalls

Without Jenkins automation, teams would struggle with the following issues:

* Error-prone manual build and deployment procedures
* Inconsistent environments causing integration challenges
* Slow detection of issues due to infrequent code merges
* Poor visibility into the status of builds and deployments
* Challenges in collaborative teamwork and communication
* Increased risk of human-induced errors

The following diagram highlights the reasons to choose Jenkins as a CI/CD tool:

![The image lists ten reasons to use Jenkins, highlighting features like open source, extensive plugin ecosystem, flexibility, platform agnosticism, and strong community support.](https://kodekloud.com/kk-media/image/upload/v1752879920/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-What-is-Jenkins-Why-do-we-need-Jenkins/ten-reasons-to-use-jenkins.jpg)

By automating key processes, Jenkins not only speeds up the development lifecycle but also ensures that workflows remain consistent and reliable.

![The image lists nine challenges associated with Jenkins, including manual build processes, lack of consistency, delayed feedback, limited scalability, poor visibility, collaboration difficulties, increased human error risk, resource intensiveness, and lack of automated testing integration.](https://kodekloud.com/kk-media/image/upload/v1752879921/notes-assets/images/Jenkins-Project-Building-CICD-Pipeline-for-Scalable-Web-Applications-What-is-Jenkins-Why-do-we-need-Jenkins/jenkins-challenges-manual-builds-feedback.jpg)

In summary, Jenkins provides a robust and flexible solution that addresses many of the challenges associated with manual processes. By automating tasks from building to testing and deployment, Jenkins enables development teams to deliver software more efficiently and reliably.

For more details on Jenkins and CI/CD practices, consider exploring the [Jenkins Documentation](https://www.jenkins.io/doc/) and [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/).

- [Watch Video](https://learn.kodekloud.com/user/courses/jenkins-project-building-ci-cd-pipeline-for-scalable-web-applications/module/4b025d4d-3ef9-479d-a483-3aa7a206a553/lesson/f52331cd-9c18-4e4c-9c06-82e2d17ac877)
