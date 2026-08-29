# Demo Overview of GCP dashboard

Source: https://notes.kodekloud.com/docs/GCP-Cloud-Digital-Leader-Certification/GCP-account-and-Resource-hierarchy/Demo-Overview-of-GCP-dashboard/page

Overview of navigating the Google Cloud Console dashboard, locating project identifiers, monitoring resources, Cloud Shell, activity logs, recommendations, and quick links for managing GCP projects.

Welcome back. In this lesson we'll explore the Google Cloud Platform (GCP) Console dashboard: how to navigate it, where to find key project identifiers, and which dashboard panels help you monitor and manage resources.

At the top-left of the console you’ll see the Google Cloud logo and the current project selector. In this demo the active project is "Learning Google Cloud."

<Frame>
  <img alt="A screenshot of the Google Cloud Console welcome page for a project named &#x22;Learning Google cloud,&#x22; showing the project number and project ID. Quick-access tiles and buttons are visible for creating a VM, running a BigQuery query, creating a GKE cluster, and creating a storage bucket." />
</Frame>

Why the project matters

* Project ID: a user-assigned, globally unique string used in APIs and resource names.
* Project number: a system-assigned numeric identifier used internally by GCP and in some support scenarios.

<Callout icon="lightbulb">
  Project ID is a user-assigned, globally unique string identifier (used in APIs and resource names). Project number is a system-assigned numeric identifier that is also unique and is used internally by GCP. Keep both handy when configuring services or opening support requests.
</Callout>

Top-bar features

* Quick search: find GCP resources, Console pages, or documentation.
* Cloud Shell (terminal icon): launches an in-browser shell with gcloud and Linux tools. When active, a small terminal appears at the bottom of the Console.
* Notifications (bell icon): view recent events and messages about your account and resources.
* Project-level controls and quick actions near the right side of the header.

Example: quickly check the currently active project from Cloud Shell or a local terminal:

```bash theme={null}
