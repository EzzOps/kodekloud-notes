# Demo Explore and Trigger Jenkins Projects 1

Source: https://notes.kodekloud.com/docs/Migrating-Jenkins-Pipelines-to-GitHub-Actions/Analyze-Your-Existing-Jenkins-Pipelines/Demo-Explore-and-Trigger-Jenkins-Projects-1/page

Walkthrough of two Jenkins jobs, a Freestyle ASCII artwork job and a scripted Pipeline, demonstrating job behavior and migration considerations to GitHub Actions

In this lesson we explore and trigger two Jenkins projects to inspect their configuration and runtime behavior: a Freestyle job that renders ASCII artwork, and a scripted Pipeline job that demonstrates basic stage flow. Both jobs are configured inline in Jenkins (no SCM and no automated triggers), making them ideal examples for understanding job structure and migrating Jenkins logic to other CI/CD systems.

## Overview

|                Project | Type              |  SCM | Triggers | Key utilities                                     |
| ---------------------: | ----------------- | ---: | -------: | ------------------------------------------------- |
| Generate ASCII Artwork | Freestyle         | None |     None | `curl`, `jq`, `cowsay`                            |
|      scripted-pipeline | Scripted Pipeline | None |     None | Jenkins Pipeline steps (node, stage, echo, sleep) |

<Callout icon="lightbulb">
  This walkthrough helps you understand how simple shell-driven Freestyle jobs compare to scripted Pipelines, which is useful when planning migrations (for example, to GitHub Actions).
</Callout>

***

## Generate ASCII Artwork (Freestyle)

This Freestyle job calls the adviceslip API to fetch an advice message, validates the message length using `jq` and shell tests, and—if the message is long enough—renders it as ASCII art using the `cowsay` utility.

<Frame>
  <img alt="A dark-themed Jenkins web interface for a job titled &#x22;Generate ASCII Artwork,&#x22; showing the job description and permalinks in the main area with a builds panel and navigation menu on the left." />
</Frame>

Configuration notes:

* No Source Code Management (job is configured without SCM).
* No automated triggers.
* Single build step: Execute shell, which performs three logical phases: build, test, deploy.

<Frame>
  <img alt="A dark-themed Jenkins job &#x22;Configure&#x22; page showing the left navigation (General, Source Code Management, Triggers, etc.) and the main panel with Triggers and Environment options (checkboxes for build triggers, workspace cleanup, timestamps, etc.). The Save and Apply buttons are visible at the bottom." />
</Frame>

High-level step behavior:

* Build: fetch an advice message from adviceslip API and save it to `advice.json`.
* Test: extract message with `jq` and assert it contains more than 5 words; otherwise exit non‑zero to mark the build as failed.
* Deploy: install and run `cowsay` (Debian/Ubuntu example) and pipe the advice into a randomly-selected cowfile.

Shell script used in the job:

```bash theme={null}
