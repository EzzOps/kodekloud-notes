# Verify your free credits via gcloud CLI:
gcloud auth login
gcloud beta billing accounts list
```

***

## Cleanup Best Practices

To prevent unexpected charges:

* List all active resources:
  ```bash theme={null}
  gcloud compute instances list
  gcloud storage buckets list
  ```
* Delete or stop resources when not in use:
  ```bash theme={null}
  gcloud compute instances delete INSTANCE_NAME
  gcloud storage rm gs://BUCKET_NAME --recursive
  ```
* Review your Billing page regularly:
  * Check current spend
  * Set up budget alerts under Billing > Budgets & alerts

***

## References

* [Google Cloud Free Tier Overview][gcpfree]
* [Google Cloud Console Sign-up][gcpsignup]
* [GCP Documentation][gcpdocs]

[gcpfree]: https://cloud.google.com/free

[gcpsignup]: https://console.cloud.google.com/freetrial

[gcpdocs]: https://cloud.google.com/docs

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/e0cc2e03-d889-468c-af73-0866856711aa/lesson/ecdeaf7d-7707-48fc-bc04-f46f31bae669)


# Demo Creating a personal GCP account

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-02/Demo-Creating-a-personal-GCP-account/page

This quick-start guide explains how to set up a personal Google Cloud Platform account and activate a free trial.

Welcome to this quick-start guide. In this lesson, you’ll learn how to set up a personal Google Cloud Platform (GCP) account, activate your free trial, and verify billing details. Depending on your region, you may need to provide additional information—such as credit card data—so have those details ready before you begin.

## 1. Open the Google Cloud Console

1. In a new browser tab, go to `https://console.cloud.google.com`.
2. Sign in with your Google account:
   * Enter your Gmail address and click **Next**.
   * Type your password and click **Next** again.

Once authenticated, you’ll land on the GCP Console dashboard. If you’re eligible for the free trial, you should see a banner prompting you to start it.

## 2. Activate Your Free Trial

If the “Start your free trial” banner is not visible, click the gift-box icon in the blue header bar to display the activation prompt.

![The image shows a Google Cloud sign-up page for a free trial, asking for account information such as country and project type, with details about a \$300 credit offer.](https://kodekloud.com/kk-media/image/upload/v1752875440/notes-assets/images/GCP-DevOps-Project-Demo-Creating-a-personal-GCP-account/google-cloud-signup-free-trial.jpg)

Follow these steps:

1. Click **Activate**.
2. Select your **Country** of residence.
3. Choose **Personal project** (or another relevant option) for your trial.
4. Read and accept the **Terms of Service**.

Next, complete the billing verification section:

* **Business information**
* **Primary contact details**
* **Credit card information** (for identity verification only)

![The image shows a Google Cloud Platform signup page offering a free trial with \$300 credit, requiring credit card details for verification but promising no autocharge after the trial ends.](https://kodekloud.com/kk-media/image/upload/v1752875441/notes-assets/images/GCP-DevOps-Project-Demo-Creating-a-personal-GCP-account/google-cloud-platform-signup-free-trial.jpg)

5. Click **Start My Free Trial**.

> **lightbulb** Your credit card is used only for verification. You won’t be charged unless you exceed the \$300 free credit or continue using paid services after 90 days. To avoid any unexpected charges, disable billing or close your billing account before the trial ends.

***

Congratulations! You’ve successfully activated your GCP free trial and can now explore core services, create projects, and manage resources from the Google Cloud Console.

## Next Steps

* Learn how to create and manage projects in GCP
* Explore essential GCP services: Compute Engine, Cloud Storage, and IAM
* Review [GCP Free Trial FAQ](https://cloud.google.com/free/docs/gcp-free-tier#free-trial) for more details

- [Watch Video](https://learn.kodekloud.com/user/courses/gcp-devops-project/module/e0cc2e03-d889-468c-af73-0866856711aa/lesson/5db0ea1d-3968-4256-9583-b910aea4c7cc)
