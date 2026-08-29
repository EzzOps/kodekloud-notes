# Check status
git status

# Stage all changes and commit
git add .
git commit -m "application change: update login heading to LOGIN V2"

# Push to remote (CodeCommit)
git push origin master
```

Example output when the push completes:

```text theme={null}
Counting objects: 100% (177/177), done.
Writing objects: 100% (63/63), 194.80 KiB, done.
To https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/aws-microservice-project
   eb72454..3257666  master -> master
```

## 3) Start a new build in AWS CodeBuild

* In the AWS Console go to **CodeBuild → Build projects**.
* Select your project and click **Start build**.
* Monitor the build logs. The buildspec should perform steps such as:
  * Checking `aws --version`
  * Building the Docker image
  * Tagging the image (including the Git commit hash)
  * Pushing the image to the ECR repository

When the build finishes you should see the newly pushed image in Amazon ECR (tagged with the commit hash). Confirm the new image in the ECR console:

<Frame>
  <img alt="The image shows the Amazon Elastic Container Registry interface with a list of images under the repository &#x22;cryptoproject,&#x22; displaying details like image tags, artifact type, push dates, and size." />
</Frame>

## 4) Update the Amazon ECS service to use the new task definition

* In the AWS Console open **ECS → Task Definitions** and verify that CodeBuild (or your pipeline) registered a new task definition revision.
* Navigate to **Clusters → \<your production cluster> → Services → \<your service> → Update**.
* From the task definition drop-down, choose the new revision (for example, revision 3), proceed through the update flow and click **Update**.
* ECS will perform a rolling deployment: old tasks will be replaced by tasks using the new task definition.

## 5) Monitor the deployment and inspect the running tasks

* The service will show a deployment in progress. Wait until the deployment shows primary status 100% and all tasks are healthy.
* Under the cluster **Tasks** tab you should see the recently launched task(s) and timestamps matching your deployment.

Here’s the running tasks view showing newly launched tasks:

<Frame>
  <img alt="The image shows the Amazon Elastic Container Service (ECS) console, displaying details of running tasks within a cluster named &#x22;ProductionCluster&#x22; for a service called &#x22;crypto-app.&#x22; Tasks are listed with their status, launch type, and resource specifications." />
</Frame>

### Inspect the task and application

* Select a task, open the container details to view the image URI and network bindings.
* Use the network binding URL (public IP / load balancer target) to open the application and confirm the UI change (the login heading should now show `LOGIN V2`).

Open task details (container configuration, image, and bindings) to inspect further:

<Frame>
  <img alt="The image shows a screenshot of the AWS Management Console, specifically the Amazon Elastic Container Service (ECS) interface, displaying task details and configuration for a service running with Fargate." />
</Frame>

Click the network binding URL to verify the running app shows `LOGIN V2`.

View the runtime task overview and bindings (ports, ENI, subnet, etc.):

<Frame>
  <img alt="The image shows an Amazon Elastic Container Service (ECS) console displaying details about a running task in a production cluster, including task overview and network bindings for specific ports." />
</Frame>

## 6) Trace the running image back to the Git commit

* In the ECS task details note the container `image` URI. The image tag commonly contains the Git commit hash (for example `3257666`).
* In the AWS Console open **ECR → \<your repository>** and find the image tag used by your running task.
* Copy that commit hash and open **CodeCommit → \<your repository> → Commits**.
* Search or filter by the commit hash to find the exact commit that introduced the change.

Open the commit in CodeCommit to review the diff and confirm the change:

<Frame>
  <img alt="The image shows an AWS CodeCommit repository page listing recent commits for a project named &#x22;aws-microservice-project,&#x22; with details such as commit IDs, messages, dates, authors, and actions." />
</Frame>

Example snippet showing the relevant change:

```html theme={null}
<h2 class="login-title">LOGIN</h2>
<h2 class="login-title">LOGIN V2</h2>
```

This proves the traceability from running task → ECR image → CodeCommit commit. Tagging images with the commit hash makes it straightforward to debug, audit, and roll back deployments.

> **lightbulb** Tagging images with the commit hash improves traceability. When a deployment behaves unexpectedly, you can identify the exact commit that produced the image running in production and inspect that commit in your repository.

## Quick reference — typical commands and locations

| Action         | Where / Console                           | Example command or note                                      |
| -------------- | ----------------------------------------- | ------------------------------------------------------------ |
| Edit file      | Cloud9 editor                             | `templates/login.html`                                       |
| Commit & push  | Cloud9 terminal                           | `git add . && git commit -m "..." && git push origin master` |
| Start build    | AWS Console → CodeBuild                   | Click **Start build** or trigger via pipeline                |
| Check image    | ECR console                               | New image tagged with commit hash (e.g. `3257666`)           |
| Update service | ECS console → Clusters → Service → Update | Select new task definition revision                          |
| Trace commit   | CodeCommit → Commits                      | Search by commit hash shown in ECR image tag                 |

## Summary

* Edited `templates/login.html` in Cloud9 and pushed the change to AWS CodeCommit.
* Started CodeBuild which built and pushed a Docker image to Amazon ECR (image tagged with the commit hash).
* Updated the ECS service to a new task definition revision and validated the UI change (`LOGIN V2`).
* Traced the running container image back to the specific CodeCommit commit for full traceability.

Links and references

* [AWS Cloud9](https://aws.amazon.com/cloud9/)
* [AWS CodeCommit](https://aws.amazon.com/codecommit/)
* [AWS CodeBuild](https://aws.amazon.com/codebuild/)
* [Amazon ECR](https://aws.amazon.com/ecr/)
* [Amazon ECS](https://aws.amazon.com/ecs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/building-scalable-microservices-on-aws-deploy-a-crypto-app/module/87867a08-358d-4890-933e-f6b072182388/lesson/c1388d56-f8c6-494e-9dfc-56154f208c91)


# About the Terraform Associate Exam

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Terraform-Associate-004/Course-Introduction/About-the-Terraform-Associate-Exam/page

Overview of the HashiCorp Terraform Associate exam, covering purpose, target candidates, format, logistics, question types, preparation tips, and registration requirements

Hey there — welcome.

If you're reading this lesson, you're probably thinking about earning your Terraform Associate certification, or maybe you've already decided and you're ready to get started. Either way, you're in the right place.

You may be wondering: do I really need another certification, and is it worth the time? Those are fair questions. The Terraform Associate credential is more than a line on your resume. It signals to employers that you understand infrastructure as code at a practical level, that you can work with Terraform in real-world scenarios, and that you're committed to your career in cloud engineering.

In this lesson you'll learn what to expect from the exam: its format, logistics, who should take it, and what passing demonstrates. Whether you are new to Terraform or already using it and want to formalize your knowledge, this lesson is designed to meet you where you are and help you pass.

Why this certification matters

* Industry recognition: Many DevOps and cloud engineering job postings list Terraform Associate or HashiCorp certification as preferred or required. Having the credential tells hiring managers you’ve proven your Terraform skills via a standardized assessment.
* Career opportunities: Certifications don’t guarantee a job, but they demonstrate commitment to professional development and a specific skill set, which helps in a competitive market.
* Validates foundational skills: The exam focuses on core Terraform and Infrastructure-as-Code concepts — writing configurations, managing state, using modules, and collaborating with tools like [Terraform Cloud](https://www.terraform.io/cloud) or [Terraform Enterprise](https://www.hashicorp.com/products/terraform-enterprise) — rather than advanced edge cases.

Is this exam right for you?
The exam is aimed at cloud engineers and DevOps professionals, or those working toward those roles.

<Frame>
  <img alt="The image shows a person working on a laptop with code on the screen, alongside text describing the ideal candidates for an exam: Cloud Engineers, DevOps Professionals, and others with related skills and experience." />
</Frame>

HashiCorp recommends around six months of Terraform experience, but that’s a guideline, not a strict requirement. Hands-on practice with the exam objectives—whether in a lab environment or at work—can be sufficient.

You should also have basic terminal skills and an understanding of cloud architecture fundamentals (VMs, networks, storage), since Terraform is used to deploy and manage those resources. Don’t let imposter syndrome stop you: with focused practice and study of the objectives, this exam is attainable.

Exam essentials and logistics

* Duration: 60 minutes. This is generally enough time if you have prepared; many candidates finish with time to spare. If English isn’t your native language, you can request extra time during registration.
* Delivery: Online proctored through [Certiverse](https://www.certiverse.com). You’ll take the exam from a quiet location while a live proctor monitors via webcam.
* Language: The exam is offered in English only. If you need additional time due to language, request it during registration.
* Cost: Approximately \$70 (there is no free retake — if you fail, you must pay the full fee to attempt the exam again).
* Validity: The certification is valid for two years. To recertify you can retake the Associate exam or pursue other HashiCorp certifications or updated exams that may be offered; passing a newer HashiCorp certification typically extends or replaces your existing credential.
* Results: You receive a pass/fail result immediately after finishing. Within about 24–48 hours you’ll get a detailed performance report and your [Credly badge](https://www.credly.com).

<Frame>
  <img alt="The image provides details about the Terraform Certified Associate Exam, including its duration, delivery method, language, cost, validity, and results. It also displays the Terraform Certified Associate badge." />
</Frame>

Question formats

* Multiple choice: One correct answer from typically 4–6 options.
* Multi-select: Choose multiple correct answers. The question will always indicate exactly how many choices to select (e.g., “Choose two”).
* True/False: Decide whether a presented statement or code snippet is true or false.

A few important notes about the content

* Cloud-agnostic: The exam tests Terraform itself, not deep provider-specific knowledge. You may see AWS, Azure, or GCP mentioned, but you won’t be tested on provider-specific minutiae.
* Practical focus: Expect scenario- and code-based questions. You might be asked to identify an error in a configuration snippet or to choose the best approach for managing state remotely.

Registration and test-room requirements

* Register using the exact name on your government-issued ID. If the name on your registration and your ID don’t match, the proctor may deny access to the exam.

> **lightbulb** Register with the same name that appears on your government-issued ID to avoid being denied entry by the proctor.

* Testing environment: Use a private, quiet room with stable internet. Lock the door or post a notice to prevent interruptions. Unexpected people or noises can lead the proctor to pause or invalidate your exam.

> **warning** Do not allow others into the room while testing. Any unexpected activity visible to the proctor can cause the exam to be stopped or invalidated.

* Computer setup: Your machine must have a working webcam and microphone. Use your laptop’s built-in devices if possible so the proctor can see and hear you. The proctoring software may flag unusual activity (e.g., eyes off-screen for extended periods), so keep your hands visible and behave as you would in a physical test center.

<Frame>
  <img alt="The image provides information on exam logistics for scheduling and delivery of the HashiCorp certification, accompanied by a photo of a person using a computer, wearing headphones." />
</Frame>

If you prepare your space, run the required system checks ahead of time, and follow the procedures, the proctored experience should be smooth. Most candidates do not encounter problems.

Wrap-up
That covers the exam format, logistics, who the exam is for, and what passing demonstrates. Upcoming course content covers the exam objectives and the specific topics you need to study to prepare.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-terraform-associate-004/module/ab6bded4-e4cf-4208-9368-f5313fcfcf03/lesson/b51fbe0c-77cd-474a-8337-52d40ecca752)
