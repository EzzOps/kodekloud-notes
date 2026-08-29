# OpenAI Account Setup

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Pre-Requisites/OpenAI-Account-Setup/page

This tutorial teaches how to navigate the OpenAI website, sign up for an account, and locate API keys.

Welcome! In this tutorial, you’ll learn how to navigate the OpenAI website, sign up for an account, and locate your API keys. Let’s get started.

***

## 1. Homepage Overview

Open your browser and go to [https://openai.com](https://openai.com). The homepage highlights key resources:

| Section   | Description                                    | Examples                           |
| --------- | ---------------------------------------------- | ---------------------------------- |
| Research  | Browse model releases, papers, and demos       | DALL·E, GPT-4                      |
| Safety    | Standards for ethical AI, copyright, deepfakes | “Safety at every step” guidelines  |
| Company   | OpenAI’s mission, team, and corporate values   | About Us, Careers                  |
| Developer | API reference, tutorials, SDKs                 | API docs, code samples             |
| Stories   | Use cases, news, and blog articles             | Customer spotlights, announcements |

<Frame>
  ![The image shows a webpage with a selection of colorful cards related to ChatGPT, featuring options for different models and articles about using AI for writing and research.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879177/notes-assets/images/Introduction-to-OpenAI-OpenAI-Account-Setup/chatgpt-colorful-cards-webpage.jpg)
</Frame>

***

## 2. Exploring the Menu

### Research

Under **Research**, you’ll find model releases and research insights:

* **DALL·E**: Generate high-quality images from textual prompts.
* **GPT-4**: State-of-the-art LLM for advanced text generation.

<Callout icon="lightbulb">
  OpenAI is developing experimental video-generation models—imagine a woolly mammoth running in the snow!
</Callout>

### Safety

The **Safety** section covers:

* Ethics and responsible AI
* Copyright guidance
* Misinformation and deepfake prevention

<Frame>
  ![The image shows a webpage from OpenAI with the text "Safety at every step" and a statement about AI's potential to improve life while ensuring safety.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879178/notes-assets/images/Introduction-to-OpenAI-OpenAI-Account-Setup/openai-safety-webpage-ai-potential.jpg)
</Frame>

### Company

Visit **Company → About Us** to learn OpenAI’s mission, values, and organizational structure.

***

## 3. Accessing the API

1. Go to **Products → API** in the top menu.
2. Click **Login** (or **Sign Up** if you don’t have an account yet).
3. Explore the left sidebar for:
   * API reference
   * Quickstart guides
   * Sample code

Example JavaScript snippet to create a chat completion with GPT-4:

```javascript theme={null}
import OpenAI from "openai";
const openai = new OpenAI();

const completion = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [
    { role: "user", content: "Write a haiku about AI." }
  ]
});

console.log(completion.choices[0].message.content);
```

***

## 4. Creating Your Account

Follow these steps to set up your OpenAI account:

1. Click **Sign Up** on the API page.
2. Enter your email address and create a password.
3. Verify your email via the confirmation link.
4. Complete your profile:
   * Full name
   * Organization (optional)
   * Birth date

<Frame>
  ![The image shows a web page for creating an account on OpenAI, with options to sign up using an email address, Google, Microsoft, or Apple accounts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879179/notes-assets/images/Introduction-to-OpenAI-OpenAI-Account-Setup/openai-account-creation-signup-options.jpg)
</Frame>

***

## 5. Your Profile and API Keys

Once logged in, click your initials in the top-right corner to open **Profile & Keys**. Here you can:

* Update organization name and billing details
* Adjust interface settings and preferences
* Create, view, or revoke API keys

<Frame>
  ![The image shows a webpage displaying a list of API keys for an organization on the OpenAI platform, including details like name, secret key, creation date, last used date, project access, creator, and permissions.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879180/notes-assets/images/Introduction-to-OpenAI-OpenAI-Account-Setup/openai-api-keys-list-details.jpg)
</Frame>

To generate a new key, select **Create new secret key**. You’ll also see options for:

* Admin vs. user permissions
* Project-based access controls
* Billing and usage dashboards
* Rate limits and quotas
* Data control settings

<Frame>
  ![The image shows a screenshot of the "Data controls" settings page on the OpenAI platform, with options for visibility settings for threads, usage dashboard, and chat completions. The interface is displayed in a dark theme.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879182/notes-assets/images/Introduction-to-OpenAI-OpenAI-Account-Setup/data-controls-settings-openai-dark-theme.jpg)
</Frame>

***

## Next Steps

In the following section, we’ll dive into OpenAI’s detailed documentation, explore advanced model features, and walk through sample integrations.

***

## Links and References

* [OpenAI API Documentation](https://platform.openai.com/docs)
* [ChatGPT Overview](https://openai.com/blog/chatgpt)
* [DALL·E](https://openai.com/dall-e-2)
* [Safety Guidelines](https://openai.com/policies/usage-policies)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/192b48b6-ae6c-4126-8784-a84f0d284a41/lesson/b82918dd-28ca-410c-ad50-3fc8db6ea3cd" />
</CardGroup>
