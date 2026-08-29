# Understanding Branching

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Git-and-GitHub-Basics/Understanding-Branching/page

Explains Git branching workflow, feature branches, merge strategies, best practices and collaboration to keep main stable and enable safe parallel development.

What is branching?

In Git, a branch represents an independent line of development. The `main` (historically `master`) branch typically contains production-ready code that’s frequently deployed. When you need to build a new feature, fix a bug, or experiment without affecting `main`, you create a feature branch. A feature branch is an isolated copy of the codebase where you and your teammates can commit, iterate, and test changes before merging them back into `main`.

<Frame>
  <img alt="The image is a flowchart representing a Git workflow process, illustrating the steps from coding to production, including branching, committing, reviewing, approving, merging, and deployment." />
</Frame>

Why branches matter

* Isolation: Implement changes without risking `main`.
* Collaboration: Multiple contributors can work on the same feature branch.
* Safer releases: Code is validated by CI and peer review before merging.
* Parallel development: Different features and fixes can be developed simultaneously.

Typical feature-branch workflow

1. Create a descriptive branch from `main`.
2. Make changes locally; commit often with meaningful messages.
3. Push the branch to the remote repository.
4. Open a pull request (PR) to merge the feature branch into `main`.
5. CI runs automated checks (tests, linters) and reviewers inspect the code.
6. Address feedback by updating the branch and pushing additional commits.
7. Once CI passes and reviewers approve, merge the branch into `main`.
8. Deploy `main` to staging or production as your release process requires.

Common Git commands for this flow:

```bash theme={null}
