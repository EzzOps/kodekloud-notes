# Expected output:
# yes
```

* A simple keep-alive loop you might use while debugging locally:

```bash theme={null}
while true; do echo hello; sleep 10; done
```

## Best practices for taking these mock exams

* Always set the indicated kubectl context before starting a question.
* Read each task carefully: note the namespace, resource names, and exact file paths required (e.g., `/opt/...`).
* Use `kubectl -n <namespace> get ...` and `-o yaml`/`-o jsonpath` frequently to inspect current state.
* When decoding base64 strings, redirect output to the exact path specified by the task.
* Keep an eye on the clock and prioritize higher‑weighted tasks first.

## Links and references

* [Certified Kubernetes Administrator (CKA) preparation course — KodeKloud](https://learn.kodekloud.com/user/courses/cka-certification-course-certified-kubernetes-administrator)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* Basic kubectl reference: `kubectl --help`

Good luck with your preparation — practice with purpose, and make use of the multi‑cluster labs to build confidence across all CKA domains.

- [Watch Video](https://learn.kodekloud.com/user/courses/ultimate-certified-kubernetes-administrator-cka-mock-exam-series/module/e88f8a83-f202-45e4-9397-63f104b0e8cf/lesson/140bb955-0d24-49a2-bcb6-af2ed1898dca)


# Course Introduction

Source: https://notes.kodekloud.com/docs/Ultimate-Certified-Kubernetes-Application-Developer-CKAD-Mock-Exam-Series/Certified-Kubernetes-Application-Developer-Mock-Exam-Series/Course-Introduction/page

Overview of KodeKloud CKAD mock exam series, structure, workflow, scoring, environment, time management, and practice tips for Kubernetes application developer certification

Hello and welcome — I’m Vijay Palazhi from KodeKloud. This Ultimate Mock Exam Series for the CKAD (Certified Kubernetes Application Developer) is designed to mirror the real exam with timed, hands-on labs so you can build confidence and improve your practical skills.

In this lesson/article we’ll cover the mock exam structure, how to use the environment, and what to expect during an attempt.

What the CKAD assesses

* The CKAD focuses on application-centric tasks built for Kubernetes and covers five primary domains. Below is a concise breakdown of the domains and their approximate weightings:

|                                       Knowledge Area | Weight |
| ---------------------------------------------------: | :----: |
|                         Application design and build |   20%  |
|                               Application deployment |   20%  |
| Application environment, configuration, and security |   25%  |
|                        Observability and maintenance |   15%  |
|                                   Service networking |   20%  |

This mock exam series closely simulates the official CKAD: tasks are curated by KodeKloud experts, the environment is timed, and the labs emphasize hands-on problem solving.

<Frame>
  <img alt="The image shows a webpage from KodeKloud offering a Certified Kubernetes Application Developer (CKAD) Mock Exam Series with a list of lab exams and a video introduction featuring a person speaking." />
</Frame>

Mock exam environment and workflow

* You can interact with up to three Kubernetes clusters during an exam.
* Each mock exam contains 20 questions. While specific questions may vary between attempts, the total number and format remain consistent.
* Every question displays its knowledge area and the assigned weight (for example, 4%), so prioritize your time by question weight.
* Navigation is via Next Question and Back Question buttons.
* You have up to two hours to complete the exam.

Switching cluster contexts

* Use kubectl to change contexts when a task requires a different cluster. Example:

```bash theme={null}
kubectl config use-context cluster1
```

Practice switching contexts early in the exam so you don’t lose time later.

> **lightbulb** The exam environment simulates the real CKAD experience: multiple clusters, time limits, and weighted questions. Practice switching contexts and reading each question’s weightage before you begin.

If a task requires a different cluster, switch to it the same way:

```bash theme={null}
kubectl config use-context cluster2
```

<Frame>
  <img alt="The image shows a task interface from KodeKloud on the left with a terminal on the right, displaying the &#x22;KodeKloud&#x22; logo and a command prompt." />
</Frame>

Scoring, submission, and feedback

* To submit your attempt, click the End Exam button. The system validates your answers automatically.
* The platform provides solutions and feedback for any questions you answered incorrectly so you can review and learn from mistakes.
* Minimum passing score for the mock exam is 66%.

> **warning** Time management is critical. Review each question’s weight and attempt higher-weight questions first. Remember: the mock exam enforces the same time pressure and cluster context switches as the real CKAD.

Quick checklist before you begin a mock exam

* Ensure you’re comfortable switching kubectl contexts.
* Read each question fully and note the weight percentage.
* Allocate time to high-weight questions first.
* Keep an eye on the timer and use navigation to move between questions efficiently.

Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [KodeKloud CKAD Course & Mock Exams](https://kodekloud.com/)
* [CKAD Exam Curriculum — CNCF](https://www.cncf.io/certification/ckad/)

That’s all for this lesson. Good luck with your practice — use these mock exams to build speed, accuracy, and familiarity with real-world CKAD scenarios.

- [Watch Video](https://learn.kodekloud.com/user/courses/ultimate-certified-kubernetes-application-developer-ckad-mock-exam-series/module/81339e83-64b3-4922-ad99-a5b0a55e1fd8/lesson/33750844-4eb1-4e2b-bec7-a862ee258337)
